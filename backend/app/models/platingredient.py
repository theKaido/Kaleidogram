from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


class PlatIngredient(Base):
    """Class representing PlatIngredient link."""

    __tablename__ = "platingredient"
    id_plat = Column(Integer, ForeignKey("plat.id"), primary_key=True)
    id_ingredient = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
