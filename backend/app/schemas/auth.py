from pydantic import BaseModel


class Authentification(BaseModel):
    """Payload for registering a new user account."""

    login: str
    password: str
    email: str


class PasswordUpdate(BaseModel):
    """Payload for changing a user's password."""

    current_password: str
    new_password: str
