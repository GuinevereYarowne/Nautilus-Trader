FROM golang:1.21-alpine
WORKDIR /app
COPY . .
EXPOSE 8080
CMD ["go", "run", "main.go"]