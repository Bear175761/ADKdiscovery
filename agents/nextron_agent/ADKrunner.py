#TODO: Currently not working,  this file will test the agent locally thru an ADK runner.
import asyncio

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    Part,
    TaskState,
    TextPart,
)
from a2a.utils import new_agent_text_message, new_task

from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts

from agent import root_agent

from nextron_agent import config



# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage
session_service = InMemorySessionService()

USER_ID = "user_1"
SESSION_ID = "session_001" # Using a fixed ID for simplicity

session = asyncio.run( session_service.create_session(
    app_name=config.app_name,
    user_id=USER_ID,
    session_id=SESSION_ID
))

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=root_agent, # The agent we want to run
    app_name=config.app_name,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)

async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])  
    final_response_text = "Agent did not produce a final response." # Default 

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")    
        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
               # Assuming text response in the first part
               final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
               final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found 
    print(f"<<< Agent Response: {final_response_text}") 

# # this would be an example without having to handle user input yourself
# async def run_conversation():
#     await call_agent_async("What is the weather like in London?",
#                                        runner=runner,
#                                        user_id=USER_ID,
#                                        session_id=SESSION_ID)

#     await call_agent_async("How about Paris?",
#                                        runner=runner,
#                                        user_id=USER_ID,
#                                        session_id=SESSION_ID) # Expecting the tool's error message

#     await call_agent_async("Tell me the weather in New York",
#                                        runner=runner,
#                                        user_id=USER_ID,
#                                        session_id=SESSION_ID)
# async def run_team_conversation():
#         print("\n--- Testing Agent Team Delegation ---")
#         session_service = InMemorySessionService()
#         APP_NAME = "weather_tutorial_agent_team"
#         USER_ID = "user_1_agent_team"
#         SESSION_ID = "session_001_agent_team"
#         session = await session_service.create_session(
#             app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
#         )
#         print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

#         actual_root_agent = globals()[weather_team]
#         runner_agent_team = Runner( # Or use InMemoryRunner
#             agent=actual_root_agent,
#             app_name=APP_NAME,
#             session_service=session_service
#         )
#         print(f"Runner created for agent '{actual_root_agent.name}'.")

#         # --- Interactions using await (correct within async def) ---
#         await call_agent_async(query = "Hello there!",
#                                runner=runner_agent_team,
#                                user_id=USER_ID,
#                                session_id=SESSION_ID)
#         await call_agent_async(query = "What is the weather in New York?",
#                                runner=runner_agent_team,
#                                user_id=USER_ID,
#                                session_id=SESSION_ID)
#         await call_agent_async(query = "Thanks, bye!",
#                                runner=runner_agent_team,
#                                user_id=USER_ID,
#                                session_id=SESSION_ID)

#TODO: Make a runner
# if __name__ == "__main__":
#     try:
#         asyncio.run(run_team_conversation())
#     except Exception as e:
#         print(f"An error occurred: {e}")
