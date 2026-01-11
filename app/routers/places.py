from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..database import get_db
from ..crud.place import create_place, get_places, get_place, delete_place, update_place

router = APIRouter(prefix="/places", tags=["places"])

@router.post("/", response_model=schemas.Place)
def create_place_endpoint(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    """
        Tworzy nowe miejsce w systemie.

        Args:
            place (schemas.PlaceCreate): Dane nowego miejsca.
            db (Session): Sesja bazy danych.

        Returns:
            schemas.Place: Utworzony obiekt miejsca.
        """
    return create_place(db, place)


@router.get("/", response_model=List[schemas.Place])
def read_places_endpoint(db: Session = Depends(get_db)):
    """
        Pobiera listę wszystkich dostępnych miejsc.

        Args:
            db (Session): Sesja bazy danych.

        Returns:
            List[schemas.Place]: Lista obiektów miejsc.
        """
    return get_places(db)


@router.get("/{place_id}", response_model=schemas.Place)
def read_place_endpoint(place_id: int, db: Session = Depends(get_db)):
    """
        Pobiera szczegółowe informacje o konkretnym miejscu na podstawie ID.

        Args:
            place_id (int): ID miejsca.
            db (Session): Sesja bazy danych.

        Raises:
            HTTPException: 404 jeśli miejsce nie istnieje.

        Returns:
            schemas.Place: Obiekt znalezionego miejsca.
        """
    place = get_place(db, place_id)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.put("/{place_id}", response_model=schemas.Place)
def update_place_endpoint(place_id: int, place_update: schemas.PlaceCreate, db: Session = Depends(get_db)):
    """
        Aktualizuje dane istniejącego miejsca.

        Args:
            place_id (int): ID miejsca do aktualizacji.
            place_update (schemas.PlaceCreate): Nowe dane miejsca.
            db (Session): Sesja bazy danych.

        Raises:
            HTTPException: 404 jeśli miejsce nie istnieje.

        Returns:
            schemas.Place: Zaktualizowany obiekt miejsca.
    """
    place = update_place(db, place_id, place_update)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.delete("/{place_id}", status_code=204)
def delete_place_endpoint(place_id: int, db: Session = Depends(get_db)):
    """
    Usuwa miejsce z systemu.

    Args:
        place_id (int): ID miejsca do usunięcia.
        db (Session): Sesja bazy danych.

    Raises:
        HTTPException: 404 jeśli miejsce nie istnieje.
    """
    deleted = delete_place(db, place_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Place not found")