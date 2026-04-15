/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { Terminal, Smartphone, Activity, Cpu, Zap, ShieldAlert, RefreshCw, ChevronRight } from 'lucide-react';

export default function App() {
  const [uptime, setUptime] = useState('00:00:00');
  const [devices, setDevices] = useState<string[]>(['emulator-5554', 'emulator-5556']);
  const [selectedDevice, setSelectedDevice] = useState('emulator-5554');
  const [isRefreshing, setIsRefreshing] = useState(false);

  const refreshDevices = () => {
    setIsRefreshing(true);
    // Simulate ADB call
    setTimeout(() => {
      setIsRefreshing(false);
    }, 800);
  };

  useEffect(() => {
    const start = Date.now();
    const timer = setInterval(() => {
      const diff = Date.now() - start;
      const h = Math.floor(diff / 3600000).toString().padStart(2, '0');
      const m = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
      const s = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
      setUptime(`${h}:${m}:${s}`);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col h-screen w-full overflow-hidden border border-line">
      {/* Header */}
      <header className="h-[60px] border-b-2 border-line flex items-center px-6 justify-between bg-bg">
        <div className="font-mono font-bold text-xl tracking-tighter flex items-center gap-3">
          AIRTOUCH-FAST <span className="text-[10px] bg-ink text-bg px-1.5 py-0.5 rounded-sm align-middle">v1.0.4-BETA</span>
        </div>
        <div className="font-mono text-[12px] flex items-center gap-4">
          <span>PID: 14202</span>
          <span className="h-3 w-[1px] bg-line opacity-20"></span>
          <span className="text-accent font-bold flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse shadow-[0_0_4px_#FF4E00]"></span>
            DAEMON ACTIVE
          </span>
        </div>
      </header>

      {/* Main Container */}
      <div className="grid grid-cols-[280px_1fr_300px] flex-1 overflow-hidden">
        
        {/* Left Sidebar */}
        <div className="border-r border-line flex flex-col overflow-hidden">
          <div className="section-header flex items-center gap-2">
            <Smartphone size={12} /> Device Environment
          </div>
          <div className="p-5 border-b border-line space-y-4">
            <div className="stat-group">
              <span className="stat-label">ADB EXECUTABLE PATH</span>
              <div className="flex gap-2 mt-1">
                <input 
                  type="text" 
                  defaultValue="adb"
                  className="bg-white/50 border border-line/20 px-2 py-1 font-mono text-[11px] flex-1 focus:outline-none focus:border-accent"
                  placeholder="e.g. C:\adb\adb.exe"
                />
                <button className="bg-ink text-bg px-2 py-1 font-mono text-[10px] hover:bg-accent transition-colors">SET</button>
              </div>
            </div>
            <div className="stat-group">
              <div className="flex items-center justify-between mb-2">
                <span className="stat-label">TARGET DEVICE</span>
                <button 
                  onClick={refreshDevices}
                  className={`text-accent hover:opacity-80 transition-all ${isRefreshing ? 'animate-spin' : ''}`}
                >
                  <RefreshCw size={10} />
                </button>
              </div>
              <div className="space-y-1">
                {devices.map(serial => (
                  <button
                    key={serial}
                    onClick={() => setSelectedDevice(serial)}
                    className={`w-full flex items-center justify-between px-3 py-2 font-mono text-[11px] border transition-all ${
                      selectedDevice === serial 
                        ? 'bg-ink text-bg border-ink' 
                        : 'bg-white/30 border-line/10 hover:border-line/40'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <div className={`w-1.5 h-1.5 rounded-full ${selectedDevice === serial ? 'bg-accent' : 'bg-line/20'}`}></div>
                      {serial}
                    </div>
                    {selectedDevice === serial && <ChevronRight size={10} />}
                  </button>
                ))}
              </div>
            </div>
            <div className="stat-group">
              <span className="stat-label">ABI</span>
              <span className="stat-value">x86_64 (LDPlayer)</span>
            </div>
            <div className="stat-group">
              <span className="stat-label">MAX CONTACTS</span>
              <span className="stat-value">10</span>
            </div>
            <div className="stat-group">
              <span className="stat-label">RESOLUTION</span>
              <span className="stat-value">32767 x 32767</span>
            </div>
          </div>

          <div className="section-header flex items-center gap-2">
            <Terminal size={12} /> Command History
          </div>
          <div className="bg-black/5 p-4 flex-grow overflow-y-auto font-mono text-[12px] leading-relaxed">
            <div className="log-entry border-l-[#2ECC71]">v 1</div>
            <div className="log-entry border-l-[#2ECC71]">^ 10 32767 32767 128</div>
            <div className="log-entry border-l-[#2ECC71]">$ 1842</div>
            <div className="log-entry border-l-accent">d 0 15000 22000 50</div>
            <div className="log-entry border-l-accent">c</div>
            <div className="log-entry border-l-accent">m 0 15500 22500 50</div>
            <div className="log-entry border-l-accent">c</div>
            <div className="log-entry border-l-accent">u 0</div>
            <div className="log-entry border-l-accent">c</div>
            <div className="log-entry border-l-accent opacity-40 italic">w 500</div>
          </div>
        </div>

        {/* Center Visualizer */}
        <div className="border-r border-line p-6 flex flex-col gap-5 overflow-y-auto">
          <div className="section-header flex items-center gap-2">
            <Activity size={12} /> Touch Injection Map
          </div>
          <div className="aspect-[9/16] w-full max-w-[320px] border-2 border-line mx-auto relative bg-white flex items-center justify-center shadow-inner">
            <div className="absolute w-[30px] h-[30px] border border-accent rounded-full bg-accent/10 top-[40%] left-[60%] flex items-center justify-center">
              <div className="w-1 h-1 bg-accent rounded-full"></div>
              <span className="absolute -top-[18px] left-0 text-[9px] font-mono text-accent whitespace-nowrap">ID: 0 @ {selectedDevice}</span>
            </div>
            <span className="text-[10px] opacity-30 font-mono">1080 x 1920 CANVAS</span>
          </div>
          
          <div className="section-header flex items-center gap-2">
            <Zap size={12} /> Injection Controls
          </div>
          <div className="grid grid-cols-2 gap-[1px] bg-line border border-line">
            <button className="control-btn">[R] RESET ALL</button>
            <button className="control-btn">[T] TEST TAP</button>
            <button className="control-btn">[S] SWIPE SEQ</button>
            <button className="control-btn">[K] KILL DAEMON</button>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="flex flex-col overflow-hidden">
          <div className="section-header flex items-center gap-2">
            <Cpu size={12} /> Coordinate Mapping
          </div>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse font-mono text-[11px]">
              <thead>
                <tr className="border-b border-line">
                  <th className="text-left font-serif italic p-2 opacity-60">Airtest</th>
                  <th className="text-left font-serif italic p-2 opacity-60">Minitouch</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-black/5">
                  <td className="p-2">x: 540</td>
                  <td className="p-2">x: 16383</td>
                </tr>
                <tr className="border-b border-black/5">
                  <td className="p-2">y: 960</td>
                  <td className="p-2">y: 16383</td>
                </tr>
                <tr className="border-b border-black/5">
                  <td className="p-2">x: 0</td>
                  <td className="p-2">x: 0</td>
                </tr>
                <tr className="border-b border-black/5">
                  <td className="p-2">y: 1920</td>
                  <td className="p-2">y: 32767</td>
                </tr>
                <tr className="border-b border-black/5">
                  <td className="p-2">x: 1080</td>
                  <td className="p-2">x: 32767</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="section-header flex items-center gap-2">
            <ShieldAlert size={12} /> Performance Metrics
          </div>
          <div className="p-4 space-y-4">
            <div className="stat-group">
              <span className="stat-label">LATENCY</span>
              <span className="stat-value text-[#2ECC71]">1.24ms</span>
            </div>
            <div className="stat-group">
              <span className="stat-label">THROUGHPUT</span>
              <span className="stat-value">840 cmd/sec</span>
            </div>
            <div className="stat-group">
              <span className="stat-label">SOCKET BUFFER</span>
              <div className="w-full h-1 bg-black/10 mt-2">
                <div className="w-[12%] h-full bg-ink"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="h-8 border-t border-line flex items-center px-4 font-mono text-[10px] gap-6 bg-bg">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#2ECC71] shadow-[0_0_4px_#2ECC71]"></span>
          ADB FORWARD: 127.0.0.1:5037
        </div>
        <div>SOCKET: TCP_NODELAY</div>
        <div className="ml-auto">UPTIME: {uptime}</div>
      </footer>
    </div>
  );
}
