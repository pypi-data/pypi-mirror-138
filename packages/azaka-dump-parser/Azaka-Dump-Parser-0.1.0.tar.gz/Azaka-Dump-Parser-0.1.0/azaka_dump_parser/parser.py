from __future__ import annotations

import gzip
import typing as t

from .vote import Vote
from .trait import Trait
from .tag import Tag

__all__ = ("Parser",)
TYPES = t.Union[Vote, Trait, Tag]


class Parser:
    __slots__ = ("filename", "cls")

    def __init__(self, filename: str, cls: TYPES) -> None:
        self.filename = filename
        self.cls = cls

    @property
    def _file(self) -> gzip.GzipFile:
        return gzip.open(filename=self.filename, mode="rb")
    
    def __enter__(self) -> Parser:
        return self

    def __exit__(self, *_) -> None:
        self._file.close()

    def parse(self) -> t.Generator[TYPES, None, None]:
        yield from self.cls.from_dump(self._file)
