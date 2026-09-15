from pydantic import BaseModel


class AllergeneCreate(BaseModel):
    """Payload for creating or renaming an allergene."""

    nom: str
