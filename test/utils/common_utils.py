from pathlib import Path


def get_project_root_str() -> str:
    return str(Path(__file__).parent.parent.parent)
