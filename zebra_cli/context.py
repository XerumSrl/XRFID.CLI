import time
from zebra_cli.config import ConfigManager
from zebra_cli.websocket_listener import WebSocketListener
import httpx
from typing import Optional
import base64
import queue
import threading
import re

class ZebraRFIDClient:
    """Simplified client for the most important Zebra RFID APIs"""

    def __init__(self, base_url: str, token: str, debug: bool = False):
        self.base_url = base_url.rstrip('/')
        self.debug = debug
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        self.client = httpx.Client(
            verify=False,  # For self-signed certificates
            timeout=10.0
        )
    
    def start_scan(self):
        """Starts RFID tag scanning"""
        try:
            response = self.client.put(
                f"{self.base_url}/cloud/start",
                headers=self.headers
            )
            
            if response.status_code in [200, 201, 202]:
                return response.json() if response.content else {"status": "success"}
            elif response.status_code == 409:
                return {"status": "already_active"}
            else:
                print(f"❌ Start scan error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error starting scan: {e}")
            return None
    
    def stop_scan(self):
        """Stops RFID tag scanning"""
        try:
            response = self.client.put(
                f"{self.base_url}/cloud/stop",
                headers=self.headers
            )
            if response.status_code in [200, 201, 202]:
                return response.json() if response.content else {"status": "success"}
            elif response.status_code == 409:
                return {"status": "already_stopped"}
            else:
                print(f"❌ Stop scan error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error stopping scan: {e}")
            return None
    
    def get_status(self):
        """Gets the general reader status - more reliable for connection verification"""
        try:
            response = self.client.get(
                f"{self.base_url}/cloud/status",
                headers=self.headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json() if response.content else {"status": "unknown"}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print(f"❌ Error 401: Token not authorized")
                return None
            elif e.response.status_code == 403:
                print(f"❌ Error 403: Access denied")
                return None
            elif e.response.status_code == 404:
                print(f"⚠️  /status endpoint not found - possible different API")
                return {"status": "unknown"}
            elif e.response.status_code == 500:
                # Extract error message from JSON if available
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('message', 'Internal server error')
                    
                    if 'Authorization header missing' in error_msg:
                        print(f"🔐 Reader requires Bearer token authentication")
                        print(f"💡 Access the web interface to get a valid token")
                    elif 'jwt token signature verification failed' in error_msg:
                        print(f"❌ HTTP 500 Error: Invalid JWT token for this reader")
                        print(f"💡 Token was issued for another server. Possible solutions:")
                        print(f"   1. Get a valid token from the reader's web interface")
                        print(f"   2. Configure the reader to accept your issuer")
                        print(f"   3. Verify reader access credentials")
                    else:
                        print(f"❌ HTTP 500 Error: {error_msg}")
                except:
                    print(f"❌ HTTP 500 Error: {e.response.text}")
                return None
            else:
                print(f"❌ HTTP Error {e.response.status_code}: {e.response.text}")
                return None
        except httpx.TimeoutException:
            print(f"❌ Timeout during connection to {self.base_url}")
            return None
        except httpx.ConnectError:
            print(f"❌ Unable to connect to {self.base_url}")
            return None
        except Exception as e:
            print(f"❌ Error during status request: {e}")
            return None
    
    def get_bearer_token(self, username: str, password: str) -> Optional[str]:
        """
        Attempts to get a Bearer token from the Zebra reader using various methods.
        Args:
            username: Username for authentication
            password: Password for authentication
        Returns:
            str: Bearer token if successful, None if failed
        """
        # Method 1: Try standard REST endpoint
        token = self._try_rest_login(username, password)
        if token:
            return token
        # Method 2: Try web interface
        token = self._try_web_login(username, password)
        if token:
            return token
        # If all methods fail, return None
        return None

    def _try_rest_login(self, username: str, password: str) -> Optional[str]:
        """Attempts login via REST endpoint using Basic Authentication"""
        endpoints = [
                "/cloud/localRestLogin",  # Main Zebra endpoint
                "/auth/login", 
                "/login"
        ]        
        credentials = f"{username}:{password}"
        basic_auth_header = f"Basic {base64.b64encode(credentials.encode('utf-8')).decode('utf-8')}"
        
        for endpoint in endpoints:
            # GET with Basic Auth (main method for Zebra)
            try:
                response = httpx.get(
                    f"{self.base_url}{endpoint}",
                    headers={
                        "Authorization": basic_auth_header,
                        "Accept": "application/json"
                    },
                    verify=False,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        # Zebra puts JWT in the 'message' field
                        token = (data.get('token') or data.get('bearerToken') or 
                                data.get('access_token') or data.get('accessToken') or
                                data.get('jwt') or data.get('JWT') or
                                data.get('message'))
                        
                        if token and isinstance(token, str) and token.count('.') == 2:
                            return token
                    except Exception:
                        pass
            except Exception:
                pass
        return None
    
    def _try_web_login(self, username: str, password: str) -> Optional[str]:
        """Attempts to extract token from web interface"""
        try:
            # Access main page
            response = httpx.get(
                f"{self.base_url}/",
                verify=False,
                timeout=10.0,
                follow_redirects=True
            )
            
            if response.status_code != 200:
                return None
                
            content = response.text

            # Pattern for JWT tokens
            jwt_pattern = r'["\']([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)["\']'
            matches = re.findall(jwt_pattern, content)
            
            for match in matches:
                if len(match) > 50:  # JWTs are generally long
                    print(f"✅ Possible token found in web interface")
                    return match
                    
            # Look for token references in the page
            if 'token' in content.lower():
                print("🔍 Token mentioned in web interface, but not automatically extracted")
                
        except Exception:
            pass
            
        return None

    def get_version(self):
        """Gets the reader version information"""
        try:
            response = self.client.get(
                f"{self.base_url}/cloud/version",
                headers=self.headers,
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json() if response.content else {"version": "unknown"}
            else:
                print(f"❌ Version request error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting version: {e}")
            return None

    def close(self):
        """Closes the HTTP client."""
        if hasattr(self, 'client'):
            self.client.close()

    def get_mode(self):
        """Gets the current reader mode (if available)."""
        try:
            response = self.client.get(
                f"{self.base_url}/cloud/mode",
                headers=self.headers,
                timeout=10.0
            )
            if self.debug:
                print(f"🔍 Debug: GET {self.base_url}/cloud/mode -> Status: {response.status_code}")
            if response.status_code == 200:
                return response.json() if response.content else {"mode": "unknown"}
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Exception during get_mode: {e}")
            return None

    def set_mode(self, mode_config: dict):
        """Sets the reader's operating mode with the provided configuration"""
        try:
            response = self.client.put(
                f"{self.base_url}/cloud/mode",
                headers=self.headers,
                json=mode_config,
                timeout=10.0
            )
            if self.debug:
                print(f"🔍 Debug: PUT {self.base_url}/cloud/mode -> Status: {response.status_code}")
            if response.status_code in [200, 201, 202]:
                return response.json() if response.content else {"status": "success"}
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Exception during set_mode: {e}")
            return None

    def explore_endpoints(self):
        """Explores some common endpoints for reader configuration"""
        endpoints_to_try = [
            "/cloud/mode",
            "/cloud/config", 
            "/cloud/status",
            "/api/config",
            "/api/mode",
            "/config",
            "/mode",
            "/status",
            "/info"
        ]
        
        results = {}
        
        for endpoint in endpoints_to_try:
            try:
                response = self.client.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    timeout=10.0
                )
                
                if response.status_code in [200, 201, 202]:
                    try:
                        data = response.json() if response.content else None
                        results[endpoint] = {
                            "status": "success",
                            "status_code": response.status_code,
                            "data": data
                        }
                    except:
                        results[endpoint] = {
                            "status": "success",
                            "status_code": response.status_code,
                            "data": response.text[:200] if response.text else None
                        }
                else:
                    results[endpoint] = {
                        "status": "error",
                        "status_code": response.status_code,
                        "error": response.text[:100] if response.text else "Unknown error"
                    }
                    
            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "status_code": "N/A",
                    "error": str(e)[:100]
                }
        
        return results

class AppContext:
    """Manages the CLI application state."""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.config_manager = ConfigManager()
        self.ip_address = None
        self.token = None
        self.username = None  # Store last used username
        self.password = None  # Store last used password
        self.rest_client = None
        self.rest_client_http = None  # HTTP fallback client
        self.ws_uri = None
        self.ws_fallback_uris = []  # Fallback URIs for WebSocket
        self.protocol = "https"  # Default protocol
        self.preferred_protocol = None  # Protocol that worked - persists after login
        self.is_fxr90 = False  # Boolean flag to indicate if the connected reader is FXR90

        # Permanent WebSocket connection
        self.ws_listener = None
        self.ws_data_queue = None
        self.ws_stop_event = None

        # Load existing configuration if available
        self._load_existing_config()

    def _load_existing_config(self):
        """Loads existing configuration if available."""
        config = self.config_manager.load_config()
        if config:
            self.ip_address = config.get("ip_address")
            self.token = config.get("token")
            self.ws_uri = config.get("ws_uri")
            self.protocol = config.get("protocol", "https")
            self.preferred_protocol = config.get("preferred_protocol")  # Load persistent protocol
            # Recreate fallback URIs if we have IP (following Zebra directionality pattern)
            if self.ip_address:
                if self.protocol == "http":
                    ws_uris = [
                        f"ws://{self.ip_address}/ws",        # Primary: Built-in WebSocket server (HTTP default port)
                        f"ws://{self.ip_address}:80/ws",     # Fallback: Built-in WebSocket server (HTTP with explicit port 80)
                        f"wss://{self.ip_address}/ws",       # Fallback: Built-in WebSocket server (HTTPS)
                    ]
                else:
                    ws_uris = [
                        f"wss://{self.ip_address}/ws",       # Primary: Built-in WebSocket server (HTTPS)
                        f"ws://{self.ip_address}/ws",        # Fallback: Built-in WebSocket server (HTTP default port)
                        f"ws://{self.ip_address}:80/ws",     # Fallback: Built-in WebSocket server (HTTP with explicit port 80)
                    ]
                self.ws_uri = ws_uris[0]
                self.ws_fallback_uris = ws_uris[1:]
            if self.ip_address and self.token:
                if self.protocol == "http":
                    self.rest_client = ZebraRFIDClient(
                        base_url=f"http://{self.ip_address}",
                        token=self.token,
                        debug=self.debug
                    )
                else:
                    self.rest_client = ZebraRFIDClient(
                        base_url=f"https://{self.ip_address}",
                        token=self.token,
                        debug=self.debug
                    )
                
                # Create HTTP fallback client
                self.rest_client_http = ZebraRFIDClient(
                    base_url=f"http://{self.ip_address}",
                    token=self.token,
                    debug=self.debug
                )
                
                print("✅ Configuration loaded - use WebSocket options (w, m, p) to start monitoring")
    
    def connect(self, ip: str, token: str):
        """
        Establishes connection with the Zebra RFID reader.
        
        Args:
            ip: IP address of the RFID reader
            token: Bearer token for REST API authentication
            
        Raises:
            ValueError: If token is invalid or connection fails
            ConnectionError: If reader is unreachable
        """
        
        # Try HTTPS first (more common for Zebra), then HTTP as fallback
        connection_successful = False
        used_protocol = None
        
        for protocol in ["https", "http"]:
            base_url = f"{protocol}://{ip}"
            
            # Create temporary client to test connection
            temp_client = ZebraRFIDClient(base_url=base_url, token=token, debug = self.debug)
            
            try:
                print(f"🔍 Attempting {protocol.upper()} connection...")
                
                # Try to get general status first (more reliable)
                result = temp_client.get_status()
                
                # If it fails, try get_mode as fallback
                if result is None:
                    print(f"🔄 Trying mode endpoint on {protocol.upper()}...")
                    result = temp_client.get_mode()
                
                if result is not None:
                    print(f"✅ {protocol.upper()} connection successful!")
                    connection_successful = True
                    used_protocol = protocol
                    temp_client.close()
                    break
                    
            except Exception as e:
                print(f"❌ {protocol.upper()} connection failed: {e}")
                
            temp_client.close()
        
        if not connection_successful:
            raise ConnectionError("❌ Invalid token or reader unreachable on HTTP/HTTPS")
        
        # Save credentials
        self.ip_address = ip
        self.token = token
        self.protocol = used_protocol
        self.preferred_protocol = used_protocol  # Remember the protocol that worked
        
        # Configure WebSocket URIs based on the protocol that worked
        # Following Zebra directionality.html pattern: connect to built-in /ws endpoint only
        # Try default port first (no explicit port specification)
        if used_protocol == "http":
            ws_uris = [
                f"ws://{ip}/ws",             # Primary: Built-in WebSocket server (HTTP default port)
                f"ws://{ip}:80/ws",          # Fallback: Built-in WebSocket server (HTTP with explicit port 80)
                f"wss://{ip}/ws",            # Fallback: Built-in WebSocket server (HTTPS)
            ]
        else:
            ws_uris = [
                f"wss://{ip}/ws",            # Primary: Built-in WebSocket server (HTTPS)
                f"ws://{ip}/ws",             # Fallback: Built-in WebSocket server (HTTP default port)
                f"ws://{ip}:80/ws",          # Fallback: Built-in WebSocket server (HTTP with explicit port 80)
            ]
        
        self.ws_uri = ws_uris[0]
        self.ws_fallback_uris = ws_uris[1:]
        
        print(f"🔗 WebSocket configured: {self.ws_uri}")
        if self.debug:
            print(f"[DEBUG] connect_and_authenticate - Using Zebra directionality pattern: built-in /ws endpoint")
            print(f"[DEBUG] connect_and_authenticate - WebSocket URIs: {ws_uris}")
        
        # Save configuration to disk with persistent protocol
        config_data = {
            "ip_address": ip,
            "token": token,
            "protocol": used_protocol,
            "preferred_protocol": used_protocol,
            "ws_uri": self.ws_uri
        }
        self.config_manager.save_config_dict(config_data)
        
        # Create REST clients (main HTTPS + HTTP fallback)
        self.rest_client = ZebraRFIDClient(
            base_url=f"{used_protocol}://{ip}",
            token=token,
            debug=self.debug
        )
        
        # Always create HTTP client for scan operations
        self.rest_client_http = ZebraRFIDClient(
            base_url=f"http://{ip}",
            token=token,
            debug=self.debug
        )
        
        print("✅ Connection established - use WebSocket options (7, 8, 9, t) to start monitoring")

    def disconnect(self):
        """Removes connection configuration and closes permanent WebSocket."""
        # Close permanent WebSocket if running
        self.stop_websocket()
        
        if self.rest_client:
            self.rest_client.close()
        if self.rest_client_http:
            self.rest_client_http.close()
        
        self.ip_address = None
        self.token = None
        self.rest_client = None
        self.rest_client_http = None
        self.ws_uri = None
        self.ws_fallback_uris = []
        self.config_manager.clear_config()

    def login_and_connect(self, ip: str, username: str, password: str) -> bool:
        """
        Performs automatic login and connection to Zebra reader with protocol persistence.
        
        Args:
            ip: Reader IP address
            username: Username
            password: Password
            
        Returns:
            bool: True if login and connection successful, False otherwise
        """
        # Use preferred protocol if available, otherwise try both
        protocols_to_try = []
        if self.preferred_protocol:
            # Use ONLY the protocol that worked previously
            protocols_to_try = [self.preferred_protocol]
        else:
            # First time: try HTTPS then HTTP
            protocols_to_try = ["https", "http"]
        
        for protocol in protocols_to_try:
            base_url = f"{protocol}://{ip}"
            
            try:
                # Create temporary client for login
                client = ZebraRFIDClient(base_url, "dummy-token", debug=self.debug)
                token = client.get_bearer_token(username, password)
                client.close()
                
                if token:
                    # Immediately connect after getting token
                    try:
                        self._connect_with_protocol(ip, token, protocol)
                        # Save the credentials and protocol that worked
                        self.username = username
                        self.password = password
                        self.preferred_protocol = protocol
                        
                        # Get device version information to check if it's FXR90
                        try:
                            if self.rest_client:  # Type guard to ensure rest_client exists
                                version_data = self.rest_client.get_version()
                                
                                if version_data:
                                    model = version_data.get("model", "").upper()
                                    
                                    if model == "FXR90":
                                        self.is_fxr90 = True
                                        print(f"✅ Detected FXR90 reader (Model: {model})")
                                    else:
                                        self.is_fxr90 = False
                                        print(f"ℹ️  Detected {model} reader (not FXR90)")
                                        
                                    if self.debug:
                                        print(f"[DEBUG] Version info: {version_data}")
                                else:
                                    print(f"⚠️  Could not retrieve version info")
                                    self.is_fxr90 = False
                            else:
                                self.is_fxr90 = False
                                
                        except Exception as e:
                            print(f"⚠️  Error getting version info: {e}")
                            self.is_fxr90 = False
                        
                        print("✅ Login successful")
                        return True
                        
                    except Exception as e:
                        continue
                        
            except Exception as e:
                if not self.preferred_protocol:
                    # Only on first time show protocol errors
                    continue
                else:
                    # If we have a preferred protocol and it fails, show error
                    print(f"❌ Error during login: {e}")
                    break
        
        # If all protocols fail, show manual guide
        if not self.preferred_protocol:
            # Only if it's the first time, show guide for HTTPS
            print()
            print("💡 Example: python main.py connect --ip [IP] --token [TOKEN]")
            print()
        
        return False

    def get_client(self):
        """
        Returns the authenticated REST client.
        
        Returns:
            The authenticated REST client
            
        Raises:
            ValueError: If connection has not been established
        """
        if self.rest_client is None:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        return self.rest_client
    
    def get_ws_uri(self):
        """
        Returns the WebSocket URI.
        
        Returns:
            The WebSocket URI
            
        Raises:
            ValueError: If connection has not been established
        """
        if self.ws_uri is None:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        return self.ws_uri
    
    def is_connected(self):
        """Checks if a connection has been established."""
        return self.rest_client is not None
    
    def get_stored_credentials(self):
        """
        Returns the stored username and password from last successful login.
        
        Returns:
            tuple: (username, password) or (None, None) if not available
        """
        return (self.username, self.password)
    
    # Convenience methods for most common operations
    def start_scan(self):
        """Starts RFID tag scanning."""
        if not self.rest_client:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        
        # If reader FXR90 try HTTPS directly
        if self.is_fxr90:
            result = self.rest_client.start_scan()
            if result:
                return result
        else:
            # Try HTTP first (works better for scan operations)
            if self.rest_client_http:
                result = self.rest_client_http.start_scan()
                if result:
                    return result
            
            # Fallback to HTTPS if HTTP doesn't work
            return self.rest_client.start_scan()
    
    def stop_scan(self):
        """Stops RFID tag scanning."""
        if not self.rest_client:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        
        # If reader FXR90 try HTTPS directly
        if self.is_fxr90:
            result = self.rest_client.stop_scan()
            if result:
                return result
        else:
            # Try HTTP first (works better for scan operations)
            if self.rest_client_http:
                result = self.rest_client_http.stop_scan()
                if result:
                    return result
            
            # Fallback to HTTPS if HTTP doesn't work
            result = self.rest_client.stop_scan()
            if result:
                return result
    
    def get_mode(self):
        """Gets the current reader mode."""
        if not self.rest_client:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        
        return self.rest_client.get_mode()

    def set_mode(self, mode_config: dict):
        """Sets the reader's operating mode with the provided configuration"""
        if not self.rest_client:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        
        return self.rest_client.set_mode(mode_config)

    def explore_endpoints(self):
        """Explores available endpoints for reader configuration"""
        if not self.rest_client:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        
        return self.rest_client.explore_endpoints()
    
    def get_status(self):
        """
        Returns the general reader status (proxy to ZebraRFIDClient.get_status).
        Useful to know if the radio is active (radioActivity field).
        """
        if not self.rest_client:
            raise ValueError('Connection not established. Please run the "connect" command first.')
        return self.rest_client.get_status()
    
    def _connect_with_protocol(self, ip: str, token: str, protocol: str):
        """
        Simplified connection with specific protocol without get_mode.
        
        Args:
            ip: Reader IP address
            token: Bearer token for authentication
            protocol: Protocol to use ('http' or 'https')
        """
        # Save credentials
        self.ip_address = ip
        self.token = token
        self.protocol = protocol
        
        # Configure WebSocket URIs based on protocol
        # Following Zebra directionality.html pattern: connect to built-in /ws endpoint only
        # Try default port first (no explicit port specification)
        if protocol == "http":
            ws_uris = [
                f"ws://{ip}/ws",             # Primary: Built-in WebSocket server (HTTP default port)
                f"ws://{ip}:80/ws",          # Fallback: Built-in WebSocket server (HTTP with explicit port 80)
                f"wss://{ip}/ws",            # Fallback: Built-in WebSocket server (HTTPS)
            ]
        else:
            ws_uris = [
                f"wss://{ip}/ws",            # Primary: Built-in WebSocket server (HTTPS)
                f"ws://{ip}/ws",             # Fallback: Built-in WebSocket server (HTTP default port)
                f"ws://{ip}:80/ws",          # Fallback: Built-in WebSocket server (HTTP with explicit port 80)
            ]
        
        self.ws_uri = ws_uris[0]
        self.ws_fallback_uris = ws_uris[1:]
        
        # Save configuration to disk
        config_data = {
            "ip_address": ip,
            "token": token,
            "protocol": protocol,
            "preferred_protocol": protocol,
            "ws_uri": self.ws_uri
        }
        self.config_manager.save_config_dict(config_data)
        
        # Create REST clients
        self.rest_client = ZebraRFIDClient(
            base_url=f"{protocol}://{ip}",
            token=token,
            debug=self.debug
        )
        
        # Always create HTTP client for scan operations
        self.rest_client_http = ZebraRFIDClient(
            base_url=f"http://{ip}",
            token=token,
            debug=self.debug
        )

    # Permanent WebSocket management methods
    def start_websocket(self, debug: bool = False):
        """
        Starts the permanent WebSocket connection.
        
        Args:
            debug: Whether to enable debug logging for WebSocket messages
        """
        # Force reset if any WebSocket components exist (handle stuck connections)
        if self.ws_listener or self.ws_data_queue or self.ws_stop_event:
            print("🔄 Detected existing WebSocket state, force resetting...")
            self.force_reset_websocket()
            
        if not self.is_connected():
            raise ValueError('Connection not established. Please run the "connect" command first.')
        
        # Initialize WebSocket components
        if self.ws_data_queue is None:
            self.ws_data_queue = queue.Queue()
        if self.ws_stop_event is None:
            self.ws_stop_event = threading.Event()
        else:
            self.ws_stop_event.clear()
        
        # Start WebSocket listener
        ws_uri = self.get_ws_uri()
        
        self.ws_listener = WebSocketListener(
            ws_uri, 
            self.ws_data_queue, 
            self.ws_stop_event,
            fallback_uris=self.ws_fallback_uris,
            debug=debug
        )
        
        self.ws_listener.start()
    
    def stop_websocket(self):
        """Stops the permanent WebSocket connection."""
        print("🔌 Stopping WebSocket connection...")

        # Set the stop event first to prevent reconnections
        if self.ws_stop_event:
            self.ws_stop_event.set()
        
        # Force close the WebSocket connection if it exists
        if self.ws_listener and hasattr(self.ws_listener, 'ws') and self.ws_listener.ws:
            try:
                print("🔌 Closing WebSocket connection...")
                self.ws_listener.ws.close()
            except Exception as e:
                print(f"⚠️  Error closing WebSocket: {e}")
        
        # Wait for the listener thread to stop
        if self.ws_listener and self.ws_listener.is_alive():
            print("⏳ Waiting for WebSocket listener to stop...")
            self.ws_listener.join(timeout=5.0)  # Increased timeout
            if self.ws_listener.is_alive():
                print("⚠️  WebSocket listener did not stop within timeout")
        
        # Reset WebSocket components
        self.ws_listener = None
        self.ws_data_queue = None
        self.ws_stop_event = None
        
        print("✅ WebSocket stopped and cleaned up")
    
    def force_reset_websocket(self):
        """Forces complete reset of all WebSocket components - use when connection is stuck."""
        print("💥 Force resetting WebSocket state...")
        
        # Force kill any existing threads
        if self.ws_listener:
            try:
                if hasattr(self.ws_listener, 'ws') and self.ws_listener.ws:
                    self.ws_listener.ws.close()
            except:
                pass
            
            # Don't wait for graceful shutdown, just reset
            self.ws_listener = None
        
        # Clear all WebSocket state
        self.ws_data_queue = None
        self.ws_stop_event = None
        
        # Small delay to let server-side connections timeout
        import time
        time.sleep(2)
        
        print("💥 WebSocket state force reset complete")

    def ensure_websocket_running(self, debug=False):
        """
        Ensures the permanent WebSocket connection is running.
        This method guarantees that the WebSocket listener is active and 
        continuously filling the data queue with incoming messages.
        
        Args:
            debug: Whether to enable debug logging for WebSocket messages
            
        Returns:
            queue.Queue: The WebSocket data queue for reading messages
        """

        wb_running = self.is_websocket_running()

        if not wb_running:
            if self.debug:
                print(f"[DEBUG] ensure_websocket_running - Starting WebSocket (not running)")            
            self.start_websocket(debug=debug)
        else:            
            if self.debug:
                print(f"[DEBUG] ensure_websocket_running - WebSocket already running, reusing connection")
        
        # Always return the same queue instance for all monitoring commands
        # This queue is continuously filled by the permanent WebSocket listener
      
        self.clear_websocket_buffer(wb_running)

        return self.ws_data_queue
    
    def is_websocket_running(self):
        """Checks if the permanent WebSocket is running and connected."""
        if self.ws_listener:
            # Check both if thread is alive AND if WebSocket connection is active
            return self.ws_listener.is_alive() and self.ws_listener.is_connected()
        return False
    
    def get_websocket_status(self):
        """Returns detailed WebSocket status for debugging."""
        # Safely get WebSocket URI without throwing exceptions
        try:
            configured_uri = self.get_ws_uri() if hasattr(self, 'ws_uri') else None
        except ValueError:
            configured_uri = None
            
        status = {
            'is_running': self.is_websocket_running(),
            'thread_alive': self.ws_listener.is_alive() if self.ws_listener else False,
            'websocket_connected': self.ws_listener.is_connected() if self.ws_listener else False,
            'configured_uri': configured_uri,
            'listener_uri': getattr(self.ws_listener, 'uri', None) if self.ws_listener else None,
            'queue_size': self.ws_data_queue.qsize() if self.ws_data_queue else 0,
            'debug_mode': self.debug
        }
        return status
    
    def get_websocket_data(self):
        """
        Gets data from the permanent WebSocket queue.
        
        Returns:
            Tag data from the WebSocket queue, or None if no data available
        """
        if not self.ws_data_queue:
            return None
        
        try:
            return self.ws_data_queue.get_nowait()
        except queue.Empty:
            return None
    
    def is_fxr90_reader(self) -> bool:
        """
        Returns whether the connected reader is an FXR90 model.
        
        Returns:
            bool: True if the reader is FXR90, False otherwise
        """
        return self.is_fxr90
    
    def clear_websocket_buffer(self, wb_running):
        """
        Clears any old data from the WebSocket queue.
        Useful when starting monitoring to avoid showing stale buffered data.
        """
        if not self.ws_data_queue:
            return

        # Wait if the last message in the queue is too old
        import datetime, sys
        diff = 100
        print("Checking for retained messages to clear...")
        print("Press ENTER to interrupt waiting and continue after next clear...")
        
        while diff > 6:
            if not wb_running:
                time.sleep(5)
            # Check for user input (non-blocking)
            user_break = False
            try:
                if sys.platform == 'win32':
                    import msvcrt
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key in [b'\r', b'\n']:
                            print("⏩ Forced exit from waiting loop by user request (ENTER)")
                            user_break = True
                else:
                    import select
                    if select.select([sys.stdin], [], [], 0)[0]:
                        line = sys.stdin.readline()
                        if line.strip() == '':
                            print("⏩ Forced exit from waiting loop by user request (ENTER)")
                            user_break = True
            except Exception:
                pass
            if user_break:
                break
            
            try:
                last_msg = self.ws_data_queue.queue[0]
                msg_ts = None
                if isinstance(last_msg, dict):
                    msg_ts = last_msg.get('timestamp')
                    if not msg_ts and 'data' in last_msg and isinstance(last_msg['data'], dict):
                        msg_ts = last_msg['data'].get('timestamp')
                if msg_ts:
                    try:
                        # Normalize msg_time to UTC
                        msg_time = None
                        if isinstance(msg_ts, str):
                            # ISO8601 con/without Z
                            try:
                                if msg_ts.endswith('Z'):
                                    msg_time = datetime.datetime.fromisoformat(msg_ts.replace('Z', '+00:00')).astimezone(datetime.timezone.utc)
                                else:
                                    msg_time = datetime.datetime.fromisoformat(msg_ts)
                                    if msg_time.tzinfo:
                                        msg_time = msg_time.astimezone(datetime.timezone.utc)
                                    else:
                                        msg_time = msg_time.replace(tzinfo=datetime.timezone.utc)
                            except Exception:
                                # Try as float epoch
                                msg_time = datetime.datetime.fromtimestamp(float(msg_ts), tz=datetime.timezone.utc)
                        elif isinstance(msg_ts, (float, int)):
                            msg_time = datetime.datetime.fromtimestamp(float(msg_ts), tz=datetime.timezone.utc)
                        elif isinstance(msg_ts, datetime.datetime):
                            msg_time = msg_ts.astimezone(datetime.timezone.utc) if msg_ts.tzinfo else msg_ts.replace(tzinfo=datetime.timezone.utc)
                        else:
                            print(f"⚠️  Invalid timestamp format: {msg_ts}")
                            break

                        # Current time in UTC
                        now_utc = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

                        print(f"   🕒 Last message timestamp (UTC): {msg_time}")
                        print(f"   ⏳ Current time (UTC): {now_utc}")

                        try:
                            diff = (now_utc - msg_time).total_seconds()
                        except Exception as e:
                            print(f"⚠️  Error computing time diff: {e}")
                            break

                        print(f"   ⏳ Last message was {diff:.1f}s ago")
                        if diff > 1:
                            print(f"⏳ Waiting for fresh WebSocket data")
                            cleared_count = 0
                            try:
                                while True:
                                    self.ws_data_queue.get_nowait()
                                    cleared_count += 1
                            except queue.Empty:
                                pass
                            if cleared_count > 0:
                                print(f"🗑️  Cleared {cleared_count} old buffered messages")                               
                    except Exception:
                        print(f"⚠️  Error processing last message timestamp: {msg_ts}")
                        pass
            except Exception:
                print(f"⚠️  Error checking last WebSocket message timestamp, clearing buffer\n")
                break