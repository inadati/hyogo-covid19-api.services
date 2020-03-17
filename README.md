# gqlkit

## Getting started
1. Install docker and docker-compose in your environment.  
Also, prepare an environment for golang and node.js.

2. Because we use prisma2 lift  
Also install prisma2.

```
npm i -g prisma2
```

3. I have all the necessary tools  
Let's git clone gqlkit.

```
git clone git@github.com:gqlkit-repos/gqlkit.git
```

4. Let's start the service with docker-compose.

```
cd gqlkit
docker-compose up -d
```

5. Go to the "gqlkit-server/lift" directory and then  
Migrate your DB model using prisma2.

```
cd gqlkit-server/lift
prisma2 lift save
prisma2 lift up
```

6. Prepare the necessary golang packages before starting gqlkit-server.  
Since the package described in the Dockerfile will probably be needed later,  
For now, let's put everything in.

```
go get -u github.com/hako/branca
go get -u github.com/segmentio/ksuid
go get -u github.com/lib/pq
go get -u github.com/jinzhu/gorm
go get -u github.com/99designs/gqlgen/handler
go get -u github.com/vektah/gqlparser
go get -u github.com/gin-gonic/gin
go get -u github.com/machinebox/graphql
```

7. Let's start gqlkit-server.

```
go run server.go
```

Congrats!  
It's the beginning of a great graphql app development!
