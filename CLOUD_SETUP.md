# Cloud Setup

We are using Google Cloud to deploy this application.

## Prerequisites

- A Google Cloud account
- Google Cloud SDK installed and configured
- Docker installed
- A Google Cloud project created `tennis-booking-assistant`
- Billing enabled for your project

## Steps to Deploy

### Authentication

**Authentication at OpenAI**
1. Enable Google Secret Manager API
2. Store `OPENAI_API_KEY` in Google Secret Manager
   1. Grant role `Secret Manager Secret Accessor` to default compute service account

**User management via Google**
1. Enable `Google+` API
2. Configure OAuth Consent Screen under "APIs & Services" (External)
3. Create OAuth 2.0 Credentials for Web application with redirect URLs for the app
4. Set environment variables `OAUTH_GOOGLE_CLIENT_ID` and `OAUTH_GOOGLE_CLIENT_SECRET`
5. Use chainlit to create an environment variable `CHAINLIT_AUTH_SECRET` that is used to sign authentication tokens using `chainlit create-secret`

### Image storage

1. Enable Google Artifact Registry API to store your Docker images
2. Create a Docker repository in Artifact Registry `europe-west1-docker.pkg.dev/tennis-booking-assistant/tennis-agent-repo`
3. Authenticate Docker locally to use Google Artifact Registry:
   ```bash
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```

## Manual Deployment

1. Build your Docker image:
   ```bash
   docker build -t tennis-booking-assistant .
   ```
2. Tag your Docker image for Artifact Registry:
   ```bash
   docker tag tennis-booking-assistant europe-west1-docker.pkg.dev/tennis-booking-assistant/tennis-app-repo/tennis-booking-assistant:latest
    ```
3. Push your Docker image to Artifact Registry:
    ```bash
    docker push europe-west1-docker.pkg.dev/tennis-booking-assistant/tennis-app-repo/tennis-booking-assistant:latest
    ```

4. Use the new image in Google Cloud Run to deploy a new container

## Automatic Deployment

The CI/CD pipeline of this repository contains a `docker-gcp-deploy.yml` workflow,
that builds the Docker image, tags it, pushes it to GCP registry and re-deploys a
Google Cloud Run service with the new image.

To set it up initially follow the instructions in `docker-gcp-deploy.yml`.
