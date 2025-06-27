#!/usr/bin/env python3
"""
🔥 GOD-TIER PhantomAutoBuyBot - Advanced Monitoring Dashboard
Real-time monitoring and analytics dashboard
"""

import asyncio
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import aiohttp
from aiohttp import web, WSMsgType
import aiofiles

class DashboardServer:
    def __init__(self, port: int = 8687):
        self.port = port
        self.app = web.Application()
        self.websockets = set()
        self.stats = {
            'sessions': 0,
            'success_rate': 0.0,
            'avg_duration': 0.0,
            'errors': 0,
            'last_run': None,
            'status': 'idle'
        }
        self.setup_routes()
        
    def setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get('/', self.dashboard_page)
        self.app.router.add_get('/ws', self.websocket_handler)
        self.app.router.add_get('/api/stats', self.get_stats)
        self.app.router.add_get('/api/logs', self.get_logs)
        self.app.router.add_get('/api/sessions', self.get_sessions)
        self.app.router.add_static('/static', Path(__file__).parent / 'static')
        
    async def dashboard_page(self, request):
        """Serve the main dashboard page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 GOD-TIER PhantomAutoBuyBot Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header .subtitle { opacity: 0.8; font-size: 1.2em; }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-card h3 { margin-bottom: 10px; opacity: 0.8; }
        .stat-card .value { font-size: 2em; font-weight: bold; }
        .stat-card .trend { font-size: 0.9em; margin-top: 5px; }
        
        .charts-section { margin-bottom: 30px; }
        .chart-container { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 20px;
        }
        
        .logs-section { }
        .log-container { 
            background: rgba(0,0,0,0.3); 
            padding: 20px; 
            border-radius: 10px; 
            max-height: 400px; 
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .log-entry { 
            margin-bottom: 5px; 
            padding: 5px; 
            border-radius: 3px;
        }
        .log-info { background: rgba(0,123,255,0.2); }
        .log-success { background: rgba(40,167,69,0.2); }
        .log-warning { background: rgba(255,193,7,0.2); }
        .log-error { background: rgba(220,53,69,0.2); }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-running { background: #28a745; animation: pulse 2s infinite; }
        .status-idle { background: #6c757d; }
        .status-error { background: #dc3545; animation: pulse 2s infinite; }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .connection-status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 0.9em;
        }
        .connected { background: rgba(40,167,69,0.8); }
        .disconnected { background: rgba(220,53,69,0.8); }
    </style>
</head>
<body>
    <div class="connection-status" id="connectionStatus">Connecting...</div>
    
    <div class="container">
        <div class="header">
            <h1>🔥 GOD-TIER PhantomAutoBuyBot</h1>
            <div class="subtitle">Advanced Monitoring Dashboard</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>System Status</h3>
                <div class="value">
                    <span class="status-indicator" id="statusIndicator"></span>
                    <span id="systemStatus">Loading...</span>
                </div>
                <div class="trend" id="lastRun">Last run: Never</div>
            </div>
            
            <div class="stat-card">
                <h3>Total Sessions</h3>
                <div class="value" id="totalSessions">0</div>
                <div class="trend" id="sessionsTrend">+0 today</div>
            </div>
            
            <div class="stat-card">
                <h3>Success Rate</h3>
                <div class="value" id="successRate">0%</div>
                <div class="trend" id="successTrend">No data</div>
            </div>
            
            <div class="stat-card">
                <h3>Avg Duration</h3>
                <div class="value" id="avgDuration">0s</div>
                <div class="trend" id="durationTrend">No data</div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <h3>Performance Over Time</h3>
                <canvas id="performanceChart" width="800" height="200"></canvas>
            </div>
        </div>
        
        <div class="logs-section">
            <div class="chart-container">
                <h3>Real-time Logs</h3>
                <div class="log-container" id="logContainer">
                    <div class="log-entry log-info">Dashboard initialized...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        class Dashboard {
            constructor() {
                this.ws = null;
                this.reconnectInterval = 5000;
                this.connect();
                this.setupChart();
            }
            
            connect() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws`;
                
                this.ws = new WebSocket(wsUrl);
                
                this.ws.onopen = () => {
                    console.log('Connected to dashboard');
                    this.updateConnectionStatus(true);
                };
                
                this.ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                };
                
                this.ws.onclose = () => {
                    console.log('Disconnected from dashboard');
                    this.updateConnectionStatus(false);
                    setTimeout(() => this.connect(), this.reconnectInterval);
                };
                
                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };
            }
            
            updateConnectionStatus(connected) {
                const status = document.getElementById('connectionStatus');
                status.textContent = connected ? 'Connected' : 'Disconnected';
                status.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
            }
            
            handleMessage(data) {
                switch(data.type) {
                    case 'stats':
                        this.updateStats(data.data);
                        break;
                    case 'log':
                        this.addLogEntry(data.data);
                        break;
                    case 'session':
                        this.updateSession(data.data);
                        break;
                }
            }
            
            updateStats(stats) {
                document.getElementById('systemStatus').textContent = stats.status;
                document.getElementById('totalSessions').textContent = stats.sessions;
                document.getElementById('successRate').textContent = `${stats.success_rate}%`;
                document.getElementById('avgDuration').textContent = `${stats.avg_duration}s`;
                
                const indicator = document.getElementById('statusIndicator');
                indicator.className = `status-indicator status-${stats.status}`;
                
                if (stats.last_run) {
                    document.getElementById('lastRun').textContent = `Last run: ${stats.last_run}`;
                }
            }
            
            addLogEntry(log) {
                const container = document.getElementById('logContainer');
                const entry = document.createElement('div');
                entry.className = `log-entry log-${log.level}`;
                entry.textContent = `[${log.timestamp}] ${log.message}`;
                
                container.appendChild(entry);
                container.scrollTop = container.scrollHeight;
                
                // Keep only last 100 entries
                while (container.children.length > 100) {
                    container.removeChild(container.firstChild);
                }
            }
            
            setupChart() {
                // Simple chart implementation
                const canvas = document.getElementById('performanceChart');
                const ctx = canvas.getContext('2d');
                
                // Draw placeholder chart
                ctx.fillStyle = 'rgba(255,255,255,0.1)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = 'white';
                ctx.font = '16px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('Performance chart will appear here', canvas.width/2, canvas.height/2);
            }
        }
        
        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', () => {
            new Dashboard();
        });
    </script>
</body>
</html>
        """
        return web.Response(text=html, content_type='text/html')
    
    async def websocket_handler(self, request):
        """Handle WebSocket connections"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.websockets.add(ws)
        print(f"📊 [DASHBOARD] Client connected (total: {len(self.websockets)})")
        
        # Send initial stats
        await self.send_to_client(ws, 'stats', self.stats)
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    await self.handle_client_message(ws, data)
                elif msg.type == WSMsgType.ERROR:
                    print(f'WebSocket error: {ws.exception()}')
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            self.websockets.discard(ws)
            print(f"📊 [DASHBOARD] Client disconnected (total: {len(self.websockets)})")
        
        return ws
    
    async def send_to_client(self, ws, msg_type, data):
        """Send message to specific client"""
        try:
            await ws.send_text(json.dumps({
                'type': msg_type,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }))
        except Exception as e:
            print(f"Error sending to client: {e}")
    
    async def broadcast(self, msg_type, data):
        """Broadcast message to all connected clients"""
        if not self.websockets:
            return
        
        message = json.dumps({
            'type': msg_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        
        # Send to all clients
        disconnected = set()
        for ws in self.websockets:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.add(ws)
        
        # Remove disconnected clients
        self.websockets -= disconnected
    
    async def handle_client_message(self, ws, data):
        """Handle messages from clients"""
        msg_type = data.get('type')
        
        if msg_type == 'get_logs':
            logs = await self.get_recent_logs()
            await self.send_to_client(ws, 'logs', logs)
        elif msg_type == 'get_sessions':
            sessions = await self.get_recent_sessions()
            await self.send_to_client(ws, 'sessions', sessions)
    
    async def get_stats(self, request):
        """API endpoint for stats"""
        return web.json_response(self.stats)
    
    async def get_logs(self, request):
        """API endpoint for logs"""
        logs = await self.get_recent_logs()
        return web.json_response(logs)
    
    async def get_sessions(self, request):
        """API endpoint for sessions"""
        sessions = await self.get_recent_sessions()
        return web.json_response(sessions)
    
    async def get_recent_logs(self):
        """Get recent log entries"""
        logs = []
        log_file = Path('logs') / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        if log_file.exists():
            try:
                async with aiofiles.open(log_file, 'r') as f:
                    lines = await f.readlines()
                    # Get last 50 lines
                    for line in lines[-50:]:
                        if line.strip():
                            logs.append({
                                'timestamp': datetime.now().strftime('%H:%M:%S'),
                                'level': 'info',
                                'message': line.strip()
                            })
            except Exception as e:
                print(f"Error reading logs: {e}")
        
        return logs
    
    async def get_recent_sessions(self):
        """Get recent session data"""
        sessions = []
        vector_db_path = Path('vector_db.json')
        
        if vector_db_path.exists():
            try:
                async with aiofiles.open(vector_db_path, 'r') as f:
                    content = await f.read()
                    data = json.loads(content)
                    sessions = data.get('sessions', [])[-10:]  # Last 10 sessions
            except Exception as e:
                print(f"Error reading sessions: {e}")
        
        return sessions
    
    async def update_stats(self, new_stats):
        """Update dashboard stats"""
        self.stats.update(new_stats)
        await self.broadcast('stats', self.stats)
    
    async def log_event(self, level, message):
        """Log an event to dashboard"""
        log_data = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'level': level,
            'message': message
        }
        await self.broadcast('log', log_data)
    
    async def start_server(self):
        """Start the dashboard server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        
        print(f"🔥 [DASHBOARD] Server started on http://0.0.0.0:{self.port}")
        return runner

# Global dashboard instance
dashboard = None

async def start_dashboard(port: int = 8687):
    """Start the dashboard server"""
    global dashboard
    dashboard = DashboardServer(port)
    runner = await dashboard.start_server()
    return dashboard, runner

async def update_dashboard_stats(**kwargs):
    """Update dashboard stats"""
    global dashboard
    if dashboard:
        await dashboard.update_stats(kwargs)

async def log_to_dashboard(level: str, message: str):
    """Log message to dashboard"""
    global dashboard
    if dashboard:
        await dashboard.log_event(level, message)

if __name__ == "__main__":
    async def main():
        dashboard_instance, runner = await start_dashboard()
        
        # Keep server running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down dashboard...")
            await runner.cleanup()
    
    asyncio.run(main())