from sqlalchemy.orm import Session
from .. import models, schemas


def create_review(db: Session, place_id: int, review: schemas.ReviewCreate) -> models.Review | None:
    """
    Tworzy nową recenzję dla określonego miejsca.
    Args:
        db (Session): Instancja sesji bazy danych.
        place_id (int): Unikalny identyfikator miejsca, do którego przypisana jest recenzja.
        review (schemas.ReviewCreate): Obiekt zawierający dane recenzji.

    Returns:
        models.Review | None: Obiekt utworzonej recenzji lub None, jeśli miejsce nie istnieje.
    """

    place_exists = db.query(models.Place.id).filter(models.Place.id == place_id).first()

    if not place_exists:
        return None

    db_review = models.Review(
        **review.model_dump(),
        place_id=place_id,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
