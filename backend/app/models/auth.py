from sqlalchemy import Column, Integer, String

from app.database import Base


class Auth(Base):
    """Class representing Auth table."""

    __tablename__ = "auth"
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
