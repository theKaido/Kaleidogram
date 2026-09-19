from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from app.dependencies.auth import get_current_user
from app.routers.allergene import router as router_allergene
from app.routers.allergene_ingredient import router as router_allergene_ingredient
from app.routers.auth import router as router_auth
from app.routers.ingredient import router as router_ingredient
from app.routers.plat import router as router_plat
from app.routers.plat_ingredient import router as router_plat_ingredient
from app.routers.restaurant import router as router_restaurant

load_dotenv()

app = FastAPI()

app.include_router(
    router_allergene,
    prefix="/allergenes",
    tags=["Allergenes"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    router_ingredient,
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(router_plat, prefix="/plats", tags=["Plats"])
app.include_router(router_restaurant, prefix="/restaurants", tags=["Restaurants"])
app.include_router(router_auth, prefix="/auth", tags=["Authentificiation"])
app.include_router(router_plat_ingredient, prefix="/plat-ingredident", tags=["Plat_Ingredient"])
app.include_router(router_allergene_ingredient, tags=["AllergeneIngredient"])


@app.get("/health")
def health():
    """Return a basic liveness status for the API.

    Returns:
        A status payload confirming the API is running.

    """
    return {"status": "ok"}
