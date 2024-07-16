
# TSC Project

## Project Description

This project is an application named TSC, which uses Docker to manage dependencies and the runtime environment. The project includes configuration files for Docker, as well as scripts and requirements needed to run the application. The main goal of this project is to create a microservice providing a JSON API to work with word details taken from Google Translate.

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

## Known Flaws and Possible Improvements
While the current implementation of the Translation Service Challenge fulfills the primary requirements, there are some known areas for improvement and potential flaws that should be addressed in future iterations:

# 1. Error Handling:

Currently, error handling is basic. Adding more comprehensive error handling can improve the robustness of the application. For example, handling specific HTTP errors from the Google Translate API, database connectivity issues, and input validation errors.

# 2. Database Optimization:

Using a NoSQL database provides flexibility, but the current schema might not be optimized for all use cases. Reviewing and optimizing the database schema and indexing strategies can improve performance, especially for large datasets.

# 3. API Rate Limiting:

Implementing rate limiting can prevent abuse of the API. This is particularly important when interacting with external services like Google Translate to avoid hitting rate limits.

# 4. Testing:

Although basic tests might be in place, increasing the test coverage, including unit tests, integration tests, and end-to-end tests, can ensure the reliability of the application. Automated testing frameworks can be integrated into the CI/CD pipeline.

# 5. Security:

While authentication is not required as per the challenge, adding optional authentication mechanisms can be beneficial for real-world applications. Securing endpoints and sensitive data should be considered.

# 6. Documentation:

Enhancing documentation with detailed API endpoint descriptions, example requests/responses, and setup instructions can make it easier for developers to understand and use the service.

# 7. Logging and Monitoring:

Implementing logging and monitoring can help in tracking the application's performance and diagnosing issues. Tools like Prometheus, Grafana, and ELK stack can be integrated for this purpose.

# 8. Deployment and Scalability:

While Docker and Docker Compose are used for containerization, further work on orchestration using Kubernetes can help in scaling the application more efficiently. Additionally, optimizing the Dockerfile and docker-compose.yml for production environments is recommended.

# 9. Fallback Mechanism:

The current fallback to Google Translate when a word is not found in the database is a good start. However, adding a caching layer can reduce latency and the number of requests to the external API.

# 10. User Experience:

Improving the API's user experience by providing more informative error messages, consistent responses, and additional metadata can enhance usability.