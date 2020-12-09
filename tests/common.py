from pathlib import Path


def get_directory_size(path: Path) -> int:
    # inspired from https://stackoverflow.com/a/1392549
    root_directory = Path(path)
    return sum(f.stat().st_size for f in root_directory.glob("**/*") if f.is_file())
