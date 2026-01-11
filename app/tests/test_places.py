def test_create_place_all_fields(client):
    """
    Test tworzenia nowego miejsca z wszystkimi polami (wymaganymi i opcjonalnymi).
    """
    payload = {
        "name": "Test Place Full",
        "description": "A place with all optional fields",
        "street_address": "123 Main St",
        "city": "Test City",
        "country": "Testland",
        "visit_duration": "2 hours",
        "is_free": True
    }

    response = client.post("/places/", json=payload)

    assert response.status_code == 200

    data = response.json()

    # Sprawdzam wymagane pola
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

    # Sprawdzam pola opcjonalne
    assert data["street_address"] == payload["street_address"]
    assert data["city"] == payload["city"]
    assert data["country"] == payload["country"]
    assert data["visit_duration"] == payload["visit_duration"]
    assert data["is_free"] == payload["is_free"]

    # Sprawdzam, czy miejsce otrzymało unikalny identyfikator
    assert "id" in data
    assert isinstance(data["id"], int)

    # Sprawdzam, czy lista recenzji istnieje i jest pusta na start
    assert "reviews" in data
    assert data["reviews"] == []

def test_create_place_required_fields_only(client):
    """
    Test tworzenia nowego miejsca z minimalnym zestawem wymaganych pól.
    """
    payload = {
        "name": "Minimal Place",
        "description": "Only required fields"
    }

    response = client.post("/places/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

    assert data["street_address"] is None
    assert data["city"] is None
    assert data["country"] is None
    assert data["visit_duration"] is None
    assert data["is_free"] is None
    assert data["reviews"] == []

    assert "id" in data
    assert isinstance(data["id"], int)


def test_create_place_missing_name(client):
    """
    Test tworzenia miejsca bez wymaganego pola 'name'.
    """

    payload = {"description": "No name"}

    response = client.post("/places/", json=payload)

    assert response.status_code == 422

    # Sprawdzam treść odpowiedzi
    data = response.json()
    assert data["detail"][0]["loc"][-1] == "name"
    assert "Field required" in data["detail"][0]["msg"]


def test_read_places(client):
    """
    Test odczytu wszystkich miejsc.
    """

    client.post("/places/", json={"name": "Place 1", "description": "Desc 1"})
    client.post("/places/", json={"name": "Place 2", "description": "Desc 2"})

    response = client.get("/places/")

    assert response.status_code == 200

    data = response.json()

    # Sprawdzam, czy w odpowiedzi są dokładnie 2 miejsca
    assert len(data) == 2

    names = [p["name"] for p in data]

    # Sprawdzam, czy nazwy utworzonych miejsc są obecne w odpowiedzi
    assert "Place 1" in names
    assert "Place 2" in names


def test_read_place_success(client):
    """
    Test odczytu pojedynczego miejsca po jego utworzeniu.
    """

    r = client.post("/places/", json={"name": "Single Place", "description": "Desc"})

    # Pobieram id utworzonego miejsca z odpowiedzi
    place_id = r.json()["id"]

    response = client.get(f"/places/{place_id}")

    assert response.status_code == 200

    data = response.json()

    # Sprawdzam, czy id w odpowiedzi zgadza się z utworzonym miejscem
    assert data["id"] == place_id

    # Sprawdzam, czy nazwa miejsca w odpowiedzi jest zgodna z wysłaną
    assert data["name"] == "Single Place"


def test_read_place_not_found(client):
    """
    Test odczytu miejsca, które nie istnieje.
    """

    response = client.get("/places/99999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Place not found"


def test_update_place_success(client):
    """
    Test aktualizacji istniejącego miejsca.
    """

    r = client.post("/places/", json={"name": "Old Name", "description": "Old Desc"})

    place_id = r.json()["id"]

    response = client.put(
        f"/places/{place_id}",
        json={"name": "New Name", "description": "New Desc"}
    )

    assert response.status_code == 200

    data = response.json()

    # Sprawdzam, czy dane w odpowiedzi zostały zaktualizowane poprawnie
    assert data["name"] == "New Name"
    assert data["description"] == "New Desc"


def test_update_place_not_found(client):
    """
    Test aktualizacji miejsca, które nie istnieje.
    """

    response = client.put(
        "/places/99999",
        json={"name": "No Place", "description": "Does not exist"}
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Place not found"


def test_delete_place_success(client):
    """
    Test usunięcia istniejącego miejsca.
    """

    r = client.post("/places/", json={"name": "To Delete", "description": "Temp"})
    place_id = r.json()["id"]

    response = client.delete(f"/places/{place_id}")

    assert response.status_code == 204

    # Sprawdzam, czy miejsce faktycznie zostało usunięte
    response = client.get(f"/places/{place_id}")
    assert response.status_code == 404

def test_delete_place_not_found(client):
    """
    Test usunięcia miejsca, które nie istnieje.
    """

    response = client.delete("/places/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Place not found"

def test_place_contains_reviews(client):
    """
    Test sprawdzający, czy miejsce zwraca przypisane do niego recenzje.
    """

    place_response = client.post(
        "/places/",
        json={
            "name": "Place with reviews",
            "description": "Test place"
        }
    )
    assert place_response.status_code == 200
    place_id = place_response.json()["id"]

    review_response = client.post(
        f"/places/{place_id}/reviews",
        json={
            "title": "Great place",
            "content": "Really enjoyed it",
            "rating": 5
        }
    )
    assert review_response.status_code == 200

    response = client.get(f"/places/{place_id}")
    assert response.status_code == 200
    place = response.json()

    assert "reviews" in place
    assert len(place["reviews"]) == 1
    assert place["reviews"][0]["rating"] == 5
