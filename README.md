# PlaceExplorer

PlaceExplorer to aplikacja do dodawania ciekawych miejsc do odwiedzenia oraz ich oceniania. Umożliwia pełne zarządzanie miejscami w bazie danych (CRUD) oraz dodawanie opinii przez użytkowników.  

Aplikacja w czasie rzeczywistym wyświetla dane o stanie serwera, takie jak:
- status serwera,
- aktualny czas,
- liczba aktywnych połączeń.  


## Technologie
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, WebSockets
- **Frontend:** React, Vite
- **Testy:** Pytest

## Uruchomienie

### Backend
1. Uruchom bazę danych:
```
docker compose up -d
```
2. Utwórz i aktywuj wirtualne środowisko
```
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```
3. Zainstaluj zależności
```
pip install -r requirements.txt
```
4. Uruchom serwer
```
uvicorn app.main:app --reload
```

### Frontend

1. Przejdź do katalogu frontend:
```
cd frontend
```
2. Zainstaluj zależności:
```
npm install
```

3. Uruchom frontend:
```
npm run dev
```

4. Otwórz aplikację w przeglądarce pod adresem http://localhost:5173.

### Testy
Uruchom testy poleceniem:
```
python -m pytest
```
