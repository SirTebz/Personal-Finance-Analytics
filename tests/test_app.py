def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Personal Finance Analytics" in response.data


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
