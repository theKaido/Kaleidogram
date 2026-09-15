from fastapi import APIRouter, HTTPException

from app.dependencies.database import DbSession
from app.models.allergene import Allergene
from app.schemas.allergene import AllergeneCreate

router = APIRouter()


@router.get("/allergene")
def get_allergene(db: DbSession):
    """Return all allergenes.

    Args:
        db: Database session

    Returns:
        List of Allergenes

    """
    return db.query(Allergene).all()


@router.post("/allergene")
def allergene_create(db: DbSession, body: AllergeneCreate):
    """Create a new allergene.

    Args:
        db: Database session.
        body: Allergene creation payload.

    Returns:
        The created allergene.

    """
    allergene = Allergene(nom=body.nom)
    db.add(allergene)
    db.commit()
    db.refresh(allergene)
    return allergene


@router.get("/allergene/{id_allergene}")
def get_allergene_with_id(db: DbSession, id_allergene: int):
    """Return a single allergene by id.

    Args:
        db: Database session.
        id_allergene: Id of the allergene to fetch.

    Returns:
        The matching allergene.

    Raises:
        HTTPException: If no allergene matches the given id.

    """
    allergene = db.query(Allergene).filter(Allergene.id == id_allergene).first()
    if allergene is None:
        raise HTTPException(status_code=404, detail="Allergene non trouvé")
    return allergene


@router.put("/allergene/{id_allergene}")
def update_allergene_name(db: DbSession, id_allergene, body: AllergeneCreate):
    """Update the name of an existing allergene.

    Args:
        db: Database session.
        id_allergene: Id of the allergene to update.
        body: Payload containing the new name.

    Returns:
        The updated allergene.

    Raises:
        HTTPException: If no allergene matches the given id.

    """
    allergene = db.query(Allergene).filter(Allergene.id == id_allergene).first()
    if allergene is None:
        raise HTTPException(status_code=404, detail="Allergene non trouvé")
    allergene.nom = body.nom
    db.commit()
    db.refresh(allergene)
    return allergene


@router.delete("/allergene/{id_allergene}")
def remove_allergene(db: DbSession, id_allergene: int):
    """Delete an allergene by id.

    Args:
        db: Database session.
        id_allergene: Id of the allergene to delete.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If no allergene matches the given id.

    """
    allergene = db.query(Allergene).filter(Allergene.id == id_allergene).first()
    if allergene is None:
        raise HTTPException(status_code=404, detail="Allergene non trouvé")
    db.delete(allergene)
    db.commit()
    return {"message": "Allergène supprimé"}
