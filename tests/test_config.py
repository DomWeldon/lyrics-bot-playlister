def test_config_attrs():
    """Are config attributes as expected?"""
    # arrange
    from lyrics_bot_playlister import config

    # act
    # assert
    assert config.lyrics.ROOT_URL is not None
    assert config.lyrics.BAND_NAME is not None
    assert "McFly" not in config.lyrics.BAND_NAME
