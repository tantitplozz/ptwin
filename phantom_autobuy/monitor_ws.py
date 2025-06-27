"""
📊 GOD-TIER WebSocket Monitor
Real-time monitoring and control system
"""

import asyncio
import json
import websockets
import logging
from datetime import datetime
from .config import MONITOR_PORT, MONITOR_HOST

class MonitorServer:
    def __init__(self):
        self.clients = set()
        self.status = {
            'bot_status': 'initializing',
            'current_step': 'startup',
            'start_time': datetime.now().isoformat(),
            'metrics': {
                'total_sessions': 0,
                'successful_purchases': 0,
                'failed_attempts': 0,
                'detection_events': 0
            },
            'current_session': {
                'session_id': None,
                'phase': 'idle',
                'progress': 0,
                'last_action': None,
                'errors': []
            }
        }
        
    async def register_client(self, websocket):
        """Register new WebSocket client"""
        self.clients.add(websocket)
        print(f"📊 [MONITOR] Client connected. Total clients: {len(self.clients)}")
        
        # Send current status to new client
        await self.send_to_client(websocket, {
            'type': 'status_update',
            'data': self.status
        })
        
    async def unregister_client(self, websocket):
        """Unregister WebSocket client"""
        self.clients.discard(websocket)
        print(f"📊 [MONITOR] Client disconnected. Total clients: {len(self.clients)}")
        
    async def broadcast(self, message):
        """Broadcast message to all connected clients"""
        if self.clients:
            disconnected = set()
            for client in self.clients:
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
                except Exception as e:
                    print(f"⚠️ [MONITOR] Broadcast error: {e}")
                    disconnected.add(client)
                    
            # Remove disconnected clients
            for client in disconnected:
                self.clients.discard(client)
                
    async def send_to_client(self, client, message):
        """Send message to specific client"""
        try:
            await client.send(json.dumps(message))
        except Exception as e:
            print(f"⚠️ [MONITOR] Send error: {e}")
            
    def update_status(self, key, value):
        """Update status and broadcast to clients"""
        if '.' in key:
            # Handle nested keys like 'current_session.phase'
            keys = key.split('.')
            current = self.status
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value
        else:
            self.status[key] = value
            
        # Broadcast update
        asyncio.create_task(self.broadcast({
            'type': 'status_update',
            'data': self.status,
            'timestamp': datetime.now().isoformat()
        }))
        
    def log_event(self, event_type, data):
        """Log event and broadcast to clients"""
        event = {
            'type': 'event',
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        asyncio.create_task(self.broadcast(event))
        
    def update_metrics(self, metric, value):
        """Update metrics"""
        if metric in self.status['metrics']:
            if isinstance(value, (int, float)):
                self.status['metrics'][metric] += value
            else:
                self.status['metrics'][metric] = value
        else:
            self.status['metrics'][metric] = value
            
        asyncio.create_task(self.broadcast({
            'type': 'metrics_update',
            'data': self.status['metrics'],
            'timestamp': datetime.now().isoformat()
        }))

# Global monitor instance
monitor = MonitorServer()

async def handle_client(websocket, path):
    """Handle WebSocket client connection"""
    await monitor.register_client(websocket)
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                await handle_client_message(websocket, data)
            except json.JSONDecodeError:
                await monitor.send_to_client(websocket, {
                    'type': 'error',
                    'message': 'Invalid JSON format'
                })
            except Exception as e:
                await monitor.send_to_client(websocket, {
                    'type': 'error',
                    'message': str(e)
                })
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await monitor.unregister_client(websocket)
        
async def handle_client_message(websocket, data):
    """Handle message from WebSocket client"""
    message_type = data.get('type')
    
    if message_type == 'get_status':
        await monitor.send_to_client(websocket, {
            'type': 'status_response',
            'data': monitor.status
        })
        
    elif message_type == 'get_logs':
        # Send recent logs (would be implemented with actual log storage)
        await monitor.send_to_client(websocket, {
            'type': 'logs_response',
            'data': []  # Placeholder for actual logs
        })
        
    elif message_type == 'control_command':
        command = data.get('command')
        await handle_control_command(websocket, command, data.get('params', {}))
        
    else:
        await monitor.send_to_client(websocket, {
            'type': 'error',
            'message': f'Unknown message type: {message_type}'
        })
        
async def handle_control_command(websocket, command, params):
    """Handle control commands from clients"""
    if command == 'pause':
        monitor.update_status('bot_status', 'paused')
        await monitor.send_to_client(websocket, {
            'type': 'command_response',
            'command': command,
            'status': 'success',
            'message': 'Bot paused'
        })
        
    elif command == 'resume':
        monitor.update_status('bot_status', 'running')
        await monitor.send_to_client(websocket, {
            'type': 'command_response',
            'command': command,
            'status': 'success',
            'message': 'Bot resumed'
        })
        
    elif command == 'stop':
        monitor.update_status('bot_status', 'stopping')
        await monitor.send_to_client(websocket, {
            'type': 'command_response',
            'command': command,
            'status': 'success',
            'message': 'Bot stopping...'
        })
        
    elif command == 'get_screenshot':
        # Return latest screenshot path
        await monitor.send_to_client(websocket, {
            'type': 'command_response',
            'command': command,
            'status': 'success',
            'data': {'screenshot_path': 'latest_screenshot.png'}
        })
        
    else:
        await monitor.send_to_client(websocket, {
            'type': 'command_response',
            'command': command,
            'status': 'error',
            'message': f'Unknown command: {command}'
        })

async def start_monitor():
    """Start WebSocket monitor server"""
    print(f"📊 [MONITOR] Starting WebSocket server on {MONITOR_HOST}:{MONITOR_PORT}")
    
    try:
        # Update initial status
        monitor.update_status('bot_status', 'starting')
        monitor.update_status('current_step', 'monitor_initialization')
        
        # Start WebSocket server
        server = await websockets.serve(
            handle_client,
            MONITOR_HOST,
            MONITOR_PORT,
            ping_interval=20,
            ping_timeout=10
        )
        
        print(f"✅ [MONITOR] WebSocket server started successfully")
        monitor.update_status('bot_status', 'ready')
        monitor.log_event('monitor_started', {
            'host': MONITOR_HOST,
            'port': MONITOR_PORT
        })
        
        # Keep server running
        await server.wait_closed()
        
    except Exception as e:
        print(f"❌ [MONITOR] Server error: {e}")
        monitor.update_status('bot_status', 'error')
        monitor.log_event('monitor_error', {'error': str(e)})
        raise

# Helper functions for bot integration
def update_bot_status(status):
    """Update bot status"""
    monitor.update_status('bot_status', status)
    
def update_current_step(step):
    """Update current step"""
    monitor.update_status('current_step', step)
    
def update_session_info(session_id, phase, progress=None):
    """Update session information"""
    monitor.update_status('current_session.session_id', session_id)
    monitor.update_status('current_session.phase', phase)
    if progress is not None:
        monitor.update_status('current_session.progress', progress)
        
def log_action(action, details=None):
    """Log bot action"""
    monitor.update_status('current_session.last_action', action)
    monitor.log_event('bot_action', {
        'action': action,
        'details': details or {}
    })
    
def log_error(error, context=None):
    """Log error"""
    error_data = {
        'error': str(error),
        'context': context or {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Add to current session errors
    current_errors = monitor.status.get('current_session', {}).get('errors', [])
    current_errors.append(error_data)
    monitor.update_status('current_session.errors', current_errors[-10:])  # Keep last 10 errors
    
    # Log event
    monitor.log_event('error', error_data)
    
    # Update metrics
    monitor.update_metrics('failed_attempts', 1)
    
def log_success(details=None):
    """Log successful operation"""
    monitor.log_event('success', details or {})
    monitor.update_metrics('successful_purchases', 1)
    
def log_detection_event(detection_type, details=None):
    """Log detection event"""
    monitor.log_event('detection', {
        'type': detection_type,
        'details': details or {}
    })
    monitor.update_metrics('detection_events', 1)

# HTML Dashboard (served via HTTP if needed)
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>GOD-TIER PhantomAutoBuyBot Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
        .container { max-width: 1200px; margin: 0 auto; }
        .status-card { background: #2d2d2d; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric { background: #3d3d3d; padding: 15px; border-radius: 5px; text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; color: #4CAF50; }
        .logs { background: #000; padding: 15px; border-radius: 5px; height: 300px; overflow-y: auto; font-family: monospace; }
        .error { color: #f44336; }
        .success { color: #4CAF50; }
        .warning { color: #ff9800; }
        .controls button { margin: 5px; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .pause { background: #ff9800; }
        .resume { background: #4CAF50; }
        .stop { background: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 GOD-TIER PhantomAutoBuyBot Monitor</h1>
        
        <div class="status-card">
            <h2>Bot Status: <span id="bot-status">Connecting...</span></h2>
            <p>Current Step: <span id="current-step">-</span></p>
            <p>Session: <span id="session-id">-</span></p>
            <p>Progress: <span id="progress">0%</span></p>
        </div>
        
        <div class="controls">
            <button class="pause" onclick="sendCommand('pause')">⏸️ Pause</button>
            <button class="resume" onclick="sendCommand('resume')">▶️ Resume</button>
            <button class="stop" onclick="sendCommand('stop')">⏹️ Stop</button>
            <button onclick="sendCommand('get_screenshot')">📸 Screenshot</button>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-value" id="total-sessions">0</div>
                <div>Total Sessions</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="successful-purchases">0</div>
                <div>Successful Purchases</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="failed-attempts">0</div>
                <div>Failed Attempts</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="detection-events">0</div>
                <div>Detection Events</div>
            </div>
        </div>
        
        <div class="status-card">
            <h3>Live Logs</h3>
            <div class="logs" id="logs"></div>
        </div>
    </div>
    
    <script>
        const ws = new WebSocket('ws://localhost:8686');
        const logs = document.getElementById('logs');
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            if (data.type === 'status_update') {
                updateStatus(data.data);
            } else if (data.type === 'event') {
                addLog(data);
            } else if (data.type === 'metrics_update') {
                updateMetrics(data.data);
            }
        };
        
        function updateStatus(status) {
            document.getElementById('bot-status').textContent = status.bot_status;
            document.getElementById('current-step').textContent = status.current_step;
            document.getElementById('session-id').textContent = status.current_session.session_id || '-';
            document.getElementById('progress').textContent = status.current_session.progress + '%';
            updateMetrics(status.metrics);
        }
        
        function updateMetrics(metrics) {
            document.getElementById('total-sessions').textContent = metrics.total_sessions;
            document.getElementById('successful-purchases').textContent = metrics.successful_purchases;
            document.getElementById('failed-attempts').textContent = metrics.failed_attempts;
            document.getElementById('detection-events').textContent = metrics.detection_events;
        }
        
        function addLog(event) {
            const logEntry = document.createElement('div');
            const timestamp = new Date(event.timestamp).toLocaleTimeString();
            logEntry.innerHTML = `[${timestamp}] ${event.event_type}: ${JSON.stringify(event.data)}`;
            
            if (event.event_type === 'error') logEntry.className = 'error';
            else if (event.event_type === 'success') logEntry.className = 'success';
            else if (event.event_type === 'detection') logEntry.className = 'warning';
            
            logs.appendChild(logEntry);
            logs.scrollTop = logs.scrollHeight;
        }
        
        function sendCommand(command) {
            ws.send(JSON.stringify({
                type: 'control_command',
                command: command
            }));
        }
    </script>
</body>
</html>
"""