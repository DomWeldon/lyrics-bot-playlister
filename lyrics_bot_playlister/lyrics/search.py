import string
import typing

from .. import project_types as pt


def _list_contains_sequence(
    li: typing.List[typing.Any], se: typing.List[typing.Any]
) -> bool:
    """Does the list contain the sequence?"""
    n = len(se)
    if n > len(li):
        return False

    if n == len(li) and li == se:
        return True

    for i in range(len(li[:-n])):
        rows = li[i : i + n]  # noqa: E203
        if rows == se:
            return True

    return False


def _remove_punctuation(s: str) -> str:
    """Get rid of all punctuation"""
    return "".join(
        x.lower() for x in s if x.lower() in string.ascii_lowercase + " "
    )


def find_songs_from_lyrics(
    lyrics: typing.List[str], songs: typing.List[pt.Song]
) -> typing.List[pt.Song]:
    """Find a song based on a sequence of lyrics."""
    matches = [
        song
        for song in songs
        if _list_contains_sequence(
            [_remove_punctuation(line) for line in song.lines],
            [_remove_punctuation(line) for line in lyrics],
        )
    ]

    if matches:
        return matches

    # can we match on just one lyric?
    for line in lyrics:
        matches = [
            song
            for song in songs
            if _list_contains_sequence(
                [_remove_punctuation(line_) for line_ in song.lines],
                [_remove_punctuation(line)],
            )
        ]
        if matches:
            return matches

    # are commas being confused with new lines?
    if any("," in line for line in lyrics):
        for line in lyrics:
            matches = [
                song
                for song in songs
                if _list_contains_sequence(
                    [_remove_punctuation(line_) for line_ in song.lines],
                    [
                        _remove_punctuation(line_.strip())
                        for line_ in line.split(",")
                    ],
                )
            ]
            if matches:
                return matches

    return []
