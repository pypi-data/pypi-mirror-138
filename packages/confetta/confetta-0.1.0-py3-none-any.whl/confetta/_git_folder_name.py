from pathlib import Path
from typing import Union

__all__ = ("git_folder_name",)


def _git_folder_name(path: Path) -> Union[str, None]:
    maybe_git = path / ".git"
    if maybe_git.exists() and maybe_git.is_dir():
        return path.name

    if path == Path(path.root):
        return None

    return _git_folder_name(path.parent)


def git_folder_name(path: Union[Path, str, None] = None) -> Union[str, None]:
    if path is None:
        path = Path()
    elif isinstance(path, str):
        path = Path(path)

    if not path.is_absolute():
        path = path.absolute()

    return _git_folder_name(path)
