from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    """Payload for creating or updating a restaurant."""

    nom: str
    categorie: str
