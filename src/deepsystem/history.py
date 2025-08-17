from deepsystem.persistence import create_checkpointer
from deepsystem.system import system_summary
from operator import attrgetter
import re
from deepsystem import ui


def find_message_content():
    thread_id = system_summary.cwd
    config = {
        "configurable": {
            "thread_id": thread_id 
        }
    }
    checkpoint = create_checkpointer()
    messages = checkpoint.get(config)["channel_values"]["messages"]
    return list(map(lambda msg: msg.content, messages))


def extract_code_snippets(markdown_content: str):
    """
    Extracts all code snippets from a markdown string and returns them with their respective file extensions.
    """
    pattern = r"```(\w+)\n(.*?)```"
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    ext_map = {
        "python": "py",
        "py": "py",
        "bash": "sh",
        "sh": "sh",
        "javascript": "js",
        "js": "js",
        "typescript": "ts",
        "ts": "ts",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "c++": "cpp",
        "go": "go",
        "golang": "go",
        "rust": "rs",
        "elixir": "ex",
        "ruby": "rb",
        "php": "php",
        "html": "html",
        "css": "css",
        "json": "json",
        "xml": "xml",
        "sql": "sql",
    }
    
    snippets = []
    for lang, code in matches:
        
        ext = ext_map.get(lang.lower(), lang.lower())
        snippets.append({
            "code": code.strip(),
            "ext": ext
        })
    
    return snippets


def get_code_snippets(contents):
    snippets = []
    for content in contents:
        snippets.extend(extract_code_snippets(content))
    return snippets


def select_code_snippet():
    code_snippets = get_code_snippets(find_message_content())
    return ui.select_code_snippet(code_snippets)