from sqlalchemy import Column, Integer, String

from app.database import Base


class Ingredient(Base):
    """Class representing Ingredient table."""

    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
