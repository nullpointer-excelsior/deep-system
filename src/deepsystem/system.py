from deepsystem.config import config
from dataclasses import dataclass
import platform
import os 

@dataclass
class SystemSummary:
    os: str
    kernel: str
    cwd: str
    home: str

def get_system_summary() -> SystemSummary:
    system_name = platform.system()
    if system_name == "Darwin":
        system_name = "MacOS"
    return SystemSummary(
        os=system_name,
        kernel=platform.release(),
        cwd=os.getcwd(),
        home=os.path.expanduser("~")
    )

system_summary = get_system_summary()
