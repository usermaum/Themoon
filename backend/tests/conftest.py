import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.api.deps import get_db

# Use in-memory SQLite for speed and isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    return engine

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine, tables):
    """Returns a sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # Begin a non-ORM transaction
    transaction = connection.begin()
    
    # Bind an individual Session to the connection
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    # Rollback the transaction
    transaction.rollback()
    connection.close()
