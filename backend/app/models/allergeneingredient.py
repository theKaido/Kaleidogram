from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class AllergeneIngredient(Base):
    """Class to represent allergene ingredient link."""

    __tablename__ = "allergeneingredient"
    id_allergene = Column(Integer, ForeignKey("allergene.id"), primary_key=True)
    id_ingredient = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    id_plat = Column(Integer, ForeignKey("plat.id"))
    status = Column(String)
