# Cloud Setup

We are using Google Cloud to deploy this application.

## Prerequisites

- A Google Cloud account
- Google Cloud SDK installed and configured
- Docker installed
- A Google Cloud project created `Tennis Booking Assistant`
- Billing enabled for your project

## Steps to Deploy

1. Enable Google Secret Manager API
2. Store `OPENAI_API_KEY` in Google Secret Manager
3. Enable Google Artifact Registry API to store your Docker images
4. Create a Docker repository in Artifact Registry `europe-west3-docker.pkg.dev/tennis-booking-assistant/tennis-app-repo`
5. 


## Automation Ideas

- Use GitHub Actions to automate the deployment process and upload packages to Google Artifact Registry
- Use [PyPI](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to manage and distribute your Python packages
- 
