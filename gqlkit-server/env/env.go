package env

import (
	"os"
	"strings"
)

// var LoadErr = godotenv.Load("../.env")

var (
	// AS_SECRET_KEY string = os.Getenv("AS_SECRET_KEY")
	AS_PORT         = os.Getenv("AS_PORT")
	AS_ALLOW_ORIGIN = os.Getenv("AS_ALLOW_ORIGIN")
	AS_GORM_SETUP   = strings.Trim(os.Getenv("AS_GORM_SETUP"), "\"")
)
