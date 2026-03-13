from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_url(client: TestClient):
    response = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert len(data["short_code"]) == 6


def test_shorten_same_url_twice_returns_same_code(client: TestClient):
    response1 = client.post("/shorten", json={"original_url": "https://www.google.com"})
    response2 = client.post("/shorten", json={"original_url": "https://www.google.com"})
    assert response1.json()["short_code"] == response2.json()["short_code"]


def test_shorten_invalid_url(client: TestClient):
    response = client.post(
        "/shorten",
        json={"original_url": "nao-e-uma-url"},
    )
    assert response.status_code == 422


def test_redirect(client: TestClient):
    create = client.post("/shorten", json={"original_url": "https://www.google.com"})
    code = create.json()["short_code"]

    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.google.com/"


def test_redirect_not_found(client: TestClient):
    response = client.get("/codigo-inexistente", follow_redirects=False)
    assert response.status_code == 404


def test_stats(client: TestClient):
    create = client.post("/shorten", json={"original_url": "https://www.google.com"})
    code = create.json()["short_code"]

    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)

    stats = client.get(f"/stats/{code}")
    assert stats.status_code == 200
    assert stats.json()["access_count"] == 2


def test_stats_not_found(client: TestClient):
    response = client.get("/stats/codigo-inexistente")
    assert response.status_code == 404