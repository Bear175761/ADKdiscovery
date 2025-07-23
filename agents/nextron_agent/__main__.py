import logging

import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent import root_agent as nextron_agent
from .executor import ADKAgentExecutor
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10002)
def main(host, port):
    """Creates an agent card and then lanches a A2A server with the information given."""

    purchase_faq_skill = AgentSkill(
        id="purchase_faq",
        name="Purchase FAQs",
        description= "Handles support questions about purchases,such as product issues, specs, or support policies",
        tags=["warranty", "product_questions"],
    )
    #TODO: not completed yet
    purchase_status_skill = AgentSkill(
        id="purchase_status",
        name="Purchase Status",
        description= "Handles finding the order status of packages based on a given package or order ID.",
        tags=["product_questions", "status"],
    )
    #TODO: not completed yet
    purcahse_returns_skill = AgentSkill(
        id="purchase_returns",
        name="Purchase Returns",
        description="Handles filing returns and initiates refund requests, guiding customers through eligibility, steps, and timelines.",
        tags=["returns"],
    )

    # Agent card (metadata)
    agent_card = AgentCard(
        name=nextron_agent.name,
        description=nextron_agent.description,
        url=f'http://{host}:{port}/',
        version="1.0.0",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            purchase_faq_skill,
            purchase_status_skill,
            purcahse_returns_skill
        ],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ADKAgentExecutor(
            agent=nextron_agent,
        ),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()