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
