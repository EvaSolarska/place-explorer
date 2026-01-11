from app.schemas import PlaceCreate
from sqlalchemy.orm import Session
from app.models import Place


def create_place(db: Session, place: PlaceCreate) -> Place:
    """
    Tworzy nowe miejsce w bazie.

        Args:
            db (Session): Instancja sesji bazy danych.
            place (PlaceCreate): Dane nowego miejsca przesyłane przez klienta.

        Returns:
            Place: Obiekt reprezentujący utworzone miejsce.
     """
    db_place = Place(**place.model_dump())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place

def get_place(db: Session, place_id: int) -> Place | None:
    """
        Pobiera pojedyncze miejsce na podstawie jego identyfikatora ID.

        Args:
            db (Session): Instancja sesji bazy danych.
            place_id (int): Unikalny identyfikator miejsca.

        Returns:
            Place | None: Znaleziony obiekt Place lub None, jeśli nie istnieje.
    """
    return db.get(Place, place_id)

def get_places(db: Session) -> list[Place]:
    """
        Pobiera listę miejsc z bazy.

        Args:
            db (Session): Instancja sesji bazy danych.

        Returns:
            list[Place]: Lista obiektów Place.
    """
    return db.query(Place).all()

def update_place(db: Session, place_id: int, place_update: PlaceCreate) -> Place | None:
    """
        Aktualizuje dane istniejącego miejsca.

        Args:
            db (Session): Instancja sesji bazy danych.
            place_id (int): ID miejsca do aktualizacji.
            place_update (PlaceCreate): Nowe dane dla miejsca.

        Returns:
            Place | None: Zaktualizowany obiekt Place lub None, jeśli miejsce nie zostało znalezione.
    """
    place = get_place(db, place_id)
    if not place:
        return None
    for key, value in place_update.model_dump().items():
        setattr(place, key, value)
    db.commit()
    db.refresh(place)
    return place

def delete_place(db: Session, place_id: int) -> bool:
    """
    Usuwa miejsce z bazy danych na podstawie jego identyfikatora.

    Args:
        db (Session): Instancja sesji bazy danych.
        place_id (int): Unikalny identyfikator miejsca do usunięcia.

    Returns:
        bool:
            - True – jeśli miejsce zostało pomyślnie usunięte
            - False – jeśli miejsce o podanym ID nie istnieje
    """
    place = get_place(db, place_id)
    if not place:
        return False

    db.delete(place)
    db.commit()
    return True
