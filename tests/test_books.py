import pytest
from unittest.mock import patch


class TestBookEndpoints:

    def test_create_book_success(self, client, setup_database):
        """Test creating a book successfully"""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "description": "A test book",
            "published_year": 2023,
        }

        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert "id" in data

    def test_create_book_invalid_data(self, client, setup_database):
        """Test creating a book with invalid data"""
        book_data = {"title": "", "author": "Test Author"}  # Invalid: empty title

        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == 422

    def test_get_books_success(self, client, setup_database):
        """Test getting all books"""
        # Create a book first
        book_data = {"title": "Test Book", "author": "Test Author"}
        client.post("/api/v1/books/", json=book_data)

        response = client.get("/api/v1/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == "Test Book"

    def test_get_book_by_id_success(self, client, setup_database):
        """Test getting a specific book by ID"""
        # Create a book first
        book_data = {"title": "Test Book", "author": "Test Author"}
        create_response = client.post("/api/v1/books/", json=book_data)
        book_id = create_response.json()["id"]

        response = client.get(f"/api/v1/books/{book_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Book"

    def test_get_book_by_id_not_found(self, client, setup_database):
        """Test getting a non-existent book"""
        response = client.get("/api/v1/books/999")
        assert response.status_code == 404
