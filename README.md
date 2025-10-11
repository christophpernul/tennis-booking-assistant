# tennis-booking-assistant

An AI agent that helps to find and book tennis courts.

## Useful links
- [openai-agents-python Docu](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents Docu](https://platform.openai.com/docs/guides/agents)
- [OpenAI Traces](https://platform.openai.com/logs?api=traces)
-

## Technical setup

The dependencies can be installed with `uv sync`.
The agent is built using `openai` and `agents` frameworks and uses `gpt-4o-mini` as a default LLM model.

## CI/CD Configuration

The repository includes the following CI/CD pipelines:
- `pre-commit`: Executes `pre-commit` hooks on new commits
- `docker-build-push`: Builds a Docker image from the code, tags it properly and pushes it to GCP

## Cloud Deployment

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
   python run.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:7860` to access the Gradio interface.

### Project Structure

```
tennis-booking-assistant/
├── src/
│   ├── agent/           # AI agent logic
│   ├── booking/         # STC booking system integration
│   ├── data/           # Court data and user preferences
│   ├── interface/      # Gradio web interface
│   └── main.py         # Application entry point
├── run.py              # CLI launcher
├── test_setup.py       # Setup verification
└── pyproject.toml      # Project configuration
```

## Assistant Purpose

A user can ask a question to the AI assistant and gives him information about at which time, for how long and additional information
he wants to play tennis. The agent processes this information and then fetches the current bookings from the STC booking system and
suggests the user available courts for booking. The agent might also consider user preferences of which courts he wants to play from the
question and additional context information that is hard coded about the courts. If no booking is possible at the preferred courts of the user
the agent suggests other courts. If no courts are available for the time the user wants to play, the agent suggests a different time near
to the time the user asked for.

There is a gradio frontend that only shows a chatprompt, that ideally has the ability to get voice input. An additional HTML element is shown with the
answer of the agent.

## Assistant technical information

The agent knows context about the courts. For each court the agent knows
- the location of the court in the club
- whether the court is a middle court or not
- whether the court is only a single's court
- the court type.

Furthermore, the agent knows from the user question or for each user's name personal preferences for specific courts.

The agent should answer very short and precise and give a nice list overview of the suggested courts and times for booking.

## STC Booking System Integration

The assistant integrates with the Sport- und Tennis-Club München Süd (STC) booking system via the eBuSy platform. The system fetches real-time court availability from:

**Booking System URL:** https://siemens-tennisclub-muenchenv8.ebusy.de/lite-module/891

**Available Courts:**
- **Platz A:** links, Aufschlagtrainingsplatz, Ballmaschinenplatz (nur Einzel)
- **Platz 1-6:** links, Tennisschule (Platz 1-5 sind Mittelplätze)
- **Platz 7-9:** Eingang rechts, Sandplätze (Platz 8 ist Mittelplatz)
- **Platz 10-12:** Eingang rechts, Granulatplätze (Platz 11 ist Mittelplatz)
- **T-Platz:** Mitte, vor dem Restaurant (nur Einzel)
- **Platz 14-22:** hinten, Sandplätze (Platz 15, 18, 21 sind Mittelplätze, Platz 17 ist Wingfield)

The system automatically:
- Fetches current availability from the STC booking system
- Parses court availability data
- Suggests available courts based on user preferences
- Provides alternative times when requested slots are unavailable
