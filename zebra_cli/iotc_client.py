import sys
import requests
import urllib3
import xml.etree.ElementTree as ET
import json
from typing import Optional, Dict, Any

class IoTCException(Exception):
        """Exception specific to IOTC problems"""
        pass
    
class InvalidSessionException(IoTCException):
    """Exception for invalid sessions"""
    pass

class ZebraIoTCClient:
    """Client for Zebra RFID IoT Connector operations (shared for all steps)"""
    
    def __init__(self, protocol: str = "http", debug: bool = False, ip_address: str = "192.168.2.54"):
        self.ip_address = ip_address
        self.base_url = f"{protocol}://{ip_address}"
        self.control_url = f"{self.base_url}/control"
        self.debug = debug
        self.cmd_header = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<rm:command epcglobal:creationDate="2001-12-17T09:30:47.0Z" '
            'epcglobal:schemaVersion="0.0" '
            'xsi:schemaLocation="urn:epcglobal:rm:xsd:1 ../../../schemas/RmCommand.xsd" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:rm="urn:epcglobal:rm:xsd:1" '
            'xmlns:epcglobal="urn:epcglobal:xsd:1" '
            'xmlns:motorm="urn:motorfid:rm:xsd:1">'
        )
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def xml_login(self, username: str, password: str) -> Optional[str]:
        login_command = (
            f"{self.cmd_header}"
            f"<rm:id>99</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:doLogin>"
            f"<motorm:username>{username}</motorm:username>"
            f"<motorm:password>{password}</motorm:password>"
            f"<motorm:forceLogin>true</motorm:forceLogin>"
            f"</motorm:doLogin>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        try:
            response = requests.post(
                self.control_url,
                data=login_command,
                headers={'Content-Type': 'application/xml'},
                timeout=60,
                verify=False
            )
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                session_elements = root.findall('.//motorm:sessionID', 
                    namespaces={'motorm': 'urn:motorfid:rm:xsd:1'})
                if session_elements:
                    session_id = session_elements[0].text
                    if self.debug:
                        print(f"[DEBUG] XML Login successful, session ID: {session_id}")
                    else:
                        print(f"✅ XML Login successful, session ID: {session_id}")
                    return session_id
                else:
                    print("❌ XML Login failed: No session ID in response")
                    return None
            else:
                print(f"❌ XML Login failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ XML Login error: {e}")
            return None
        
    def test_enroll_reader(self):
        """Test function for enrollReader functionality"""
        print("🧪 TESTING: enrollReader() - Step 6")
        print("=" * 50)
        
        # Test configuration
        reader_ip = "192.168.2.54"
        username = "admin"
        password = "Password01!"
        
        client = ZebraIoTCClient(ip_address=reader_ip)
        
        # Step 1: Login
        print("1️⃣ Performing XML login...")
        session_id = client.xml_login(username, password)
        
        if not session_id:
            print("❌ Cannot proceed without valid session ID")
            return False
        
        # Step 2: Enroll reader
        print("\n2️⃣ Enrolling reader to IoT Connector...")
        result = client.enroll_reader(session_id)
        
        print(f"\n📊 ENROLLMENT RESULT: {'✅ SUCCESS' if result else '❌ FAILED'}")
        
        if result:
            print("📝 Reader is now enrolled to IoT Connector with auto-connect enabled")
            print("💡 The reader should automatically connect to IOTC after enrollment")
        else:
            print("📝 Enrollment failed - check reader configuration and credentials")
    
        return result

    def enroll_reader(self, session_id: str) -> bool:
        enroll_command = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:enrollToCloud>"
            f"<motorm:provider>2</motorm:provider>"
            f"<motorm:code>xxx</motorm:code>"
            f"<motorm:autoConnect>true</motorm:autoConnect>"
            f"</motorm:enrollToCloud>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        try:
            response = requests.post(
                self.control_url,
                data=enroll_command,
                headers={'Content-Type': 'application/xml'},
                timeout=60,
                verify=False
            )
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                result_elements = root.findall('.//g1:resultCode', 
                    namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                if result_elements:
                    result_code = result_elements[0].text
                    if result_code == "0":
                        print("✅ Reader enrolled to IoT Connector successfully")
                        return True
                    elif result_code == "65535":
                        error_desc = root.findall('.//g1:description', 
                            namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                        if error_desc and error_desc[0].text and "already enrolled" in error_desc[0].text.lower():
                            print("✅ Reader is already enrolled to IoT Connector")
                            return True
                        else:
                            error_msg = error_desc[0].text if error_desc and error_desc[0].text else "Unknown error"
                            print(f"❌ Reader enrollment failed: {error_msg}")
                            return False
                    else:
                        print(f"❌ Reader enrollment failed with result code: {result_code}")
                        error_elements = root.findall('.//g1:description', 
                            namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                        if error_elements:
                            print(f"   Error message: {error_elements[0].text}")
                        return False
                else:
                    print("❌ Could not parse enrollment response")
                    return False
            else:
                print(f"❌ Enrollment request failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Reader enrollment error: {e}")
            return False

    def _parse_xml_response(self, xml_data: str) -> ET.Element:
        """
        Parses the XML response from the reader.
        """
        try:
            return ET.fromstring(xml_data)
        except ET.ParseError as e:
            raise IoTCException(f"XML parsing error: {e}")
    
    def _get_xml_text(self, root: ET.Element, tag: str) -> Optional[str]:
        """
        Extracts text from an XML tag, handling namespaces.
        """
        namespaces = {
            'g1': 'urn:epcglobal:rm:xsd:1',
            'g2': 'urn:epcglobal:xsd:1', 
            'g3': 'urn:motorfid:rm:xsd:1'
        }
        
        elements = root.findall(f".//{tag}", namespaces)
        if elements and elements[0].text is not None:
            return elements[0].text.strip()
        return None
    
    def is_reader_enrolled(self, session_id: str) -> bool:
        """
        Checks if the reader is already enrolled to the IOTC cloud.
        """
        # Exact replica of the JavaScript XML command
        get_cloud_enrollment_status = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:isEnrolledToCloud/>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            # Replica of the JavaScript fetch call
            response = requests.post(
                self.control_url,
                data=get_cloud_enrollment_status,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=120  # Aggiunto timeout ragionevole
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}")

            # Parse the XML response
            root = self._parse_xml_response(response.text)
            
            # Replica of the JavaScript logic: check resultCode
            result_code = self._get_xml_text(root, "g1:resultCode")
            if self.debug:
                print(f"[DEBUG] resultCode length= {1 if result_code else 0}")
            
            if result_code == "0":
                # Check isEnrolled
                is_enrolled = self._get_xml_text(root, "g3:isEnrolled")
                if is_enrolled == "true":
                    if self.debug:
                        print("[DEBUG] device already enrolled.")
                    return True
                else:
                    if self.debug:
                        print("[DEBUG] device not enrolled")
                    return False
            else:
                # Handle invalid session error (replica of JavaScript logic)
                description = self._get_xml_text(root, "g1:description")
                if (description and 
                    "Not active session. Cannot process request ( Invalid session Id )" in description):
                    raise InvalidSessionException("Invalid Session")

                if self.debug:
                    print("[DEBUG] device not enrolled")
                return False
                
        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")

    def get_endpoint_mapping(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets the current endpoint mapping (needed for mapWSEP and mapMQTTEP).
        """
        if self.debug:
            print("[DEBUG] Getting current endpoint mapping..")

        # Command to get the current mapping
        mapping_cmd = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:cloudEndpointsMapping>"
            f"<motorm:operation>VIEW</motorm:operation>"
            f"<motorm:data></motorm:data>"
            f"</motorm:cloudEndpointsMapping>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            response = requests.post(
                self.control_url,
                data=mapping_cmd,
                headers={'Content-Type': 'application/xml'},
                timeout=60
            )
            
            if response.status_code == 200:
                root = self._parse_xml_response(response.text)
                result_code = self._get_xml_text(root, "g1:resultCode")
                
                if result_code == "0":
                    data_text = self._get_xml_text(root, "g3:data")
                    if data_text:
                        ep_mapping = json.loads(data_text)
                        self.ep_mapping = ep_mapping
                        return ep_mapping
            
            return None
            
        except Exception as e:
            print(f"Error getting endpoint mapping: {e}")
            return None

    def get_all_endpoints(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the complete list of available endpoints via manageCloudEndpoints (operation: VIEW).
        """
        if self.debug:
            print("[DEBUG] Getting all available endpoints (manageCloudEndpoints)...")

        endpoints_cmd = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:manageCloudEndpoints>"
            f"<motorm:operation>VIEW</motorm:operation>"
            f"<motorm:data></motorm:data>"
            f"</motorm:manageCloudEndpoints>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )

        try:
            response = requests.post(
                self.control_url,
                data=endpoints_cmd,
                headers={'Content-Type': 'application/xml'},
                timeout=60
            )
            if response.status_code == 200:
                root = self._parse_xml_response(response.text)
                result_code = self._get_xml_text(root, "g1:resultCode")
                if result_code == "0":
                    data_text = self._get_xml_text(root, "g3:data")
                    if data_text:
                        endpoints = json.loads(data_text)
                        if self.debug:
                            print(f"[DEBUG] All endpoints loaded: {endpoints}")
                        return endpoints
            if self.debug:
                print("[DEBUG] Failed to get all endpoints")
            return None
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Error getting all endpoints: {e}")
            return None
        
    def is_iotc_connected(self, session_id: str) -> bool:
        """
        Check if the reader is connected to IoT Connector using isConnectedToCloud command.
        """
        print("🔍 Checking IoT Connector connection status...")
        
        if not session_id:
            print("❌ No valid session ID provided")
            return False
            
        # Build the isConnectedToCloud command exactly like JavaScript
        is_connected_command = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:isConnectedToCloud/>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            print("📡 Sending isConnectedToCloud command...")
            response = requests.post(
                self.control_url,
                data=is_connected_command,
                headers={'Content-Type': 'application/xml'},
                timeout=60,
                verify=False
            )
            
            if response.status_code == 200:
                print("📋 Parsing connection response...")
                root = ET.fromstring(response.text)
                
                # Check result code first (like JavaScript)
                result_code_elements = root.findall('.//g1:resultCode', 
                    namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                
                if result_code_elements and result_code_elements[0].text == "0":
                    print("✅ Command executed successfully")
                    
                    # Look for g3:isConnected element (like JavaScript)
                    # Need to find the correct namespace for g3
                    for elem in root.iter():
                        if 'isConnected' in elem.tag:
                            status = elem.text.strip() if elem.text else ""
                            print(f"🔗 Connection status found: '{status}'")
                            
                            if status.lower() == 'true':
                                print("✅ Reader is connected to IoT Connector")
                                return True
                            elif status.lower() == 'false':
                                print("❌ Reader is not connected to IoT Connector")
                                return False
                    
                    print("⚠️ No isConnected element found in successful response")
                    print(f"📝 Raw response: {response.text}")
                    return False
                else:
                    print("❌ Command failed or returned error")
                    print(f"📝 Raw response: {response.text}")
                    return False
            else:
                print(f"❌ HTTP error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking IOTC connection: {e}")
            return False

    def connect_iotc(self, session_id: str) -> bool:
        """
        Connect the reader to IoT Connector.
        
        This function initiates a connection to the IoT Connector cloud service.
        """
        print("🔄 Connecting reader to IoT Connector...")
        print("⏳ This may take a few minutes, please wait...")
        
        connect_command = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName>MyFX9600</rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:connectToCloud/>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )

        try:
            response = requests.post(
                self.control_url,
                data=connect_command,
                headers={'Content-Type': 'application/xml'},
                timeout=600,  # 10 minutes timeout for cloud connection
                verify=False
            )
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                
                # Check result code
                result_elements = root.findall('.//g1:resultCode', 
                    namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                
                if result_elements and result_elements[0].text == "0":
                    print("✅ Reader connected to IoT Connector successfully")
                    return True
                else:
                    result_code = result_elements[0].text if result_elements else "Unknown"
                    print(f"❌ Reader connection failed with result code: {result_code}")
                    
                    # Try to get additional error information
                    error_elements = root.findall('.//g1:description', 
                        namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                    if error_elements:
                        print(f"   Error message: {error_elements[0].text}")
                    
                    return False
            else:
                print(f"❌ Connection request failed with status code: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("⏰ Connection request timed out - this may be normal for cloud connections")
            print("ℹ️ Check reader status manually to verify connection")
            return False
        except Exception as e:
            print(f"❌ IoT Connector connection error: {e}")
            return False
  
    def disconnect_iotc(self, session_id: str) -> bool:
        """
        Disconnect the reader from IoT Connector.
        
        This function stops the connection to the IoT Connector cloud service.
        This operation may take several minutes to complete.
        """
        print("🔄 Disconnecting reader from IoT Connector...")
        print("⏳ This may take a few minutes, please wait...")
        
        disconnect_command = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName>MyFX9600</rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:disconnectFromCloud/>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )

        try:
            response = requests.post(
                self.control_url,
                data=disconnect_command,
                headers={'Content-Type': 'application/xml'},
                timeout=600,  # 10 minutes timeout for cloud disconnection
                verify=False
            )
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                
                # Check result code
                result_elements = root.findall('.//g1:resultCode', 
                    namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                
                if result_elements and result_elements[0].text == "0":
                    print("✅ Reader disconnected from IoT Connector successfully")
                    return True
                else:
                    result_code = result_elements[0].text if result_elements else "Unknown"
                    print(f"❌ Reader disconnection failed with result code: {result_code}")
                    
                    # Try to get additional error information
                    error_elements = root.findall('.//g1:description', 
                        namespaces={'g1': 'urn:epcglobal:rm:xsd:1'})
                    if error_elements:
                        print(f"   Error message: {error_elements[0].text}")
                    
                    return False
            else:
                print(f"❌ Disconnection request failed with status code: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("⏰ Disconnection request timed out - this may be normal for cloud operations")
            print("ℹ️ Check reader status manually to verify disconnection")
            return False
        except Exception as e:
            print(f"❌ IoT Connector disconnection error: {e}")
            return False

    # WS Endpoint #

    def add_wsep(self, session_id: str) -> bool:
        """
        Adds a WebSocket Endpoint (WSEP) to the reader named "PDWC".
        """
        print("[DEBUG] Adding WS endpoint..")
        
        # Exact replica of the JavaScript wsEpConfig configuration
        # Modification: use "ws" instead of "wss" for HTTP compatibility
        ws_ep_config = {
            "name": "WS",
            "description": "WS Test", 
            "type": "WEBSOCKET",
            "configuration": {
                "endpoint": {      
                    "protocol": "ws"
                },
                "additional": {
                    "batching": {
                        "maxPayloadSizePerReport": 0,
                        "reportingInterval": 0
                    },
                    "retention": {
                        "maxEventRetentionTimeInMin": 500,
                        "maxNumEvents": 150000,
                        "throttle": 500
                    }
                },
                "security": {
                    "verifyServerCertificate": False,
                    "verifyServerHostName": False
                }
            }
        }
        
        # Exact replica of the JavaScript XML command
        wsep_config_cmd = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:manageCloudEndpoints>"
            f"<motorm:operation>ADD</motorm:operation>"
            f"<motorm:data>{json.dumps(ws_ep_config)}</motorm:data>"
            f"</motorm:manageCloudEndpoints>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            # Replica of the JavaScript fetch call
            response = requests.post(
                self.control_url,
                data=wsep_config_cmd,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}...")

            # Check HTTP status before attempting XML parsing
            if response.status_code != 200:
                if self.debug:
                    print(f"[DEBUG] HTTP error {response.status_code}")
                return False
            
            # Parse the XML response
            root = self._parse_xml_response(response.text)
            
            # Replica of the JavaScript logic: check resultCode == "0"
            result_code = self._get_xml_text(root, "g1:resultCode")
            
            if result_code == "0":
                if self.debug:
                    print("[DEBUG] ws ep added successfully")
                return True
            else:
                # Check for 'already available' error and treat as success
                error_desc = self._get_xml_text(root, "g1:description")
                if error_desc and "already available" in error_desc:
                    print("ws ep already exists, treating as success")
                    return True
                print("ws ep addition failed")
                return False
                
        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")

    def is_wsep_added(self, session_id: str) -> bool:
        """
        Checks if the WebSocket Endpoint (WSEP) has already been added to the reader.
        """
        if self.debug:
            print("[DEBUG] checking IOTC endpoints added..")
        
        # XML command to view endpoints
        iswsadded = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:manageCloudEndpoints>"
            f"<motorm:operation>VIEW</motorm:operation>"
            f"<motorm:data></motorm:data>"
            f"</motorm:manageCloudEndpoints>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            # Replica of the JavaScript fetch call
            response = requests.post(
                self.control_url,
                data=iswsadded,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )
            
            if(self.debug):
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}...")
            
            # Parse the XML response
            root = self._parse_xml_response(response.text)
            
            # Replica of the JavaScript logic: check resultCode
            result_code = self._get_xml_text(root, "g1:resultCode")
            
            if result_code == "0":
                # Check if g3:data exists and has content
                data_text = self._get_xml_text(root, "g3:data")
                if data_text:
                    try:
                        # Parse the JSON contained in g3:data (replica of JavaScript logic)
                        epdata = json.loads(data_text)
                        
                        # Loop through endpoints to find WEBSOCKET named "WS"
                        # (exact replica of the JavaScript for loop)
                        for ep in epdata:
                            if (ep.get('type') == "WEBSOCKET" and 
                                ep.get('name') == "WS"):
                                if self.debug:
                                    print("[DEBUG] WS EP already added")
                                return True

                        if self.debug:
                            print("[DEBUG] WS EP not added")
                        return False
                        
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        print("WS EP not added")
                        return False
                else:
                    if self.debug:
                        print("[DEBUG] WS EP not added")
                    return False
            else:
                if self.debug:
                    print("[DEBUG] WS EP not added")
                return False
                
        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")

    def map_wsep(self, session_id: str) -> bool:
        """
        Maps the WebSocket Endpoint "PDWC" to the reader's data interface.
        """
        if self.debug:
            print("[DEBUG] Mapping WebSocket endpoint to data interface...")
        
        try:
            # Load all available endpoints
            all_endpoints = self.get_all_endpoints(session_id)
            endpoint_names = []
            if all_endpoints:
                if isinstance(all_endpoints, list):
                    endpoint_names = [ep.get("name", "") for ep in all_endpoints if isinstance(ep, dict)]
                elif isinstance(all_endpoints, dict):
                    if "endpoints" in all_endpoints:
                        endpoint_names = [ep.get("name", "") for ep in all_endpoints["endpoints"] if isinstance(ep, dict)]
                    else:
                        for v in all_endpoints.values():
                            if isinstance(v, list):
                                endpoint_names.extend([ep.get("name", "") for ep in v if isinstance(ep, dict)])
            else:
                if self.debug:
                    print("[DEBUG] Unable to load the complete list of endpoints, using only current mapping")
                if self.ep_mapping and isinstance(self.ep_mapping, dict):
                    for v in self.ep_mapping.values():
                        if isinstance(v, list):
                            endpoint_names.extend([ep.get("name", "") for ep in v if isinstance(ep, dict)])
                else:
                    current_mapping = self.get_endpoint_mapping(session_id)
                    if current_mapping and isinstance(current_mapping, dict):
                        for v in current_mapping.values():
                            if isinstance(v, list):
                                endpoint_names.extend([ep.get("name", "") for ep in v if isinstance(ep, dict)])
                    else:
                        if self.debug:
                            print("[DEBUG] Failed to get current endpoint mapping")
                        return False

            # Find WebSocket endpoint name
            ws_name = None
            for name in endpoint_names:
                if name == "WS":
                    ws_name = name
                    break
            if not ws_name:
                ws_name = "WS"  # fallback, assume name

            # Build new mapping: control/management as objects, data/event as arrays
            new_ep_map = {
                "control": {
                    "enableLocalRest": True,
                    "endpoints": ["NONE"]
                },
                "data": [ws_name],
                "event": ["NONE"],
                "management": {
                    "enableLocalRest": True,
                    "endpoints": ["NONE"]
                }
            }

            if self.debug:
                print(f"[DEBUG] Sending new ep mapping (correct schema): {json.dumps(new_ep_map, indent=2)}")

            # XML command to set mapping of endpoints
            new_ep_map_cmd = (
                f"{self.cmd_header}"
                f"<rm:id>104</rm:id>"
                f"<rm:targetName></rm:targetName>"
                f"<motorm:readerDevice>"
                f"<motorm:sessionID>{session_id}</motorm:sessionID>"
                f"<motorm:cloudEndpointsMapping>"
                f"<motorm:operation>UPDATE</motorm:operation>"
                f"<motorm:data>{json.dumps(new_ep_map)}</motorm:data>"
                f"</motorm:cloudEndpointsMapping>"
                f"</motorm:readerDevice>"
                f"</rm:command>"
            )

            response = requests.post(
                self.control_url,
                data=new_ep_map_cmd,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}")

            if response.status_code != 200:
                print(f"[DEBUG] HTTP error {response.status_code}")
                return False

            root = self._parse_xml_response(response.text)
            result_code = self._get_xml_text(root, "g1:resultCode")

            if result_code == "0":
                if self.debug:
                    print("[DEBUG] WebSocket endpoint mapped successfully")
                return True
            else:
                if self.debug:
                    print("[DEBUG] WebSocket endpoint mapping failed")
                return False
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Error in mapping WebSocket endpoint: {e}")
            return False

    def is_wsep_mapped(self, session_id: str) -> bool:
        if self.debug:
            print("[DEBUG] Checking endpoint mapping..")
        
        # XML command to view endpoint mapping
        wsep_mapping_cmd = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:cloudEndpointsMapping>"
            f"<motorm:operation>VIEW</motorm:operation>"
            f"<motorm:data></motorm:data>"
            f"</motorm:cloudEndpointsMapping>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            # Post XML command
            response = requests.post(
                self.control_url,
                data=wsep_mapping_cmd,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}")

            # Check HTTP response status before attempting XML parsing
            if response.status_code != 200:
                if self.debug:
                    print(f"[DEBUG] HTTP error {response.status_code}")
                return False
            
            # Parse the XML response
            root = self._parse_xml_response(response.text)

            # Extract <g1:resultCode> tag content
            result_code = self._get_xml_text(root, "g1:resultCode")
            
            if result_code == "0":
                # Check if g3:data exists and has content
                data_text = self._get_xml_text(root, "g3:data")
                if data_text:
                    try:
                        # Parse the JSON contained in g3:data
                        ep_mapping = json.loads(data_text)
                        
                        # Store in global variable
                        self.ep_mapping = ep_mapping
                        
                        # Loop through ep_mapping.data to find WEBSOCKET named "WS"
                        if "data" in ep_mapping and isinstance(ep_mapping["data"], list):
                            for ep in ep_mapping["data"]:
                                if (ep.get('type') == "WEBSOCKET" and 
                                    ep.get('name') == "WS"):
                                    if self.debug:
                                        print("[DEBUG] WS Endpoint already mapped")
                                    return True

                        if self.debug:
                            print("[DEBUG] WS Endpoint not mapped")
                        return False
                        
                    except json.JSONDecodeError as e:
                        print(f"[DEBUG] Error parsing JSON: {e}")
                        print("[DEBUG] Get WebSocket Endpoint mapping failed")
                        return False
                else:
                    # If there is no g3:data, return True
                    return True
            else:
                print("[DEBUG] Get WebSocket Endpoint mapping failed")
                return False
                
        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")

    # MQTT Endpoint #

    def add_mqttep(self, session_id: str, reader_name: str, host_name: str, mqtt_name: str) -> bool:
        """
        Adds a MQTT Endpoint (MQTTEP) to the reader device.
        """
        if self.debug:
            print(f"[DEBUG] Adding MQTT endpoint with client_id='{reader_name}', hostname='{host_name}'..")

        mqtt_ep_config = {
            "name": mqtt_name,
            "description": "MQTT Endpoint set with CLI", 
            "type": "MQTT",
            "configuration": {
                "additional": {
                    "cleanSession": True,
                    "clientId": reader_name,
                    "debug": False,
                    "keepAlive": 60
                },
                "additionalConfig": {
                    "batching": None,
                    "retention": {
                        "maxEventRetentionTimeInMin": 500,
                        "maxNumEvents": 150000,
                        "throttle": 100
                    }
                },
                "basicAuthentication": {
                    "password": "6E8D861803860A797F97CBC7D40911BBCD08CC510457353958ADDDCD84845D3D000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "username": "admin"
                },
                "enableSecurity": False,
                "endpoint": {
                    "hostname": host_name,
                    "port": 1883,
                    "protocol": "tcp"
                },
                "security": {
                    "certificates": {
                        "certAlgorithm": "RS256",
                        "certFormat": "PEM"
                    },
                    "useLocalCerts": True,
                    "verifyServerCertificate": False,
                    "verifyServerHostName": False
                },
                "topics": {
                    "control": {
                        "command": {
                            "topic": f"ccmds/{reader_name}"
                        },
                        "response": {
                            "qos": 0,
                            "retain": False,
                            "topic": f"crsp/{reader_name}"
                        }
                    },
                    "management": {
                        "command": {
                            "topic": f"mcmds/{reader_name}"
                        },
                        "response": {
                            "qos": 0,
                            "retain": False,
                            "topic": f"mrsp/{reader_name}"
                        }
                    },
                    "managementEvents": {
                        "qos": 0,
                        "retain": False,
                        "topic": f"mevents/{reader_name}"
                    },
                    "tagEvents": {
                        "qos": 0,
                        "retain": False,
                        "topic": f"tevents/{reader_name}"
                    }
                }
            }
        }
            
        # XML command to add MQTT endpoint
        mqtt_config_cmd = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:manageCloudEndpoints>"
            f"<motorm:operation>ADD</motorm:operation>"
            f"<motorm:data>{json.dumps(mqtt_ep_config)}</motorm:data>"
            f"</motorm:manageCloudEndpoints>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )

        try:
            # Post XML command to add MQTT endpoint
            response = requests.post(
                self.control_url,
                data=mqtt_config_cmd,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}")

            # Check HTTP status before attempting XML parsing
            if response.status_code != 200:
                if self.debug:
                    print(f"[DEBUG] HTTP error {response.status_code}")
                return False

            # Parse the XML response
            root = self._parse_xml_response(response.text)

            # Check resultCode == "0"
            result_code = self._get_xml_text(root, "g1:resultCode")

            if result_code == "0":
                if self.debug:
                    print("[DEBUG] MQTT ep added successfully")
                return True
            else:
                # Check for 'already available' error and treat as success
                error_desc = self._get_xml_text(root, "g1:description")
                if error_desc and "already available" in error_desc:
                    print("MQTT ep already exists, treating as success")
                    return True
                print("MQTT ep addition failed")
                return False

        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")

    def is_mqttep_added(self, session_id: str, mqtt_name: str) -> bool:
        """
        Checks if the MQTT Endpoint (MQTTEP) has already been added to the reader.
        """
        if self.debug:
            print(f"[DEBUG] checking if MQTT endpoint '{mqtt_name}' is added..")
        
        # XML command to view endpoints
        is_mqtt_added = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:manageCloudEndpoints>"
            f"<motorm:operation>VIEW</motorm:operation>"
            f"<motorm:data></motorm:data>"
            f"</motorm:manageCloudEndpoints>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            # Post XML command to view MQTT endpoints
            response = requests.post(
                self.control_url,
                data=is_mqtt_added,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )
            
            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}...")
            
            # Parse the XML response
            root = self._parse_xml_response(response.text)
            
            # Check resultCode
            result_code = self._get_xml_text(root, "g1:resultCode")
            
            if result_code == "0":
                # Check if g3:data exists and has content
                data_text = self._get_xml_text(root, "g3:data")
                if data_text:
                    try:
                        # Parse the JSON contained in g3:data (replica of JavaScript logic)
                        epdata = json.loads(data_text)
                        
                        # Loop through endpoints to find MQTT named as specified
                        for ep in epdata:
                            if (ep.get('type') == "MQTT" and 
                                ep.get('name') == mqtt_name):
                                if self.debug:
                                    print(f"[DEBUG] MQTT EP '{mqtt_name}' already added")
                                return True

                        if self.debug:
                            print(f"[DEBUG] MQTT EP '{mqtt_name}' not added")
                        return False
                        
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        print(f"MQTT EP '{mqtt_name}' not added")
                        return False
                else:
                    if self.debug:
                        print(f"[DEBUG] MQTT EP '{mqtt_name}' not added")
                    return False
            else:
                if self.debug:
                    print(f"[DEBUG] MQTT EP '{mqtt_name}' not added")
                return False
                
        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")

    def map_mqttep(self, session_id: str, mqtt_name: str) -> bool:
        """
        Maps the MQTT Endpoint to the reader's data interface.
        """
        if self.debug:
            print(f"[DEBUG] Mapping MQTT endpoint '{mqtt_name}' to data interface..")

        try:
            # Load all available endpoints
            all_endpoints = self.get_all_endpoints(session_id)
            endpoint_names = []
            if all_endpoints:
                if isinstance(all_endpoints, list):
                    endpoint_names = [ep.get("name", "") for ep in all_endpoints if isinstance(ep, dict)]
                elif isinstance(all_endpoints, dict):
                    if "endpoints" in all_endpoints:
                        endpoint_names = [ep.get("name", "") for ep in all_endpoints["endpoints"] if isinstance(ep, dict)]
                    else:
                        for v in all_endpoints.values():
                            if isinstance(v, list):
                                endpoint_names.extend([ep.get("name", "") for ep in v if isinstance(ep, dict)])
            else:
                if self.debug:
                    print("[DEBUG] Unable to load the complete list of endpoints, using only current mapping")
                if self.ep_mapping and isinstance(self.ep_mapping, dict):
                    for v in self.ep_mapping.values():
                        if isinstance(v, list):
                            endpoint_names.extend([ep.get("name", "") for ep in v if isinstance(ep, dict)])
                else:
                    current_mapping = self.get_endpoint_mapping(session_id)
                    if current_mapping and isinstance(current_mapping, dict):
                        for v in current_mapping.values():
                            if isinstance(v, list):
                                endpoint_names.extend([ep.get("name", "") for ep in v if isinstance(ep, dict)])
                    else:
                        if self.debug:
                            print("[DEBUG] Failed to get current endpoint mapping")
                        return False

            # Find MQTT endpoint name
            mqtt_endpoint_name = None
            for name in endpoint_names:
                if name == mqtt_name:
                    mqtt_endpoint_name = name
                    break
            if not mqtt_endpoint_name:
                mqtt_endpoint_name = mqtt_name  # fallback, assume name

            # Build new mapping: control/management as objects, data/event as arrays
            new_ep_map = {
                "control": {
                    "enableLocalRest": True,
                    "endpoints": [mqtt_endpoint_name]
                },
                "data": [mqtt_endpoint_name],
                "event": [mqtt_endpoint_name],
                "management": {
                    "enableLocalRest": True,
                    "endpoints": [mqtt_endpoint_name]
                }
            }

            if self.debug:
                print(f"[DEBUG] sending new MQTT ep mapping (correct schema): {json.dumps(new_ep_map, indent=2)}")

            # Exact replica of the JavaScript XML command
            new_ep_map_cmd = (
                f"{self.cmd_header}"
                f"<rm:id>104</rm:id>"
                f"<rm:targetName></rm:targetName>"
                f"<motorm:readerDevice>"
                f"<motorm:sessionID>{session_id}</motorm:sessionID>"
                f"<motorm:cloudEndpointsMapping>"
                f"<motorm:operation>UPDATE</motorm:operation>"
                f"<motorm:data>{json.dumps(new_ep_map)}</motorm:data>"
                f"</motorm:cloudEndpointsMapping>"
                f"</motorm:readerDevice>"
                f"</rm:command>"
            )

            response = requests.post(
                self.control_url,
                data=new_ep_map_cmd,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}")

            if response.status_code != 200:
                print(f"[DEBUG] HTTP error {response.status_code}")
                return False

            root = self._parse_xml_response(response.text)
            result_code = self._get_xml_text(root, "g1:resultCode")

            if result_code == "0":
                if self.debug:
                    print(f"[DEBUG] MQTT ep '{mqtt_name}' mapped successfully")
                return True
            else:
                if self.debug:
                    print(f"[DEBUG] MQTT ep '{mqtt_name}' mapping failed")
                return False
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Error in MQTT mapping: {e}")
            return False

    def is_mqttep_mapped(self, session_id: str, mqtt_name: str) -> bool:
        """
        Checks if the MQTT Endpoint is mapped in the data interface.
        """
        if self.debug:
            print(f"[DEBUG] Checking if MQTT endpoint '{mqtt_name}' is mapped..")
        
        # Exact replica of the JavaScript XML command
        mqtt_mapping_cmd = (
            f"{self.cmd_header}"
            f"<rm:id>104</rm:id>"
            f"<rm:targetName></rm:targetName>"
            f"<motorm:readerDevice>"
            f"<motorm:sessionID>{session_id}</motorm:sessionID>"
            f"<motorm:cloudEndpointsMapping>"
            f"<motorm:operation>VIEW</motorm:operation>"
            f"<motorm:data></motorm:data>"
            f"</motorm:cloudEndpointsMapping>"
            f"</motorm:readerDevice>"
            f"</rm:command>"
        )
        
        try:
            # Replica of the JavaScript fetch call
            response = requests.post(
                self.control_url,
                data=mqtt_mapping_cmd,
                headers={
                    'Content-Type': 'application/xml'
                },
                timeout=60
            )

            if self.debug:
                print(f"[DEBUG] Response status: {response.status_code}")
                print(f"[DEBUG] Response data: {response.text}")

            # Check HTTP status before attempting XML parsing
            if response.status_code != 200:
                if self.debug:
                    print(f"[DEBUG] HTTP error {response.status_code}")
                return False
            
            # Parse the XML response
            root = self._parse_xml_response(response.text)
            
            # Replica of the JavaScript logic: check resultCode == "0"
            result_code = self._get_xml_text(root, "g1:resultCode")
            
            if result_code == "0":
                # Check if g3:data exists and has content
                data_text = self._get_xml_text(root, "g3:data")
                if data_text:
                    try:
                        # Parse the JSON contained in g3:data (replica of JavaScript logic)
                        ep_mapping = json.loads(data_text)
                        
                        # Store in global variable (as in JavaScript)
                        self.ep_mapping = ep_mapping
                        
                        # Loop through ep_mapping.data to find MQTT endpoint
                        if "data" in ep_mapping and isinstance(ep_mapping["data"], list):
                            for ep in ep_mapping["data"]:
                                if (ep.get('type') == "MQTT" and 
                                    ep.get('name') == mqtt_name):
                                    if self.debug:
                                        print(f"[DEBUG] MQTT EP '{mqtt_name}' already mapped")
                                    return True

                        if self.debug:
                            print(f"[DEBUG] MQTT EP '{mqtt_name}' not mapped")
                        return False
                        
                    except json.JSONDecodeError as e:
                        if self.debug:
                            print(f"[DEBUG] Error parsing JSON: {e}")
                        return False
                else:
                    # No data content - assume not mapped
                    if self.debug:
                        print(f"[DEBUG] No endpoint mapping data found")
                    return False
            else:
                if self.debug:
                    print(f"[DEBUG] Getting MQTT endpoint mapping failed")
                return False
                
        except requests.RequestException as e:
            raise IoTCException(f"HTTP request error: {e}")
        except Exception as e:
            if isinstance(e, (InvalidSessionException, IoTCException)):
                raise
            raise IoTCException(f"Unexpected error: {e}")