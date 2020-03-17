package handler

import (
	"gqlkit/graph"
	"gqlkit/graph/generated"
	"net/http"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/playground"
)

func Playground() http.HandlerFunc {
	return playground.Handler("GraphQL playground", "/")
}

func Graphql() *handler.Server {
	return handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: &graph.Resolver{}}))
}
