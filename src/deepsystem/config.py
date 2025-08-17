import toml
from pathlib import Path
from typing import TypedDict, List, Callable
from deepsystem import ui

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


def _load_configuration() -> DeepSystemConfiguration:
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


_config_instance = _load_configuration()


def get_configuration() -> DeepSystemConfiguration:
    return _config_instance


def reduce_config(reducer_callback: Callable[[DeepSystemConfiguration], DeepSystemConfiguration]) -> DeepSystemConfiguration:
    config_updated = reducer_callback(_config_instance)
    with CONFIG_FILEPATH.open('w') as file:
        toml.dump(config_updated, file)
    return config_updated


def update_ai_model():
    global _config_instance
    
    model_choices = _config_instance['ai']['model']['choices']
    selected = ui.select_model(model_choices)
    
    if selected:
        
        def reducer(config: DeepSystemConfiguration):
            config["ai"]['model']['selected'] = selected
            return config
        
        _config_instance = reduce_config(reducer)
        return True
    
    return False