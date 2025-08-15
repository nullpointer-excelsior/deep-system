import toml
from pathlib import Path
from dataclasses import dataclass, field
from typing import TypedDict, List
from system import FzfCommand

CONFIG_DIR = Path.home() / '.config' / 'deepsystem'
CONFIG_FILEPATH = CONFIG_DIR / 'config.toml'
DATABASE_FILEPATH = CONFIG_DIR / 'database.sqlite'


class AIModelConfig(TypedDict):
    selected: str
    choices: List[str]


class AIConfig(TypedDict):
    provider: str
    model: AIModelConfig


class DatabaseConfig(TypedDict):
    path: str


class DeepSystemConfiguration(TypedDict):
    ai: AIConfig
    database: DatabaseConfig


def get_configuration() -> DeepSystemConfiguration:
    """
    Loads configuration from a TOML file. If the file does not exist,
    it is created with a default configuration and then read.
    """

    # Ensure the config directory exists
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Define the default configuration data
    default_config_data: DeepSystemConfiguration = {
        'ai': {
            'provider': 'openai',
            'model': {
                'selected': 'gpt-4.1-nano',
                'choices': ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1", "gpt-5-nano", "gpt-5", "gpt-5-mini", "o3", "o3-mini", "o4-mini"]
            }
        },
        'database': {
            'path': str(DATABASE_FILEPATH)
        }
    }

    # Write the default config only if the file doesn't exist
    if not CONFIG_FILEPATH.exists():
        with CONFIG_FILEPATH.open('w') as f:
            toml.dump(default_config_data, f)
    
    # Create the database file if it doesn't exist
    if not DATABASE_FILEPATH.exists():
        DATABASE_FILEPATH.touch()

    # Load the configuration from the TOML file
    with CONFIG_FILEPATH.open('r') as f:
        config_data = toml.load(f)
    
    return config_data


def update_ai_model():
    config = get_configuration()
    selected = FzfCommand([]).input_values(config['ai']['model']['choices'])
    if selected:
        config['ai']['model']['selected'] = selected
        with open(CONFIG_FILEPATH, 'w') as f:
            toml.dump(config, f)




