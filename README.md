
# TSC Project

## Project Description

This project is an application named TSC, which uses Docker to manage dependencies and the runtime environment. The project includes configuration files for Docker, as well as scripts and requirements needed to run the application. The main goal of this project is to create a microservice providing a JSON API to work with word definitions and translations taken from Google Translate.

## Directory Structure

- `app/` - The main application.
- `Dockerfile` - Configuration file for building the Docker image.
- `docker-compose.yml` - Configuration file for Docker Compose.
- `requirements.txt` - List of Python dependencies.

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:
   git clone https://github.com/sebastiangebala/TSC.git

2. Navigate to the project directory:
   cd TSC

## Running the Application

Build the Docker images and start the containers:
   docker-compose up --build

## Access to Application

Open your browser and navigate to:
   http://localhost:8000/docs

## Endpoints

- **Get the details about the given word**
  - The response includes definitions, synonyms, translations, and examples.
  - Data fetched from Google Translate is saved in the database. When a request arrives, the handler first looks for the word in the database and falls back to Google Translate only if it is not there.

- **Get the list of the words stored in the database**
  - Supports pagination, sorting, and filtering by word. Partial match is used for filtering.
  - Definitions, synonyms, and translations are not included in the response by default but can be enabled with corresponding query parameters.

- **Delete a word from the database**

## Non-Functional Requirements

- Python 3
- FastAPI in async mode
- NoSQL database
- Dockerfile and docker-compose.yml included
- Authentication is not required

## Authors

- Sebastian Gebala

