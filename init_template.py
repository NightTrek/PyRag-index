
import os
from openai import OpenAI

def init():
    os.environ["OPENAI_API_KEY"] = "" # OpenRouter or OpenAI API key
    os.environ["SERPER_API_KEY"] = "" # serper.dev API key NOT REQUIRED


    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
    os.environ["OPENAI_MODEL_NAME"] = 'anthropic/claude-3-sonnet'#   # DEFAULT MODEL if you dont specify one
    os.environ["VAULT_API_KEY"] = "" #   # Get your API key at https://vault.pash.city/

    return OpenAI(
        api_key="", # OpenRouter or OpenAI API key
        base_url="https://openrouter.ai/api/v1",
    )


