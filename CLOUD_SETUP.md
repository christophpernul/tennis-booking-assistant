# Cloud Setup

We are using Google Cloud to deploy this application.

## Prerequisites

- A Google Cloud account
- Google Cloud SDK installed and configured
- Docker installed
- A Google Cloud project created `tennis-booking-assistant`
- Billing enabled for your project

## Steps to Deploy

1. Enable Google Secret Manager API
2. Store `OPENAI_API_KEY` in Google Secret Manager
   1. Grant role `Secret Manager Secret Accessor` to default compute service account
3. Enable Google Artifact Registry API to store your Docker images
4. Create a Docker repository in Artifact Registry `europe-west3-docker.pkg.dev/tennis-booking-assistant/tennis-app-repo`
5. Download and install Docker Desktop
6. Authenticate Docker to use Google Artifact Registry:
   ```bash
   gcloud auth configure-docker europe-west3-docker.pkg.dev
   ```

## Deployment

1. Build your Docker image:
   ```bash
   docker build -t tennis-booking-assistant .
   ```
2. Tag your Docker image for Artifact Registry:
   ```bash
   docker tag tennis-booking-assistant europe-west3-docker.pkg.dev/tennis-booking-assistant/tennis-app-repo/tennis-booking-assistant:latest
    ```
3. Push your Docker image to Artifact Registry:
    ```bash
    docker push europe-west3-docker.pkg.dev/tennis-booking-assistant/tennis-app-repo/tennis-booking-assistant:latest
    ```


## Automation Ideas

- Use GitHub Actions to automate the deployment process and upload packages to Google Artifact Registry
- Use [PyPI](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to manage and distribute your Python packages
-
