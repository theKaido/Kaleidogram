from pydantic import BaseModel


class PlatCreate(BaseModel):
    """Payload for creating or updating a dish."""

    nom: str
    categorie: str
    id_restaurant: int
