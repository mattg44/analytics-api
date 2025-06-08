import sqlmodel
import os

from loguru import logger


DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL == "":
    raise NotImplementedError(
        "DATABASE_URL is not set. Please set the DATABASE_URL environment variable."
    )

engine = sqlmodel.create_engine(
    DATABASE_URL,
    echo=True,
)


def init_db_session():
    """
    Initializes the database session by creating all tables defined in the SQLModel metadata.

    Logs the start and completion of the database session initialization process.
    """
    logger.info("Initializing database session")
    sqlmodel.SQLModel.metadata.create_all(engine)
    logger.info("Database session initialized")


def get_db_session():
    """
    Yields a SQLModel database session for use in database operations.

    This function manages the lifecycle of a database session, ensuring that the session is properly opened and closed.
    It logs the creation and closure of the session for debugging and monitoring purposes.

    Yields:
        sqlmodel.Session: An active database session object.
    """
    logger.info("Getting database session")
    with sqlmodel.Session(engine) as session:
        yield session
    logger.info("Database session closed")
