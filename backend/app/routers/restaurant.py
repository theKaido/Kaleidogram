from fastapi import APIRouter, HTTPException

from app.dependencies.auth import CurrentUser
from app.dependencies.database import DbSession
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate

router = APIRouter()


@router.get("/restaurant")
def get_restaurant(db: DbSession, current_user: CurrentUser):
    """Return the restaurants owned by the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        List of restaurants owned by the user.

    """
    return db.query(Restaurant).filter(Restaurant.auth_id == current_user.id).all()


@router.post("/restaurant")
def restaurant_create(db: DbSession, body: RestaurantCreate, current_user: CurrentUser):
    """Create a new restaurant owned by the authenticated user.

    Args:
        db: Database session.
        body: Restaurant creation payload.
        current_user: Authenticated user who will own the restaurant.

    Returns:
        The created restaurant.

    """
    restaurant = Restaurant(
        nom=body.nom, categorie=body.categorie, auth_id=current_user.id
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get("/restaurant/{id_restaurant}")
def get_restaurant_with_id(
    db: DbSession, id_restaurant: int, current_user: CurrentUser
):
    """Return a single restaurant owned by the authenticated user.

    Args:
        db: Database session.
        id_restaurant: Id of the restaurant to fetch.
        current_user: Authenticated user, used to scope the restaurant to its owner.

    Returns:
        The matching restaurant.

    Raises:
        HTTPException: If no restaurant matches the given id for this user.

    """
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == id_restaurant, Restaurant.auth_id == current_user.id)
        .first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return restaurant


@router.put("/restaurant/{id_restaurant}")
def update_restaurant(
    db: DbSession, id_restaurant: int, body: RestaurantCreate, current_user: CurrentUser
):
    """Update the name and/or category of an existing restaurant.

    Args:
        db: Database session.
        id_restaurant: Id of the restaurant to update.
        body: Payload containing the fields to update.
        current_user: Authenticated user, used to scope the restaurant to its owner.

    Returns:
        The updated restaurant.

    Raises:
        HTTPException: If no restaurant matches the given id for this user.

    """
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == id_restaurant, Restaurant.auth_id == current_user.id)
        .first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    if body.nom:
        restaurant.nom = body.nom
    if body.categorie:
        restaurant.categorie = body.categorie
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.delete("/restaurant/{id_restaurant}")
def delete_restaurant(db: DbSession, id_restaurant: int, current_user: CurrentUser):
    """Delete a restaurant owned by the authenticated user.

    Args:
        db: Database session.
        id_restaurant: Id of the restaurant to delete.
        current_user: Authenticated user, used to scope the restaurant to its owner.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If no restaurant matches the given id for this user.

    """
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == id_restaurant, Restaurant.auth_id == current_user.id)
        .first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant supprimé"}
