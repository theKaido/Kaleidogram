from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class Restaurant(Base):
    """Class representing Restaurant table."""

    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie = Column(String)
    auth_id = Column(Integer, ForeignKey("auth.id"), nullable=False)
