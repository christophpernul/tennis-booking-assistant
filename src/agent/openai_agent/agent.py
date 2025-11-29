"""
Tennis booking AI agent that processes user requests and suggests available courts.
"""

from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    SQLiteSession,
    trace,
    gen_trace_id,
    OpenAIChatCompletionsModel,
)

from src.agent.openai_agent.prompts import SYSTEM_PROMPT
from src.agent.openai_agent.tools import (
    get_court_availability_tool,
    get_court_attributes_tool,
)


class OpenAIAgent:
    def __init__(
        self,
        trace_id: str,
        llm_api_key: str,
        llm_name: str,
        llm_api_base_url: str = None,
    ):
        if llm_name.startswith("gpt"):
            model = llm_name
        elif llm_name.startswith("gemini"):
            gemini_client = AsyncOpenAI(base_url=llm_api_base_url, api_key=llm_api_key)
            model = OpenAIChatCompletionsModel(
                model=llm_name, openai_client=gemini_client
            )
        else:
            raise RuntimeError(
                f"Model not known, make sure it is either an OpenAI or a Gemini model, got: {llm_name}"
            )
        self.agent = Agent(
            name="BookingRecommender",
            model=model,
            instructions=self._get_system_message(),
            tools=[
                get_court_availability_tool,
                get_court_attributes_tool,
            ],
        )
        self.session = SQLiteSession(trace_id)

    @staticmethod
    def _get_system_message() -> str:
        """Get the system message for the AI agent."""
        return SYSTEM_PROMPT

    async def run_agent(self, user_message: str) -> str:
        """Run the agent with the given user message."""
        print("Starting booking manager...")
        response = await Runner.run(
            self.agent,
            user_message,
            session=self.session,
            # context=self.context
        )
        return response.final_output


class BookingManager:
    """AI agent for tennis court booking assistance."""

    def __init__(self, llm_api_key: str, llm_name: str, llm_api_base_url: str = None):
        self.trace_id = gen_trace_id()
        self.openai_agent = OpenAIAgent(
            trace_id=self.trace_id,
            llm_api_key=llm_api_key,
            llm_name=llm_name,
            llm_api_base_url=llm_api_base_url,
        )

    async def run(
        self, message: str, history: list[dict] = None
    ) -> tuple[str, list[dict]]:
        """
        Process a chat message and return the agent's response.

        Args:
            message: User's message
            history: Chat history in messages format

        Returns:
            Tuple of (response, updated_history)
        """
        if history is None:
            history = []

        if not message.strip():
            return "", history

        try:
            with trace("Tennis Agent", trace_id=self.trace_id):
                print(
                    f"View trace: https://platform.openai.com/traces/trace?trace_id={self.trace_id}"
                )
                # yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
                response = await self.openai_agent.run_agent(message)
        except Exception as e:
            print(f"Error processing request: {e}")
            response = "I'm sorry, I encountered an error processing your request. Please try again."

        # Update history with messages format
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})

        return response, history
