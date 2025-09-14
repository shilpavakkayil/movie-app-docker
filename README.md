# movie-app-docker
A Python containerized command-line app for querying the movie database REST API server build using Docker and Docker Compose. The app returns the number of movies for the input years.

## Components
- movie-server
- movie-client

## Requirements
- Docker
- Docker Compose

## Project structure
- movie-app-docker
    - movie-client
        - Docker file
        - movie-client.py
        - requirements.py
    - movie-server
        - Docker file
        - [ Server files]
        - Makefile
    - .github
        - workflows
            - action.yml
    - Makefile
    - docker-compose.yml

## Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/shilpavakkayil/movie-app-docker.git
cd movie-app-docker
```

### 2. Build the Application

```bash
# Build all Docker images
docker compose build
```

### 3. Start the Movie Server

```bash
# Start the server in detached mode
docker compose up -d movie-server
```

### 4. Run the Movie Client

```bash
# Query movies for a specific year
docker compose run --rm movie-client --server http://movie-server:8080 1999

# Query multiple years
docker compose run --rm movie-client --server http://movie-server:8080 2020 2021 2022
```

## Continuous Integration

This project includes GitHub Actions for automated testing:

- **Triggers**: Pushes to `main` branch and pull requests to `main`
- **Actions**: 
  - Build Docker images
  - Start services
  - Run test





