from deepsystem.system import FzfCommand
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple


def create_temporal_snippets(snippets: List[Dict[str, str]]) -> Tuple[str, List[str]]:
    """
    Create temporary files from provided snippets in the given temporary directory.

    :param snippets: List of dictionaries with 'code' and 'ext' keys.
    :return: Tuple containing the temporary directory path and list of created file names.
    """
    temp_dir = tempfile.gettempdir()
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

    return temp_dir, created_files


def convert_files_to_markdown(filenames: list) -> str:
    markdown_content = "\n"
    for file_path in filenames:
        file_name = os.path.basename(file_path)
        markdown_content += f"**{file_name}**\n"
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                extension = os.path.splitext(file_name)[1][1:]
                markdown_content += f"```{extension}\n{content}\n```\n"
        except Exception as e:
            markdown_content += f"Error reading file: {e}\n"
    return markdown_content


def create_temp_file(content: str) -> str:
    """
    Creates a temporary text file with the given content and returns its path.
    """
    temp_dir = Path(tempfile.gettempdir())
    temp_file_path = temp_dir / "temp_clipboard.txt"
    temp_file_path.write_text(content, encoding="utf-8")
    return str(temp_file_path)
