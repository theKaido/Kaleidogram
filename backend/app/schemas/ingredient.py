from pydantic import BaseModel


class IngredientCreate(BaseModel):
    """Payload for creating or renaming an ingredient."""

    nom: str
