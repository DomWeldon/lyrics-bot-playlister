import fastapi


def test_root(test_client: fastapi.testclient.TestClient):
    # arrange
    expected_status = fastapi.status.HTTP_200_OK

    # act
    r = test_client.get("/")

    # assert
    assert r.status_code == expected_status
