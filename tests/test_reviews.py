import pytest


class TestReviewEndpoints:

    @pytest.fixture
    def sample_book(self, client, setup_database):
        """Create a sample book for testing reviews"""
        book_data = {
            "title": "Sample Book",
            "author": "Sample Author",
            "isbn": "1234567890",
            "description": "A sample book for testing",
            "published_year": 2023,
        }
        response = client.post("/api/v1/books/", json=book_data)
        return response.json()

    def test_create_review_success(self, client, sample_book):
        """Test creating a review successfully"""
        review_data = {
            "reviewer_name": "John Doe",
            "rating": 5,
            "review_text": "Excellent book!",
        }

        response = client.post(
            f"/api/v1/books/{sample_book['id']}/reviews", json=review_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["reviewer_name"] == review_data["reviewer_name"]
        assert data["rating"] == review_data["rating"]
        assert data["book_id"] == sample_book["id"]

    def test_create_review_book_not_found(self, client, setup_database):
        """Test creating a review for non-existent book"""
        review_data = {
            "reviewer_name": "John Doe",
            "rating": 5,
            "review_text": "Great book!",
        }

        response = client.post("/api/v1/books/999/reviews", json=review_data)
        assert response.status_code == 404
        assert "Book not found" in response.json()["detail"]

    def test_get_reviews_success(self, client, sample_book):
        """Test getting reviews for a book"""
        # Create a review first
        review_data = {
            "reviewer_name": "Jane Doe",
            "rating": 4,
            "review_text": "Good book!",
        }
        client.post(f"/api/v1/books/{sample_book['id']}/reviews", json=review_data)

        response = client.get(f"/api/v1/books/{sample_book['id']}/reviews")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["reviewer_name"] == "Jane Doe"

    def test_get_reviews_book_not_found(self, client, setup_database):
        """Test getting reviews for non-existent book"""
        response = client.get("/api/v1/books/999/reviews")
        assert response.status_code == 404


class TestIntegrationCacheMiss:

    def test_cache_miss_integration(self, client, setup_database):
        """Integration test: Cache miss scenario with database fallback"""
        # Create test books
        book1_data = {"title": "Integration Book 1", "author": "Author 1"}
        book2_data = {"title": "Integration Book 2", "author": "Author 2"}

        client.post("/api/v1/books/", json=book1_data)
        client.post("/api/v1/books/", json=book2_data)

        # Get books (should work even with cache miss)
        response = client.get("/api/v1/books/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        titles = [book["title"] for book in data]
        assert "Integration Book 1" in titles
        assert "Integration Book 2" in titles
