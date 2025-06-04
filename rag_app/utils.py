import os
import json
from datetime import datetime
from typing import Tuple

def str_to_bool(x: str) -> bool:
    """
    Convert a string to a boolean value.

    Args:
        x (str): The string to convert. Expected values are "true" or "false".

    Returns:
        bool: True if the string is "true", False if it is "false".
    """

    match x:
        case "true":
            b = True
        case "false":
            b = False

    return b


def load_json(filepath: str) -> dict:
    """
    Load a JSON file and return its content as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file as a dictionary.
    """

    with open(filepath) as f:
        json_loaded = json.load(f)

    return json_loaded


def load_variables(config_path: str = "config.json") -> Tuple[str, str, str]:
    """
    Load configuration variables from a JSON file and set environment variables.

    Args:
        config_path (str): The path to the configuration JSON file. Defaults to "config.json".
    Returns:
        Tuple[str, str, str]: A tuple containing the chat model name, embeddings model name, and path to the documents.
    """

    # Load the configuration from the JSON file
    config = load_json(filepath=config_path)

    # Set openai api key variable
    os.environ["OPENAI_API_KEY"] = config.get("OPENAI_API_KEY")

    # Set tracing variable for LangSmith
    tracing = config.get("LANGCHAIN_TRACING_V2")
    os.environ["LANGCHAIN_TRACING_V2"] = tracing

    # Set LangSmith environment variables if tracing is enabled
    if str_to_bool(tracing):
        os.environ["LANGCHAIN_API_KEY"] = config.get("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_PROJECT"] = config.get("LANGCHAIN_PROJECT")

    # Get the chat model name
    chat_model = config.get("CHAT_MODEL")

    # Get the embeddings model name
    embeddings_model = config.get("EMBEDDINGS_MODEL")

    # Get the path to the documents
    docs_path = config.get("DOCS_PATH")

    return chat_model, embeddings_model, docs_path


def get_current_datetime() -> str:
    """
    Gets the current datetime formatted as a string.

    Returns:
        str: The current date and time in the format "YYYY-MM-DD-HH:MM:SS".
    """

    dt_now = datetime.now().replace(microsecond=0)
    dt_now = dt_now.strftime("%Y-%m-%d-%H:%M:%S")

    return dt_now
