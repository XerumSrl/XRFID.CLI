import threading
import websocket
import json
import queue
import time
import csv
import datetime
import os
import traceback
import socket
import ssl
import platform
from typing import Optional
from .tag_table_window import TagData

class WebSocketListener(threading.Thread):
    """
    Listens for WebSocket messages and processes them.
    """
    def __init__(self, uri: str, data_queue: queue.Queue, stop_event: threading.Event, fallback_uris: Optional[list] = None, debug: bool = False):
        super().__init__()
        self.uri = uri
        self.fallback_uris = fallback_uris or []
        self.all_uris = [uri] + self.fallback_uris
        self.current_uri_index = 0
        self.data_queue = data_queue
        self.stop_event = stop_event
        self.ws = None
        self.daemon = True  # Allows the main program to exit even if the thread is running
        self.debug = debug
        self._is_connected = False  # Flag for active connection
        # Connection timing for stability checking
        self._connection_open_time = None
        # Minimal counters for data tracking
        self._last_data_time = None  # Last received data time
        self._heartbeat_count = 0  # Heartbeat counter
        self.ws_recorder_active = False  # WebSocket recorder active flag
        
        # CSV Recording attributes
        self._csv_messages_file = None
        self._csv_messages_writer = None
        self._recording_start_time = None
        self._recording_tags = {}  # Dictionary to store TagData objects during recording
        self._recording_timestamp = None  # Timestamp for CSV filename

    def _split_json_messages(self, message):
        """
        Splits concatenated JSON messages into a list of individual messages.
        
        Args:
            message: String or bytes containing one or more concatenated JSON messages
        
        Returns:
            List[str]: List of individual JSON messages
        """
        if isinstance(message, bytes):
            message = message.decode('utf-8', errors='ignore')
        
        messages = []
        current_message = ""
        brace_count = 0
        in_string = False
        escape_next = False
        
        for char in message:
            current_message += char
            
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    
                    if brace_count == 0:
                        # End of JSON message
                        messages.append(current_message.strip())
                        current_message = ""
        
        # Add the last message if something remains
        if current_message.strip():
            messages.append(current_message.strip())
            
        return messages

    def on_message(self, ws, message):
        """Callback executed when receiving a message."""
        # Counters to reduce log spam
        if not hasattr(self, '_tag_counts'):
            self._tag_counts = {}
            self._last_log_time = {}
            self._heartbeat_count = 0
            
        try:
            # Split any concatenated JSON messages
            json_messages = self._split_json_messages(message)
            for json_msg in json_messages:
                if not json_msg:
                    continue
                try:
                    data = json.loads(json_msg)
                    
                    # Record all messages to CSV if recording is active
                    if self.ws_recorder_active:
                        self._write_message_to_csv(data)
                    
                    if isinstance(data, dict):
                        if 'data' in data and isinstance(data['data'], dict):
                            tag_data = data['data']
                            if 'idHex' in tag_data:
                                tag_id = tag_data['idHex']
                                rssi_raw = tag_data.get('peakRssi', 'N/A')
                                antenna_raw = tag_data.get('antenna', 'N/A')
                                timestamp = data.get('timestamp', 'N/A')
                                if rssi_raw == 'N/A' or rssi_raw is None:
                                    rssi = "N/A"
                                else:
                                    try:
                                        rssi_value = float(rssi_raw)
                                        rssi = f"{rssi_value:.1f}"
                                    except (ValueError, TypeError):
                                        rssi = "N/A"
                                if antenna_raw == 'N/A' or antenna_raw is None:
                                    antenna = "N/A"
                                else:
                                    try:
                                        antenna_value = int(antenna_raw)
                                        if antenna_value > 100:
                                            antenna = "ERR"
                                        else:
                                            antenna = str(antenna_value)
                                    except (ValueError, TypeError):
                                        antenna = "N/A"
                                self._tag_counts[tag_id] = self._tag_counts.get(tag_id, 0) + 1
                                current_time = time.time()
                                if (tag_id not in self._last_log_time or 
                                    current_time - self._last_log_time[tag_id] > 5.0):
                                    count = self._tag_counts[tag_id]
                                    time_short = timestamp if isinstance(timestamp, str) and len(timestamp) > 12 else timestamp
                                    if self.debug:
                                        if count == 1:
                                            print(f"[DEBUG][WebSocketListener] NEW: {tag_id}... | 📡 {rssi}dBm | 📶 Ant{antenna} | #{count}")
                                        else:
                                            print(f"[DEBUG][WebSocketListener] #{count}: {tag_id}... | 📡 {rssi}dBm | 📶 Ant{antenna}")
                                    self._last_log_time[tag_id] = current_time
                        elif data.get('type') == 'heartbeat':
                            self._heartbeat_count += 1
                            if self._heartbeat_count % 10 == 0 and self.debug:
                                print(f"[DEBUG][WebSocketListener] Reader heartbeat (#{self._heartbeat_count})")
                        elif data.get('type') == 'gpo':
                            pin = data.get('data', {}).get('pin', 'N/A')
                            state = data.get('data', {}).get('state', 'N/A')
                            if self.debug:
                                print(f"[DEBUG][WebSocketListener] GPIO Pin {pin}: {state}")
                        elif data.get('type') == 'RAW_DIRECTIONALITY':
                            tag_data = data.get('data', {})
                            if tag_data:
                                if self.debug:
                                    tag_id = tag_data.get('idHex', 'N/A')
                                    azimuth = tag_data.get('azimuth', 'N/A')
                                    elevation = tag_data.get('elevation', 'N/A')
                                    timestamp = data.get('timestamp', 'N/A')
                                    print(f"[DEBUG][WebSocketListener] RAW_DIR: {tag_id} (Az: {azimuth}°, El: {elevation}°) | ⏰ {timestamp}")
                        else:
                            msg_type = data.get('type', 'UNKNOWN')
                            if self.debug:
                                print(f"[DEBUG][WebSocketListener] Message type: {msg_type} | Data: {str(data)[:100]}...")
                    
                    # Process tag data for recording if recording is active (centralized processing)
                    if self.ws_recorder_active:
                        self._process_tag_data_for_recording(data)

                    self.data_queue.put(data)
                    self._last_data_time = time.time()

                except json.JSONDecodeError as e:
                    if self.debug:
                        print(f"[DEBUG][WebSocketListener] Invalid JSON: {json_msg[:30]}...")
                    error_data = {"raw_message": json_msg, "error": str(e)}
                    
                    # Record error messages to CSV if recording is active
                    if self.ws_recorder_active:
                        self._write_message_to_csv(error_data)
                    
                    self.data_queue.put(error_data)
        except Exception as e:
            if self.debug:
                print(f"[DEBUG]⚠️ Processing error: {e}")
            error_data = {"raw_message": message, "error": str(e)}
            
            # Record error messages to CSV if recording is active
            if self.ws_recorder_active:
                self._write_message_to_csv(error_data)
            
            self.data_queue.put(error_data)

    def on_error(self, ws, error):
        """Callback for error handling."""
        error_str = str(error)
        current_uri = self.all_uris[self.current_uri_index]
        
        # Save detailed error information to file
        if self.debug:
            self._save_websocket_error_report(error, current_uri)
        
        if error == "Connection to remote host was lost.":
            print(f"💡 Connection lost error, trying to skip everything")
            return

        print(f"❌ Connection failed: {current_uri}")
        print(f"   Error: {error}")
        
        if "SSL" in error_str or "wrong version number" in error_str:
            print(f"💡 SSL not supported, will try next URI if available...")
        elif "Connection refused" in error_str or "Failed to connect" in error_str:
            print(f"💡 Connection refused, will try next URI if available...")
        else:
            print(f"💡 Connection error, will try next URI if available...")
            
        # Close WebSocket to force exit from run_forever()
        if self.ws:
            self.ws.close()

    def _save_websocket_error_report(self, error, current_uri):
        """Save comprehensive WebSocket error debugging information to a JSON file."""
        try:
            # Create logs/ws-errors-reports directory if it doesn't exist
            error_reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'ws-errors-reports')
            os.makedirs(error_reports_dir, exist_ok=True)
            
            # Generate timestamp and filename
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S_%f')[:-3]  # Include milliseconds
            filename = os.path.join(error_reports_dir, f"websocket_on_error_{timestamp_str}.json")
            
            # Collect comprehensive error information
            error_report = {
                "error_details": {
                    "timestamp": timestamp.isoformat(),
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                    "error_repr": repr(error),
                    "traceback": traceback.format_exc() if hasattr(error, '__traceback__') else None
                },
                "connection_context": {
                    "current_uri": current_uri,
                    "current_uri_index": self.current_uri_index,
                    "all_uris": self.all_uris,
                    "primary_uri": self.uri,
                    "fallback_uris": self.fallback_uris,
                    "connection_open_time": self._connection_open_time,
                    "is_connected": self._is_connected,
                    "debug_mode": self.debug
                },
                "websocket_state": {
                    "ws_exists": self.ws is not None,
                    "ws_sock_state": None,
                    "ws_url": None,
                    "ws_headers": None
                },
                "thread_state": {
                    "thread_name": self.name,
                    "thread_ident": self.ident,
                    "is_alive": self.is_alive(),
                    "daemon": self.daemon,
                    "stop_event_set": self.stop_event.is_set()
                },
                "system_context": {
                    "platform": platform.platform(),
                    "python_version": platform.python_version(),
                    "hostname": socket.gethostname(),
                    "current_time": time.time(),
                    "process_id": os.getpid()
                },
                "network_diagnostics": {},
                "ssl_context": {},
                "error_classification": {
                    "is_ssl_error": False,
                    "is_connection_error": False,
                    "is_timeout_error": False,
                    "is_protocol_error": False,
                    "error_category": "unknown"
                },
                "data_flow_context": {
                    "last_data_time": self._last_data_time,
                    "heartbeat_count": self._heartbeat_count,
                    "recording_active": self.ws_recorder_active
                },
                "troubleshooting_suggestions": []
            }
            
            # Enhanced WebSocket state information
            if self.ws:
                try:
                    error_report["websocket_state"]["ws_url"] = getattr(self.ws, 'url', None)
                    if hasattr(self.ws, 'sock') and self.ws.sock:
                        sock = self.ws.sock
                        if hasattr(sock, 'getsockopt'):
                            try:
                                error_report["websocket_state"]["ws_sock_state"] = {
                                    "family": sock.family.name if hasattr(sock.family, 'name') else str(sock.family),
                                    "type": sock.type.name if hasattr(sock.type, 'name') else str(sock.type),
                                    "timeout": sock.gettimeout(),
                                    "connected": True
                                }
                            except Exception as sock_e:
                                error_report["websocket_state"]["ws_sock_state"] = f"Error reading socket state: {sock_e}"
                except Exception as ws_e:
                    error_report["websocket_state"]["ws_info_error"] = str(ws_e)
            
            # Network diagnostics
            try:
                # Extract host and port for diagnostics
                from urllib.parse import urlparse
                parsed_uri = urlparse(current_uri)
                host = parsed_uri.hostname
                port = parsed_uri.port or (443 if parsed_uri.scheme == 'wss' else 80)
                
                error_report["network_diagnostics"]["parsed_uri"] = {
                    "scheme": parsed_uri.scheme,
                    "hostname": host,
                    "port": port,
                    "path": parsed_uri.path
                }
                
                # Test basic connectivity
                try:
                    # Quick socket test
                    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    test_socket.settimeout(5)
                    result = test_socket.connect_ex((host, port))
                    test_socket.close()
                    error_report["network_diagnostics"]["socket_test"] = {
                        "result_code": result,
                        "can_connect": result == 0,
                        "test_timestamp": time.time()
                    }
                except Exception as net_e:
                    error_report["network_diagnostics"]["socket_test"] = {
                        "error": str(net_e),
                        "test_failed": True
                    }
                
                # DNS resolution test
                try:
                    addr_info = socket.getaddrinfo(host, port)
                    error_report["network_diagnostics"]["dns_resolution"] = {
                        "resolved_addresses": [addr[4][0] for addr in addr_info],
                        "resolution_successful": True
                    }
                except Exception as dns_e:
                    error_report["network_diagnostics"]["dns_resolution"] = {
                        "error": str(dns_e),
                        "resolution_failed": True
                    }
                    
            except Exception as diag_e:
                error_report["network_diagnostics"]["diagnostics_error"] = str(diag_e)
            
            # SSL context information for wss:// connections
            if current_uri.startswith('wss://'):
                try:
                    error_report["ssl_context"]["is_ssl_connection"] = True
                    error_report["ssl_context"]["ssl_version"] = ssl.OPENSSL_VERSION
                    error_report["ssl_context"]["default_verify_paths"] = ssl.get_default_verify_paths()._asdict()
                    
                    # Test SSL connectivity separately
                    try:
                        from urllib.parse import urlparse
                        parsed_uri = urlparse(current_uri)
                        host = parsed_uri.hostname
                        port = parsed_uri.port or 443
                        
                        ssl_context = ssl.create_default_context()
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE
                        
                        with socket.create_connection((host, port), timeout=5) as sock:
                            with ssl_context.wrap_socket(sock, server_hostname=host) as ssock:
                                error_report["ssl_context"]["ssl_test"] = {
                                    "ssl_handshake_successful": True,
                                    "cipher": ssock.cipher(),
                                    "server_cert_subject": dict(ssock.getpeercert()['subject'][0]) if ssock.getpeercert() else None
                                }
                    except Exception as ssl_test_e:
                        error_report["ssl_context"]["ssl_test"] = {
                            "ssl_handshake_failed": True,
                            "error": str(ssl_test_e)
                        }
                        
                except Exception as ssl_e:
                    error_report["ssl_context"]["ssl_context_error"] = str(ssl_e)
            else:
                error_report["ssl_context"]["is_ssl_connection"] = False
            
            # Error classification
            error_str = str(error).lower()
            if any(keyword in error_str for keyword in ['ssl', 'certificate', 'handshake', 'tls']):
                error_report["error_classification"]["is_ssl_error"] = True
                error_report["error_classification"]["error_category"] = "ssl_error"
                error_report["troubleshooting_suggestions"].extend([
                    "SSL/TLS connection issue detected",
                    "Try using ws:// instead of wss:// if the server supports it",
                    "Check if the server certificate is valid and trusted",
                    "Verify that the server supports the WebSocket protocol over SSL"
                ])
            elif any(keyword in error_str for keyword in ['connection refused', 'connection failed', 'cannot connect']):
                error_report["error_classification"]["is_connection_error"] = True
                error_report["error_classification"]["error_category"] = "connection_error"
                error_report["troubleshooting_suggestions"].extend([
                    "Connection refused - server may not be running or accessible",
                    "Check if the host and port are correct",
                    "Verify network connectivity to the target host",
                    "Check if firewall rules allow the connection"
                ])
            elif any(keyword in error_str for keyword in ['timeout', 'timed out']):
                error_report["error_classification"]["is_timeout_error"] = True
                error_report["error_classification"]["error_category"] = "timeout_error"
                error_report["troubleshooting_suggestions"].extend([
                    "Connection timeout - server may be slow to respond",
                    "Try increasing connection timeout values",
                    "Check network latency to the target host",
                    "Verify that the server is responding to requests"
                ])
            elif any(keyword in error_str for keyword in ['protocol', 'handshake', 'upgrade']):
                error_report["error_classification"]["is_protocol_error"] = True
                error_report["error_classification"]["error_category"] = "protocol_error"
                error_report["troubleshooting_suggestions"].extend([
                    "WebSocket protocol error detected",
                    "Verify that the server supports WebSocket connections",
                    "Check if the WebSocket endpoint path is correct",
                    "Ensure proper WebSocket headers are being sent"
                ])
            else:
                error_report["error_classification"]["error_category"] = "general_error"
                error_report["troubleshooting_suggestions"].extend([
                    "General WebSocket error detected",
                    "Check server logs for more information",
                    "Verify WebSocket server configuration",
                    "Try connecting with a different WebSocket client to isolate the issue"
                ])
            
            # Add URI specific suggestions
            if self.current_uri_index < len(self.all_uris) - 1:
                error_report["troubleshooting_suggestions"].append(f"Will attempt next URI: {self.all_uris[self.current_uri_index + 1]}")
            else:
                error_report["troubleshooting_suggestions"].append("All configured URIs have been attempted")
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(error_report, f, indent=2, default=str)
            
            if self.debug:
                print(f"[DEBUG] WebSocket error report saved: {filename}")
            
            # Brief notification to user
            print(f"📋 Detailed error report saved: {os.path.basename(filename)}")
            
        except Exception as save_error:
            print(f"⚠️  Failed to save error report: {save_error}")
            if self.debug:
                print(f"[DEBUG] Error report save failure: {traceback.format_exc()}")

    def on_close(self, ws, close_status_code, close_msg):
        """Callback executed on connection closure."""
        current_uri = self.all_uris[self.current_uri_index]
        self._is_connected = False
        
        # DEBUG: Log detailed close information
        if self.debug:
            print(f"[DEBUG] on_close called - URI: {current_uri}")
            print(f"[DEBUG] close_status_code: {close_status_code} (type: {type(close_status_code)})")
            print(f"[DEBUG] close_msg: {close_msg} (type: {type(close_msg)})")
            print(f"[DEBUG] stop_event is set: {self.stop_event.is_set()}")
        
        if self.stop_event.is_set():
            print(f"🔌 WebSocket connection closed (intentional): {current_uri}")
            return  # Don't attempt to reconnect if stop event is set
        
        # Stop reading data recording if active
        self._stop_csv_recording()

        # Check if this was an immediate disconnection
        connection_duration = 0
        if hasattr(self, '_connection_open_time'):
            if self._connection_open_time:
                connection_duration = time.time() - self._connection_open_time
            else:
                print("[DEBUG] _connection_open_time is not set")
                connection_duration = 0

        is_immediate_disconnect = connection_duration < 1.0  # Less than 1 second
        
        # Format close details
        code_str = str(close_status_code) if close_status_code is not None else "None"
        msg_str = str(close_msg) if close_msg is not None else "None"
        
        print(f"🔌 WebSocket connection closed: {current_uri}")
        print(f"   Code: {code_str}, Message: {msg_str}")
        
        if is_immediate_disconnect:
            print(f"   ⏱️  Connection lasted only {connection_duration:.1f} seconds")
        
        # Provide context based on the close code
        if close_status_code is None:
            print("   ⚠️  Close code is None - possible network issue or server not ready")
            if current_uri.startswith('ws://') and is_immediate_disconnect:
                print("   💡 This often happens when IOTC service is not ready yet")
                print("   💡 Try running IOTC setup (option 2) to activate the service")
            else:
                print("   💡 This could indicate network connectivity issues or server unavailable")
        elif close_status_code == 1000:
            print("   ✅ Normal closure")
        elif close_status_code == 1006:
            print("   ⚠️  Abnormal closure - connection lost without proper close frame")
            print("   💡 Often indicates server not ready or network issues")
        elif close_status_code == 1002:
            print("   ⚠️  Protocol error - WebSocket server rejected the connection")
        elif close_status_code == 1011:
            print("   ⚠️  Server error - internal server error occurred")
        else:
            print(f"   ℹ️  Close code {close_status_code} - see WebSocket RFC for details")
        
        print("� Connection attempt completed - returning to menu")
        # Always stop after any disconnection - no automatic reconnection
        self.stop_event.set()

    def on_open(self, ws):
        """Callback executed when the connection opens."""
        current_uri = self.all_uris[self.current_uri_index]
        
        # Record connection open time for stability checking
        self._connection_open_time = time.time()
        
        print(f"✅ WebSocket connection opened: {current_uri}")
        
        # Mark as connected
        self._is_connected = True

    def run(self):
        """Main thread for WebSocket management."""
        if self.debug:
            print(f"[DEBUG] WebSocketListener.run - Starting persistent connection")
            print(f"[DEBUG] WebSocketListener.run - Primary URI: {self.uri}")
            print(f"[DEBUG] WebSocketListener.run - Fallback URIs: {self.fallback_uris}")
            
        print("🔗 Initializing persistent WebSocket listener...")
        print("📋 Configured URIs:")
        for i, uri in enumerate(self.all_uris, 1):
            print(f"   {i}. {uri}")
            
        # Try each URI once, no retry loops
        for uri_index, current_uri in enumerate(self.all_uris):
            if self.stop_event.is_set():
                if self.debug:
                    print(f"[DEBUG] WebSocketListener.run - Stop event set, breaking")
                print("🛑 WebSocket listener stopping")
                break
                
            try:
                self.current_uri_index = uri_index
                
                if self.debug:
                    print(f"[DEBUG] WebSocketListener.run - Attempting connection to: {current_uri}")
                
                print(f"\n🔗 WebSocket connection attempt ({uri_index + 1}/{len(self.all_uris)}): {current_uri}")
                
                # Configure SSL for wss:// connections (more stable configuration)
                sslopt = None
                if current_uri.startswith('wss://'):
                    # Disable trace for SSL to avoid interference
                    websocket.enableTrace(False)
                    
                    # Simplified and stable SSL configuration
                    import ssl
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    # Simplified SSL configuration for stability
                    sslopt = {
                        "cert_reqs": ssl.CERT_NONE,
                        "check_hostname": False
                    }
                    if self.debug:
                        print("🔒 SSL verification disabled for wss://")
                else:
                    # Disable trace for non-SSL connections
                    websocket.enableTrace(False)
                
                # Connect without authentication headers (Zebra WebSocket doesn't use them)
                if self.debug:
                    print(f"🔍 [DEBUG] Connecting without authentication headers")
                
                self.ws = websocket.WebSocketApp(
                    current_uri,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )
                
                # run_forever with appropriate SSL configuration
                # This will block until connection closes
                if sslopt is not None:
                    if self.debug:
                        print("[DEBUG] SSL options provided")
                    self.ws.run_forever(sslopt=sslopt)
                else:
                    if self.debug:
                        print("[DEBUG] No SSL options provided")
                    self.ws.run_forever()
                
                # If we get here, the connection was closed
                if self.stop_event.is_set():
                    break
                
                # Try next URI if available
                if uri_index < len(self.all_uris) - 1:
                    print(f"🔄 Trying next URI...")
                    time.sleep(1)  # Brief pause between attempts
                else:
                    print(f"❌ All {len(self.all_uris)} WebSocket URIs attempted without success")
                    break
                
            except Exception as e:
                print(f"❌ Exception during connection to {current_uri}: {e}")
                if uri_index < len(self.all_uris) - 1:
                    print(f"🔄 Trying next URI...")
                    time.sleep(1)  # Brief pause between attempts
                else:
                    print(f"❌ All {len(self.all_uris)} WebSocket URIs attempted without success")
                    break                 
        
    def is_connected(self):
        """Checks if the WebSocket connection is active."""
        return self._is_connected and self.ws is not None

    def close(self):
        """Forcibly closes the listener and WebSocket connection."""
        try:
            print("🔌 Terminating WebSocket listener...")
            
            # Stop CSV recording if active
            self._stop_csv_recording()
            
            self.stop_event.set()
            
            if self.ws:
                try:
                    self.ws.close()
                except Exception as e:
                    print(f"⚠️  Error closing WebSocket: {e}")
                    
            # Wait a bit to allow clean closure
            if self.is_alive():
                self.join(timeout=2.0)
                if self.is_alive():
                    print("⚠️  Listener not terminated within timeout")
                    
        except Exception as e:
            print(f"⚠️  Error during listener closure: {e}")

    def start_recording(self):
        """Starts the WebSocket listener event recording and CSV file creation."""
        if not self.ws_recorder_active:
            self.ws_recorder_active = True
            self._start_csv_recording()
        elif self.debug:
            print(f"[DEBUG][WebSocketListener] Recording already active")

    def stop_recording(self):
        """Stops the WebSocket listener event recording and closes CSV files."""
        if self.ws_recorder_active:
            self.ws_recorder_active = False
            self._stop_csv_recording()
        elif self.debug:
            print(f"[DEBUG][WebSocketListener] Recording already stopped")

    def _start_csv_recording(self):
        """Initializes CSV recording - messages file immediately, tags collected in memory"""
        try:
            # Create timestamp for filenames
            self._recording_timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Create directory structure if it doesn't exist
            messages_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'record', 'messages')
            os.makedirs(messages_dir, exist_ok=True)
            
            # Create messages filename with proper directory
            messages_filename = os.path.join(messages_dir, f"messages_read_{self._recording_timestamp}.csv")
            
            # Open messages CSV file
            self._csv_messages_file = open(messages_filename, 'w', newline='', encoding='utf-8')
            
            # Create messages CSV writer
            self._csv_messages_writer = csv.writer(self._csv_messages_file)
            
            # Write messages header
            self._csv_messages_writer.writerow(['Timestamp', 'Message_Type', 'Raw_JSON'])
            
            # Flush header to disk
            self._csv_messages_file.flush()
            
            # Initialize tag data collection
            self._recording_tags = {}
            self._recording_start_time = time.time()
            
            if self.debug:
                print(f"[DEBUG][WebSocketListener] CSV recording started: {messages_filename}")
                print(f"[DEBUG][WebSocketListener] Tag data collection started in memory")
            print(f"📝 CSV recording started: {messages_filename}")
            
            # Create tag reads directory for later use
            tags_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'record', 'tag_reads')
            os.makedirs(tags_dir, exist_ok=True)
            
            print(f"📊 Tag data collection started (will export to {os.path.join(tags_dir, f'tags_read_{self._recording_timestamp}.csv')} when stopped)")
            
        except Exception as e:
            print(f"❌ Failed to start CSV recording: {e}")
            self._stop_csv_recording()
    
    def _stop_csv_recording(self):
        """Closes CSV files and exports collected tag data"""
        try:
            # Export collected tag data to CSV before cleanup
            if self._recording_tags and self._recording_timestamp:
                self._export_tags_to_csv()

            # Close messages CSV
            if self._csv_messages_writer:
                self._csv_messages_writer = None
                
            if self._csv_messages_file:
                self._csv_messages_file.close()
                self._csv_messages_file = None
                
            if self._csv_messages_file or self._recording_tags:
                if self.debug:
                    print(f"[DEBUG][WebSocketListener] CSV recording stopped")
                print("📝 CSV recording stopped")
                
            # Clear recording data
            self._recording_tags = {}
            self._recording_start_time = None
            self._recording_timestamp = None
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Error stopping CSV recording: {e}")
    
    def _export_tags_to_csv(self):
        """Exports collected tag data to CSV file"""
        try:
            if not self._recording_tags or not self._recording_timestamp:
                return
                
            # Create tag reads directory and filename
            tags_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'record', 'tag_reads')
            os.makedirs(tags_dir, exist_ok=True)
            tags_filename = os.path.join(tags_dir, f"tags_read_{self._recording_timestamp}.csv")
            
            with open(tags_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header
                writer.writerow(['EPC', 'Reads', 'Avg_RSSI', 'Min_RSSI', 'Max_RSSI', 
                               'First_Seen', 'Last_Seen', 'Rate_Per_Minute'])
                
                # Data
                for epc, tag_data in self._recording_tags.items():
                    time_elapsed = tag_data.time_since_first
                    rate_per_minute = (tag_data.read_count / time_elapsed * 60) if time_elapsed > 0 else 0
                    rssi_min = min(tag_data.rssi_values) if tag_data.rssi_values else 0
                    rssi_max = max(tag_data.rssi_values) if tag_data.rssi_values else 0
                    
                    writer.writerow([
                        epc,
                        tag_data.read_count,
                        f"{tag_data.average_rssi:.1f}",
                        f"{rssi_min:.1f}",
                        f"{rssi_max:.1f}",
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tag_data.first_seen)),
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tag_data.last_seen)),
                        f"{rate_per_minute:.1f}"
                    ])
            
            total_tags = len(self._recording_tags)
            total_reads = sum(tag.read_count for tag in self._recording_tags.values())
            
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Exported {total_tags} tags with {total_reads} total reads to {tags_filename}")
            print(f"📊 Tag data exported: {tags_filename} ({total_tags} tags, {total_reads} reads)")
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Error exporting tags to CSV: {e}")
            print(f"❌ Error exporting tag data: {e}")

    def _write_message_to_csv(self, data):
        """Writes a message to the messages CSV file"""
        if not self._csv_messages_writer:
            return
            
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            message_type = data.get('type', 'UNKNOWN') if isinstance(data, dict) else 'RAW'
            raw_json = json.dumps(data) if isinstance(data, dict) else str(data)
            
            self._csv_messages_writer.writerow([timestamp, message_type, raw_json])
            self._csv_messages_file.flush()  # Ensure data is written immediately
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Error writing message to CSV: {e}")
    
    def _process_tag_data_for_recording(self, data):
        """Processes tag data for in-memory collection"""
        if self._recording_tags is None:  # Check if recording is not active
            return
        
        try:
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Processing tag data for recording: {data}")
                
            # Process data similar to TagTableWindow.process_data
            if isinstance(data, dict) and 'data' in data:
                tag_data = data['data']
                if isinstance(tag_data, dict) and 'idHex' in tag_data:
                    epc = tag_data['idHex']
                    rssi = tag_data.get('RSSI', tag_data.get('rssi', tag_data.get('peakRssi', tag_data.get('peakRSSI', 0))))

                    # Handle RSSI
                    try:
                        if rssi is None or rssi == 'N/A' or rssi == '':
                            rssi = -50.0
                        else:
                            rssi = float(rssi)
                    except (ValueError, TypeError):
                        rssi = -50.0
                    
                    # Extract extra data
                    extra_data = {}
                    if 'azimuth' in tag_data:
                        extra_data['azimuth'] = tag_data['azimuth']
                    if 'elevation' in tag_data:
                        extra_data['elevation'] = tag_data['elevation']
                    if 'antenna' in tag_data:
                        extra_data['antenna'] = tag_data['antenna']
                    
                    if self.debug:
                        print(f"[DEBUG][WebSocketListener] Updating tag {epc} with RSSI {rssi} and extra {extra_data}")
                    
                    # Add or update tag data
                    if epc in self._recording_tags:
                        self._recording_tags[epc].add_reading(rssi, extra_data)
                    else:
                        self._recording_tags[epc] = TagData(epc, rssi, extra_data)
                        
            elif isinstance(data, dict):
                # Handle direct tag data
                epc = data.get('epc', data.get('EPC', data.get('idHex', '')))
                if epc:
                    rssi = data.get('RSSI', data.get('rssi', data.get('peakRSSI', data.get('peakRssi', 0))))
                    
                    # Handle RSSI
                    try:
                        if rssi is None or rssi == 'N/A' or rssi == '':
                            rssi = -50.0
                        else:
                            rssi = float(rssi)
                    except (ValueError, TypeError):
                        rssi = -50.0
                    
                    # Extract extra data
                    extra_data = {}
                    for key in ['azimuth', 'elevation', 'antenna']:
                        if key in data:
                            extra_data[key] = data[key]
                    
                    # Handle multiple reads (from TagTableWindow)
                    reads = 1
                    if 'reads' in data:
                        try:
                            reads = int(data['reads'])
                            if reads < 1:
                                reads = 1
                        except Exception:
                            reads = 1
                    
                    if self.debug:
                        print(f"[DEBUG][WebSocketListener] Updating tag {epc} with RSSI {rssi}, reads={reads}, extra={extra_data}")
                    
                    # Add or update tag data
                    if epc in self._recording_tags:
                        self._recording_tags[epc].add_reading(rssi, extra_data, reads=reads)
                    else:
                        tag = TagData(epc, rssi, extra_data)
                        tag.read_count = reads
                        if reads > 1:
                            tag.rssi_values = [rssi] * reads
                        self._recording_tags[epc] = tag
                        
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Error processing tag data for recording: {e}")