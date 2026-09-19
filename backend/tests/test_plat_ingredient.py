def test_get_all_plat_from_restaurant(
    authenticated_test_client, create_plat, create_restaurant
):
    """Test GET /plat-ingredident/restaurant/plat/{id_restaurant}."""
    id_restaurant = create_restaurant.json()["id"]
    plat_id = create_plat.json()["id"]

    response = authenticated_test_client.get(
        f"/plat-ingredident/restaurant/plat/{id_restaurant}"
    )
    assert response.status_code == 200
    assert plat_id in [p["id"] for p in response.json()]


def test_add_ingredient_for_plat(
    authenticated_test_client, create_plat, create_ingredient
):
    """Test POST /plat-ingredident/plat/{id_plat}/ingredient/{id_ingredient}.

    Covers: success, unknown/unowned plat, unknown ingredient, and duplicate
    link (the route itself doesn't check the ingredient exists before
    checking for a duplicate link, so order of these checks matters — see
    add_ingredient_for_plat in app/routers/plat_ingredient.py).
    """
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]

    response = authenticated_test_client.post(
        f"/plat-ingredident/plat/{plat_id}/ingredient/{ingredient_id}"
    )
    assert response.status_code == 200

    response = authenticated_test_client.post(
        f"/plat-ingredident/plat/-100/ingredient/{ingredient_id}"
    )
    assert response.status_code == 404

    response = authenticated_test_client.post(
        f"/plat-ingredident/plat/{plat_id}/ingredient/-100"
    )
    assert response.status_code == 404

    response = authenticated_test_client.post(
        f"/plat-ingredident/plat/{plat_id}/ingredient/{ingredient_id}"
    )
    assert response.status_code == 409


def test_get_ingredient_for_plat(
    authenticated_test_client, create_plat, create_ingredient
):
    """Test GET /plat-ingredident/plat/{id_plat}/ingredient."""
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]

    authenticated_test_client.post(
        f"/plat-ingredident/plat/{plat_id}/ingredient/{ingredient_id}"
    )

    response = authenticated_test_client.get(f"/plat-ingredident/plat/{plat_id}/ingredient")
    assert response.status_code == 200
    assert ingredient_id in [i["id_ingredient"] for i in response.json()]


def test_delete_ingredient_from_plat(
    authenticated_test_client, create_plat, create_ingredient
):
    """Test DELETE /plat-ingredident/plat/{id_plat}/ingredient/{id_ingredient}, and confirm it sticks."""
    plat_id = create_plat.json()["id"]
    ingredient_id = create_ingredient.json()["id"]

    authenticated_test_client.post(
        f"/plat-ingredident/plat/{plat_id}/ingredient/{ingredient_id}"
    )

    response = authenticated_test_client.delete(
        f"/plat-ingredident/plat/{plat_id}/ingredient/{ingredient_id}"
    )
    assert response.status_code == 200

    response = authenticated_test_client.get(f"/plat-ingredident/plat/{plat_id}/ingredient")
    assert ingredient_id not in [i["id_ingredient"] for i in response.json()]

    response = authenticated_test_client.delete(
        f"/plat-ingredident/plat/{plat_id}/ingredient/{ingredient_id}"
    )
    assert response.status_code == 404
