import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Hello world route returns 200
def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

# Database route returns 200 with mocked MongoDB
def test_db_route(client):
    with patch("app.db") as mock_db:
        mock_db.test_collection.find_one.return_value = {"message": "Hello, World!"}
        response = client.get('/test-db')
        assert response.status_code == 200
        assert b"DB connected. Found: Hello, World!" in response.data

# Database route handles MongoDB being unavailable
def test_db_unavailable(client):
    with patch("app.db") as mock_db:
        mock_db.test_collection.insert_one.side_effect = Exception("MongoDB unavailable")
        response = client.get('/test-db')
        assert response.status_code == 500
        assert b"Database error" in response.data

# Unknown route returns 404
def test_unknown_route(client):
    response = client.get('/unknown')
    assert response.status_code == 404