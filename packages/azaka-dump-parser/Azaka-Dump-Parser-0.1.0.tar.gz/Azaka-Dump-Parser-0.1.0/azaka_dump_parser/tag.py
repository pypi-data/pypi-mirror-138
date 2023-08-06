from __future__ import annotations

import gzip
import json
import typing as t

__all__ = ("Tag",)


class Tag:

    __slots__ = (
        "id",
        "name",
        "description",
        "meta",
        "searchable",
        "applicable",
        "vns",
        "cat",
        "aliases",
        "parents",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.meta: bool = data["meta"]
        self.searchable: bool = data["searchable"]
        self.applicable: bool = data["applicable"]
        self.vns: int = data["vns"]
        self.cat: str = data["cat"]
        self.aliases: t.Iterable[t.Optional[str]] = data["aliases"]
        self.parents: t.Iterable[t.Optional[int]] = data["parents"]

    @classmethod
    def from_dump(cls, file: gzip.GzipFile) -> t.Generator[Tag, None, None]:
        for data in json.load(file):
            yield cls(data)

    def __repr__(self) -> str:
        return f"<Tag id={self.id}>"
