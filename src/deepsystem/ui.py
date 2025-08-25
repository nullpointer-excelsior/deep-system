from deepsystem.system import FzfCommand
from pathlib import Path
from deepsystem import filesystem 
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

console = Console()


def display_markdown(content):
    print('')
    console.print(Markdown(content))
    print('')


def display_code(code):
    syntax = Syntax(code, "python", theme="monokai", line_numbers=False)
    print('')
    console.print(syntax)
    print('')


def select_options(options):
    return FzfCommand(['--layout', 'reverse']).input_values(options)


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