from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Place(Base):
    """
    Klasa reprezentująca miejsce, które może zostać odwiedzone przez użytkownika (np. atrakcja turystyczna, muzeum).

    Atrybuty:
        id (int):
            Unikalny identyfikator miejsca.

        name (str):
            Nazwa miejsca.

        description (Optional[str]):
            Szczegółowy opis miejsca.

        street_address (Optional[str]):
            Adres miejsca.

        city (Optional[str]):
            Miasto, w którym znajduje się miejsce.

        country (Optional[str]):
            Kraj, w którym znajduje się miejsce.

        visit_duration (Optional[str]):
            Szacowany czas zwiedzania (np. "30 minut", "1-2 godziny").

        is_free (Optional[bool]):
            Informacja, czy wstęp do miejsca jest bezpłatny.

        created_at (datetime):
            Data i godzina utworzenia rekordu w bazie danych.

        updated_at (datetime):
            Data i godzina ostatniej aktualizacji rekordu.

        reviews (List[Review]):
            Lista recenzji powiązanych z danym miejscem.
            Relacja jeden-do-wielu z klasą Review.
    """

    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    description = Column(Text)

    street_address = Column(String(300), nullable=True)
    city = Column(String(100), nullable=True, index=True)
    country = Column(String(100), nullable=True, index=True)

    visit_duration = Column(String(100), nullable=True)
    is_free = Column(Boolean, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")



class Review(Base):
    """
     Klasa reprezentująca recenzję wystawioną przez użytkownika dla konkretnego miejsca.

     Atrybuty:
         id (int):
             Unikalny identyfikator recenzji.

         title (str):
             Tytuł recenzji podsumowujący opinię użytkownika.

         content (str):
             Treść recenzji.

         rating (int):
             Ocena miejsca w skali od 1 do 5.

         created_at (datetime):
             Data i godzina dodania recenzji.

         place_id (int):
             Identyfikator miejsca, którego dotyczy recenzja
             (klucz obcy do tabeli places).

         place (Place):
             Obiekt miejsca, do którego przypisana jest recenzja.
     """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    rating = Column(Integer)  # 1-5

    created_at = Column(DateTime, server_default=func.now())

    place_id = Column(Integer, ForeignKey("places.id"))
    place = relationship("Place", back_populates="reviews")