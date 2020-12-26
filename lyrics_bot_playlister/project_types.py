import dataclasses
import typing

SongUrl = typing.NewType("SongUrl", str)


@dataclasses.dataclass
class Song:
    title: str
    album_title: str
    band_name: str
    track_number: int
    lines: typing.List[str]
    release_year: str
