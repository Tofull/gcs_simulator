from pathlib import Path


def get_directory_size(path: Path) -> int:
    # inspired from https://stackoverflow.com/a/1392549
    root_directory = Path(path)
    return sum(f.stat().st_size for f in root_directory.glob("**/*") if f.is_file())


def get_files(path: Path):
    return [item for item in Path(path).glob("**/*") if item.is_file()]
