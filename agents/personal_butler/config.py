import os

from dataclasses import dataclass

#MODEL = "gemini-2.0-flash"
#MODEL = "gemini-live-2.5-flash"
# MODEL = "gemini-live-2.5-flash-preview-native-audio"
# for a list of compatible models visit, 
# https://ai.google.dev/gemini-api/docs/models#model-variations
# https://docs.litellm.ai/docs/providers/openai#openai-chat-completion-models
# https://docs.litellm.ai/docs/providers/anthropic

@dataclass
class BotConfiguration:
    """Configuration for research-related models and parameters.

    Attributes:
        critic_model (str): Model for evaluation tasks.
        worker_model (str): Model for working/generation tasks.
        max_search_iterations (int): Maximum search iterations allowed.
    """

    critic_model: str = "gemini-2.5-pro"
    worker_model: str = "gemini-live-2.5-flash-preview-native-audio"
    # worker_model: str = "gemini-2.5-flash"
    live_model: str = "gemini-live-2.5-flash-preview-native-audio"
    basic_model: str = "gemini-2.0-flash"
    #max_search_iterations: int = 5

    app_name: str = "nextron_support_agent"


config = BotConfiguration()