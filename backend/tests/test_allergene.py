import pytest


@pytest.fixture
def create_allergene(authenticated_test_client):
    """Create a new allergene via the API and return the response."""
    return authenticated_test_client.post("/allergenes/allergene", json={"nom": "test"})


def test_get_allergene(authenticated_test_client):
    """Test that GET /allergenes/allergene returns a list."""
    response = authenticated_test_client.get("/allergenes/allergene")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_allergene(authenticated_test_client):
    """Test that POST /allergenes/allergene creates an allergene."""
    response = authenticated_test_client.post(
        "/allergenes/allergene", json={"nom": "test"}
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "test"


def test_get_allergene_with_id(authenticated_test_client, create_allergene):
    """Test GET /allergenes/allergene/{id}, found and not found."""
    allergene_id = create_allergene.json()["id"]

    response = authenticated_test_client.get(f"/allergenes/allergene/{allergene_id}")
    assert response.status_code == 200
    assert response.json()["id"] == allergene_id
    assert response.json()["nom"] == "test"

    response = authenticated_test_client.get("/allergenes/allergene/-100")
    assert response.status_code == 404


def test_update_allergene_name(authenticated_test_client, create_allergene):
    """Test PUT /allergenes/allergene/{id}, found and not found."""
    allergene_id = create_allergene.json()["id"]

    response = authenticated_test_client.put(
        f"/allergenes/allergene/{allergene_id}", json={"nom": "test_updated_name"}
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "test_updated_name"

    response = authenticated_test_client.put(
        "/allergenes/allergene/-100", json={"nom": "test_updated_name"}
    )
    assert response.status_code == 404


def test_delete_allergene(authenticated_test_client, create_allergene):
    """Test DELETE /allergenes/allergene/{id}, and confirm the deletion sticks."""
    allergene_id = create_allergene.json()["id"]

    response = authenticated_test_client.delete(f"/allergenes/allergene/{allergene_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Allergène supprimé"}

    # Proves the deletion actually happened, rather than just checking the
    # return shape of remove_allergene (which is fixed regardless).
    response = authenticated_test_client.get(f"/allergenes/allergene/{allergene_id}")
    assert response.status_code == 404

    response = authenticated_test_client.delete("/allergenes/allergene/-100")
    assert response.status_code == 404
