def test_create_review_for_place(client):
    """
    Test tworzenia recenzji dla istniejącego miejsca.
    """

    place_response = client.post(
        "/places/",
        json={
            "name": "Place with reviews",
            "description": "Test place"
        }
    )
    place_id = place_response.json()["id"]

    review_payload = {
        "title": "Great place",
        "content": "Really enjoyed visiting this place",
        "rating": 5
    }

    response = client.post(
        f"/places/{place_id}/reviews",
        json=review_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == review_payload["title"]
    assert data["content"] == review_payload["content"]
    assert data["rating"] == review_payload["rating"]
    assert data["place_id"] == place_id

    # Sprawdzam pola generowane automatycznie
    assert "id" in data
    assert "created_at" in data


def test_create_review_rating_too_high(client):
    """
    Test walidacji pola rating, gdy wartość jest większa niż 5.
    """

    place_response = client.post(
        "/places/",
        json={
            "name": "Rating too high",
            "description": "Test place"
        }
    )
    place_id = place_response.json()["id"]

    payload = {
        "title": "Invalid rating",
        "content": "Rating is too high",
        "rating": 7
    }

    response = client.post(
        f"/places/{place_id}/reviews",
        json=payload
    )

    assert response.status_code == 422

    data = response.json()

    # Sprawdzam, czy błąd dotyczy pola 'rating'
    assert data["detail"][0]["loc"][-1] == "rating"
