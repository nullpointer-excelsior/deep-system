from deepsystem.system import FzfCommand
import os
import tempfile
from pathlib import Path
from typing import List, Dict


def _create_temporal_snippets(temp_dir: str, snippets: List[Dict[str, str]]) -> List[str]:
    """
    Create temporary files from provided snippets in the given temporary directory.

    :param temp_dir: Path to the temporary directory.
    :param snippets: List of dictionaries with 'code' and 'ext' keys.
    :return: List of created file paths.
    """
    if not os.path.isdir(temp_dir):
        raise ValueError("The provided directory does not exist or is not a directory.")

    created_files = []
    for index, snippet in enumerate(snippets):
        ext = snippet.get("ext", "").strip().lstrip(".")
        if not ext:
            raise ValueError("Each snippet must contain a valid 'ext' value.")
        code = snippet.get("code", "")
        file_name = f"snippet_{index}.{ext}"
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)
        created_files.append(file_name)

    return created_files


def select_model(models):
    return FzfCommand(['--layout', 'reverse']).input_values(models)


def select_code_snippet(snippets: list) -> str:
    tempdir = tempfile.gettempdir()
    values = _create_temporal_snippets(tempdir, snippets)
   
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