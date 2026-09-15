from fastapi import APIRouter, HTTPException

from app.dependencies.auth import CurrentUser
from app.dependencies.database import DbSession
from app.models.ingredient import Ingredient
from app.models.plat import Plat
from app.models.platingredient import PlatIngredient
from app.models.restaurant import Restaurant

router = APIRouter()


@router.get("/restaurant/plat/{id_restaurant}")
def get_all_plat_from_restaurant(
    db: DbSession, id_restaurant: int, current_user: CurrentUser
):
    """Return all dishes belonging to one of the authenticated user's restaurants.

    Args:
        db: Database session.
        id_restaurant: Id of the restaurant whose dishes are requested.
        current_user: Authenticated user, used to check restaurant ownership.

    Returns:
        List of dishes for the given restaurant.

    """
    restaurant = (
        db.query(Plat)
        .join(Restaurant)
        .filter(
            Restaurant.auth_id == current_user.id,
            Plat.id_restaurant == id_restaurant,
        )
        .all()
    )
    return restaurant


@router.post("/plat/{id_plat_existant}/ingredient/{new_id_ingredient}")
def add_ingredient_for_plat(
    db: DbSession,
    id_plat_existant: int,
    new_id_ingredient: int,
    current_user: CurrentUser,
):
    """Link an existing ingredient to an existing dish.

    Args:
        db: Database session.
        id_plat_existant: Id of the dish to add the ingredient to.
        new_id_ingredient: Id of the ingredient to link.
        current_user: Authenticated user, used to check dish ownership.

    Returns:
        The created dish/ingredient link.

    Raises:
        HTTPException: If the dish or the ingredient doesn't exist, or if the
            ingredient is already linked to this dish.

    """
    check_plat_exist = (
        db.query(Plat)
        .join(Restaurant)
        .filter(Restaurant.auth_id == current_user.id, Plat.id == id_plat_existant)
        .first()
    )

    if check_plat_exist is None:
        raise HTTPException(status_code=404, detail="Plat inexistant dans la base")

    plat_ingredient_exist = (
        db.query(PlatIngredient)
        .filter(
            PlatIngredient.id_plat == id_plat_existant,
            PlatIngredient.id_ingredient == new_id_ingredient,
        )
        .first()
    )

    if plat_ingredient_exist:
        raise HTTPException(
            status_code=409, detail="Ingredient deja existant pour ce plat"
        )

    ingredient = db.query(Ingredient).filter(Ingredient.id == new_id_ingredient).first()
    if ingredient is None:
        raise HTTPException(
            status_code=404, detail="Ingredient inexistant dans la base"
        )

    new_ingredient_plat = PlatIngredient(
        id_ingredient=new_id_ingredient, id_plat=id_plat_existant
    )
    db.add(new_ingredient_plat)
    db.commit()
    db.refresh(new_ingredient_plat)
    return new_ingredient_plat


@router.delete("/plat/{id_plat}/ingredient/{id_ingredient}")
def delete_ingredient_from_plat(
    db: DbSession, id_plat: int, id_ingredient: int, current_user: CurrentUser
):
    """Remove the link between an ingredient and a dish.

    Args:
        db: Database session.
        id_plat: Id of the dish.
        id_ingredient: Id of the ingredient to unlink.
        current_user: Authenticated user, used to scope the link to their restaurants.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If no matching link exists.

    """
    ingredient_from_plat = (
        db.query(PlatIngredient)
        .join(Plat)
        .join(Restaurant)
        .filter(
            PlatIngredient.id_ingredient == id_ingredient,
            PlatIngredient.id_plat == id_plat,
            Restaurant.auth_id == current_user.id,
        )
        .first()
    )

    if ingredient_from_plat is None:
        raise HTTPException(
            status_code=404, detail="L'ingredient pour ce plat n'existe pas"
        )

    db.delete(ingredient_from_plat)
    db.commit()
    return {"message": "L'ingredient a bien était supprimé"}


@router.get("/plat/{id_plat}/ingredient")
def get_ingredient_for_plat(db: DbSession, id_plat: int, current_user: CurrentUser):
    """Return the ingredients linked to a dish.

    Args:
        db: Database session.
        id_plat: Id of the dish.
        current_user: Authenticated user, used to scope the dish to their restaurants.

    Returns:
        List of ingredient names and ids linked to the dish.

    """
    ingredient_from_plat = (
        db.query(PlatIngredient, Ingredient)
        .join(Plat)
        .join(Restaurant)
        .join(Ingredient, Ingredient.id == PlatIngredient.id_ingredient)
        .filter(
            PlatIngredient.id_plat == id_plat, Restaurant.auth_id == current_user.id
        )
        .all()
    )
    return [
        {"nom": ingredient.nom, "id_ingredient": ingredient.id}
        for plat_ing, ingredient in ingredient_from_plat
    ]
