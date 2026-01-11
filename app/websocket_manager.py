from fastapi import WebSocket
from typing import Set
from datetime import datetime
import asyncio


class ConnectionManager:
    """
    Zarządza połączeniami WebSocket oraz obsługuje rozsyłanie wiadomości do podłączonych klientów.

    Attributes:
        active_connections: Zbiór aktualnie aktywnych połączeń WebSocket.
        broadcast_task: Zadanie w tle odpowiedzialne za cykliczne wysyłanie statusu.
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.broadcast_task: asyncio.Task | None = None

    async def connect(self, websocket: WebSocket):
        """
        Akceptuje nowe połączenie WebSocket i dodaje je do listy aktywnych.

        Jeśli jest to pierwsze aktywne połączenie, uruchamia zadanie w tle (_broadcast_status).

            Args:
                websocket (WebSocket): Instancja połączenia WebSocket.
        """
        await websocket.accept()
        self.active_connections.add(websocket)

        # Uruchom zadanie w tle tylko wtedy, gdy pojawił się pierwszy użytkownik
        if len(self.active_connections) == 1:
            if self.broadcast_task is None or self.broadcast_task.done():
                self.broadcast_task = asyncio.create_task(self._broadcast_status())

    def disconnect(self, websocket: WebSocket):
        """
        Usuwa połączenie WebSocket z listy aktywnych.

        Jeśli po rozłączeniu lista klientów jest pusta, zadanie w tle jest anulowane.

        Args:
            websocket (WebSocket): Połączenie WebSocket do usunięcia.
        """
        self.active_connections.discard(websocket)

        # Zatrzymaj zadanie w tle, jeśli nie ma już nikogo nasłuchującego
        if not self.active_connections and self.broadcast_task:
            self.broadcast_task.cancel()
            self.broadcast_task = None

    async def broadcast(self, message: dict):
        """
        Wysyła wiadomość JSON do wszystkich aktualnie podłączonych klientów.

        Args:
            message (dict): Słownik z danymi do wysłania w formacie JSON.
        """
        if not self.active_connections:
            return

        disconnected = []

        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending message, disconnecting client: {e}")
                disconnected.append(connection)

        for conn in disconnected:
            self.active_connections.discard(conn)

    async def _broadcast_status(self):
        """
        Zadanie w tle, które co sekundę rozsyła status serwera.

        Wysyła słownik z kluczami:
            - status: aktualny status serwera
            - timestamp: bieżący czas
            - connected_clients: liczba podłączonych klientów
        """
        try:
            while True:
                data = {
                    "status": "running",
                    "timestamp": datetime.now().isoformat(),
                    "connected_clients": len(self.active_connections)
                }
                await self.broadcast(data)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Unexpected error in broadcast task: {e}")


manager = ConnectionManager()