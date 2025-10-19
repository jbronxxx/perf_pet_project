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

### Code Quality and Formatting

This project uses `pre-commit` hooks to ensure consistent code style and quality. Before every commit, the following checks are automatically performed:

*   **`darker`**: Formats Python code using `black` (with a line length of 100 characters) and sorts imports using `isort`. `darker` only reformats changed lines, making it efficient.
*   **`flake8`**: Lints Python code to catch common errors and style violations (with a maximum line length of 100 characters).

#### Setup

1.  **Install development dependencies:**
    Ensure you have the development dependencies installed, which includes `pre-commit`, `darker`, and `flake8`.
    ```sh
    pip install -r requirements-dev.txt
    ```

2.  **Install Git hooks:**
    Activate the `pre-commit` hooks for your local Git repository. This only needs to be done once per repository clone.
    ```sh
    pre-commit install
    ```

#### Usage

*   **Automatic checks on commit:**
    Once installed, `pre-commit` will automatically run `darker` and `flake8` on staged files before each commit. If any issues are found, `pre-commit` will either fix them automatically (e.g., `darker`) or report them, preventing the commit until they are resolved.

*   **Manually run all checks:**
    To run all `pre-commit` checks on all files in the project at any time (e.g., before pushing to a remote repository), use:
    ```sh
    pre-commit run --all-files
    ```
    This is useful for ensuring the entire codebase adheres to the defined standards.

*   **Addressing `flake8` errors:**
    `flake8` will report errors that `darker` cannot automatically fix (e.g., very long string literals, complex expressions that would break if reformatted). These errors (like `E501 line too long`) must be fixed manually.

### Running Tests

To run the test suite, ensure you have activated your Python virtual environment and then run `pytest`:
```sh
pytest
```
*(Note: This assumes you have a local Python environment set up. Alternatively, you can run tests inside the Docker container.)*
