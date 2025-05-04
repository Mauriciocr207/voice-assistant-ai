from enum import Enum
from pathlib import Path

class Config(Enum):
    RESOURCES_DIR = Path(__file__).parent.parent / "resources"