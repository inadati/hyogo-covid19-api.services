FROM golang:1.13.4

RUN apt update -y && \
    apt install -y tzdata

ENV TZ=Asia/Tokyo

RUN go get -u github.com/hako/branca && \
    go get -u github.com/segmentio/ksuid && \
    go get -u github.com/lib/pq && \
    go get -u github.com/jinzhu/gorm && \
    go get -u github.com/99designs/gqlgen/handler && \
    go get -u github.com/vektah/gqlparser && \
    go get -u github.com/go-chi/chi && \
    go get -u github.com/machinebox/graphql

WORKDIR /go/src/app
COPY . .

CMD ["go", "run", "server.go"]