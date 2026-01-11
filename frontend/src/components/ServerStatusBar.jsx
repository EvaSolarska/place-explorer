export default function ServerStatusBar({ status }) {
  const formattedTime = status.timestamp
    ? new Date(status.timestamp).toLocaleTimeString('pl-PL', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    : '—';

  return (
    <div className="bg-slate-800 text-white text-sm px-6 py-2.5 flex justify-between items-center shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
        <span>
          Status serwera: <span className="font-bold text-emerald-400">{status.status}</span>
        </span>
      </div>

      <div className="flex items-center gap-6 text-slate-300">
        <span>Czas: <span className="text-white font-medium">{formattedTime}</span></span>
        <span>Użytkownicy: <span className="text-white font-medium">{status.connected_clients}</span></span>
      </div>
    </div>
  );
}