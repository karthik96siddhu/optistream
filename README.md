# optistream

<!-- Docker command -->

## docker build -t optistream-backend:latest .

## docker run -d -p 8000:8000 --name optistream-api --env-file .env optistream-backend:latest

<!-- -d: Runs it in detached mode (in the background). -->
<!-- -p 8000:8000: Forwards port 8000 from your laptop into the container's internal port 8000. -->
<!-- --env-file .env: Automatically injects your database and storage configurations directly into the container. -->
