# Tennis Booking Assistant

An AI agent that helps to find and book tennis courts.

## Architecture

The system includes the following pieces

### Python Agent

The Python implementation is modularized and contains
- `src/agent`: Contains implementation of agent including tools using OpenAI Agent SDK
- `src/booking`: Contains API to fetch latest court bookings and performs data cleaning and preparation tasks
- `src/data`: Contains information and utility for court metadata

The Python dependencies are managed with a `pyproject.toml` file and can easily be installed via `uv`.

### User Interface

The user interface is a simple `chainlit` application, that serves the agent. It is contained in `run.py`.

### Cloud Deployment

A `Dockerfile` is included in the respository, that sets up the necessary dependencies and runs the
application. This Docker file is used for a deployment on Google Cloud.

For this a project was created including an artifact registry. The Docker images are pushed from this repository
to the registry via automatic CI/CD pipelines that allow for continuous deployment of the application.

The latest image is automatically deployed in a `Google Cloud Run` service.

### CI/CD Setup in GitHub

The repository includes the following CI/CD pipelines:
- `pre-commit`: Executes `pre-commit` hooks on new commits
- `docker-gcp-deploy`: Builds a Docker image from the code, tags it properly, pushes it to GCP and deploys it with Google Cloud Run


## Technical setup

The dependencies can be installed with `uv sync`.
The agent is built using `openai` and `agents` frameworks and uses `gpt-4o-mini` as a default LLM model.

### Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Test the setup:**
   ```bash
   python test_setup.py
   ```

4. **Run the application:**
   ```bash
   chainlit run run.py -w
   ```

5. **Open your browser:**
   Navigate to `http://localhost:8000` to access the Gradio interface.

### Project Structure

```
tennis-booking-assistant/
├── src/
│   ├── agent/           # AI agent logic
│   ├── booking/         # STC booking system integration
│   ├── data/           # Court data and user preferences
│   └── main.py         # Application entry point
├── run.py              # CLI launcher
├── test_setup.py       # Setup verification
└── pyproject.toml      # Project configuration
```

### Useful links
- [openai-agents-python Docu](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents Docu](https://platform.openai.com/docs/guides/agents)
- [OpenAI Traces](https://platform.openai.com/logs?api=traces)

#### Models

[OpenAI](https://platform.openai.com/settings/organization/general)
[Gemini](https://aistudio.google.com/projects)

## Assistant Overview

A user can ask a question to the AI assistant and gives him information about at which time, for how long and additional information
he wants to play tennis. The agent processes this information and then fetches the current bookings from the STC booking system and
suggests the user available courts for booking. The agent might also consider user preferences of which courts he wants to play from the
question and additional context information that is hard coded about the courts. If no booking is possible at the preferred courts of the user
the agent suggests other courts. If no courts are available for the time the user wants to play, the agent suggests a different time near
to the time the user asked for.

The agent knows context about the courts. For each court the agent knows
- the location of the court in the club
- whether the court is a middle court or not
- whether the court is only a single's court
- whether the court is inside during Winter or not
- the court type.

Furthermore, the agent knows from the user question or for each user's name personal preferences for specific courts.

### STC Booking System Integration

The assistant integrates with the Sport- und Tennis-Club München Süd (STC) booking system via the eBuSy platform.
The system fetches real-time court availability from:

**Booking System URL:** https://siemens-tennisclub-muenchenv8.ebusy.de/lite-module/891

The system automatically:
- Fetches current availability from the STC booking system
- Parses court availability data
- Suggests available courts based on user preferences
- Provides alternative times when requested slots are unavailable
