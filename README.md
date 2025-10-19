# Performance Testing Pet Project

This is a sample pet project designed for performance testing. It's a simple Flask API that connects to a PostgreSQL database, all running inside Docker containers.

## Tech Stack

*   **Backend:** Python 3.10, Flask
*   **Database:** PostgreSQL
*   **Containerization:** Docker, Docker Compose

---

## Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Installation & Launch

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd simple_api_app
    ```

2.  **Create the environment file:**
    This project uses a `.env` file to manage environment variables. You can create your own by copying the example file:
    ```sh
    cp .env.example .env
    ```
    Now, open the `.env` file and fill in the values. For local development, the default values from `.env.example` are usually sufficient.

3.  **Build and run the containers:**
    Use Docker Compose to build the images and start the services.
    ```sh
    docker-compose up --build
    ```
    *   The `--build` flag forces a rebuild of the application image, which is useful when you change dependencies or the `Dockerfile`.
    *   The application will be available at `http://localhost:8080`.
    *   The PostgreSQL database will be accessible on port `5432` of your host machine.

---

## Development

### Useful Docker Commands

*   **Start services in the background:**
    ```sh
    docker-compose up -d
    ```

*   **Stop services:**
    This command stops the containers but preserves the database data.
    ```sh
    docker-compose down
    ```

*   **Stop services and delete data:**
    To stop the containers and completely wipe the database volume (useful for a clean start):
    ```sh
    docker-compose down -v
    ```

*   **View logs:**
    You can view the logs for all services or a specific one.
    ```sh
    # View all logs
    docker-compose logs -f

    # View logs for the app service only
    docker-compose logs -f app
    ```

*   **Access a running container:**
    To get a shell inside the running `app` container for debugging:
    ```sh
    docker-compose exec app bash
    ```

### Running Tests

To run the test suite, first ensure you have installed the development dependencies locally:
```sh
pip install -r requirements-dev.txt
```
Then, run pytest:
```sh
pytest
```
*(Note: This assumes you have a local Python environment set up. Alternatively, you can run tests inside the Docker container.)*
