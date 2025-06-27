import redis
from redis.asyncio import from_url
import json
import logging
from typing import List, Optional
from app.schemas import BookResponse
from app.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        try:
            self.redis_client = from_url(settings.redis_url, decode_responses=True)
            # Test connection
            # self.redis_client.ping()
        except redis.RedisError as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis_client = None

    def get_books(self) -> Optional[List[BookResponse]]:
        """Get books from cache"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return None

        try:
            cached_data = self.redis_client.get("books:all")
            if cached_data:
                books_data = json.loads(cached_data)
                return [BookResponse(**book) for book in books_data]
            return None
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set_books(self, books: List[BookResponse]):
        """Set books in cache with TTL"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return

        try:
            books_data = [book.model_dump()() for book in books]
            self.redis_client.setex(
                "books:all", settings.redis_ttl, json.dumps(books_data, default=str)
            )
        except redis.RedisError as e:
            logger.error(f"Cache set error: {e}")

    def invalidate_books(self):
        """Invalidate books cache"""
        if not self.redis_client:
            logger.warning("Redis client not available")
            return

        try:
            self.redis_client.delete("books:all")
        except redis.RedisError as e:
            logger.error(f"Cache invalidation error: {e}")
