from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):

    """
    Bazowy schemat recenzji zawierający wspólne pola
    wykorzystywane przy tworzeniu i odczycie recenzji.

    Atrybuty:
        title (str):
            Tytuł recenzji.

        content (str):
            Treść recenzji.

        rating (int):
            Ocena miejsca w skali od 1 do 5.
    """

    title: str
    content: str
    rating: int = Field(
        ge=1,
        le=5,
        description="Rating musi być w zakresie 1–5"
    )

class ReviewCreate(ReviewBase):

    """
    Schemat wykorzystywany podczas tworzenia nowej recenzji.

    Dziedziczy wszystkie pola z klasy ReviewBase.
    """

    pass

class Review(ReviewBase):

    """
    Schemat reprezentujący recenzję odczytywaną z bazy danych.

    Atrybuty:
        id (int):
            Unikalny identyfikator recenzji.

        created_at (datetime):
            Data i godzina utworzenia recenzji.

        place_id (int):
            Identyfikator miejsca, którego dotyczy recenzja.

    Konfiguracja:
        model_config (ConfigDict):
            Umożliwia tworzenie modelu z obiektów ORM.
    """

    id: int
    created_at: datetime
    place_id: int

    model_config = ConfigDict(from_attributes=True)

class PlaceBase(BaseModel):
    """
    Bazowy schemat miejsca zawierający podstawowe informacje
    opisujące lokalizację.

    Atrybuty:
        name (str):
            Nazwa miejsca.

        description (str):
            Szczegółowy opis miejsca.

        street_address (Optional[str]):
            Dokładny adres ulicy.

        city (Optional[str]):
            Miasto, w którym znajduje się miejsce.

        country (Optional[str]):
            Kraj, w którym znajduje się miejsce.

        visit_duration (Optional[str]):
            Szacowany czas wizyty (np. „1–2 godziny”).

        is_free (Optional[bool]):
            Informacja, czy wstęp jest bezpłatny.
    """

    name: str
    description: str
    street_address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    visit_duration: Optional[str] = None
    is_free: Optional[bool] = None

class PlaceCreate(PlaceBase):

    """
    Schemat wykorzystywany do tworzenia nowego miejsca.

    Dziedziczy wszystkie pola z klasy PlaceBase.
    """

    pass

class Place(PlaceBase):

    """
     Schemat reprezentujący miejsce odczytywane z bazy danych.

     Atrybuty:
         id (int):
             Unikalny identyfikator miejsca.

         created_at (datetime):
             Data i godzina utworzenia miejsca.

         updated_at (datetime):
             Data i godzina ostatniej aktualizacji miejsca.

         reviews (List[Review]):
             Lista recenzji przypisanych do miejsca.

    Konfiguracja:
        model_config (ConfigDict):
            Umożliwia tworzenie modelu z obiektów ORM.
     """

    id: int
    created_at: datetime
    updated_at: datetime
    reviews: list[Review] = []

    model_config = ConfigDict(from_attributes=True)