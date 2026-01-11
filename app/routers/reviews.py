from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..crud.review import create_review as create_review_crud

router = APIRouter(prefix="/places", tags=["reviews"])

@router.post("/{place_id}/reviews", response_model=schemas.Review)
def add_new_review(place_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """
        Tworzy nową recenzję dla określonego miejsca (place_id).

        Args:
            place_id (int): Unikalny identyfikator miejsca.
            review (schemas.ReviewCreate): Dane nowej recenzji .
            db (Session): Sesja bazy danych.

        Raises:
            HTTPException: 404 jeśli miejsce nie zostanie znalezione w bazie danych.

        Returns:
            schemas.Review: Obiekt utworzonej recenzji.
        """
    db_review = create_review_crud(db, place_id, review)

    if db_review is None:
        raise HTTPException(status_code=404, detail="Place not found")

    return db_review