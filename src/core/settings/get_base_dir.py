from pathlib import Path


def get_base_dir() -> Path:
    src_dir: Path = Path(__file__).parent.parent.parent
    base_dir: Path = src_dir.parent
    return base_dir
