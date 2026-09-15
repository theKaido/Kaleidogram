from sqlalchemy import Column, Integer, String

from app.database import Base


class Allergene(Base):
    """Class to represent allergene table."""

    __tablename__ = "allergene"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
