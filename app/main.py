from fastapi import FastAPI
from app.routers import places, reviews
from app.models import Base
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import websocket as ws_router

# Inicjalizacja aplikacji
app = FastAPI(
    title="PlaceExplorer",
    description="Aplikacja do odkrywania i oceniania ciekawych miejsc",
    version="1.0.0",
)

# Konfiguracja CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicjalizacja bazy danych
Base.metadata.create_all(bind=engine)

# Rejestracja routerów
app.include_router(places.router)
app.include_router(reviews.router)
app.include_router(ws_router.router)
