def test_get_plat(authenticated_test_client):
    """Test that GET /plats/plat returns a list."""
    response = authenticated_test_client.get("/plats/plat")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_plat(authenticated_test_client, create_restaurant):
    """Test POST /plats/plat, success and unknown/unowned restaurant."""
    id_restaurant = create_restaurant.json()["id"]

    response = authenticated_test_client.post(
        "/plats/plat",
        json={"nom": "test", "categorie": "entree", "id_restaurant": id_restaurant},
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "test"

    response = authenticated_test_client.post(
        "/plats/plat",
        json={"nom": "test", "categorie": "entree", "id_restaurant": -100},
    )
    assert response.status_code == 404


def test_get_plat_with_id(authenticated_test_client, create_plat):
    """Test GET /plats/plat/{id}, found and not found."""
    plat_id = create_plat.json()["id"]

    response = authenticated_test_client.get(f"/plats/plat/{plat_id}")
    assert response.status_code == 200
    assert response.json()["id"] == plat_id

    response = authenticated_test_client.get("/plats/plat/-100")
    assert response.status_code == 404


def test_update_plat(authenticated_test_client, create_plat):
    """Test PUT /plats/plat/{id}, found and not found.

    NOTE: update_plat is typed with body: PlatCreate (the same schema as
    creation), which requires id_restaurant even though the route never
    reads it. Sending it here to match the schema's real requirement — a
    dedicated PlatUpdate schema without id_restaurant would be cleaner.
    """
    plat_id = create_plat.json()["id"]
    id_restaurant = create_plat.json()["id_restaurant"]

    response = authenticated_test_client.put(
        f"/plats/plat/{plat_id}",
        json={"nom": "updated_name", "categorie": "dessert", "id_restaurant": id_restaurant},
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "updated_name"
    assert response.json()["categorie"] == "dessert"

    response = authenticated_test_client.put(
        "/plats/plat/-100",
        json={"nom": "updated_name", "categorie": "dessert", "id_restaurant": id_restaurant},
    )
    assert response.status_code == 404


def test_delete_plat(authenticated_test_client, create_plat):
    """Test DELETE /plats/plat/{id}, and confirm the deletion sticks."""
    plat_id = create_plat.json()["id"]

    response = authenticated_test_client.delete(f"/plats/plat/{plat_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Plat supprimé"}

    response = authenticated_test_client.get(f"/plats/plat/{plat_id}")
    assert response.status_code == 404

    response = authenticated_test_client.delete("/plats/plat/-100")
    assert response.status_code == 404


def test_plat_ownership_isolation(
    authenticated_test_client, second_authenticated_test_client, create_plat
):
    """Test that a plat created by user A is invisible to user B.

    Created through user A's own restaurant — same ownership logic as
    restaurants.
    """
    plat_id = create_plat.json()["id"]

    response = second_authenticated_test_client.get(f"/plats/plat/{plat_id}")
    assert response.status_code == 404
