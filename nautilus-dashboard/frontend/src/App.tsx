import React from 'react';
import './App.css';
import KlineChart from './components/KlineChart';
import StatusMonitor from './components/StatusMonitor';

function App() {
  return (
    <div className="App" style={{ padding: 20, fontFamily: 'Arial, Helvetica, sans-serif' }}>
      <h1 style={{ marginBottom: 12 }}>Nautilus Trader — Market Dashboard</h1>
      <div style={{ display: 'flex', gap: 20, alignItems: 'flex-start' }}>
        <div style={{ flex: 1 }}>
          <KlineChart />
        </div>
        <div style={{ width: 300 }}>
          <StatusMonitor />
        </div>
      </div>
    </div>
  );
}

export default App;
