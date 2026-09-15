from fastapi import APIRouter, HTTPException

from app.dependencies.auth import CurrentUser
from app.dependencies.database import DbSession
from app.models.plat import Plat
from app.models.restaurant import Restaurant
from app.schemas.plat import PlatCreate

router = APIRouter()


@router.get("/plat")
def get_plat(db: DbSession, current_user: CurrentUser):
    """Return the dishes belonging to the authenticated user's restaurants.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        List of dishes owned by the user's restaurants.

    """
    return (
        db.query(Plat)
        .join(Restaurant)
        .filter(Restaurant.auth_id == current_user.id)
        .all()
    )


@router.post("/plat")
def create_plat(db: DbSession, body: PlatCreate, current_user: CurrentUser):
    """Create a new dish for one of the authenticated user's restaurants.

    Args:
        db: Database session.
        body: Dish creation payload, including the target restaurant id.
        current_user: Authenticated user, used to check restaurant ownership.

    Returns:
        The created dish.

    Raises:
        HTTPException: If the target restaurant doesn't exist or isn't owned by the user.

    """
    restaurant = (
        db.query(Restaurant)
        .filter(
            Restaurant.id == body.id_restaurant, Restaurant.auth_id == current_user.id
        )
        .first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Id_restaurant non trouvé")
    plat = Plat(
        nom=body.nom, categorie=body.categorie, id_restaurant=body.id_restaurant
    )
    db.add(plat)
    db.commit()
    db.refresh(plat)
    return plat


@router.get("/plat/{id_plat}")
def get_plat_with_id(db: DbSession, id_plat: int, current_user: CurrentUser):
    """Return a single dish owned by one of the authenticated user's restaurants.

    Args:
        db: Database session.
        id_plat: Id of the dish to fetch.
        current_user: Authenticated user, used to scope the dish to their restaurants.

    Returns:
        The matching dish.

    Raises:
        HTTPException: If no dish matches the given id for this user.

    """
    plat = (
        db.query(Plat)
        .join(Restaurant)
        .filter(Plat.id == id_plat, Restaurant.auth_id == current_user.id)
        .first()
    )
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    return plat


@router.put("/plat/{id_plat}")
def update_plat(
    db: DbSession, id_plat: int, current_user: CurrentUser, body: PlatCreate
):
    """Update the name and/or category of an existing dish.

    Args:
        db: Database session.
        id_plat: Id of the dish to update.
        current_user: Authenticated user, used to scope the dish to their restaurants.
        body: Payload containing the fields to update.

    Returns:
        The updated dish.

    Raises:
        HTTPException: If no dish matches the given id for this user.

    """
    plat = (
        db.query(Plat)
        .join(Restaurant)
        .filter(Plat.id == id_plat, Restaurant.auth_id == current_user.id)
        .first()
    )
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    if body.nom:
        plat.nom = body.nom
    if body.categorie:
        plat.categorie = body.categorie
    db.commit()
    db.refresh(plat)
    return plat


@router.delete("/plat/{id_plat}")
def delete_plat(db: DbSession, id_plat: int, current_user: CurrentUser):
    """Delete a dish owned by one of the authenticated user's restaurants.

    Args:
        db: Database session.
        id_plat: Id of the dish to delete.
        current_user: Authenticated user, used to scope the dish to their restaurants.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If no dish matches the given id for this user.

    """
    plat = (
        db.query(Plat)
        .join(Restaurant)
        .filter(Plat.id == id_plat, Restaurant.auth_id == current_user.id)
        .first()
    )
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    db.delete(plat)
    db.commit()
    return {"message": "Plat supprimé"}
