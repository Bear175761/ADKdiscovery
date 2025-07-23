#TODO: Rewrite fully to fix nextron
# This file stores the code to execute A2A requests with ADK.

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

class ADKAgentExecutor(AgentExecutor):
    def __init__(
        self,
        agent,
        status_message="Processing request...",
        artifact_name="response",
    ):
        """Initialize a generic ADK agent executor.

        Args:
            agent: The ADK agent instance
            status_message: Message to display while processing
            artifact_name: Name for the response artifact
        """
        self.agent = agent
        self.status_message = status_message
        self.artifact_name = artifact_name
        self.runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        #context is an object providing information about the incoming request such as the users message and any existing task details.
        #event_queue is used by the executor to send events back to the client.
        query = context.get_user_input()
        # Queue up any tasks
        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)

        # Helper class for agents to publish updates to a task's event queue.
        # Simplifies the process of creating and enqueueing standard task events.
        updater = TaskUpdater(event_queue, task.id, task.contextId)

        if context.call_context:
            user_id = context.call_context.user.user_name
        else:
            user_id = "a2a_user"

        try:
            # Update status with custom message
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message, task.contextId, task.id),
            )

            # Process with ADK agent
            # usint task.contextId will ensure each task refers to a seperate ADK session
            session = await self.runner.session_service.create_session(
                app_name=self.agent.name,
                user_id=user_id,
                state={},
                session_id=task.contextId,
            )

            # Prepare the user's message in ADK format
            content = types.Content(
                role="user", parts=[types.Part.from_text(text=query)]
            )

            response_text = ""

            # Key Concept: run_async executes the agent logic and yields Events.
            # We iterate through events to find the final answer.
            async for event in self.runner.run_async(
                user_id=user_id, session_id=session.id, new_message=content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_text += part.text + "\n"
                        elif hasattr(part, "function_call"):
                            # Log or handle function calls if needed
                            pass  # Function calls are handled internally by ADK

            # Add response as artifact with custom name
            await updater.add_artifact(
                [Part(root=TextPart(text=response_text))],
                name=self.artifact_name,
            )

            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Error: {e!s}", task.contextId, task.id),
                final=True,
            )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancel the execution of a specific task."""
        raise NotImplementedError(
            "Cancellation is not implemented for ADKAgentExecutor... yet"
        )