package cors

import (
	"gqlkit/env"
	"net/http"
)

func Middleware() func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "application/json")
			w.Header().Set("Access-Control-Allow-Origin", env.AS_ALLOW_ORIGIN)
			w.Header().Set("Access-Control-Allow-Headers", "authorization,content-type")
			w.Header().Set("Access-Control-Allow-Methods", "OPTIONS,GET,POST")
			next.ServeHTTP(w, r)
		})
	}
}
