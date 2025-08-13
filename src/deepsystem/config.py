import tomllib
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DeepSystemConfig:
    """Configuration class for the DeepSystem application."""
    llm_provider: str = 'openai'
    model: str = ''
    database_path: str = ''

def get_configuration() -> DeepSystemConfig:
    """
    Loads configuration from a TOML file. If the file does not exist,
    it is created with a default configuration and then read.
    """
    config_path = Path.home() / '.config' / 'deepsystem' / 'config.toml'
    database_path = Path.home() / '.config' / 'deepsystem' / 'database.sqlite'
    default_config_content = (
        "[ai]\n"
        "provider = 'openai'\n"
        "model = 'gpt-4o'\n"
        "[database]\n"
        f"path = '{database_path}'\n"
    )

    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(default_config_content)

    if not database_path.exists():
        database_path.parent.mkdir(parents=True, exist_ok=True)
        database_path.write_text("")

    with config_path.open('rb') as f:
        config_data = tomllib.load(f)
    
    # Check if the main section exists, otherwise return a default config
    ai_section = config_data.get('ai', {})
    database_section = config_data.get('database', {})

    return DeepSystemConfig(
        llm_provider=ai_section.get('provider', 'openai'),
        model=ai_section.get('model', ''),
        database_path=database_section.get('path', '')
    )

config = get_configuration()