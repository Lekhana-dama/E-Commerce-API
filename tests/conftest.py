import os
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.dependencies.database import get_db
from app.database.database import Base
from app.main import app
from fastapi.testclient import TestClient


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise RecursionError(
        "Test_DAtaBASE_URL is not configured"
    )

test_engine=create_engine(TEST_DATABASE_URL)
TestingSessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
    
)

@pytest.fixture(scope="session",autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db():
    database=TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db]=override_get_db
    with TestClient(app) as test_client:
            yield test_client
    app.dependency_overrides.clear()