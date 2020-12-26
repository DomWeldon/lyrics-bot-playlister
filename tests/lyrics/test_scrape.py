from unittest import mock

import lxml.html


def test__etree_from_url(
    mock_requests_get_song_list: mock.Mock, patch_requests_get_song_list: None
):
    """Check that the request is performed and parsed."""
    # arrange
    from lyrics_bot_playlister.lyrics import scrape

    mock_url = "some_url"

    # act
    etree = scrape._etree_from_url(mock_url)

    # assert
    mock_requests_get_song_list.assert_called_once_with(mock_url)
    assert type(etree) == lxml.html.HtmlElement


def test_get_song_urls(
    mock_requests_get_song_list: mock.Mock, patch_requests_get_song_list: None
):
    """Check that it parses the list of songs correctly"""
    # arrange
    from lyrics_bot_playlister.lyrics import scrape

    root_url, mock_url = "http://example.com", "/lyrics/woof.html"

    # act
    songs = scrape.get_song_urls(mock_url, root_url)

    # assert
    mock_requests_get_song_list.assert_called_once_with(root_url + mock_url)
    assert len(songs)


def test_get_song(
    mock_requests_get_song: mock.Mock, patch_requests_get_song: None
):
    """Check that it parses a song correctly"""
    # arrange
    from lyrics_bot_playlister.lyrics import scrape

    root_url, mock_url = "http://example.com", "/lyrics/woof.html"

    # act
    song = scrape.get_song(root_url + mock_url)

    # assert
    mock_requests_get_song.assert_called_once_with(root_url + mock_url)
    assert song.title == "Beautiful Head"
    assert song.album_title == "The National"
    assert song.band_name == "The National"
    assert song.track_number == 1
    assert song.release_year == "2001"
    assert "Redefining yourself" in song.lines
    assert "Designing yourself" in song.lines
