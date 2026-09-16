# NOTE: app/routers/allergene_ingredient.py is mounted with NO prefix in
# app/main.py (app.include_router(router_allergene_ingredient, tags=[...])),
# so its paths start directly at "/plat/...". Also note the inconsistency
# already in the router: the POST route uses the plural "allergenes" in its
# path, while GET/PUT/DELETE use the singular "allergene" — not a test bug,
# that's really how the routes are declared.


def test_add_new_allergene_for_ingredient(
    authenticated_test_client, create_plat, create_ingredient, create_allergene
):
    """Test POST /plat/{id_plat}/ingredient/{id_ingredient}/allergenes/{id_allergene}."""
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]
    allergene_id = create_allergene.json()["id"]

    response = authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergenes/{allergene_id}",
        json={"status": "present"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "present"

    response = authenticated_test_client.post(
        f"/plat/-100/ingredient/{ingredient_id}/allergenes/{allergene_id}",
        json={"status": "present"},
    )
    assert response.status_code == 404

    response = authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergenes/{allergene_id}",
        json={"status": "present"},
    )
    assert response.status_code == 409

    # Regression check: an unknown ingredient/allergene id used to crash with
    # an unhandled ForeignKeyViolation (500) instead of a clean 404.
    response = authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/-100/allergenes/{allergene_id}",
        json={"status": "present"},
    )
    assert response.status_code == 404

    response = authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergenes/-100",
        json={"status": "present"},
    )
    assert response.status_code == 404


def test_get_allergene_for_ingredient(
    authenticated_test_client, create_plat, create_ingredient, create_allergene
):
    """Test GET /plat/{id_plat}/ingredient/{id_ingredient}/allergene."""
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]
    allergene_id = create_allergene.json()["id"]

    authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergenes/{allergene_id}",
        json={"status": "present"},
    )

    response = authenticated_test_client.get(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergene"
    )
    assert response.status_code == 200
    assert {"nom_allergene": "test_allergene", "status": "present"} in response.json()


def test_update_status_ingredient_allergene(
    authenticated_test_client, create_plat, create_ingredient, create_allergene
):
    """Test PUT /plat/{id_plat}/ingredient/{id_ingredient}/allergene/{id_allergene}."""
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]
    allergene_id = create_allergene.json()["id"]

    authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergenes/{allergene_id}",
        json={"status": "present"},
    )

    response = authenticated_test_client.put(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergene/{allergene_id}",
        json={"status": "trace"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "trace"

    response = authenticated_test_client.put(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergene/-100",
        json={"status": "trace"},
    )
    assert response.status_code == 404


def test_delete_ingredient_allergene(
    authenticated_test_client, create_plat, create_ingredient, create_allergene
):
    """Test DELETE /plat/{id_plat}/ingredient/{id_ingredient}/allergene/{id_allergene}."""
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]
    allergene_id = create_allergene.json()["id"]

    authenticated_test_client.post(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergenes/{allergene_id}",
        json={"status": "present"},
    )

    response = authenticated_test_client.delete(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergene/{allergene_id}"
    )
    assert response.status_code == 200

    response = authenticated_test_client.get(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergene"
    )
    assert response.json() == []

    response = authenticated_test_client.delete(
        f"/plat/{plat_id}/ingredient/{ingredient_id}/allergene/{allergene_id}"
    )
    assert response.status_code == 404
