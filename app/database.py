from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Wczytuje zmienne środowiskowe z pliku .env
load_dotenv()

# Odczyt URL do bazy danych ze zmiennej środowiskowej
DATABASE_URL = os.getenv("DATABASE_URL")

# Sprawdzenie, czy URL do bazy został poprawnie ustawiony
if DATABASE_URL is None:
    raise ValueError("Brak zmiennej DATABASE_URL w środowisku")

# Tworzy silnik SQLAlchemy, który zarządza połączeniem z bazą danych
engine = create_engine(DATABASE_URL)

# Fabryka sesji do pracy z bazą danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():

    """
    Generator zwracający sesję SQLAlchemy i zamykający ją po użyciu.

    Yields:
        Session: instancja sesji do pracy z bazą danych.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()