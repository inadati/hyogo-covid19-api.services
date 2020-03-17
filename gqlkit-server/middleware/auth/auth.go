package auth

import (
	"context"
	"fmt"
	"gqlkit/env"
	"gqlkit/graph/model"
	"log"
	"net/http"
	"strings"

	"github.com/hako/branca"
	"github.com/jinzhu/gorm"
)

var users []*model.User

func UserEjector(ctx context.Context) *model.User {
	raw, _ := ctx.Value("User").(*model.User)
	return raw
}

func Middleware() func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

			bearerToken := r.Header.Get("Authorization")

			if bearerToken == "" {
				next.ServeHTTP(w, r)
			} else {

				bearerToken = strings.Replace(bearerToken, "Bearer ", "", 1)

				b := branca.NewBranca(env.AS_SECRET_KEY)

				message, err := b.DecodeToString(bearerToken)
				if err != nil {
					log.Println(fmt.Errorf("An undecodable or invalid token was entered."))
					return
				}

				userInfo := strings.Split(message, "/")
				userEmail := userInfo[0]
				userPassword := userInfo[1]

				db, err := gorm.Open("postgres", env.AS_GORM_SETUP)
				defer db.Close()

				db.Where("email = ? AND password = ?", userEmail, userPassword).First(&users)
				user := users[0]

				ctx := context.WithValue(r.Context(), "User", user)
				next.ServeHTTP(w, r.WithContext(ctx))
			}

		})
	}
}
