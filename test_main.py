from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_search_books():
    r = client.get("/books", params={"q": "Python"})
    assert r.status_code == 200
    assert any("Python" in b["title"] for b in r.json())


def test_search_books_treats_sql_characters_as_data():
    r = client.get("/books", params={"q": "' OR '1'='1"})
    assert r.status_code == 200
    assert r.json() == []


def test_get_book():
    r = client.get("/books/1")
    assert r.status_code == 200
    assert "title" in r.json()


def test_add_and_list_reviews():
    client.post("/reviews", json={"book_id": 1, "text": "Great read"})
    r = client.get("/reviews/1")
    assert r.status_code == 200
    assert "Great read" in r.json()


def test_cors_only_allows_the_local_origin():
    allowed = client.get("/books", headers={"Origin": "http://localhost:8000"})
    blocked = client.get("/books", headers={"Origin": "https://example.com"})

    assert allowed.headers["access-control-allow-origin"] == "http://localhost:8000"
    assert "access-control-allow-origin" not in blocked.headers


def test_source_uses_environment_values_for_secrets():
    source = Path(__file__).with_name("main.py").read_text()

    assert 'os.environ.get("BOOKSTORE_API_KEY")' in source
    assert 'os.environ.get("BOOKSTORE_SECRET_TOKEN")' in source
    assert "sk-live-" not in source
    assert "supersecret-" not in source


def test_frontend_renders_reviews_as_text():
    source = Path("static/index.html").read_text()

    assert ".innerHTML" not in source
    assert ".textContent" in source
