import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database import Base

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

class Config:
    """Create config class with environment variables."""

    SQLALCHEMY_DATABASE_URI = (
            "postgresql://"
            + POSTGRES_USER + ":"
            + POSTGRES_PASSWORD
            + "@localhost/" + POSTGRES_DB
    )
    TESTING = True

@pytest.fixture(scope="session")
def db_engine_testing():
    """Create kaleidogram_test if needed, and prepare the schema. Runs once per pytest session."""
    admin_url = Config.SQLALCHEMY_DATABASE_URI
    admin_engine = create_engine(admin_url)
    admin_connection = admin_engine.connect().execution_options(isolation_level="AUTOCOMMIT")
    exists = admin_connection.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :name"),
        {"name": "kaleidogram_test"},
    ).scalar()
    if not exists:
        admin_connection.execute(text("CREATE DATABASE kaleidogram_test"))
    admin_connection.close()
    admin_engine.dispose()
    config_test = Config.SQLALCHEMY_DATABASE_URI + "_test"
    engine = create_engine(config_test)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(db_engine_testing):
    """Give each test its own connection/transaction, rolled back after the test."""
    connection = db_engine_testing.connect()
    transaction = connection.begin()
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()