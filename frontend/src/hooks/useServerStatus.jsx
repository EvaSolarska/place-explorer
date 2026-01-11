import { useState, useEffect } from 'react';

export const useServerStatus = () => {
  const [serverStatus, setServerStatus] = useState({
    status: 'connecting...',
    timestamp: '',
    connected_clients: 0,
  });

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/status");

    ws.onopen = () => console.log("WebSocket połączony");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setServerStatus(data);
      } catch (e) {
        console.error("Błąd parsowania:", e);
      }
    };

    ws.onerror = (err) => console.error("Błąd WS:", err);
    ws.onclose = () => console.log("WebSocket zamknięty");

    return () => ws.close();
  }, []);

  return serverStatus;
};
