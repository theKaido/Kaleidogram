def test_get_restaurant(authenticated_test_client):
    """Test that GET /restaurants/restaurant returns a list."""
    response = authenticated_test_client.get("/restaurants/restaurant")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_restaurant(authenticated_test_client):
    """Test that POST /restaurants/restaurant creates a restaurant."""
    response = authenticated_test_client.post(
        "/restaurants/restaurant", json={"nom": "test", "categorie": "test_categorie"}
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "test"


def test_get_restaurant_with_id(authenticated_test_client, create_restaurant):
    """Test GET /restaurants/restaurant/{id}, found and not found."""
    restaurant_id = create_restaurant.json()["id"]

    response = authenticated_test_client.get(f"/restaurants/restaurant/{restaurant_id}")
    assert response.status_code == 200
    assert response.json()["id"] == restaurant_id

    response = authenticated_test_client.get("/restaurants/restaurant/-100")
    assert response.status_code == 404


def test_update_restaurant(authenticated_test_client, create_restaurant):
    """Test PUT /restaurants/restaurant/{id}, found and not found."""
    restaurant_id = create_restaurant.json()["id"]

    response = authenticated_test_client.put(
        f"/restaurants/restaurant/{restaurant_id}",
        json={"nom": "updated_name", "categorie": "test_categorie"},
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "updated_name"

    response = authenticated_test_client.put(
        "/restaurants/restaurant/-100",
        json={"nom": "updated_name", "categorie": "test_categorie"},
    )
    assert response.status_code == 404


def test_delete_restaurant(authenticated_test_client, create_restaurant):
    """Test DELETE /restaurants/restaurant/{id}, and confirm the deletion sticks."""
    restaurant_id = create_restaurant.json()["id"]

    response = authenticated_test_client.delete(f"/restaurants/restaurant/{restaurant_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Restaurant supprimé"}

    response = authenticated_test_client.get(f"/restaurants/restaurant/{restaurant_id}")
    assert response.status_code == 404

    response = authenticated_test_client.delete("/restaurants/restaurant/-100")
    assert response.status_code == 404


def test_restaurant_ownership_isolation(
    authenticated_test_client, second_authenticated_test_client, create_restaurant
):
    """A restaurant created by user A must be invisible/untouchable by user B.

    This is real business logic (Restaurant.auth_id == current_user.id), not
    boilerplate — worth keeping even though it's the only ownership test
    written so far. The same pattern applies to plat.py and, transitively,
    plat_ingredient.py / allergene_ingredient.py.
    """
    restaurant_id = create_restaurant.json()["id"]

    response = second_authenticated_test_client.get(f"/restaurants/restaurant/{restaurant_id}")
    assert response.status_code == 404

    response = second_authenticated_test_client.get("/restaurants/restaurant")
    assert restaurant_id not in [r["id"] for r in response.json()]

    response = second_authenticated_test_client.delete(f"/restaurants/restaurant/{restaurant_id}")
    assert response.status_code == 404
