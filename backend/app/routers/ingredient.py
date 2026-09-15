from fastapi import APIRouter, HTTPException

from app.dependencies.database import DbSession
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate

router = APIRouter()


@router.get("/ingredient")
def get_ingredient(db: DbSession):
    """Return all ingredients.

    Args:
        db: Database session.

    Returns:
        List of ingredients.

    """
    return db.query(Ingredient).all()


@router.post("/ingredient")
def ingredient_create(db: DbSession, body: IngredientCreate):
    """Create a new ingredient.

    Args:
        db: Database session.
        body: Ingredient creation payload.

    Returns:
        The created ingredient.

    """
    ingredient = Ingredient(nom=body.nom)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.get("/ingredient/{id_ingredient}")
def get_ingredient_with_id(db: DbSession, id_ingredient: int):
    """Return a single ingredient by id.

    Args:
        db: Database session.
        id_ingredient: Id of the ingredient to fetch.

    Returns:
        The matching ingredient.

    Raises:
        HTTPException: If no ingredient matches the given id.

    """
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient non trouvé")
    return ingredient


@router.put("/ingredient/{id_ingredient}")
def update_ingredient_name(db: DbSession, id_ingredient: int, body: IngredientCreate):
    """Update the name of an existing ingredient.

    Args:
        db: Database session.
        id_ingredient: Id of the ingredient to update.
        body: Payload containing the new name.

    Returns:
        The updated ingredient.

    Raises:
        HTTPException: If no ingredient matches the given id.

    """
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient non trouvé")
    ingredient.nom = body.nom
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.delete("/ingredient/{id_ingredient}")
def delete_ingredient(db: DbSession, id_ingredient: int):
    """Delete an ingredient by id.

    Args:
        db: Database session.
        id_ingredient: Id of the ingredient to delete.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If no ingredient matches the given id.

    """
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient non trouvé")
    db.delete(ingredient)
    db.commit()
    return {"message": "Ingredient supprimé"}
