import shutil
from itertools import count
from pathlib import Path
from typing import Type

from pydantic import BaseModel


def camel_case(name: str) -> str:
    return "".join([name[0].lower(), name[1:]])


class Directory:
    @classmethod
    def create(cls, path: Path):
        print(f"Creating {path}")
        path.mkdir(parents=True, exist_ok=False)

    @classmethod
    def clean(cls, path: Path):
        print(f"Cleaning {path}")
        for child in path.iterdir():
            try:
                child.unlink()
            except IsADirectoryError:
                cls.remove(child)

    @classmethod
    def remove(cls, path: Path):
        print(f"Removing {path}")
        shutil.rmtree(path)  # also works when not empty

    @classmethod
    def create_or_clean(cls, path: Path):
        if path.exists():
            cls.clean(path)
        else:
            cls.create(path)


def auto_index(prefix: str, parent_cls: Type[BaseModel]) -> str:
    """Generate an auto-incremented string index for pydantic objects."""
    try:
        parent_cls._counter  # type:ignore
    except AttributeError:

        @classmethod
        def reset_counter(cls):
            cls._counter = count(start=1)

        # I somehow prefer this dirty stuff, rather than copy/pasting to
        # define reset_counter() directly in the classes' definitions...
        parent_cls.reset_counter = reset_counter  # type:ignore
        parent_cls.reset_counter()  # type:ignore

    return f"{prefix}{parent_cls._counter.__next__()}"  # type:ignore
