"""
config_parser.py

This module provides functions to load configuration from a YAML file and extract Apprise URLs,
handling environment variable lookups.
"""

# pylint: disable=C0301

import os
from typing import Dict, Any, List
import yaml


def load_config(config_file_path: str) -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.

    Args:
        config_file_path (str): The path to the YAML configuration file.

    Returns:
        Dict[str, Any]: A dictionary containing the loaded configuration.

    Raises:
        FileNotFoundError: If the specified config file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_file_path}")

    with open(config_file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def get_apprise_urls(config: Dict[str, Any]) -> List[str]:
    """
    Extracts Apprise URLs from the configuration, handling environment variable lookups.

    Args:
        config (Dict[str, Any]): The loaded configuration dictionary.

    Returns:
        List[str]: A list of resolved Apprise notification URLs.
    """
    apprise_urls = config.get("apprise_urls", [])
    resolved_urls = []
    for url in apprise_urls:
        if isinstance(url, str) and url.startswith("env:"):
            env_var_name = url[4:]  # Remove "env:" prefix
            env_value = os.getenv(env_var_name)
            if env_value:
                resolved_urls.append(env_value)
            else:
                print(
                    f"WARNING: Environment variable '{env_var_name}' not set for Apprise URL. Skipping."
                )
        else:
            resolved_urls.append(url)
    return resolved_urls
