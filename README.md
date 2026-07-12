# optistream

## Quick Start

### Run Local Server

```bash
uvicorn app.main:app --reload
```

### Run Tests

```bash
# Run tests and generate Allure report
./run_tests.sh

# Or just run tests
pytest

# View existing report
allure open allure-report
```

### Docker

```bash
docker build -t optistream-backend:latest .
```

## CI/CD Pipeline

This project uses **GitHub Actions** for automated testing.

- Every push/PR runs tests automatically
- Allure reports generated on each run
- Reports available as GitHub artifacts
- View results in: `Actions` tab → Select run → `Artifacts`

### docker run -d -p 8000:8000 --name optistream-api --env-file .env optistream-backend:latest

<!-- -d: Runs it in detached mode (in the background). -->
<!-- -p 8000:8000: Forwards port 8000 from your laptop into the container's internal port 8000. -->
<!-- --env-file .env: Automatically injects your database and storage configurations directly into the container. -->

<!-- "When Dockerizing our microservices, I avoid standard single-stage Docker configurations because they result in bloated images and security vulnerabilities. Instead, I architect a multi-stage pipeline to separate compilation tools from the runtime layer, reducing our production image footprint significantly. Furthermore, I implement a strict non-root execution policy inside the runtime stage, ensuring the application container adheres to the principle of least privilege in production." -->
