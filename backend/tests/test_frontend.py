import re

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app, dist_dir


pytestmark = pytest.mark.skipif(
    not (dist_dir / "index.html").is_file(),
    reason="Build the frontend before running deployment integration tests",
)
client = TestClient(app)


def test_frontend_and_asset_are_served():
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="root"' in response.text
    script = re.search(r'src="(/assets/[^\"]+\.js)"', response.text)
    assert script is not None
    assert client.get(script.group(1)).status_code == 200


def test_frontend_routes_and_api_stay_separate():
    assert client.get("/dashboard").text == client.get("/").text
    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/api/not-a-route").status_code == 404


def test_frontend_cannot_serve_files_outside_build_directory():
    response = client.get("/%2e%2e/%2e%2e/backend/app/main.py")
    assert response.status_code == 404
