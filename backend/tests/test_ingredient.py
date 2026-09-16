import pytest


@pytest.fixture
def create_ingredient(authenticated_test_client):
    """Create a new ingredient via the API and return the response."""
    return authenticated_test_client.post(
        "/ingredients/ingredient", json={"nom": "test"}
    )


def test_get_ingredient(authenticated_test_client):
    """Test that GET /ingredients/ingredient returns a list."""
    response = authenticated_test_client.get("/ingredients/ingredient")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_ingredient(authenticated_test_client):
    """Test that POST /ingredients/ingredient creates an ingredient."""
    response = authenticated_test_client.post(
        "/ingredients/ingredient", json={"nom": "test"}
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "test"


def test_get_ingredient_with_id(authenticated_test_client, create_ingredient):
    """Test GET /ingredients/ingredient/{id}, found and not found."""
    ingredient_id = create_ingredient.json()["id"]

    response = authenticated_test_client.get(f"/ingredients/ingredient/{ingredient_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ingredient_id

    response = authenticated_test_client.get("/ingredients/ingredient/-100")
    assert response.status_code == 404


def test_update_ingredient_name(authenticated_test_client, create_ingredient):
    """Test PUT /ingredients/ingredient/{id}, found and not found."""
    ingredient_id = create_ingredient.json()["id"]

    response = authenticated_test_client.put(
        f"/ingredients/ingredient/{ingredient_id}", json={"nom": "test_updated_name"}
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "test_updated_name"

    response = authenticated_test_client.put(
        "/ingredients/ingredient/-100", json={"nom": "test_updated_name"}
    )
    assert response.status_code == 404


def test_delete_ingredient(authenticated_test_client, create_ingredient):
    """Test DELETE /ingredients/ingredient/{id}, and confirm the deletion sticks."""
    ingredient_id = create_ingredient.json()["id"]

    response = authenticated_test_client.delete(
        f"/ingredients/ingredient/{ingredient_id}"
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Ingredient supprimé"}

    response = authenticated_test_client.get(f"/ingredients/ingredient/{ingredient_id}")
    assert response.status_code == 404

    response = authenticated_test_client.delete("/ingredients/ingredient/-100")
    assert response.status_code == 404
