package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"gqlkit/env"
	"gqlkit/graph/generated"
	"gqlkit/graph/model"

	"github.com/jinzhu/gorm"
	_ "github.com/lib/pq"
)

func (r *queryResolver) ReadInfectedPeoples(ctx context.Context) ([]*model.InfectedPeople, error) {
	db, err := gorm.Open("postgres", env.AS_GORM_SETUP)
	defer db.Close()
	if err != nil {
		return nil, fmt.Errorf(err.Error())
	}

	db.Order("no desc").Find(&r.infected_peoples)
	for _, infected_people := range r.infected_peoples {
		db.Where("infected_people_id = ?", infected_people.ID).Order("no").Find(&infected_people.InfectedPlaces)
	}

	return r.infected_peoples, nil
}

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type queryResolver struct{ *Resolver }
