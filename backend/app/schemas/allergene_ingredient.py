from pydantic import BaseModel


class AllergeneIngredientClass(BaseModel):
    """Payload for creating or updating an allergene/ingredient link's status."""

    status: str
