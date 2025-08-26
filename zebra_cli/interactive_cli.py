"""
Persistent interactive CLI for Zebra RFID
"""
import os
import sys
import time
import json
from typing import Optional
import getpass
import requests
import urllib3

from zebra_cli.context import AppContext
from zebra_cli.plotter import Plotter, EnhancedPlotter
from zebra_cli.tag_table_window import TagTableWindow

from zebra_cli.api_submenu import ApiSubmenu
import queue
import threading

# Import of converted IOTC functions
try:
    from zebra_cli.iotc_client import ZebraIoTCClient as IOTCClient
    IOTC_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ IOTC modules not available: {e}")
    IOTC_AVAILABLE = False

class InteractiveCLI:
    """Persistent interactive CLI for Zebra RFID"""

    def __init__(self, debug: bool = False, pre_commands: Optional[list[str]] = None):
        # Step 1: Set code page to UTF-8 on Windows for Unicode support
        import sys, os
        if os.name == 'nt':
            try:
                os.system('chcp 65001 >nul')
                if debug:
                    print("[DEBUG] Code page set to UTF-8 (65001)")
            except Exception as e:
                if debug:
                    print(f"[DEBUG] Failed to set code page: {e}")
        self.app_context = AppContext(debug=debug)
        self.running = True
        self.listener = None
        self.data_queue = None
        self.stop_event = None
        self.tag_table_window = None
        self.debug = debug
        self._pre_commands = pre_commands or []
        self.login_attempts = 0  # Track login attempts
        # API submenu instance
        self.api_submenu = ApiSubmenu(self.app_context)
        
    def _supports_unicode(self) -> bool:
        """Detects if the terminal likely supports Unicode borders and wide characters."""
        import sys, os
        # Windows terminals with chcp 65001, modern Linux/macOS terminals, and VSCode terminals usually support Unicode
        if sys.platform == 'win32':
            try:
                import ctypes
                codepage = ctypes.windll.kernel32.GetConsoleOutputCP()
                if codepage == 65001:
                    return True
            except Exception:
                pass
            # Fallback: check environment
            return 'WT_SESSION' in os.environ or 'TERM_PROGRAM' in os.environ

    def clear_screen(self):
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        """Shows the application header"""
        print("🏷️" + "=" * 58)
        print("   XRFID CLI - Interactive Mode")
        print("=" * 60)
        
        # Show connection status and reading status next to IP
        if self.app_context.is_connected():
            reading_str = ""
            try:
                status = self.app_context.get_status()
                radio = None
                if status:
                    for key in status.keys():
                        if key.lower().replace("_", "").replace("-", "") == 'radioactivity':
                            radio = status[key]
                            break
                else:
                    print("[WARNING] Status is None")
                if radio == 'active':
                    reading_str = "  📡 Reading: IN PROGRESS"
                elif radio == 'inactive':
                    reading_str = "  ⏹️  Reading: STOPPED"
                elif radio:
                    reading_str = f"  ❓ Reading: {radio}"
                else:
                    reading_str = "  ❓ Reading: Status undetermined"
            except Exception:
                reading_str = "  ⚠️ Reading: Status error"
            print(f"✅ Connected to: {self.app_context.ip_address}{reading_str}")
            if self.app_context.protocol:
                print(f"🔐 Protocol: {self.app_context.protocol.upper()}")
            else:
                print("🔐 Protocol: NONE")
        else:
            print("❌ Not connected")
        print("-" * 60)
    
    def show_menu(self):
        """Shows the main XRFID CLI menu with perfectly aligned borders (including emoji and wide characters), or ASCII fallback if needed."""
        use_unicode = self._supports_unicode()
        try:
            from wcwidth import wcswidth as _wcswidth
        except ImportError:
            _wcswidth = None
        
        def wcswidth(text):
            if _wcswidth is not None:
                try:
                    width = _wcswidth(text)
                    # Handle None by defaulting to fallback calculation
                    if width is None:
                        return sum(2 if ord(c) > 127 else 1 for c in text)
                    return width
                except (TypeError, ValueError):
                    # Handle errors by using fallback calculation
                    return sum(2 if ord(c) > 127 else 1 for c in text)
            else:
                # Fallback: treat all non-ASCII as width 2
                return sum(2 if ord(c) > 127 else 1 for c in text)
        width = 60
        def row(text: str) -> str:
            # Manual spacing is used for best alignment. This function ensures the right border is always correct.
            content = f" {text} "
            row_width = wcswidth(content)
            pad = (width + 2) - row_width
            # Always pad right so border is at the same column
            return (f"│{content}{' ' * pad}│" if use_unicode else f"|{content}{' ' * pad}|")
        # Borders
        top = "┌" + "─" * (width + 2) + "┐" if use_unicode else "+" + "-" * (width + 2) + "+"
        sep = "├" + "─" * (width + 2) + "┤" if use_unicode else "+" + "-" * (width + 2) + "+"
        bottom = "└" + "─" * (width + 2) + "┘" if use_unicode else "+" + "-" * (width + 2) + "+"
        print("\n📋 XRFID CLI - Main Menu:")
        print(top)
        print(row("CONNECTION:"))
        print(row("l  / login         🔐    Automatic login and connection"))
        print(row("d  / disconnect    🔌    Disconnect"))
        print(sep)
        print(row("READER OPERATIONS:"))
        print(row("s  / start         🟢    Start scanning "))
        print(row("x  / stop          🔴    Stop scanning "))
        print(row("r  / restApi       🔧    REST API requests (submenu)"))
        print(sep)
        print(row("MONITORING:"))
        print(row("w  / websocket     🔌    Simple WebSocket connection"))
        print(row("m  / monitoring    📋    Tag table"))
        print(row("p  / plot          📊    RSSI plot "))
        print(row("a  / atr           📍    ATR7000 - Localization (submenu)"))
        print(sep)
        print(row("IOT CONNECTOR (IOTC):"))
        print(row("i  / iotc          🌐    IoT Connector setup (+ parameters)"))
        print(row("di / disconnectIOTC🔌    Disconnect from IOTC"))
        print(sep)
        print(row("UTILITIES:"))
        print(row("c  / clear         🧹    Clear screen"))
        print(row("rs / reset         💥    Force reset WebSocket connections"))
        print(row("h  / help          ❓    Command help"))
        print(row("q  / quit          🚪    Exit"))
        print(bottom)
    
    def get_user_input(self, prompt: str = "\n🎯 Command or shortcut: ") -> str:
        """Gets input from user or from preset command list"""
        if self._pre_commands:
            return self._pre_commands.pop(0)
        try:
            # Ensure no active listeners in main menu
            if hasattr(self, 'data_queue') and self.data_queue:
                # Empty queue to avoid unwanted prints
                try:
                    while not self.data_queue.empty():
                        self.data_queue.get_nowait()
                except:
                    pass

            user_input = input(prompt).strip()

            if (user_input.startswith('i ') and user_input.split()[0] == 'i') or (user_input.startswith('iotc ') and user_input.split()[0] == 'iotc'):
                return user_input   
            else:
                return user_input.lower()
        except KeyboardInterrupt:
            print("\n\n👋 User requested exit")
            return 'q'
    
    def handle_login_connect(self):     
        print("\n🔐 AUTOMATIC LOGIN AND CONNECTION")
        print("-" * 40)
        try:
            ip = input("📍 Reader IP: ").strip()
            if not ip:
                print("❌ IP required")
                return
            # If trying to connect to another reader always reset preferred protocol
            if ip != self.app_context.ip_address:
                self.app_context.preferred_protocol = None
            username = input("👤 Username [admin]: ").strip() or "admin"
            password = getpass.getpass("🔑 Password [admin]: ").strip() or "admin"
            print(f"\n🔍 Connecting to {ip}...")
            self.login_attempts += 1
            success = self.app_context.login_and_connect(ip, username, password)
            if success:
                print("✅ Login and connection completed successfully!")
                print(f"📍 IP: {self.app_context.ip_address}")
                if self.app_context.protocol:
                    print(f"🔐 Protocol: {self.app_context.protocol.upper()}")
                else:
                    print(f"🔐 Protocol: NONE")
                self.login_attempts = 0  # Reset attempts on each login
                input("\n⏸️  Press ENTER to continue...")
            else:
                if self.login_attempts < 3:
                    print(f"⚠️  Login failed, attempt {self.login_attempts}/3. Retrying...")
                    return self.handle_login_connect()
                print("❌ Login failed - Check IP, username and password")
                input("\n⏸️  Press ENTER to continue...")
        except Exception as e:
            print(f"❌ Login error: {e}")
            input("\n⏸️  Press ENTER to continue...")
    
    def handle_manual_connect(self):
        """Handles manual connection with token"""
        print("\n🔗 MANUAL CONNECTION")
        print("-" * 25)
        
        try:
            ip = input("📍 Reader IP: ").strip()
            if not ip:
                print("❌ IP required")

            
            token = input("🔑 Bearer Token: ").strip()
            if not token:
                print("❌ Token required")

            
            print(f"\n🔍 Connection attempt to {ip}...")
            self.app_context.connect(ip, token)
            print("✅ Connection established successfully!")
            input("\n⏸️  Press ENTER to continue...")
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            input("\n⏸️  Press ENTER to continue...")
    
    def handle_status(self):
        """
        Shows connection status and reader reading status.
        Reading status is derived from 'radioActivitiy' field returned by /cloud/status:
        - 'active'   → Reading in progress
        - 'inactive' → Reader stopped
        In debug mode, prints the entire status JSON.
        """
        print("\n📊 CONNECTION STATUS")
        print("-" * 20)
        if self.app_context.is_connected():
            print(f"✅ Status: Connected")
            print(f"📍 IP: {self.app_context.ip_address}")
            if self.app_context.protocol:
                print(f"🔐 Protocol: {self.app_context.protocol.upper()}")
            else:
                print("🔐 Protocol: NONE")
            print(f"🔗 WebSocket: {self.app_context.ws_uri}")
            if self.app_context.token:
                print(f"🔑 Token: {self.app_context.token[:10]}...{self.app_context.token[-4:]}")
            else:
                print("🔑 Token: NONE")
            
            # WebSocket status
            ws_status = self.app_context.get_websocket_status()
            print(f"\n📡 WEBSOCKET STATUS:")
            print(f"   Running: {'✅ Yes' if ws_status['is_running'] else '❌ No'}")
            print(f"   Configured URI: {ws_status['configured_uri']}")
            print(f"   Listener URI: {ws_status['listener_uri']}")
            print(f"   Queue Size: {ws_status['queue_size']} messages")
            print(f"   Debug Mode: {'✅ On' if ws_status['debug_mode'] else '❌ Off'}")
            
            # Reading status
            try:
                status = self.app_context.get_status()
                radio = None
                if status:
                    for key in status.keys():
                        if 'radio' in key.lower():
                            radio = status[key]
                            break
                else:
                    print("[WARNING] Status is None")
                if radio == 'active':
                    print(f"📡 Reading: ✅ IN PROGRESS")
                elif radio == 'inactive':
                    print(f"📡 Reading: ⏹️ STOPPED")
                elif radio:
                    print(f"📡 Reading: ⚠️ {radio.upper()}")
                else:
                    print(f"📡 Reading: ❓ Unknown status")
            except Exception:
                print(f"📡 Reading: ⚠️ Status error")
            
            # DEBUG: print entire JSON if requested
            if self.debug:
                status = self.app_context.get_status()
                print("\n[DEBUG] Complete status message:")
                print(json.dumps(status, indent=2, ensure_ascii=False))
        else:
            print("❌ Status: Not connected")
            print("💡 Use option 1 or 2 to connect")
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_disconnect(self):
        """Handles disconnection"""
        self.ensure_no_background_listeners()
        if self.app_context.is_connected():
            self.app_context.disconnect()
            print("✅ Disconnection completed")
        else:
            print("ℹ️  No active connection")
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_websocket_reset(self):
        """Handles WebSocket force reset"""
        self.ensure_no_background_listeners()
        print("\n💥 Force resetting WebSocket connections...")
        print("   This will forcibly close any stuck connections")
        confirm = input("⚠️  Continue? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            try:
                self.app_context.force_reset_websocket()
                print("✅ WebSocket reset completed")
                print("💡 You can now try WebSocket monitoring again (t, p commands)")
            except Exception as e:
                print(f"❌ Error during reset: {e}")
        else:
            print("ℹ️  Reset cancelled")
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_start_scan(self):
        """Starts scanning"""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        try:
            if self.debug:
                print(f"[DEBUG] handle_start_scan - About to start scan")
                print(f"[DEBUG] handle_start_scan - Connected: {self.app_context.is_connected()}")
                print(f"[DEBUG] handle_start_scan - WebSocket running: {self.app_context.is_websocket_running()}")
            print("🔄 Starting scan...")
            result = self.app_context.start_scan()
            
            if self.debug:
                print(f"[DEBUG] handle_start_scan - Start scan result: {result}")
            
            if result is None:
                print("❌ Unable to start scanning")
            elif result.get("status") == "already_active":
                print("⚠️  Scan already active")
            else:
                print("✅ Scan started successfully!")
                print("💡 Use option 'm'' to monitor tags")
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] handle_start_scan - Exception: {e}")
                import traceback
                traceback.print_exc()
            print(f"❌ Start error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_stop_scan(self):
        """Stops scanning"""
        self.ensure_no_background_listeners()
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return
        try:
            print("⏹️ Stopping scan...")
            result = self.app_context.stop_scan()
            if result:
                print("✅ Scan stopped successfully!")
            else:
                print("❌ Unable to stop scanning")
        except Exception as e:
            print(f"❌ Stop error: {e}")
        input("\n⏸️  Press ENTER to continue...")

    def handle_api_submenu(self):
        """Handles navigation to the API requests submenu"""
        self.ensure_no_background_listeners()
        
        # Transfer current connection context to API submenu if needed
        if self.app_context.is_connected():
            # Try to get reader IP from the connection context
            self.api_submenu.app_context = self.app_context
            
        # Delegate to the API submenu handler
        self.api_submenu.handle_api_submenu()

    def handle_unified_monitoring(self):
        """Starts unified monitoring: events in terminal + tag table window"""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return

        # Ensure no active listeners before starting
        self.ensure_no_background_listeners()

        print("\n📋 UNIFIED RFID TAG MONITORING")
        print("-" * 40)
        print("🎧 Real-time tag events in terminal")
        print("📊 Separate window with statistics table")
        print("💡 To stop monitoring, simply close the table window or press Ctrl+C in terminal.")
        print()

        try:
            # Ensure permanent WebSocket is running (start if needed)
            if not self.app_context.ensure_websocket_running():
                print("❌ Failed to start WebSocket connection")
                input("\n⏸️  Press ENTER to continue...")
                return
            
            # Create new objects for tag table
            self.data_queue = queue.Queue()
            self.stop_event = threading.Event()

            print(f"📡 Using permanent WebSocket connection")

            # Create tag table window
            try:
                self.tag_table_window = TagTableWindow(self.data_queue, self.stop_event, debug=self.debug)
                # Start window with improved error handling
                table_thread = self.tag_table_window.run()
                # Wait a moment to see if initialization succeeds
                time.sleep(0.5)
                if self.tag_table_window.running:
                    print("✅ Tag table window started")
                else:
                    print("⚠️  Tag table window not started correctly")
                    self.tag_table_window = None
            except ImportError:
                print("⚠️  tkinter not available - terminal events only")
                self.tag_table_window = None
            except Exception as e:
                print(f"❌ Tag table window error: {e}")
                print("   Continuing with terminal events only...")
                self.tag_table_window = None

            print("\n🎧 REAL-TIME TAG EVENTS:")
            print("-" * 30)

            # Main loop to keep monitoring alive and feed data to tag table
            try:
                while not self.stop_event.is_set():
                    try:
                        # Get data from permanent WebSocket and forward to tag table
                        event = self.app_context.get_websocket_data()
                        if event:
                            self.data_queue.put(event)
                        
                        time.sleep(0.1)  # Small delay
                        
                    except Exception as e:
                        if self.debug:
                            print(f"[DEBUG] Error in monitoring loop: {e}")
                        continue
                        
            except KeyboardInterrupt:
                print("\n⏹️  Interruption requested")

        except Exception as e:
            print(f"❌ Monitoring error: {e}")

        # Cleanup
        if self.stop_event:
            self.stop_event.set()
        if self.tag_table_window and self.tag_table_window.running:
            self.tag_table_window.on_closing()

        input("\n⏸️  Press ENTER to continue...")

    def handle_listen_events(self):
        """Starts event listening using the permanent WebSocket"""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        # Ensure permanent WebSocket is running (start if needed)
        if not self.app_context.ensure_websocket_running():
            print("❌ Failed to start WebSocket connection")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        try:
            print("🎧 TAG EVENT LISTENING ACTIVE")
            print("-" * 30)
            print("💡 Press Ctrl+C to stop")
            print(f"📡 Using permanent WebSocket connection")
            print()
            
            # Compact counters for logs
            tag_counts = {}
            last_log_time = {}
            stop_listening = False
            
            try:
                while not stop_listening:
                    try:
                        # Get data from permanent WebSocket
                        event = self.app_context.get_websocket_data()
                        
                        if event is None:
                            time.sleep(0.1)  # Small delay when no data
                            continue
                        
                        # Parse RFID tag events with Zebra format
                        if isinstance(event, dict):
                            # Zebra format: data.idHex, data.peakRssi, etc.
                            if 'data' in event and isinstance(event['data'], dict):
                                tag_data = event['data']
                                epc = tag_data.get('idHex', 'N/A')
                                rssi = tag_data.get('peakRssi', 'N/A')
                                antenna = tag_data.get('antenna', 'N/A')
                                timestamp = event.get('timestamp', 'N/A')
                                
                                if epc != 'N/A':
                                    # Compact log with counters
                                    tag_id = epc
                                    tag_counts[tag_id] = tag_counts.get(tag_id, 0) + 1
                                    current_time = time.time()
                                    
                                    # Log every 3 seconds per tag
                                    if (tag_id not in last_log_time or 
                                        current_time - last_log_time[tag_id] > 3.0):
                                        count = tag_counts[tag_id]
                                        status = "NEW" if count == 1 else f"#{count}"
                                        print(f"🏷️  {status}: {tag_id} | 📡 {rssi}dBm | 📶 Ant{antenna} | ⏰ {timestamp[-12:]}")
                                        last_log_time[tag_id] = current_time
                            
                            # Alternative formats (backward compatibility)
                            else:
                                epc = event.get('epc', event.get('EPC', 'N/A'))
                                rssi = event.get('RSSI', event.get('rssi', event.get('peakRSSI', 'N/A')))
                                antenna = event.get('antenna', event.get('ANTENNA', 'N/A'))
                                timestamp = event.get('timestamp', event.get('time', 'N/A'))
                                
                                if epc != 'N/A':
                                    print(f"🏷️  TAG: {epc} | 📡 RSSI: {rssi}dBm | 📶 Antenna: {antenna} | ⏰ {timestamp}")
                        
                    except KeyboardInterrupt:
                        print("\n⏹️  Interruption requested")
                        stop_listening = True
                        
            except KeyboardInterrupt:
                print("\n⏹️  Monitoring stopped")
            
        except Exception as e:
            print(f"❌ Listening error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def handle_plot_live_gui_enhanced(self):
        """Starts RSSI graph with tag selection in separate window"""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return

        # Make sure no active listeners before starting
        self.ensure_no_background_listeners()

        print("\n📊 RSSI GRAPH WITH TAG SELECTION")
        print("-" * 40)
        
        try:
            # Ensure permanent WebSocket is running (start if needed)
            if not self.app_context.ensure_websocket_running():
                print("❌ Failed to start WebSocket connection")
                input("\n⏸️  Press ENTER to continue...")
                return
            
            print("🔍 Searching for available tags (5 seconds)...")
            print("💡 Make sure there are tags in the reader's field")
            
            # Collect tags for 5 seconds using permanent WebSocket
            recent_tags = set()
            start_time = time.time()
            
            while time.time() - start_time < 5:
                try:
                    event = self.app_context.get_websocket_data()
                    
                    if event is None:
                        time.sleep(0.1)
                        continue
                    
                    # Extract EPC from tag
                    epc = None
                    if isinstance(event, dict):
                        if 'data' in event and isinstance(event['data'], dict):
                            epc = event['data'].get('idHex')
                        else:
                            epc = event.get('epc', event.get('EPC'))
                    
                    if epc and epc != 'N/A':
                        recent_tags.add(epc)
                        if len(recent_tags) == 1:
                            print(f"✅ First tag detected: {epc}")
                        elif len(recent_tags) <= 9:
                            print(f"✅ Tag {len(recent_tags)}: {epc}")
                            
                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG] Error during tag discovery: {e}")
                    continue
            
            # Convert to list and limit to 9 tags
            available_tags = list(recent_tags)[:9]
            
            print(f"\n📋 Tags detected: {len(available_tags)}")
            
            # Tag selection menu
            selected_epc = None
            
            if available_tags:
                print("\n🎯 TAG SELECTION FOR RSSI GRAPH:")
                print("-" * 35)
                
                for i, tag in enumerate(available_tags, 1):
                    print(f"  {i}. {tag}")
                print(f"  0. Enter EPC manually")
                print(f"  a. All tags (multiple graph)")
                
                while True:
                    choice = input("\n🔢 Select tag (1-9, 0, a): ").strip().lower()
                    
                    if choice == 'a':
                        selected_epc = 'ALL'
                        break
                    elif choice == '0':
                        manual_epc = input("📝 Enter tag EPC: ").strip()
                        if manual_epc:
                            selected_epc = manual_epc
                            break
                        else:
                            print("❌ Invalid EPC")
                    else:
                        try:
                            tag_index = int(choice) - 1
                            if 0 <= tag_index < len(available_tags):
                                selected_epc = available_tags[tag_index]
                                break
                            else:
                                print(f"❌ Invalid number. Use 1-{len(available_tags)}, 0 or a")
                        except ValueError:
                            print("❌ Invalid input. Use a number or 'a'")
            else:
                print("⚠️  No tags detected")
                manual_epc = input("📝 Enter tag EPC manually (or ENTER for all): ").strip()
                selected_epc = manual_epc if manual_epc else 'ALL'
            
            # Start graph with selected tag
            print(f"\n🎯 Selected tag: {selected_epc if selected_epc != 'ALL' else 'ALL TAGS'}")
            print("🖼️  Opening graph window...")
            
            # Create plotter with tag filter that uses permanent WebSocket
            plotter = EnhancedPlotter(selected_epc, debug=self.debug)
            
            print("💡 Close the graph window or press Ctrl+C to stop")
            print(f"📡 Using permanent WebSocket connection")
            
            try:
                plotter.plot_live_rssi_gui_permanent(self.app_context)
            except KeyboardInterrupt:
                print("\n⏹️  Graph interrupted")
                
        except Exception as e:
            print(f"❌ Error during plotting: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def handle_plot_live_gui(self):
        """Starts RSSI graph in separate window using permanent WebSocket"""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        # Ensure permanent WebSocket is running (start if needed)
        if not self.app_context.ensure_websocket_running():
            print("❌ Failed to start WebSocket connection")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        # Make sure no active listeners before starting
        self.ensure_no_background_listeners()
        
        try:
            plotter = Plotter(debug=self.debug)
            
            print("🖼️  RSSI GRAPH - SEPARATE WINDOW")
            print("-" * 36)
            print("💡 Close the graph window or press Ctrl+C to stop")
            print(f"📡 Using permanent WebSocket connection")
            print("🔄 Opening window...")
            
            try:
                plotter.plot_live_rssi_gui_permanent(self.app_context)
            except KeyboardInterrupt:
                print("\n⏹️  Graph interrupted")
            
        except Exception as e:
            print(f"❌ Error during plotting: {e}")
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_stop_monitoring(self):
        """Stops active monitoring"""
        print("⏹️  Stopping monitoring in progress...")
        
        stopped_something = False
        
        try:
            # 1. Stop ALL existing stop events
            if hasattr(self, 'stop_event') and self.stop_event:
                self.stop_event.set()
                print("✅ Stop command sent to main monitoring")
                stopped_something = True
            
            # 2. Stop specifically ATR7000 listener if present
            if hasattr(self, 'atr7000_listener') and self.atr7000_listener:
                try:
                    # Call stop method if present (no WebSocket closing)
                    if hasattr(self.atr7000_listener, 'stop'):
                        self.atr7000_listener.stop()
                    # Set to None to avoid reuse
                    self.atr7000_listener = None
                    print("✅ ATR7000 listener stopped and removed")
                    stopped_something = True
                except Exception as e:
                    print(f"⚠️  Error stopping ATR7000: {e}")
            
            # 3. Clean main listener reference (do NOT close permanent WebSocket)
            if hasattr(self, 'listener') and self.listener:
                try:
                    # Only wait for thread to finish, do NOT close permanent WebSocket
                    if hasattr(self.listener, 'join'):
                        self.listener.join(timeout=1)
                    self.listener = None
                    print("✅ Main listener reference removed")
                    stopped_something = True
                except Exception as e:
                    print(f"⚠️  Error stopping listener: {e}")
            
            # 4. Close tag table window
            if hasattr(self, 'tag_table_window') and self.tag_table_window:
                if hasattr(self.tag_table_window, 'running') and self.tag_table_window.running:
                    try:
                        # Close in tkinter main thread if possible
                        if hasattr(self.tag_table_window, 'root') and self.tag_table_window.root:
                            self.tag_table_window.root.after(0, self.tag_table_window.on_closing)
                        else:
                            self.tag_table_window.on_closing()
                        self.tag_table_window = None
                        print("✅ Tag table window closed and removed")
                        stopped_something = True
                    except Exception as e:
                        print(f"⚠️  Error closing table: {e}")
            
            # 5. Clean ALL queues
            for attr_name in ['data_queue']:
                if hasattr(self, attr_name):
                    queue_obj = getattr(self, attr_name)
                    if queue_obj:
                        try:
                            queue_size = queue_obj.qsize()
                            if queue_size > 0:
                                print(f"🗑️  Cleaning {queue_size} messages from {attr_name}...")
                                while not queue_obj.empty():
                                    queue_obj.get_nowait()
                                stopped_something = True
                        except:
                            pass
                        # Set queue to None
                        setattr(self, attr_name, None)
            
            # 6. Reset all monitoring attributes
            self.stop_event = None
            
            if not stopped_something:
                print("ℹ️  No active monitoring to stop")
            else:
                print("✅ All monitoring has been stopped and cleaned")
                # Short pause to allow complete closure
                time.sleep(0.5)
                
        except Exception as e:
            print(f"❌ Error stopping monitoring: {e}")
        
        input("\n⏸️  Press ENTER to continue...")
    
    def show_help(self):
        """Shows command help"""
        print()
        print("TIPS:")
        print("  • Protocol (HTTP/HTTPS) is auto-detected and remembered after login")
        print("  • WebSocket adapts to chosen protocol")
        print("  • Use Ctrl+C to interrupt monitoring or plotting")
        print("  • Tag table and RSSI plot open in separate windows")
        print("  • Most commands require an active connection")
        print("  • For ATR7000 features, use the ATR submenu (a / atr)")
        print("  • For API requests features, use the REST API submenu (r / restApi)")
        print()
        print("IOTC COMMAND PARAMETERS:")
        print("  • Default WebSocket setup: i -type ws")
        print("  • MQTT setup: i -type mqtt -hostname <broker> -readername <name> -endpointname <endpoint>")
        print("  • Example: i -type mqtt -hostname mqtt.broker.com -readername MyReader -endpointname MQTT_CLI")
        print()
        print("TROUBLESHOOTING:")
        print("  • Ensure reader is powered on and reachable")
        print("  • Credentials are usually admin/admin")
        print("  • If WebSocket fails, run IOTC setup again")
        print("  • If you encounter connection or token issues try using the commands disconnect and login to reconnect to the reader")
        print("  • If anything else fails try the command q / quit and restart the application")
        print()
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_tag_table(self):
        """Opens a separate window with RFID tag table"""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            return
        
        print("\n📋 RFID TAG TABLE - SEPARATE WINDOW")
        print("-" * 50)
        
        try:
            # Stop any previous monitoring
            if self.stop_event:
                self.stop_event.set()
                time.sleep(1)
            
            # Ensure permanent WebSocket is running
            if not self.app_context.ensure_websocket_running():
                print("❌ Failed to start WebSocket connection")
                input("\n⏸️  Press ENTER to continue...")

            
            # Create new objects for WebSocket
            self.data_queue = queue.Queue()
            self.stop_event = threading.Event()


            
            print(f"� Using permanent WebSocket connection")
            
            # Create table window using permanent WebSocket data queue
            if self.app_context.ws_data_queue:
                self.tag_table_window = TagTableWindow(                               
                    self.app_context.ws_data_queue, 
                    self.stop_event, 
                    debug=self.debug
                )
            else:
                print("⚠️  App context ws_data_queue is None")
                self.tag_table_window = TagTableWindow(                               
                    queue.Queue(), 
                    self.stop_event, 
                    debug=self.debug
                )
            
            # Start the window in a separate thread
            table_thread = self.tag_table_window.run()
            
            print("✅ Tag table started in separate window")
            print("📋 The table will show:")
            print("   • EPC of detected tags")
            print("   • Number of reads per tag")
            print("   • Average, minimum and maximum RSSI")
            print("   • First and last seen times")
            print("   • Read rate per minute")
            print("   • Color coding for activity status:")
            print("     🟢 Active (< 2 seconds)")
            print("     🟡 Recent (< 10 seconds)")
            print("     🔴 Inactive (> 10 seconds)")
            print("\n💡 Available functions in window:")
            print("   • 🗑️ Clear Table: Remove all data")
            print("   • 💾 Export CSV: Save data in CSV format")
            print("\n⚠️  Monitoring stops automatically when returning to menu")
            
        except ImportError:
            print("❌ Error: tkinter not available")
            print("   Install tkinter to use the separate window")
        except Exception as e:
            print(f"❌ Error starting tag table: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def ensure_no_background_listeners(self):
        """Ensures there are no active WebSocket listeners in background"""
        try:
            listeners_stopped = False
            
            # 1. Stop main listener if active
            if hasattr(self, 'listener') and self.listener:
                try:
                    print("⚠️  Detected active WebSocket listener - forcing closure...")
                    # Use the new close() method to terminate the listener
                    if hasattr(self.listener, 'close'):
                        self.listener.close()
                    else:
                        # Only stop the thread, do NOT close permanent WebSocket
                        if hasattr(self.listener, 'stop_event') and self.listener.stop_event:
                            self.listener.stop_event.set()
                        # Wait for thread to finish without closing WebSocket
                        if hasattr(self.listener, 'join'):
                            self.listener.join(timeout=2)
                    listeners_stopped = True
                except Exception as e:
                    print(f"⚠️  Error closing main listener: {e}")
                finally:
                    self.listener = None  # Reset in any case
            
            # 2. Stop main stop_event if active
            if hasattr(self, 'stop_event') and self.stop_event and not self.stop_event.is_set():
                print("⚠️  Detected active stop event - forcing closure...")
                self.stop_event.set()
                listeners_stopped = True
                time.sleep(0.2)  # Pause for propagation
                self.stop_event = None
            
            # 3. Stop ATR7000 listener if active (maximum priority)
            if hasattr(self, 'atr7000_listener') and self.atr7000_listener:
                try:
                    print("⚠️  Detected active ATR7000 listener - forcing closure...")
                    # Use the new close() method if available
                    if hasattr(self.atr7000_listener, 'close'):
                        self.atr7000_listener.close()
                    else:
                        # Only stop the thread, do NOT close permanent WebSocket
                        if hasattr(self.atr7000_listener, 'stop'):
                            self.atr7000_listener.stop()
                        if hasattr(self.atr7000_listener, 'join'):
                            self.atr7000_listener.join(timeout=2)
                    listeners_stopped = True
                except Exception as e:
                    print(f"⚠️  Error closing ATR7000: {e}")
                finally:
                    self.atr7000_listener = None
            
            # 4. Close table window if open
            if hasattr(self, 'tag_table_window') and self.tag_table_window:
                if hasattr(self.tag_table_window, 'running') and self.tag_table_window.running:
                    print("⚠️  Detected active table window - forcing closure...")
                    try:
                        self.tag_table_window.on_closing()
                        listeners_stopped = True
                    except Exception as e:
                        print(f"⚠️  Error closing table: {e}")
                    finally:
                        self.tag_table_window = None
            
            # 5. Clean ALL queues if present
            for attr_name in ['data_queue']:
                if hasattr(self, attr_name):
                    queue_obj = getattr(self, attr_name)
                    if queue_obj:
                        try:
                            queue_size = queue_obj.qsize()
                            if queue_size > 0:
                                print(f"⚠️  Emptying {queue_size} messages from {attr_name}...")
                                while not queue_obj.empty():
                                    queue_obj.get_nowait()
                                listeners_stopped = True
                        except Exception as e:
                            print(f"⚠️  Queue cleanup error {attr_name}: {e}")
                        finally:
                            setattr(self, attr_name, None)
            
            if listeners_stopped:
                print("✅ Automatic cleanup completed successfully")
                time.sleep(1)  # Longer pause to allow complete closure
            else:
                print("ℹ️  No active listeners to close")
                
        except Exception as e:
            print(f"⚠️  Error during automatic cleanup: {e}")
            # Forced reset in case of error
            try:
                self.listener = None
                self.atr7000_listener = None
                self.stop_event = None
                self.data_queue = None
                self.tag_table_window = None
                print("✅ Forced reset completed")
            except:
                pass
    
    def cleanup_all_resources(self):
        """Cleans all resources before application shutdown"""
        import time  # Explicit import to ensure availability in function scope
        print("🧹 Resource cleanup in progress...")
        
        try:
            # 1. Stop all stop events
            if self.stop_event:
                print("   ⏹️  Stopping WebSocket events...")
                self.stop_event.set()
            
            # 2. Clean listener reference (do NOT close permanent WebSocket)
            if self.listener:
                print("   🔌 Stopping monitoring thread...")
                # Wait for listener thread to finish, but do NOT close WebSocket
                if hasattr(self.listener, 'join'):
                    self.listener.join(timeout=2)
            
            # 3. Close ATR7000 listener if present
            if hasattr(self, 'atr7000_listener') and self.atr7000_listener:
                print("   📍 Closing ATR7000 listener...")
                if hasattr(self.atr7000_listener, 'stop'):
                    self.atr7000_listener.stop()
            
            # 4. Close tag table window
            if self.tag_table_window and hasattr(self.tag_table_window, 'running') and self.tag_table_window.running:
                print("   📋 Closing tag table window...")
                try:
                    # Use after() to close in tkinter main thread
                    if hasattr(self.tag_table_window, 'root') and self.tag_table_window.root:
                        self.tag_table_window.root.after(0, self.tag_table_window.on_closing)
                        # Wait a moment for closure
                        time.sleep(0.5)
                except Exception as e:
                    print(f"   ⚠️  Error closing table: {e}")
            
            # 5. Close plotters if present
            # If there are open matplotlib windows, close them
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
            
            # 6. Clean queues
            if hasattr(self, 'data_queue') and self.data_queue:
                print("   🗑️  Emptying data queues...")
                try:
                    while not self.data_queue.empty():
                        self.data_queue.get_nowait()
                except:
                    pass
            
            # 7. Disconnect from reader
            if self.app_context and self.app_context.is_connected():
                print("   🔌 Disconnecting from reader...")
                try:
                    self.app_context.disconnect()
                except:
                    pass
            
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")
        
        # Wait a moment to allow all threads to close
        time.sleep(1)
    
    def run(self):
        """Main loop of the interactive CLI"""
        import time  # Explicit import to ensure availability in function scope
        print("🚀 Starting XRFID CLI...")
        time.sleep(1)
        command_map = {
            'l': self.handle_login_connect, 'login': self.handle_login_connect,
            'd': self.handle_disconnect, 'disconnect': self.handle_disconnect,
            's': self.handle_start_scan, 'start': self.handle_start_scan,
            'x': self.handle_stop_scan, 'stop': self.handle_stop_scan,
            'w': self.startWebsocket, 'websocket': self.startWebsocket,
            'r': self.handle_api_submenu, 'restapi': self.handle_api_submenu,
            'm': self.handle_unified_monitoring, 'monitoring': self.handle_unified_monitoring,
            'p': self.handle_plot_live_gui_enhanced, 'plot': self.handle_plot_live_gui_enhanced,
            'a': self.handle_atr7000_submenu, 'atr': self.handle_atr7000_submenu,
            'i': self.handle_iotc_setup_ws, 'iotc': self.handle_iotc_setup_ws,
            'di': self.handle_iotc_disconnect, 'disconnectIOTC': self.handle_iotc_disconnect,
            'c': lambda: None, 'clear': lambda: None,
            'rs': self.handle_websocket_reset, 'reset': self.handle_websocket_reset,
            'h': self.show_help, 'help': self.show_help,
            'q': self._quit, 'quit': self._quit
        }
        while self.running:
            try:
                self.ensure_no_background_listeners()
                self.clear_screen()
                self.show_header()
                self.show_menu()
                choice = self.get_user_input()
                
                # Handle parameterized IOTC commands first
                if (choice.startswith('i ') and choice.split()[0] == 'i') or (choice.startswith('iotc ') and choice.split()[0] == 'iotc'):
                    self.handle_parameterized_iotc_setup(choice)
                else:
                    action = command_map.get(choice)
                    if action:
                        action()
                    else:
                        print(f"\n❌ Invalid command or shortcut '{choice}'")
                        input("⏸️  Press ENTER to continue...")
            except KeyboardInterrupt:
                print("\n\n👋 User requested exit")
                self.running = False
                self.cleanup_all_resources()
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("⏸️  Press ENTER to continue...")
                self.cleanup_all_resources()

    def _quit(self):
        print("\n👋 Closing CLI...")
        self.cleanup_all_resources()
        self.running = False

    def startWebsocket(self):
        """Opens WebSocket (if not already open) and prints read tags until ENTER is pressed."""
        if not self.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return

        # Ensure WebSocket is running (start if needed)
        if not self.app_context.ensure_websocket_running():
            print("❌ Failed to start WebSocket connection")
            input("\n⏸️  Press ENTER to continue...")
            return

        print("🔌 WebSocket connection active and ready.")

        print("🎧 Listening for tag events. Press ENTER to stop.")
        print("--------------------------------------------------")

        import threading
        import sys
        stop_event = threading.Event()

        def input_thread():
            input()
            stop_event.set()

        t = threading.Thread(target=input_thread)
        t.daemon = True
        t.start()

        try:
            while not stop_event.is_set():
                data = self.app_context.get_websocket_data()
                if data:
                    # Simple tag display
                    if isinstance(data, dict) and 'data' in data:
                        tag_data = data['data']
                        tag_id = tag_data.get('idHex', 'N/A')
                        rssi = tag_data.get('peakRssi', 'N/A')
                        antenna = tag_data.get('antenna', 'N/A')
                        timestamp = data.get('timestamp', 'N/A')
                        print(f"📡 Tag: {tag_id} | RSSI: {rssi}dBm | Ant: {antenna} | Time: {timestamp}")
                import time
                time.sleep(0.1)
        except Exception as e:
            print(f"❌ Error during WebSocket listening: {e}")

        print("⏹️  WebSocket listening stopped.")
        input("\n⏸️  Press ENTER to continue...")

    def handle_atr7000_submenu(self):
        """Delegates ATR menu handling to the separate AtrSubmenu class."""
        self.ensure_no_background_listeners()
        if not hasattr(self, 'atr_submenu'):
            from zebra_cli.atr_submenu import AtrSubmenu
            self.atr_submenu = AtrSubmenu(self)
        self.atr_submenu.handle_submenu()
    
    def handle_parameterized_iotc_setup(self, command: str):
        """Handles parameterized IOTC setup commands"""
        # Parse command and parameters
        parts = command.split()
        
        if len(parts) == 1:
            # No parameters, use default behavior
            self.handle_iotc_setup_ws()
            return
        
        param_parts = parts[1:]  # Remove the command part, keep only parameters
        
        # Parse parameters
        try:
            params = self._parse_command_parameters(param_parts)
        except ValueError as e:
            print(f"\n❌ Parameter error: {e}")
            print("💡 Usage examples:")
            print("   i -type ws")
            print("   i -type mqtt -hostname broker.example.com -readername Reader1 -endpointname MQTT_EP")
            input("⏸️  Press ENTER to continue...")
            return
        
        # Validate required parameters
        if 'type' not in params:
            print("\n❌ Required parameter 'type' is missing")
            print("💡 Usage: i -type <ws|mqtt> [additional parameters]")
            input("⏸️  Press ENTER to continue...")
            return
        
        setup_type = params['type']
        
        if setup_type not in ['ws', 'mqtt']:
            print(f"\n❌ Invalid type '{setup_type}'. Must be 'ws' or 'mqtt'")
            input("⏸️  Press ENTER to continue...")
            return
        
        if setup_type == 'mqtt':
            # Validate MQTT-specific required parameters
            required_mqtt_params = ['hostname', 'readername', 'endpointname']
            missing_params = []
            
            for param in required_mqtt_params:
                if param not in params or not params[param].strip():
                    missing_params.append(param)
            
            if missing_params:
                print(f"\n❌ Missing required MQTT parameters: {', '.join(missing_params)}")
                print("💡 Usage: i -type mqtt -hostname <broker> -readername <name> -endpointname <endpoint>")
                input("⏸️  Press ENTER to continue...")
                return
        
        # Execute setup based on type
        if setup_type == 'ws':
            self.handle_iotc_setup_ws()
        else:  # mqtt
            self.handle_iotc_setup_mqtt(
                host_name=params['hostname'],
                reader_name=params['readername'],
                endpoint_name=params['endpointname']
            )
    
    def _parse_command_parameters(self, param_parts: list[str]) -> dict[str, str]:
        """Parses command parameters in the format: -key value -key value..."""
        params = {}
        i = 0
        
        while i < len(param_parts):
            # Check if current part is a parameter flag (starts with -)
            if not param_parts[i].startswith('-'):
                raise ValueError(f"Expected parameter flag starting with '-', got '{param_parts[i]}'")
            
            # Extract parameter name (remove the -)
            param_name = param_parts[i][1:]
            
            # Check if we have a value for this parameter
            if i + 1 >= len(param_parts):
                raise ValueError(f"Parameter '-{param_name}' is missing a value")
            
            # Check if next part is not another flag
            if param_parts[i + 1].startswith('-'):
                raise ValueError(f"Parameter '-{param_name}' is missing a value (found another flag '{param_parts[i + 1]}')")
            
            # Store the parameter and its value
            value = param_parts[i + 1]
            params[param_name] = value
            i += 2
        
        return params

    def prompt_protocol(self) -> str:
        print("⚠️  Protocol not found in context. Please enter protocol (http or https).")
        while True:
            protocol = input("Protocol: ").strip()
            if protocol in ["http", "https"]:
                return protocol
            print("❌ Invalid protocol. Please enter 'http' or 'https'.")

    def _show_setup_results(self, completed: list, skipped: list, failed: list):
        """Shows the IOTC setup results"""
        print("\n" + "="*60)
        print("📊 IOTC SETUP RESULTS")
        print("="*60)
        
        if completed:
            print("✅ STEPS COMPLETED:")
            for step in completed:
                print(f"   • {step}")
        
        if skipped:
            print("\n⏭️  STEPS SKIPPED (already configured):")
            for step in skipped:
                print(f"   • {step}")
        
        if failed:
            print("\n❌ STEPS FAILED:")
            for step in failed:
                print(f"   • {step}")
            print("\n💡 Please check the reader configuration and try again")
        
        if not failed:
            print("\n🎉 IOTC SETUP COMPLETED SUCCESSFULLY!")
            print("🚀 Reader is ready for WebSocket connections!")
            print("💡 Next steps:")
            print("   • Use 'm' or 'w' command to start tag monitoring")
            print("   • Use 'di' command to disconnect from IOTC")
        else:
            print(f"\n⚠️  Setup completed with {len(failed)} error(s)")
            print("💡 Some features may not work correctly")

    def handle_iotc_disconnect(self):
        """Handle IOTC disconnection (Step 9)"""
        print("\n🔌 DISCONNECT FROM IOTC")
        print("-" * 40)
        
        if not IOTC_AVAILABLE:
            print("❌ IOTC modules not available")
            input("\n⏸️  Press ENTER to continue...")
            return
            
        if not self.app_context.ip_address:
            print("❌ Reader not connected")
            print("💡 Use 'l' to login first")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        if self.app_context.is_fxr90:
            print("💡 FXR90 detected - no need for disconnection procedure from IOTC")
            input("\n⏸️  Press ENTER to continue...")
            return

        try:
            print(f"📡 Disconnecting reader {self.app_context.ip_address} from IOTC...")
            print("⏳ This may take a few minutes...")

            disconnector = IOTCClient(debug=self.debug, ip_address=self.app_context.ip_address)
            if self.app_context.username and self.app_context.password:
                session_id = disconnector.xml_login(self.app_context.username, self.app_context.password)
            elif self.app_context.username is None:
                print("⚠️  No username provided - cannot disconnect")
                raise ValueError("Username is None")
            else:
                print("⚠️  No password provided - cannot disconnect")
                raise ValueError("Password is None")
            
            if not session_id:
                print("❌ Failed to establish session")
                input("\n⏸️  Press ENTER to continue...")
                return
                
            result = disconnector.disconnect_iotc(session_id)
            
            if result:
                print("✅ Successfully disconnected from IOTC!")
                print("🔌 Reader is now disconnected from IoT Connector")
            else:
                print("❌ Failed to disconnect from IOTC")
                print("💡 Check reader configuration and try again")
                
        except Exception as e:
            print(f"❌ Disconnection error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    # WEBSOCKET #
    
    def handle_iotc_setup_ws(self):
        """Handles intelligent IOTC setup - analyzes status and executes only necessary steps"""
        if not IOTC_AVAILABLE:
            print("\n❌ IOTC modules not available!")
            input("⏸️  Press ENTER to continue...")
            return
            
        print("\n🌐 IOT CONNECTOR (IOTC) INTELLIGENT SETUP")
        print("=" * 50)
        
        if not self.app_context.is_connected():
            print("❌ Not connected to reader!")
            print("   Please login first using 'l' command")
            input("⏸️  Press ENTER to continue...")
            return
        
        try:
            ip = self.app_context.ip_address
            print(f"📡 Analyzing IOTC status for: {ip}")
            print("🔍 Checking current configuration...")
            print()
            
            # Step-by-step intelligent setup
            if ip:
                if self.app_context.is_fxr90:
                    self._execute_iotc_fxr90_setup(ip, self.app_context.token)
                else:
                    self._execute_iotc_setup_ws(ip)
            else:
                print("⚠️ IP address is None")
                raise ValueError("IP address is None")

        except Exception as e:
            print(f"❌ Setup error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def _execute_iotc_setup_ws(self, ip: str):
        """Executes intelligent IOTC setup by analyzing status step by step"""
        steps_completed = []
        steps_skipped = []
        steps_failed = []
        session_id = None

        try:
            # PHASE 0: Preliminary Reader Enrollment Check, IOTC client creation and authentication
            print("\n🔍 PHASE 0: Preliminary Reader Enrollment Check")
            print("-" * 50)

            # Create IOTC client
            if self.app_context.protocol:
                client = IOTCClient(protocol=self.app_context.protocol, debug=self.debug, ip_address=ip)
            else:
                protocol = self.prompt_protocol()
                client = IOTCClient(protocol=protocol, debug=self.debug, ip_address=ip)

            # Try and get credentials from context
            username, password = self.app_context.get_stored_credentials()
            if not username or not password:
                print("⚠️  Credentials not found in context. Please enter username and password.")
                username = input("Username: ").strip()
                password = getpass.getpass("Password: ").strip()

            # Try login to obtain session_id
            try:
                session_id = client.xml_login(username, password)
                if not session_id:
                    raise Exception("Login returned None") 
                print(f"✅ Login successful - Session ID: {session_id[:20]}...")
            except Exception as e:
                print(f"❌ Login failed: {e}")
                steps_failed.append("0. Authentication")
                return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # Now check enrollment
            print("🔍 Checking current enrollment status...")

            is_enrolled = client.is_reader_enrolled(session_id)

            if is_enrolled:
                print("✅ Reader already enrolled in IOTC")
                steps_skipped.append("1. Reader Enrollment (already done)")
            else:
                print("⚠️  Reader not enrolled - will enroll later in sequence")

            # PHASE 1: Check if WebSocket Endpoint exists, if not we will create it
            print("\n🔍 PHASE 1: WebSocket Endpoint Configuration Check")
            print("-" * 50)

            wsep_exists = client.is_wsep_added(session_id)

            if wsep_exists:
                print("✅ WebSocket Endpoint already exists")
                steps_skipped.append("2. WebSocket Endpoint Creation (already exists)")
            else:
                print("📝 Creating WebSocket Endpoint...")
                wsep_added = client.add_wsep(session_id)
                if wsep_added:
                    print("✅ WebSocket Endpoint created successfully")
                    steps_completed.append("2. WebSocket Endpoint Creation")
                else:
                    print("❌ Failed to create WebSocket Endpoint")
                    steps_failed.append("2. WebSocket Endpoint Creation")
                    return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # Check if WebSocket endpoint is already mapped
            wsep_mapped = client.is_wsep_mapped(session_id)

            if wsep_mapped:
                print("✅ WebSocket Endpoint already mapped to reader")
                steps_skipped.append("3. WebSocket Endpoint Mapping (already done)")
            else:
                print("🔗 Mapping WebSocket Endpoint to reader...")
                # If not already mapped, Map WebSocket endpoint
                mapping_result = client.map_wsep(session_id)
                if mapping_result:
                    print("✅ WebSocket Endpoint mapped successfully")
                    steps_completed.append("3. WebSocket Endpoint Mapping")
                else:
                    print("❌ Failed to map WebSocket Endpoint")
                    steps_failed.append("3. WebSocket Endpoint Mapping")
                    return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # PHASE 2: Re-check enrollment and enroll if needed using the same client
            print("\n🔍 PHASE 2: Reader Enrollment Check (if needed)")
            print("-" * 50)

            if not is_enrolled:
                print("📝 Enrolling reader in IOTC...")
                # We need to check if it exists
                try:
                    enroll_result = client.enroll_reader(session_id)
                    if enroll_result:
                        print("✅ Reader enrolled successfully")
                        steps_completed.append("4. Reader Enrollment")
                    else:
                        print("❌ Failed to enroll reader")
                        steps_failed.append("4. Reader Enrollment")
                        return self._show_setup_results(steps_completed, steps_skipped, steps_failed)
                except ImportError:                    
                    print("❌ Failed to enroll reader. error while enrolling")
                    steps_failed.append("4. Reader Enrollment")
                    return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # PHASE 3: Check if there were errors in endpoint configuration steps and print result
            print("\n🔍 PHASE 3: IOTC Connection Status Check")
            print("-" * 50)
            print("\n🔍 Checking endpoint configuration completion...")
            
            if steps_failed:
                print(f"❌ STEPS FAILED - {len(steps_failed)} endpoint configuration step(s) failed:")
                for failed_step in steps_failed:
                    print(f"   • {failed_step}")
                print("💡 Resolve configuration issues before continuing")
                return self._show_setup_results(steps_completed, steps_skipped, steps_failed)
            
            print("✅ Endpoint configuration completed successfully!")
            print("🎯 All endpoints are ready for IOTC connection")

            # PHASE 4: IOTC Connection
            print("\n🌐 PHASE 4: IoT Connector Service Activation")
            print("-" * 50)
            print("💡 NOW that all endpoints are configured, we can activate the service")
            
            # Disconnect from previous IOTC connection to reconnect to the correct one            
            print("⏳ Disconnecting from IOTC service")
            result = client.disconnect_iotc(session_id)
            
            if result:
                print("✅ Successfully disconnected from IOTC!")
                print("🔌 Reader is now disconnected from IoT Connector")
            else:
                print("❌ Failed to disconnect from IOTC")
                print("💡 Check reader configuration and try again")

            # Extended stabilization time for IOTC service
            # This might not be needed if reader is fast enough to disconnect from IOTC but added for safety
            stabilization_time = 10  # This value may need adjustment based on testing
            print(f"⏳ Waiting {stabilization_time} seconds to allow the IOTC service to stabilize")
            # Countdown with updates every 10 seconds
            for remaining in range(stabilization_time, 0, -10):
                if remaining <= stabilization_time:
                    time.sleep(10)
                    if remaining > 10:
                        print(f"⏳ {remaining-10} seconds remaining... (IOTC is stabilizing)")
                else:
                    time.sleep(1)

            # Re-check connection status before attempting reconnection
            current_connection_status = client.is_iotc_connected(session_id)

            if current_connection_status:
                steps_skipped.append("5. IOTC Service Activation")
            else:
                print("🚀 Activating IoT Connector...")

                connect_result = client.connect_iotc(session_id)
                
                if connect_result:
                    print("✅ IoT Connector service activated successfully!")
                    steps_completed.append("5. IOTC Service Activation")
                else:
                    # Check for specific error: already connected
                    last_error = getattr(client, 'last_error', None)
                    error_str = str(last_error).lower() if last_error else ''
                    exc_type, exc_value, _ = sys.exc_info()
                    exc_str = str(exc_value).lower() if exc_value else ''
                    
                    if (
                        'already connected to cloud' in error_str or
                        '65535' in error_str or
                        'already connected to cloud' in exc_str or
                        '65535' in exc_str or
                        (last_error and hasattr(last_error, 'code') and str(getattr(last_error, 'code', '')).strip() == '65535')
                    ):
                        print("✅ Service already activated")
                        steps_skipped.append("5. IOTC Service Activation")
                    else:
                        print(f"❌ Failure during IoT Connector activation")
                        print(f"   Error: {last_error if last_error else exc_value}")
                        steps_failed.append("5. IOTC Service Activation")
                        return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # Extended stabilization time for IOTC service to reconnect from previous step
            stabilization_time = 30  # This value may need adjustment based on testing (usually longer than the disconnection time of step 4)
            print(f"⏳ Waiting {stabilization_time} seconds to allow the IOTC service to finish initializing…")
            print(f"💡 The IOTC service may take time to become fully operational")
            # Countdown with updates every 10 seconds
            for remaining in range(stabilization_time, 0, -10):
                if remaining <= stabilization_time:
                    time.sleep(10)
                    if remaining > 10:
                        print(f"⏳ {remaining-10} seconds remaining... (IOTC is initializing)")
                else:
                    time.sleep(1)

            # PHASE 5: Permanent WebSocket Activation with Controlled Timeout
            print("\n🔗 PHASE 5: Permanent WebSocket Activation")
            print("-" * 50)
            
            print(f"🔗 IOTC initialization period completed. Testing WebSocket connection...")
            
            # IMPORTANT: Verify reader is still responsive after IOTC setup
            print(f"🔍 Verifying reader responsiveness after IOTC activation...")
            try:
                reader_status = self.app_context.get_status()
                if reader_status:
                    print(f"✅ Reader is responsive and operational")
                else:
                    print(f"⚠️  Reader may be busy reconnecting finalizing IOTC setup - waiting additional time...")
                    time.sleep(15)  # Additional wait if reader seems busy
            except Exception as e:
                print(f"⚠️  Reader status check failed: {e} - proceeding with caution...")
            
            websocket_connected = False
            
            try:
                # IMPORTANT: Check current WebSocket state before any manipulation
                ws_status = self.app_context.get_websocket_status()

                if self.debug:
                    print(f"[DEBUG] Current WebSocket state before IOTC setup:")
                    print(f"   - Running: {ws_status['is_running']}")
                    print(f"   - Thread alive: {ws_status['thread_alive']}")
                    print(f"   - WebSocket connected: {ws_status['websocket_connected']}")
                    print(f"   - URI: {ws_status['configured_uri']}")
                
                # Stop any existing WebSocket connection first - COMPLETE cleanup
                if hasattr(self.app_context, 'ws_listener') and self.app_context.ws_listener:
                    print("🔄 Stopping any existing WebSocket connection...")
                    self.app_context.stop_websocket()
                    time.sleep(2)  # Longer wait to ensure complete cleanup
                    
                    # Verify cleanup was successful
                    ws_status_after = self.app_context.get_websocket_status()
                    if self.debug:
                        print(f"[DEBUG] WebSocket state after cleanup:")
                        print(f"   - Running: {ws_status_after['is_running']}")
                        print(f"   - Thread alive: {ws_status_after['thread_alive']}")
                
                # Simple WebSocket connection test
                print(f"🔍 Testing WebSocket endpoint...")

                self.app_context.start_websocket(debug=self.debug)
                time.sleep(3)  # Same wait time as login
                
                if self.app_context.is_websocket_running():                                                
                    print(f"✅ Permanent WebSocket connection established!")
                    steps_completed.append("6. WebSocket permanent connection established")
                    websocket_connected = True                           
                else:
                    print(f"⚠️  Failed to establish permanent WebSocket connection - IOTC service may need more time to initialize")
                    steps_failed.append("6. WebSocket permanent connection failed")
                    websocket_connected = False
                    
                    # Get detailed diagnostics about WHY it's not responding
                    ws_status = self.app_context.get_websocket_status()
                    if self.debug:
                        print(f"[DEBUG] WebSocket diagnostic information:")
                        print(f"   - Thread running: {ws_status['is_running']}")
                        print(f"   - Thread alive: {ws_status['thread_alive']}")
                        print(f"   - WebSocket connected: {ws_status['websocket_connected']}")
                        print(f"   - Current URI: {ws_status['configured_uri']}")

                    # Check if the thread is alive but not connected (connection closed immediately)
                    if ws_status['thread_alive'] and not ws_status['websocket_connected']:
                        print(f"🔍 WebSocket thread is alive but connection closed immediately")
                        print(f"💡 This usually means:")
                        print(f"   • IOTC service is not fully ready yet (needs more initialization time)")
                        print(f"   • WebSocket endpoint exists but service backend is still starting")
                        print(f"   • Network connectivity issues to the WebSocket endpoint")
                        print(f"💡 Recommendation: Wait a few minutes and try WebSocket monitoring (option 7-10)")
                    elif not ws_status['thread_alive']:
                        print(f"🔍 WebSocket thread failed to start or crashed immediately")
                        print(f"💡 This could indicate:")
                        print(f"   • Network configuration issues")
                        print(f"   • Reader WebSocket service not responding")
                        print(f"   • SSL/TLS configuration problems")
                        
            except Exception as e:
                print(f"❌ Error during WebSocket setup: {e}")
                steps_failed.append(f"6. WebSocket Error: {str(e)}")
            
            if self.debug:
                # IMPORTANT: Stop WebSocket if it's not properly connected to avoid background spam
                if not websocket_connected:
                    try:
                        time.sleep(1)  # Allow clean shutdown
                        print("✅ WebSocket stopped - no background reconnections")
                    except Exception as e:
                        print(f"⚠️  Error stopping WebSocket: {e}")
                else:
                    print("💡 WebSocket is active and ready for monitoring")

            steps_completed.append("7. Setup Complete")
            self._show_setup_results(steps_completed, steps_skipped, steps_failed)
            
        except Exception as e:
            print(f"❌ Error during WebSocket endpoint setup: {e}")
            steps_failed.append(f"Setup process (Error: {str(e)})")
            self._show_setup_results(steps_completed, steps_skipped, steps_failed)

    # MQTT #

    def handle_iotc_setup_mqtt(self, host_name: str, reader_name: str, endpoint_name: str):
        """Handles MQTT-specific IOTC setup with provided parameters"""
        if not IOTC_AVAILABLE:
            print("\n❌ IOTC modules not available!")
            input("⏸️  Press ENTER to continue...")
            return
            
        print("\n🌐 IOT CONNECTOR (IOTC) MQTT SETUP")
        print("=" * 50)
        
        if not self.app_context.is_connected():
            print("❌ Not connected to reader!")
            print("   Please login first using 'l' command")
            input("⏸️  Press ENTER to continue...")
            return
        
        try:
            ip = self.app_context.ip_address
            print(f"📡 Analyzing IOTC status for: {ip}")
            print("🔍 Checking current configuration...")
            print()
            
            # Step-by-step intelligent setup
            if ip:
                if self.app_context.is_fxr90:
                    self._execute_iotc_fxr90_setup(ip, self.app_context.token, host_name, reader_name, endpoint_name)
                else:
                    self._execute_iotc_setup_mqtt(ip, host_name, reader_name, endpoint_name)
            else:
                print("⚠️ IP address is None")
                raise ValueError("IP address is None")

        except Exception as e:
            print(f"❌ MQTT setup error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def _execute_iotc_setup_mqtt(self, ip: str, host_name: str, reader_name: str, endpoint_name: str):
        """Executes intelligent IOTC MQTT setup by analyzing status step by step"""
        steps_completed = []
        steps_skipped = []
        steps_failed = []
        session_id = None

        try:
            # PHASE 0: Preliminary Reader Enrollment Check, IOTC client creation and authentication
            print("\n🔍 PHASE 0: Preliminary Reader Enrollment Check")
            print("-" * 50)

            # Create IOTC client
            if self.app_context.protocol:
                client = IOTCClient(protocol=self.app_context.protocol, debug=self.debug, ip_address=ip)
            else:
                protocol = self.prompt_protocol()
                client = IOTCClient(protocol=protocol, debug=self.debug, ip_address=ip)

            # Try and get credentials from context
            username, password = self.app_context.get_stored_credentials()
            if not username or not password:
                print("⚠️  Credentials not found in context. Please enter username and password.")
                username = input("Username: ").strip()
                password = getpass.getpass("Password: ").strip()

            # Try login to obtain session_id
            try:
                session_id = client.xml_login(username, password)
                if not session_id:
                    raise Exception("Login returned None") 
                print(f"✅ Login successful - Session ID: {session_id[:20]}...")
            except Exception as e:
                print(f"❌ Login failed: {e}")
                steps_failed.append("0. Authentication")
                return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # Now check enrollment
            print("🔍 Checking current enrollment status...")

            is_enrolled = client.is_reader_enrolled(session_id)

            if is_enrolled:
                print("✅ Reader already enrolled in IOTC")
                steps_skipped.append("1. Reader Enrollment")
            else:
                print("📋 Reader not yet enrolled")
                print("💡 Reader will be enrolled to IOTC during setup")
                steps_completed.append("1. Reader Enrollment Status Check")

            # PHASE 1: Check if MQTT Endpoint with same name exists, if not we will create it
            print("\n🔗 PHASE 1: MQTT Endpoint Configuration")
            print("-" * 50)
            print(f"💡 Setting up MQTT endpoint with broker: {host_name}")
            print(f"💡 Reader name: {reader_name}")
            print(f"💡 Endpoint name: {endpoint_name}")

            # Check if MQTT endpoint already exists
            mqtt_exists = client.is_mqttep_added(session_id, endpoint_name)
            
            if mqtt_exists:
                print(f"✅ MQTT endpoint with name '{endpoint_name}' already exists")
                steps_skipped.append("2. MQTT Endpoint Creation")
            else:
                print(f"📋 MQTT endpoint with name '{endpoint_name}' does not exist")
                print(f"🚀 Creating MQTT endpoint...")
                
                # Create the MQTT endpoint
                mqtt_created = client.add_mqttep(session_id, reader_name, host_name, endpoint_name)
                
                if mqtt_created:
                    print(f"✅ MQTT endpoint '{endpoint_name}' created successfully!")
                    steps_completed.append("2. MQTT Endpoint Creation")
                else:
                    print(f"❌ Failed to create MQTT endpoint '{endpoint_name}'")
                    steps_failed.append("2. MQTT Endpoint Creation")
                    return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # Check if MQTT endpoint is mapped to data interface
            mqtt_mapped = client.is_mqttep_mapped(session_id, endpoint_name)
            
            if mqtt_mapped:
                print(f"✅ MQTT endpoint '{endpoint_name}' already mapped to data interface")
                steps_skipped.append("3. MQTT Endpoint Mapping")
            else:
                print(f"📋 MQTT endpoint '{endpoint_name}' not yet mapped")
                print(f"🚀 Mapping MQTT endpoint to data interface...")
                
                # If not already mapped, Map the MQTT endpoint
                mqtt_map_result = client.map_mqttep(session_id, endpoint_name)
                
                if mqtt_map_result:
                    print(f"✅ MQTT endpoint '{endpoint_name}' mapped successfully!")
                    steps_completed.append("3. MQTT Endpoint Mapping")
                else:
                    print(f"❌ Failed to map MQTT endpoint '{endpoint_name}'")
                    steps_failed.append("3. MQTT Endpoint Mapping")
                    return self._show_setup_results(steps_completed, steps_skipped, steps_failed)

            # PHASE 2: Re-check enrollment and enroll if needed using the same client
            print("\n🔍 PHASE 2: Reader Enrollment Check (if needed)")
            print("-" * 50)

            if not is_enrolled:
                print("📝 Enrolling reader in IOTC...")
                # We need to check if it exists
                try:
                    enroll_result = client.enroll_reader(session_id)
                    if enroll_result:
                        print("✅ Reader enrolled successfully")
                        steps_completed.append("6. Reader Enrollment")
                    else:
                        print("❌ Failed to enroll reader")
                        steps_failed.append("6. Reader Enrollment")
                        return self._show_setup_results(steps_completed, steps_skipped, steps_failed)
                except ImportError:                    
                    print("❌ Failed to enroll reader. error while enrolling")
                    steps_failed.append("6. Reader Enrollment")
                    return self._show_setup_results(steps_completed, steps_skipped, steps_failed)
            else:
                steps_skipped.append("4. Reader Enrollment (already enrolled)")

            # PHASE 3: IOTC Connection
            print("\n🌐 PHASE 3: IoT Connector Service Activation")
            print("-" * 50)
            print("💡 NOW that MQTT endpoint is configured, we can activate the service")
            
            # Disconnect from previous IOTC connection to reconnect to the correct one
            print("⏳ Disconnecting from IOTC service")    
            result = client.disconnect_iotc(session_id)
            
            if result:
                print("✅ Successfully disconnected from IOTC!")
                print("🔌 Reader is now disconnected from IoT Connector")
            else:
                print("❌ Failed to disconnect from IOTC")
                print("💡 Check reader configuration and try again")

            # Extended stabilization time for IOTC service
            # This might not be needed if reader is fast enough to disconnect from IOTC but added for safety
            stabilization_time = 10  # This value may need adjustment based on testing
            print(f"⏳ Waiting {stabilization_time} seconds to allow the IOTC service to stabilize")
            # Countdown with updates every 10 seconds
            for remaining in range(stabilization_time, 0, -10):
                if remaining <= stabilization_time:
                    time.sleep(10)
                    if remaining > 10:
                        print(f"⏳ {remaining-10} seconds remaining... (IOTC is stabilizing)")
                else:
                    time.sleep(1)

            # Re-check connection status before attempting reconnection
            current_connection_status = client.is_iotc_connected(session_id)

            if current_connection_status:
                print("✅ IOTC already connected")
                print("💡 The IoT Connector is already active")
                steps_skipped.append("5. IOTC Connection Status")
            else:
                print("📋 IOTC not yet connected")
                print("💡 IoT Connector service will be activated after the MQTT setup")
                steps_completed.append("5. IOTC Connection Status Check")

            if current_connection_status:
                steps_skipped.append("6. IOTC Service Activation")
            else:
                print("🚀 Activating IoT Connector...")
                
                connect_result = client.connect_iotc(session_id)
                
                if connect_result:
                    print("✅ IoT Connector service activated successfully!")
                    steps_completed.append("6. IOTC Service Activation")
                else:
                    # Check for specific error: already connected
                    last_error = getattr(client, 'last_error', None)
                    error_str = str(last_error).lower() if last_error else ''
                    exc_type, exc_value, _ = sys.exc_info()
                    exc_str = str(exc_value).lower() if exc_value else ''
                    
                    if (
                        'already connected to cloud' in error_str or
                        '65535' in error_str or
                        'already connected to cloud' in exc_str or
                        '65535' in exc_str or
                        (last_error and hasattr(last_error, 'code') and str(getattr(last_error, 'code', '')).strip() == '65535')
                    ):
                        print("✅ Service already activated")
                        steps_skipped.append("6. IOTC Service Activation")
                    else:
                        print(f"❌ Failure during IoT Connector activation")
                        print(f"   Error: {last_error if last_error else exc_value}")
                        steps_failed.append("6. IOTC Service Activation")
                        return self._show_setup_results(steps_completed, steps_skipped, steps_failed)
            
            # Extended stabilization time for IOTC service to reconnect from previous step
            stabilization_time = 30  # This value may need adjustment based on testing (usually longer than the disconnection time of step 4)
            print(f"⏳ Waiting {stabilization_time} seconds to allow the IOTC service to finish initializing…")
            print(f"💡 The IOTC service may take time to become fully operational")
            # Countdown with updates every 10 seconds
            for remaining in range(stabilization_time, 0, -10):
                if remaining <= stabilization_time:
                    time.sleep(10)
                    if remaining > 10:
                        print(f"⏳ {remaining-10} seconds remaining... (IOTC is initializing)")
                else:
                    time.sleep(1)

            # Setup completed
            print("\n🎉 MQTT IOTC SETUP COMPLETED!")
            print("-" * 50)
            print(f"✅ MQTT endpoint '{endpoint_name}' is configured and active")
            print(f"📡 Broker: {host_name}")
            print(f"🏷️  Reader: {reader_name}")
            print(f"🔗 Client ID: {reader_name}_client")
            print("💡 MQTT messages will be published to the configured broker")
            print("💡 Use 'di' command to disconnect from IOTC if needed")

            steps_completed.append("7. MQTT Setup Complete")
            self._show_setup_results(steps_completed, steps_skipped, steps_failed)
            
        except Exception as e:
            print(f"❌ Error during MQTT IOTC setup: {e}")
            steps_failed.append(f"MQTT Setup process (Error: {str(e)})")
            self._show_setup_results(steps_completed, steps_skipped, steps_failed)

    # FXR90 IOTC SETUP #

    def _execute_iotc_fxr90_setup(self, ip: str, token: Optional[str], host_name: Optional[str] = None, reader_name: Optional[str] = None, endpoint_name: Optional[str] = None):
        """Executes FXR90-specific setup by configuring WebSocket endpoint"""
        
        # Suppress SSL warnings for FXR90 self-signed certificates
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        if not token:
            print("❌ No authentication token available")
            return
        
        mqtt_setup = False
        if host_name and reader_name and endpoint_name:
            mqtt_setup = True

        print("\n🔧 FXR90 READER SETUP")
        print("=" * 30)
        print("💡 Detected FXR90 reader - using direct configuration approach")
        print()
        
        base_url = f"https://{ip}"
        verify_ssl = False  # Always False for FXR90 self-signed certificates
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # STEP 1: GET ENDPOINT CONFIG
        print("📋 STEP 1: Retrieving endpoint configuration...")
        
        config_url = f"{base_url}/cloud/config"
        
        try:
            config_response = requests.get(config_url, headers=headers, timeout=10, verify=verify_ssl)
            config_response.raise_for_status()
            config_data = config_response.json()
            
            # Extract endpointConfig from READER-GATEWAY section
            reader_gateway = config_data.get("READER-GATEWAY", {})
            endpoint_config = reader_gateway.get("endpointConfig", {})
            
            if endpoint_config:
                print("✅ Configuration retrieved successfully")
                
                # Check existing connections
                existing_connections = endpoint_config.get("data", {}).get("event", {}).get("connections", [])
                print(f"🔗 Found {len(existing_connections)} existing connection(s)")

                if mqtt_setup:
                    print("➕ Adding MQTT connections...")
                    
                    # Create complete MQTT endpoint configuration structure

                    # Data event connection for tag events
                    data_event_connection = {
                        "additionalOptions": {
                            "batching": None,
                            "retention": {
                                "maxEventRetentionTimeInMin": 500,
                                "maxNumEvents": 150000,
                                "throttle": 100
                            }
                        },
                        "description": "MQTT Endpoint set via CLI",
                        "name": endpoint_name,
                        "options": {
                            "additional": {
                                "cleanSession": True,
                                "clientId": reader_name,
                                "debug": False,
                                "keepAlive": 60,
                                "qos": 0,
                                "reconnectDelay": 1,
                                "reconnectDelayMax": 5
                            },
                            "basicAuthentication": {
                                "password": "admin",
                                "username": "admin"
                            },
                            "enableSecurity": False,
                            "endpoint": {
                                "hostName": host_name,
                                "port": 1883,
                                "protocol": "tcp"
                            },
                            "publishTopic": [
                                f"tevents/{reader_name}"
                            ],
                            "subscribeTopic": []
                        },
                        "type": "mqtt"
                    }
                    
                    # Control command response connection
                    control_connection = {
                        "additionalOptions": {
                            "batching": None,
                            "retention": {
                                "maxEventRetentionTimeInMin": 500,
                                "maxNumEvents": 150000,
                                "throttle": 100
                            }
                        },
                        "description": "MQTT Endpoint set via CLI",
                        "name": endpoint_name,
                        "options": {
                            "additional": {
                                "cleanSession": True,
                                "clientId": reader_name,
                                "debug": False,
                                "keepAlive": 60,
                                "qos": 0,
                                "reconnectDelay": 1,
                                "reconnectDelayMax": 5
                            },
                            "basicAuthentication": {
                                "password": "admin",
                                "username": "admin"
                            },
                            "enableSecurity": False,
                            "endpoint": {
                                "hostName": host_name,
                                "port": 1883,
                                "protocol": "tcp"
                            },
                            "publishTopic": [
                                f"crsp/{reader_name}"
                            ],
                            "subscribeTopic": [
                                f"ccmds/{reader_name}"
                            ]
                        },
                        "type": "mqtt"
                    }
                    
                    # Management connections
                    mgmt_response_connection = {
                        "additionalOptions": {
                            "batching": None,
                            "retention": {
                                "maxEventRetentionTimeInMin": 500,
                                "maxNumEvents": 150000,
                                "throttle": 100
                            }
                        },
                        "description": "MQTT Endpoint set via CLI",
                        "name": endpoint_name,
                        "options": {
                            "additional": {
                                "cleanSession": True,
                                "clientId": reader_name,
                                "debug": False,
                                "keepAlive": 60,
                                "qos": 0,
                                "reconnectDelay": 1,
                                "reconnectDelayMax": 5
                            },
                            "basicAuthentication": {
                                "password": "admin",
                                "username": "admin"
                            },
                            "enableSecurity": False,
                            "endpoint": {
                                "hostName": host_name,
                                "port": 1883,
                                "protocol": "tcp"
                            },
                            "publishTopic": [
                                f"mrsp/{reader_name}"
                            ],
                            "subscribeTopic": [
                                f"mcmds/{reader_name}"
                            ]
                        },
                        "type": "mqtt"
                    }

                    # Management event connection
                    mgmt_event_connection = {
                        "additionalOptions": {
                            "batching": None,
                            "retention": {
                                "maxEventRetentionTimeInMin": 500,
                                "maxNumEvents": 150000,
                                "throttle": 100
                            }
                        },
                        "description": "MQTT Endpoint set via CLI",
                        "name": endpoint_name,
                        "options": {
                            "additional": {
                                "cleanSession": True,
                                "clientId": reader_name,
                                "debug": False,
                                "keepAlive": 60,
                                "qos": 0,
                                "reconnectDelay": 1,
                                "reconnectDelayMax": 5
                            },
                            "basicAuthentication": {
                                "password": "admin",
                                "username": "admin"
                            },
                            "enableSecurity": False,
                            "endpoint": {
                                "hostName": host_name,
                                "port": 1883,
                                "protocol": "tcp"
                            },
                            "publishTopic": [
                                f"mevents/{reader_name}"
                            ],
                            "subscribeTopic": []
                        },
                        "type": "mqtt"
                    }

                    # Ensure all required structures exist and populate them
                    if "data" not in endpoint_config:
                        endpoint_config["data"] = {}
                    if "event" not in endpoint_config["data"]:
                        endpoint_config["data"]["event"] = {}
                    if "connections" not in endpoint_config["data"]["event"]:
                        endpoint_config["data"]["event"]["connections"] = []
                    if "batching" not in endpoint_config["data"]:
                        endpoint_config["data"]["batching"] = {}
                    if "retention" not in endpoint_config["data"]:
                        endpoint_config["data"]["retention"] = {}
                    
                    if "control" not in endpoint_config:
                        endpoint_config["control"] = {}
                    if "commandResponse" not in endpoint_config["control"]:
                        endpoint_config["control"]["commandResponse"] = {}
                    if "connections" not in endpoint_config["control"]["commandResponse"]:
                        endpoint_config["control"]["commandResponse"]["connections"] = []
                    
                    if "management" not in endpoint_config:
                        endpoint_config["management"] = {}
                    if "commandResponse" not in endpoint_config["management"]:
                        endpoint_config["management"]["commandResponse"] = {}
                    if "connections" not in endpoint_config["management"]["commandResponse"]:
                        endpoint_config["management"]["commandResponse"]["connections"] = []
                    if "event" not in endpoint_config["management"]:
                        endpoint_config["management"]["event"] = {}
                    if "connections" not in endpoint_config["management"]["event"]:
                        endpoint_config["management"]["event"]["connections"] = []

                    # Set all MQTT connections
                    endpoint_config["data"]["event"]["connections"] = [data_event_connection]
                    endpoint_config["control"]["commandResponse"]["connections"] = [control_connection]
                    endpoint_config["management"]["commandResponse"]["connections"] = [mgmt_response_connection]
                    endpoint_config["management"]["event"]["connections"] = [mgmt_event_connection]
                    
                    # Add data-level batching and retention sections
                    endpoint_config["data"]["batching"] = {
                        "maxPayloadSizePerReport": 0,
                        "reportingInterval": 0
                    }
                    
                    endpoint_config["data"]["retention"] = {
                        "maxEventRetentionTimeInMin": 0,
                        "maxNumEvents": 0,
                        "throttle": 1
                    }
                    
                    print(f"✅ MQTT connections added:")
                else:
                    print("➕ Adding WebSocket connection...")
                    # Add WebSocket connection to data.event.connections
                    websocket_connection = {
                        "additionalOptions": {
                            "batching": {
                                "maxPayloadSizePerReport": 0,
                                "reportingInterval": 0
                            },
                            "retention": {
                                "maxEventRetentionTimeInMin": 500,
                                "maxNumEvents": 150000,
                                "throttle": 100
                            }
                        },
                        "description": "WebSocket endpoint set via CLI",
                        "name": "WS",
                        "type": "WEBSOCKET",
                        "options": {
                            "security": {
                                "verifyPeer": False
                            }
                        }
                    }
                    
                    # Ensure the data.event.connections structure exists
                    if "data" not in endpoint_config:
                        endpoint_config["data"] = {}
                    if "event" not in endpoint_config["data"]:
                        endpoint_config["data"]["event"] = {}
                    if "connections" not in endpoint_config["data"]["event"]:
                        endpoint_config["data"]["event"]["connections"] = []
                    if "batching" not in endpoint_config["data"]:
                        endpoint_config["data"]["batching"] = {}
                    if "retention" not in endpoint_config["data"]:
                        endpoint_config["data"]["retention"] = {}

                    # Add the WebSocket connection
                    endpoint_config["data"]["event"]["connections"] = [websocket_connection]

                    # Add data-level batching and retention sections
                    endpoint_config["data"]["batching"] = {
                        "maxPayloadSizePerReport": 0,
                        "reportingInterval": 0
                    }
                    
                    endpoint_config["data"]["retention"] = {
                        "maxEventRetentionTimeInMin": 0,
                        "maxNumEvents": 0,
                        "throttle": 1
                    }

                    print("✅ WebSocket connection added")
            else:
                print("❌ No endpoint configuration found")
                return
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Configuration request failed: {e}")
            return
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse response: {e}")
            return

        # STEP 2: SET ENDPOINT CONFIG (only if changes were made
        print("\n🔧 STEP 2: Applying configuration changes...")   
        set_config_url = f"{base_url}/cloud"
        set_config_payload = {
            "command": "set_importCloudConfig",
            "command_id": "abdc123",
            "payload": {
                "endpointConfig": endpoint_config
            }
        }
        
        try:
            set_response = requests.post(set_config_url, json=set_config_payload, headers=headers, timeout=10, verify=verify_ssl)
            set_response.raise_for_status()
            set_data = set_response.json()
            
            if set_data.get("response") == "success":
                print("✅ Configuration updated successfully")
            else:
                print(f"❌ Configuration update failed: {set_data.get('response', 'Unknown error')}")
                return
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Configuration update failed: {e}")
            return
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse update response: {e}")
            return
        
        # Simplified countdown
        for remaining in range(15, 0, -5):
            time.sleep(5)
            if remaining > 5:
                print(f"⏳ {remaining-5} seconds remaining...")
        
        print("🔗 Testing connection...")
        
        # Verify reader responsiveness
        try:
            reader_status = self.app_context.get_status()
            if not reader_status:
                print("⚠️  Reader busy - waiting additional time...")
                time.sleep(30)
        except Exception as e:
            print(f"⚠️  Reader status check failed: {e}")
        
        if mqtt_setup:
            # Final status summary for MQTT
            print(f"\n🎉 FXR90 MQTT SETUP {'COMPLETED' if reader_status else 'PARTIALLY COMPLETED'}!")
            print("=" * 50)
            print("✨ Summary:")
            print("   1. ✅ Configuration retrieved")
            print("   2. ✅ MQTT connection added")
            print("   3. ✅ Configuration updated")
            print(f"   4. ✅ MQTT broker: {host_name}")
            print(f"   5. ✅ Client ID: {reader_name}")
            print(f"   6. ✅ Endpoint name: {endpoint_name}")
            print(f"   7. ✅ Topics: tevents, crsp, ccmds, mrsp, mcmds, mevents")
            print("💡 MQTT messages will be published to the configured broker")
            print("💡 Use 'di' command to disconnect from IOTC if needed")
            print("=" * 50)
        else:
            # STEP 3: WEBSOCKET CONNECTION START
            print("\n🔗 STEP 3: WebSocket Activation")
            
            # Wait for service to initialize  
            print("⏳ Initializing WebSocket service (15 seconds)...")

            websocket_connected = False
            
            try:
                # Stop any existing WebSocket connection
                if hasattr(self.app_context, 'ws_listener') and self.app_context.ws_listener:
                    print("🔄 Resetting WebSocket connection...")
                    self.app_context.stop_websocket()
                    time.sleep(2)
                
                # Start WebSocket connection
                print("🔍 Establishing WebSocket connection...")
                self.app_context.start_websocket(debug=self.debug)
                time.sleep(3)
                
                if self.app_context.is_websocket_running():
                    print("✅ WebSocket connection established!")
                    websocket_connected = True                
                else:
                    print("⚠️  WebSocket connection failed")
                    websocket_connected = False
                    
                    # Provide simplified diagnostics
                    ws_status = self.app_context.get_websocket_status()
                    if ws_status['thread_alive'] and not ws_status['websocket_connected']:
                        print("� Service may need more initialization time")
                        print("   Try WebSocket monitoring in a few minutes (w, m, p)")
                    elif not ws_status['thread_alive']:
                        print(" Network or configuration issue detected")
                        print("   Check reader connectivity and configuration")
                        
            except Exception as e:
                print(f"❌ WebSocket setup error: {e}")
                print("💡 You can manually start monitoring using 'w' or 'm' commands")
            
            # Final status summary
            print(f"\n🎉 FXR90 SETUP {'COMPLETED' if websocket_connected else 'PARTIALLY COMPLETED'}!")
            print("=" * 50)
            print("✨ Summary:")
            print("   1. ✅ Configuration retrieved")
            print("   2. ✅ WebSocket connection added")
            print("   3. ✅ Configuration updated")
            print(f"   4. {'✅' if websocket_connected else '⚠️ '} WebSocket {'active' if websocket_connected else 'needs retry'}")
            
            if websocket_connected:
                print("💡 Ready for monitoring - use commands: w, m, p")
            else:
                print("💡 Use 'w' or 'm' commands to retry WebSocket connection")
            print("=" * 50)
            
            # Cleanup if connection failed
            if not websocket_connected:
                try:
                    self.app_context.stop_websocket()
                except Exception:
                    pass
