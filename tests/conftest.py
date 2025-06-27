import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock
import os

from app.main import create_app
from app.database.connection import get_db, Base
from app.api.deps import get_cache_service
from app.services.cache_service import CacheService

from sqlalchemy.pool import NullPool

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_cache():
    return Mock(spec=CacheService)


@pytest.fixture(scope="function")
def test_app():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_cache_service] = override_get_cache
    return app


@pytest.fixture(scope="function")
def client(test_app):
    return TestClient(test_app)


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Ensure all connections are closed before dropping tables
    engine.dispose()
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture
def mock_cache():
    return Mock(spec=CacheService)
