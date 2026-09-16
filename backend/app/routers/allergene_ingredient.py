from fastapi import APIRouter, HTTPException

from app.dependencies.auth import CurrentUser
from app.dependencies.database import DbSession
from app.models.allergene import Allergene
from app.models.allergeneingredient import AllergeneIngredient
from app.models.ingredient import Ingredient
from app.models.plat import Plat
from app.models.restaurant import Restaurant
from app.schemas.allergene_ingredient import AllergeneIngredientClass

router = APIRouter()


@router.get("/plat/{id_plat}/ingredient/{id_ingredient}/allergene")
def get_allergene_for_ingredient(
    db: DbSession, id_plat: int, id_ingredient: int, current_user: CurrentUser
):
    """Return the allergenes linked to an ingredient within a dish.

    Args:
        db: Database session.
        id_plat: Id of the dish.
        id_ingredient: Id of the ingredient.
        current_user: Authenticated user, used to scope results to their restaurants.

    Returns:
        List of allergene names with their status for this ingredient/dish pair.

    """
    ingr_allergene = (
        db.query(AllergeneIngredient, Allergene)
        .join(Allergene, Allergene.id == AllergeneIngredient.id_allergene)
        .join(Plat)
        .join(Restaurant)
        .filter(
            AllergeneIngredient.id_ingredient == id_ingredient,
            AllergeneIngredient.id_plat == id_plat,
            Restaurant.auth_id == current_user.id,
        )
        .all()
    )

    return [
        {"nom_allergene": allergene.nom, "status": all_ing.status}
        for all_ing, allergene in ingr_allergene
    ]


@router.post(
    "/plat/{new_id_plat}/ingredient/{new_id_ingredient}/allergenes/{new_id_allergene}"
)
def add_new_allergene_for_ingredient(
    db: DbSession,
    new_id_plat: int,
    new_id_ingredient: int,
    new_id_allergene: int,
    current_user: CurrentUser,
    body: AllergeneIngredientClass,
):
    """Link an allergene to an ingredient within a dish.

    Args:
        db: Database session.
        new_id_plat: Id of the dish.
        new_id_ingredient: Id of the ingredient.
        new_id_allergene: Id of the allergene to link.
        current_user: Authenticated user, used to check dish ownership.
        body: Payload containing the allergene status.

    Returns:
        The created allergene/ingredient link.

    Raises:
        HTTPException: If the dish doesn't exist or isn't owned by the user, or if
            the link already exists.

    """
    check_plat = (
        db.query(Plat)
        .join(Restaurant)
        .filter(Plat.id == new_id_plat, Restaurant.auth_id == current_user.id)
        .first()
    )

    if check_plat is None:
        raise HTTPException(status_code=404, detail="Plat inexistant")

    check_ingredient = (
        db.query(Ingredient).filter(Ingredient.id == new_id_ingredient).first()
    )
    if check_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient inexistant")

    check_allergene = (
        db.query(Allergene).filter(Allergene.id == new_id_allergene).first()
    )
    if check_allergene is None:
        raise HTTPException(status_code=404, detail="Allergene inexistant")

    all_ingr = (
        db.query(AllergeneIngredient)
        .filter(
            AllergeneIngredient.id_allergene == new_id_allergene,
            AllergeneIngredient.id_ingredient == new_id_ingredient,
            AllergeneIngredient.id_plat == new_id_plat,
        )
        .first()
    )

    if all_ingr:
        raise HTTPException(
            status_code=409, detail="L'allergene pour cette ingredient est deja présent"
        )

    new_all_ingr = AllergeneIngredient(
        id_plat=new_id_plat,
        id_ingredient=new_id_ingredient,
        id_allergene=new_id_allergene,
        status=body.status,
    )

    db.add(new_all_ingr)
    db.commit()
    db.refresh(new_all_ingr)

    return new_all_ingr


@router.put("/plat/{id_plat}/ingredient/{id_ingredient}/allergene/{id_allergene}")
def update_status_ingredient_allergene(
    db: DbSession,
    id_plat: int,
    id_ingredient: int,
    id_allergene: int,
    current_user: CurrentUser,
    body: AllergeneIngredientClass,
):
    """Update the status of an allergene/ingredient link within a dish.

    Args:
        db: Database session.
        id_plat: Id of the dish.
        id_ingredient: Id of the ingredient.
        id_allergene: Id of the allergene.
        current_user: Authenticated user, used to scope the link to their restaurants.
        body: Payload containing the new status.

    Returns:
        The updated allergene/ingredient link.

    Raises:
        HTTPException: If no matching link exists.

    """
    all_ingr = (
        db.query(AllergeneIngredient)
        .join(Plat)
        .join(Restaurant)
        .filter(
            AllergeneIngredient.id_allergene == id_allergene,
            AllergeneIngredient.id_ingredient == id_ingredient,
            AllergeneIngredient.id_plat == id_plat,
            Restaurant.auth_id == current_user.id,
        )
        .first()
    )

    if all_ingr is None:
        raise HTTPException(
            status_code=404, detail="L'allergene pour cette ingredient n'existe pas"
        )

    all_ingr.status = body.status

    db.commit()
    db.refresh(all_ingr)

    return all_ingr


@router.delete("/plat/{id_plat}/ingredient/{id_ingredient}/allergene/{id_allergene}")
def delete_ingredient_allergene(
    db: DbSession,
    id_plat: int,
    id_ingredient: int,
    id_allergene: int,
    current_user: CurrentUser,
):
    """Remove the link between an allergene and an ingredient within a dish.

    Args:
        db: Database session.
        id_plat: Id of the dish.
        id_ingredient: Id of the ingredient.
        id_allergene: Id of the allergene.
        current_user: Authenticated user, used to scope the link to their restaurants.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If no matching link exists.

    """
    all_ing = (
        db.query(AllergeneIngredient)
        .join(Plat)
        .join(Restaurant)
        .filter(
            AllergeneIngredient.id_allergene == id_allergene,
            AllergeneIngredient.id_ingredient == id_ingredient,
            AllergeneIngredient.id_plat == id_plat,
            Restaurant.auth_id == current_user.id,
        )
        .first()
    )

    if all_ing is None:
        raise HTTPException(
            status_code=404, detail="L'allergène pour cet ingrédient n'existe pas"
        )

    db.delete(all_ing)
    db.commit()

    return {"message": "L'allergene lié a cette ingredient a bien été supprimé"}
