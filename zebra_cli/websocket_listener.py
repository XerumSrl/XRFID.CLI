import threading
import websocket
import json
import queue
import time
from typing import Optional

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
                            if tag_data and self.debug:
                                tag_id = tag_data.get('idHex', 'N/A')
                                azimuth = tag_data.get('azimuth', 'N/A')
                                elevation = tag_data.get('elevation', 'N/A')
                                timestamp = data.get('timestamp', 'N/A')
                                print(f"[DEBUG][WebSocketListener] RAW_DIR: {tag_id} (Az: {azimuth}°, El: {elevation}°) | ⏰ {timestamp}")
                        else:
                            msg_type = data.get('type', 'UNKNOWN')
                            if self.debug:
                                print(f"[DEBUG][WebSocketListener] Message type: {msg_type} | Data: {str(data)[:100]}...")
                    self.data_queue.put(data)
                    self._last_data_time = time.time()

                except json.JSONDecodeError as e:
                    if self.debug:
                        print(f"[DEBUG][WebSocketListener] Invalid JSON: {json_msg[:30]}...")
                    self.data_queue.put({"raw_message": json_msg, "error": str(e)})
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][WebSocketListener] Processing error: {e}")
            print(f"⚠️  Processing error: {e}")
            self.data_queue.put({"raw_message": message, "error": str(e)})

    def on_error(self, ws, error):
        """Callback for error handling."""
        error_str = str(error)
        current_uri = self.all_uris[self.current_uri_index]
        
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
                    print("[DEBUG] SSL options provided")
                    self.ws.run_forever(sslopt=sslopt)
                else:
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