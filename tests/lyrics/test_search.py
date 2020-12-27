def test__list_contains_sequence():
    """Does it behave as expected?"""
    # arrange
    from lyrics_bot_playlister.lyrics import search

    test_cases = [
        ([1], [1], True),
        ([1], [2], False),
        ([1, 2, 3, 4], [1], True),
        ([1, 2, 3, 4], [2, 3], True),
        ([1, 2, 3, 4, 5], [4, 5, 6], False),
        ([1], [1, 2], False),
    ]

    # act
    results = [
        search._list_contains_sequence(li, se) for li, se, _ in test_cases
    ]

    # assert
    for i, r in enumerate(results):
        assert test_cases[i][2] == r, (i, test_cases[i], r)


def test_find_songs_from_lyrics(mock_songs):
    # arrange
    from lyrics_bot_playlister.lyrics import search

    # act
    s0 = search.find_songs_from_lyrics(
        ["You must be somewhere in London", "Walking Abbey Lane"], mock_songs,
    )
    s1 = search.find_songs_from_lyrics(
        ["Sorrow's my body on the waves", "Sorrow's a girl inside my cake"],
        mock_songs,
    )

    # assert
    assert s0[0].title == "England"
    assert s1[0].title == "Sorrow"
