import os
import asyncio
import datetime
from typing import Optional

from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import google_search

from .config import config
from . import prompts

#Example successful data output
#"tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
#Example unsuccessful data output
#return {
#    "status": "error",
#    "error_message": f"Weather information for '{city}' is not available.",
#}

# Remember docstrings are essential for the agent to use tools correctly.

# MCP tools
# mcp_toolset, _ = await MCPToolset.from_server(
#   connection_params=StdioServerParameters(
#     command='npx',
#     args=["-y",
#       "@toolrepo/toolserver",
#     ]
#   )
# )

def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
        # print(f"--- Tool: say_hello called with name: {name} ---")
    else:
        # Default greeting if name is None or not explicitly passed
        greeting = "Hello there! Welcome to nextron, your one stop shop for all of your electronics needs. How may I help you today?"
        # print(f"--- Tool: say_hello called without a specific name (name_arg_value: {name}) ---")
    return greeting

def check_order_status(package_ID: int):
    """Retrieves the current order status

    Args: The order number or package ID
    
    Returns:
        dict: status and result or error msg.
    """

    return {
        "status": "success",
        "report": "We lost your package and it will never come, sorry",
    }

def product_support_policy(product_name: str):
    """ Function which will determine the support policies of a product.
    Args:
        product_name (str): The name of the product of which to recieve support info on.
    
    Returns:
        dict: status and result or error msg.
    """
    return {
        "status": "success",
        "report": f"{product_name} is not under a warranty, sorry"
    }

def refund_generator(purchase_ID: int):
    """ Function which will file a refund and return order.

    Args: 
        purchase_ID (int): The purchase ID of the product which needs to be returned.
    
    Returns:
        dict: status and result or error msg.
    """
    return{
        "status": "error",
        "error_message": "User is not eligible to refund this item."
    }

greeting_agent = Agent(
    # Using a potentially different/cheaper model for a simple task
    model = config.worker_model,
    # model=LiteLlm(model=MODEL_GPT_4O), # If you would like to experiment with other models
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                "Use the 'say_hello' tool to generate the greeting. "
                "If the user provides their name, make sure to pass it to the tool. "
                "Do not engage in any other conversation or tasks.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
    tools=[say_hello],
)
# answer support questions about their purchases, such as product issues, specs, or support policies
purchase_faq_agent = Agent(
    name="purchase_faq_agent",
    model=config.worker_model,
    description=(
        "Handles support questions about purchases,such as product issues, specs, or support policies "
    ),
    instruction="""
    - Your job is to answer questions about a users purchase. 
    - You will ask them which product they would like to ask a question about. 
    - You will answer any questions about product issues, specs, that a user might have.
    - If a user has asks about a warranty for a specific purchase you will use the `product_support_policy` tool in order to provide an answer
    - Do not answer any questions which are not relevant to the product at hand. Dont ask follow up questions.
    """,
    tools = [product_support_policy],
)

# to find and share the order status of a package when a customer provides a valid package or order ID.
purchase_status_agent = Agent(
    name="purchase_status_agent",
    model=config.worker_model,
    description=(
        "Handles finding the order status of packages based on a given package or order ID."
    ),
    instruction=""" 
    - Your job is to obtain the status of packages based on a given package or order ID. 
    - You will ask the user for a package ID and then use the `check_order_status` tool in order to retrieve the status of a package.
    - Tell the user when their package will arrive based on the gathered info. 
    """,
    tools = [check_order_status],
)

purchase_return_agent = Agent(
    name="purchase_return_agent",
    model=config.worker_model,
    description=(
        "Handles filing returns and initiates refund requests, guiding customers through eligibility, steps, and timelines."
    ),
    instruction="""
    - Your job is to guide the user through the process of creating a return and refunding their purchases.
    - You will ask users for their order ID and use the `refund_generator` tool in order to create a refund for the selected item.
    - If the user is not eligible for a refund you will tell them.
    """,
    tools=[refund_generator],

)

#TODO: Implement MCP with the advertising agent.
advertising_agent = Agent(
    name="advertising_agent",
    model=config.worker_model,
    description=("Notifies the user of any product deals and offers in the nextron store."),
    #tools = mcp_toolset.get_tools(),
)

customer_support_steering_agent = Agent(
    name="customer_support_steering_agent",
    model=config.worker_model,
    description=(
        "Helpful customer support agent for the company Nextron."
    ),
    instruction=prompts.ROOT_AGENT_INSTR,
    sub_agents = [
    purchase_faq_agent,
    purchase_status_agent,
    purchase_return_agent,
    greeting_agent,
    # account_recovery_agent,
    # gift_card_agent,
    # account_managment_agent,
    # update_membership_agent,
    # manage_subscription_agent
    ],
)

# Nextron Phone system greeting agent
# - Listen to available offers (MCP here)
# - Delivery order status or returns
# - Help with signing in (Live agent & auth)
# - Gift card buying
# - Membership, subscription or communications
#About the fake company.

#Export the steering agent as the root agent.
root_agent = customer_support_steering_agent
