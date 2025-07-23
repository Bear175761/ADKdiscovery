import os
import asyncio
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import google_search

from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Part

#Constants
MODEL = "gemini-2.0-flash"
# for a list of compatible models visit, 
# https://ai.google.dev/gemini-api/docs/models#model-variations
# https://docs.litellm.ai/docs/providers/openai#openai-chat-completion-models
# https://docs.litellm.ai/docs/providers/anthropic

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """

    print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
    city_normalized = city.lower().replace(" ", "") # Basic normalization

    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


MODEL = "gemini-2.0-flash"
MODEL = "gemini-live-2.5-flash"
MODEL = "gemini-live-2.5-flash-preview-native-audio"

root_agent = Agent(
    name="weather_time_agent",
    model=MODEL,
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)

# def main():
#     # --- Session Management ---
#     # Key Concept: SessionService stores conversation history & state.
#     # InMemorySessionService is simple, non-persistent storage for this tutorial.
#     session_service = InMemorySessionService()

#     # Define constants for identifying the interaction context
#     APP_NAME = "weather_tutorial_app"
#     USER_ID = "user_1"
#     SESSION_ID = "session_001" # Using a fixed ID for simplicity

#     # Create the specific session where the conversation will happen
#     session = await session_service.create_session(
#         app_name=APP_NAME,
#         user_id=USER_ID,
#         session_id=SESSION_ID
#     )
#     print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

#     # --- Runner ---
#     # Key Concept: Runner orchestrates the agent execution loop.
#     runner = Runner(
#         agent=root_agent, # The agent we want to run
#         app_name=APP_NAME,   # Associates runs with our app
#         session_service=session_service # Uses our session manager
#     )
#     print(f"Runner created for agent '{runner.agent.name}'.")
    
# if __name__ == "__main__":
#     main()