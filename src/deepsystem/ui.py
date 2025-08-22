from deepsystem.system import FzfCommand
from pathlib import Path
from typing import List, Dict
from deepsystem import filesystem 



def select_model(models):
    return FzfCommand(['--layout', 'reverse']).input_values(models)


def select_code_snippet(snippets: list) -> str:

    tempdir, values = filesystem.create_temporal_snippets(snippets)
    
    fzf = FzfCommand([
        "--preview-window=right:70%:wrap", 
        "--layout", "reverse",
        "--preview", f"bat --style=numbers --color=always {tempdir}/{{}}"
    ])
    selected = fzf.input_values(values)
    if selected:
        return Path(f"{tempdir}/{selected}").read_text()
    return None


def select_files() -> str:
    ignoredir=[
        "build",
        "test",
        ".gradle",
        "gradle",
        ".idea",
        "node_modules",
        ".venv",
        ".git",
        "__pycache__",
        "target",
        ".pytest_cache"
    ]

    fzf = FzfCommand([
        "--preview-window=right:70%:wrap", 
        "--layout", "reverse",
        "--preview", f"bat --style=numbers --color=always {{}}",
        f"--walker-skip={",".join(ignoredir)}"
    ])
    selected = fzf.select_file()
    if selected:
        return selected
    return None