package main

import (
	"gqlkit/env"
	"gqlkit/handler"
	"gqlkit/middleware/cors"
	"log"
	"net/http"

	"github.com/go-chi/chi"
)


func main() {

	r := chi.NewRouter()

	r.Use(cors.Middleware())

	r.Handle("/", handler.Playground())
	r.Handle("/query", handler.Graphql())

	log.Printf("connect to http://localhost:%s/ for GraphQL playground", env.AS_PORT)
	log.Fatal(http.ListenAndServe(":"+env.AS_PORT, r))
}
