// frontend/src/components/StatusMonitor.tsx
import React, { useEffect, useState } from 'react';

const StatusMonitor: React.FC = () => {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://localhost:8000/api/status')
        .then(res => res.json())
        .then(data => setStatus(data))
        .catch(err => console.error('Failed to fetch status:', err));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 bg-gray-800 text-white rounded">
      <h3 className="text-xl font-bold mb-4">System Status</h3>
      {status && (
        <div>
          <p>Venue: {status.venue}</p>
          <p>Connected: {status.connected ? '✓' : '✗'}</p>
          <p>Symbols: {status.symbols.join(', ')}</p>
          <p>Uptime: {status.uptime}</p>
        </div>
      )}
    </div>
  );
};

export default StatusMonitor;