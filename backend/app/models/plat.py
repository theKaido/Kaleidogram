from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class Plat(Base):
    """Class representing Plat table."""

    __tablename__ = "plat"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie = Column(String)
    id_restaurant = Column(Integer, ForeignKey("restaurant.id"))
