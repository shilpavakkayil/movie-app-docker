FROM golang:1.25-alpine AS builder
RUN apk add --no-cache git
WORKDIR /app
COPY . .
RUN go generate && go build -o movie-server .

# Run stage
FROM alpine:3.18
WORKDIR /app
COPY --from=builder /app/movie-server .
EXPOSE 8080
CMD ["./movie-server", "--port", "8080"]