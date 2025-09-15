"""
Persistent interactive CLI for Zebra RFID
"""
import os
import sys
import time
import json
import csv
import traceback
from typing import Optional
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import getpass
import requests
import urllib3
import queue
import threading
import numpy as np

from zebra_cli.context import AppContext
from zebra_cli.plotter import Plotter, EnhancedPlotter
from zebra_cli.tag_table_window import TagTableWindow
from zebra_cli.api_submenu import ApiSubmenu
from zebra_cli.atr_submenu import PositionPoint, PointDataStore, ATR7000PositionCalculator, RawDirectionalityMessage

# Optional dependencies with graceful fallbacks
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

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
        print(row("ex  / export       📤    Export collected data to pdf"))
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
        print("EXPORT FUNCTIONALITY:")
        print("  • Use 'ex' or 'export' to create PDF reports from recorded data")
        print("  • Exports CSV files from /record/tag_reads/ to PDF in /reports/")
        print("  • Includes RSSI graphs over time for each EPC")
        print("  • Requires matplotlib: pip install matplotlib")
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
                if MATPLOTLIB_AVAILABLE:
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
            'ex': self.handle_export_data, 'export': self.handle_export_data,
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
                time.sleep(0.1)
        except Exception as e:
            print(f"❌ Error during WebSocket listening: {e}")

        print("⏹️  WebSocket listening stopped.")
        input("\n⏸️  Press ENTER to continue...")

    def handle_atr7000_submenu(self):
        """Delegates ATR menu handling to the separate AtrSubmenu class."""
        self.ensure_no_background_listeners()
        if not hasattr(self, 'atr_submenu'):
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

    # Data Export #

    def handle_export_data(self):
        """Exports CSV data to PDF report with RSSI graphs for each EPC"""
        print("\n📤 EXPORT CSV DATA TO PDF REPORT")
        print("-" * 40)
        
        try:
            # Get project root directory
            project_root = os.path.dirname(os.path.dirname(__file__))
            tag_reads_dir = os.path.join(project_root, 'record', 'tag_reads')
            messages_dir = os.path.join(project_root, 'record', 'messages')
            reports_dir = os.path.join(project_root, 'reports')
            
            # Check if tag_reads directory exists
            if not os.path.exists(tag_reads_dir):
                print("❌ No tag reads directory found")
                print(f"   Expected: {tag_reads_dir}")
                print("💡 Record some data first using monitoring commands")
                input("\n⏸️  Press ENTER to continue...")
                return
            
            # Get list of CSV files in tag_reads directory
            csv_files = [f for f in os.listdir(tag_reads_dir) if f.endswith('.csv')]
            
            if not csv_files:
                print("❌ No CSV files found in tag reads directory")
                print(f"   Directory: {tag_reads_dir}")
                print("💡 Record some data first using monitoring commands")
                input("\n⏸️  Press ENTER to continue...")
                return
            
            # Sort files by name (newest first due to timestamp format)
            csv_files.sort(reverse=True)
            
            # Display available files
            print("📋 Available CSV files for export:")
            print("-" * 35)
            for i, filename in enumerate(csv_files, 1):
                # Extract timestamp from filename for display
                if 'tags_read_' in filename:
                    timestamp_part = filename.replace('tags_read_', '').replace('.csv', '')
                    try:
                        # Parse timestamp to readable format
                        dt = datetime.strptime(timestamp_part, '%Y%m%d_%H%M%S')
                        readable_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                        print(f"  {i}. {filename} ({readable_time})")
                    except:
                        print(f"  {i}. {filename}")
                else:
                    print(f"  {i}. {filename}")
            
            # Get user choice
            while True:
                try:
                    choice = input(f"\n📝 Select file to export (1-{len(csv_files)}): ").strip()
                    if not choice:
                        print("❌ Export cancelled")
                        input("\n⏸️  Press ENTER to continue...")
                        return
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(csv_files):
                        selected_file = csv_files[choice_idx]
                        break
                    else:
                        print(f"❌ Please enter a number between 1 and {len(csv_files)}")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            print(f"\n✅ Selected: {selected_file}")
            
            # Generate PDF report
            self._generate_pdf_report(selected_file, tag_reads_dir, messages_dir, reports_dir)
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            if self.debug:
                traceback.print_exc()
        
        input("\n⏸️  Press ENTER to continue...")
    
    def _generate_pdf_report(self, csv_filename: str, tag_reads_dir: str, messages_dir: str, reports_dir: str):
        """Generates PDF report from CSV data with RSSI graphs"""
        try:
            # Check if matplotlib is available for PDF generation
            if not MATPLOTLIB_AVAILABLE:
                print("❌ Missing required library: matplotlib")
                print("💡 Install required packages: pip install matplotlib")
                return
            
            # Create reports directory if it doesn't exist
            os.makedirs(reports_dir, exist_ok=True)
            
            # Extract timestamp from filename to find corresponding messages file
            timestamp_part = csv_filename.replace('tags_read_', '').replace('.csv', '')
            messages_filename = f"messages_read_{timestamp_part}.csv"
            messages_path = os.path.join(messages_dir, messages_filename)
            
            # Generate PDF filename with report_ prefix and timestamp
            pdf_filename = f"report_{timestamp_part}.pdf"
            pdf_path = os.path.join(reports_dir, pdf_filename)
            
            print(f"📊 Generating PDF report: {pdf_filename}")
            print(f"🔍 Reading tag data from: {csv_filename}")
            print(f"🔍 Reading message data from: {messages_filename}")
            
            # Read tag data
            tag_data = {}
            tags_path = os.path.join(tag_reads_dir, csv_filename)
            
            with open(tags_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    epc = row['EPC']
                    tag_data[epc] = {
                        'reads': int(row['Reads']),
                        'avg_rssi': float(row['Avg_RSSI']),
                        'min_rssi': float(row['Min_RSSI']),
                        'max_rssi': float(row['Max_RSSI']),
                        'first_seen': row['First_Seen'],
                        'last_seen': row['Last_Seen'],
                        'rate_per_minute': float(row['Rate_Per_Minute'])
                    }
            
            print(f"📋 Found {len(tag_data)} unique tags in dataset")
            
            # Read messages data to extract RSSI over time and antenna counts for each EPC
            epc_rssi_data = {}
            epc_antenna_counts = {}
            epc_antenna_rssi_stats = {}  # {epc: {antenna_id: {'min': val, 'max': val, 'sum': val, 'count': count}}}
            
            if os.path.exists(messages_path):
                # Detect if this is an ATR7000 reader
                is_atr_reader = self._is_messages_csv_from_atr(messages_path)
                reader_type = "ATR7000" if is_atr_reader else "Standard RFID"
                print(f"� Detected {reader_type} reader from message data")
                
                if is_atr_reader:
                    print("�📡 Processing message data for RSSI graphs (ATR7000 - antenna analysis skipped)")
                else:
                    print("📡 Processing message data for RSSI graphs and antenna analysis...")
            
                with open(messages_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            # Parse the raw JSON message
                            raw_json = row['Raw_JSON']
                            message_data = json.loads(raw_json)
                            
                            # Extract tag data from message
                            if isinstance(message_data, dict) and 'data' in message_data:
                                msg_tag_data = message_data['data']
                                if isinstance(msg_tag_data, dict) and 'idHex' in msg_tag_data:
                                    epc = msg_tag_data['idHex']
                                    rssi = msg_tag_data.get('peakRssi', msg_tag_data.get('rssi'))
                                    antenna = msg_tag_data.get('antenna')
                                    
                                    if epc in tag_data:  # Only process if this EPC is in our tag data
                                        # Process RSSI data for graphs
                                        if rssi is not None:
                                            try:
                                                rssi_value = float(rssi)
                                                timestamp_str = row['Timestamp']
                                                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                                                
                                                if epc not in epc_rssi_data:
                                                    epc_rssi_data[epc] = {'timestamps': [], 'rssi_values': []}
                                                
                                                epc_rssi_data[epc]['timestamps'].append(timestamp)
                                                epc_rssi_data[epc]['rssi_values'].append(rssi_value)
                                            except (ValueError, TypeError):
                                                pass  # Skip invalid RSSI values
                                        
                                        # Process antenna count and RSSI statistics data (only for non-ATR readers)
                                        if not is_atr_reader and antenna is not None:
                                            try:
                                                antenna_id = int(antenna)
                                                
                                                # Initialize antenna counts data structure
                                                if epc not in epc_antenna_counts:
                                                    epc_antenna_counts[epc] = {}
                                                if antenna_id not in epc_antenna_counts[epc]:
                                                    epc_antenna_counts[epc][antenna_id] = 0
                                                
                                                # Update antenna read count
                                                epc_antenna_counts[epc][antenna_id] += 1
                                                
                                                # Process RSSI statistics if available
                                                if rssi is not None:
                                                    try:
                                                        rssi_value = float(rssi)
                                                        
                                                        # Initialize RSSI stats data structure
                                                        if epc not in epc_antenna_rssi_stats:
                                                            epc_antenna_rssi_stats[epc] = {}
                                                        if antenna_id not in epc_antenna_rssi_stats[epc]:
                                                            epc_antenna_rssi_stats[epc][antenna_id] = {
                                                                'min': rssi_value,
                                                                'max': rssi_value,
                                                                'sum': 0,
                                                                'count': 0
                                                            }
                                                        
                                                        # Update RSSI statistics
                                                        stats = epc_antenna_rssi_stats[epc][antenna_id]
                                                        stats['min'] = min(stats['min'], rssi_value)
                                                        stats['max'] = max(stats['max'], rssi_value)
                                                        stats['sum'] += rssi_value
                                                        stats['count'] += 1
                                                        
                                                    except (ValueError, TypeError):
                                                        pass  # Skip invalid RSSI values
                                                
                                            except (ValueError, TypeError):
                                                pass  # Skip invalid antenna values
                                                
                        except (json.JSONDecodeError, KeyError):
                            continue
            else:
                print(f"⚠️  Messages file not found: {messages_filename}")
                print("📊 Will generate report without RSSI graphs and antenna analysis")
                is_atr_reader = False  # Default to non-ATR behavior when no messages file
            
            # Process ATR7000 position data if this is an ATR reader
            atr_point_store = None
            if is_atr_reader and os.path.exists(messages_path):
                try:
                    print("📍 Processing ATR7000 position data for XY variation analysis...")
                    atr_point_store = self.process_atr7000_messages_csv(messages_path)
                    if atr_point_store:
                        print(f"✅ ATR7000 position data processed successfully")
                    else:
                        print("⚠️  No position data found in ATR7000 messages")
                except Exception as e:
                    print(f"⚠️  Error processing ATR7000 position data: {e}")
                    if self.debug:
                        traceback.print_exc()
            
            # Generate PDF report
            print("📄 Creating PDF report...")
            
            with PdfPages(pdf_path) as pdf:
                # Title page
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')
                
                # Title
                ax.text(0.5, 0.9, 'RFID Tag Analysis Report', 
                       ha='center', va='center', fontsize=24, fontweight='bold')
                
                # Source files information (left aligned)
                source_files_text = f'Generated from:\n  • Tag data: {csv_filename}\n  • Message data: {messages_filename}'
                ax.text(0.1, 0.82, source_files_text, 
                       ha='left', va='top', fontsize=12)
                
                # Generation time (left aligned with vertical spacing)
                generation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ax.text(0.1, 0.72, f'Report generated: {generation_time}', 
                       ha='left', va='center', fontsize=12)
                
                # Summary statistics
                total_tags = len(tag_data)
                total_reads = sum(data['reads'] for data in tag_data.values())
                avg_rssi_overall = sum(data['avg_rssi'] for data in tag_data.values()) / total_tags if total_tags > 0 else 0
                
                summary_text = f"""Summary Statistics:
• Total Unique Tags: {total_tags}
• Total Read Events: {total_reads:,}
• Average RSSI: {avg_rssi_overall:.1f} dBm
• Data Collection Period: {tag_data[list(tag_data.keys())[0]]['first_seen'] if tag_data else 'N/A'} 
  to {tag_data[list(tag_data.keys())[0]]['last_seen'] if tag_data else 'N/A'}"""
                
                ax.text(0.1, 0.55, summary_text, ha='left', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray"))
                
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
                
                # Generate page(s) for each EPC
                for i, (epc, data) in enumerate(tag_data.items(), 1):
                    print(f"📊 Processing EPC {i}/{len(tag_data)}: {epc[:16]}...")
                    
                    # Generate Page 1: Statistics and RSSI graph (same for all readers)
                    self._generate_stats_and_rssi_page(
                        epc, data, epc_rssi_data, is_atr_reader, 
                        epc_antenna_counts, epc_antenna_rssi_stats, pdf
                    )
                    
                    # Generate Page 2: Position graphs (only for ATR readers with position data)
                    if is_atr_reader and atr_point_store is not None:
                        print(f"📍 Generating position graphs page for EPC: {epc[:16]}...")
                        self._generate_position_graphs_page(epc, atr_point_store, pdf)
            
            print(f"✅ PDF report generated successfully!")
            print(f"📄 Report saved: {pdf_path}")
            print(f"📊 {len(tag_data)} tags processed with detailed analysis")
            
        except ImportError as e:
            print(f"❌ Missing required library: {e}")
            print("💡 Install required packages: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            if self.debug:
                traceback.print_exc()

    def _generate_stats_and_rssi_page(self, epc: str, data: dict, epc_rssi_data: dict, 
                                     is_atr_reader: bool, epc_antenna_counts: dict, 
                                     epc_antenna_rssi_stats: dict, pdf):
        """
        Generates the first page with tag statistics and RSSI graph (same for all readers).
        
        Args:
            epc: EPC identifier
            data: Tag statistics data
            epc_rssi_data: RSSI time series data
            is_atr_reader: Whether this is an ATR7000 reader
            epc_antenna_counts: Antenna count data
            epc_antenna_rssi_stats: Antenna RSSI statistics
            pdf: PdfPages object to save the figure
        """
        try:
            # Create 3-section layout for better spacing
            fig = plt.figure(figsize=(8.5, 11))
            gs = fig.add_gridspec(3, 1, height_ratios=[1, 2, 0.5], hspace=0.3)
            
            # EPC Header
            fig.suptitle(f'Tag Analysis: {epc}', fontsize=16, fontweight='bold', y=0.95)
            
            # Statistics section
            ax1 = fig.add_subplot(gs[0])
            ax1.axis('off')
            
            # Build antenna counts and RSSI statistics text (only for non-ATR readers)
            antenna_text = ""
            if not is_atr_reader:
                if epc in epc_antenna_counts and epc_antenna_counts[epc]:
                    antenna_counts = epc_antenna_counts[epc]
                    # Sort antenna IDs for consistent display
                    sorted_antennas = sorted(antenna_counts.keys())
                    antenna_lines = []
                    for ant_id in sorted_antennas:
                        count = antenna_counts[ant_id]
                        
                        # Check if we have RSSI statistics for this antenna
                        rssi_info = ""
                        if (epc in epc_antenna_rssi_stats and 
                            ant_id in epc_antenna_rssi_stats[epc] and
                            epc_antenna_rssi_stats[epc][ant_id]['count'] > 0):
                            
                            stats = epc_antenna_rssi_stats[epc][ant_id]
                            avg_rssi = stats['sum'] / stats['count']
                            min_rssi = stats['min']
                            max_rssi = stats['max']
                            rssi_info = f" (RSSI: {avg_rssi:.1f} avg, {min_rssi:.1f}/{max_rssi:.1f} min/max)"
                        
                        antenna_lines.append(f"  - Antenna {ant_id}: {count:,} reads{rssi_info}")
                    antenna_text = "\n• Reads by Antenna:\n" + "\n".join(antenna_lines)
                else:
                    antenna_text = "\n• Reads by Antenna: No antenna data available"
            
            stats_text = f"""
Tag Statistics:
• EPC: {epc}
• Total Reads: {data['reads']:,}
• Average RSSI: {data['avg_rssi']:.1f} dBm
• Min/Max RSSI: {data['min_rssi']:.1f} / {data['max_rssi']:.1f} dBm
• First Seen: {data['first_seen']}
• Last Seen: {data['last_seen']}
• Read Rate: {data['rate_per_minute']:.1f} reads/minute{antenna_text}
            """
            
            ax1.text(0.1, 0.8, stats_text, fontsize=11, va='top',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue"))
            
            # Add a little bit of spacing
            ax1.text(0.1, 0.1, " ", fontsize=11, va='top')
            
            # RSSI over time graph (section 2)
            if epc in epc_rssi_data and epc_rssi_data[epc]['timestamps']:
                ax2 = fig.add_subplot(gs[1])
                
                timestamps = epc_rssi_data[epc]['timestamps']
                rssi_values = epc_rssi_data[epc]['rssi_values']
                
                # Sort by timestamp
                sorted_data = sorted(zip(timestamps, rssi_values))
                timestamps, rssi_values = zip(*sorted_data)
                
                ax2.plot(timestamps, rssi_values, 'b-', linewidth=0.5, alpha=0.3)
                ax2.scatter(timestamps, rssi_values, c='red', s=5, alpha=0.5)

                # Calculate and plot smooth curve
                # Savitzky-Golay Filter
                smooth_info = self._calculate_smooth_curve_savgol(list(timestamps), list(rssi_values))

                if smooth_info:
                    ax2.plot(smooth_info['timestamps'], smooth_info['coordinates'], 
                            'green', linewidth=2, linestyle='-', label='RSSI Smooth', alpha=1)
                    # Only show legend when we have labeled smooth curve
                    ax2.legend(fontsize=9)

                ax2.set_xlabel('Time')
                ax2.set_ylabel('RSSI (dBm)')
                ax2.set_title('RSSI Over Time')
                ax2.grid(True, alpha=0.3)
                
                # Format x-axis with adaptive interval based on data time span
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                
                # Calculate time span from tag data to choose appropriate locator
                try:
                    # Try parsing with microseconds first, then without if it fails
                    try:
                        first_seen = datetime.strptime(data['first_seen'], '%Y-%m-%d %H:%M:%S.%f')
                        last_seen = datetime.strptime(data['last_seen'], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        # Fallback to format without microseconds
                        first_seen = datetime.strptime(data['first_seen'], '%Y-%m-%d %H:%M:%S')
                        last_seen = datetime.strptime(data['last_seen'], '%Y-%m-%d %H:%M:%S')
                    
                    time_span_seconds = (last_seen - first_seen).total_seconds()
                    
                    # Choose appropriate time axis interval based on data duration (time axis markers)
                    if time_span_seconds <= 10:  # ≤ 10 seconds: show every second
                        ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
                    elif time_span_seconds <= 30:  # ≤ 30 seconds: show every 5 seconds
                        ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
                    elif time_span_seconds <= 120:  # ≤ 2 minutes: show every 15 seconds
                        ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=15))
                    elif time_span_seconds <= 300:  # ≤ 5 minutes: show every 30 seconds
                        ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
                    elif time_span_seconds <= 900:  # ≤ 15 minutes: show every minute
                        ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
                    elif time_span_seconds <= 3600:  # ≤ 1 hour: show every 5 minutes
                        ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
                    else:  # > 1 hour: show every 15 minutes
                        ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
                        
                except (ValueError, TypeError) as e:
                    # Fallback to adaptive approach based on data points if timestamp parsing fails
                    if len(timestamps) > 10:
                        ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=max(1, len(timestamps)//6)))
                    else:
                        ax2.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
                
                plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
                
                # Add statistics to graph
                stats_box = f'Avg: {data["avg_rssi"]:.1f}dBm\nMin: {data["min_rssi"]:.1f}dBm\nMax: {data["max_rssi"]:.1f}dBm'
                ax2.text(0.02, 0.98, stats_box, transform=ax2.transAxes, fontsize=9,
                        verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
            else:
                ax2 = fig.add_subplot(gs[1])
                ax2.text(0.5, 0.5, 'No RSSI time-series data available\nfor this EPC', 
                        ha='center', va='center', fontsize=12,
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.axis('off')
            
            # Note: Custom GridSpec layout eliminates need for plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            
        except Exception as e:
            print(f"❌ Error generating stats and RSSI page for EPC {epc}: {e}")
            if hasattr(self, 'debug') and self.debug:
                traceback.print_exc()

    def _generate_position_graphs_page(self, epc: str, atr_point_store, pdf):
        """
        Generates the second page with X and Y position variation graphs (ATR7000 only).
        
        Args:
            epc: EPC identifier
            atr_point_store: PointDataStore with position data
            pdf: PdfPages object to save the figure
        """
        try:
            # Create 2-section layout for position graphs with maximum space
            fig = plt.figure(figsize=(8.5, 11))
            gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.4)
            
            # Page header
            fig.suptitle(f'Position Analysis: {epc}', fontsize=16, fontweight='bold', y=0.95)
            
            # X Position Graph (section 1)
            ax_x = fig.add_subplot(gs[0])
            x_graph_created = self._generate_x_position_graph(atr_point_store, epc, ax_x)
            
            if not x_graph_created:
                # Fallback message if no X graph could be created
                ax_x.text(0.5, 0.5, 'No X coordinate data available for this EPC', 
                          ha='center', va='center', fontsize=11,
                          bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
                ax_x.set_xlim(0, 1)
                ax_x.set_ylim(0, 1)
                ax_x.axis('off')
            
            # Y Position Graph (section 2)
            ax_y = fig.add_subplot(gs[1])
            y_graph_created = self._generate_y_position_graph(atr_point_store, epc, ax_y)
            
            if not y_graph_created:
                # Fallback message if no Y graph could be created
                ax_y.text(0.5, 0.5, 'No Y coordinate data available for this EPC', 
                          ha='center', va='center', fontsize=11,
                          bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
                ax_y.set_xlim(0, 1)
                ax_y.set_ylim(0, 1)
                ax_y.axis('off')
            
            # Note: Custom GridSpec layout eliminates need for plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            
        except Exception as e:
            print(f"❌ Error generating position graphs page for EPC {epc}: {e}")
            if hasattr(self, 'debug') and self.debug:
                traceback.print_exc()

    def _generate_x_position_graph(self, point_store, epc: str, ax_x):
        """
        Generates X position variation graph for ATR7000 readers with smooth curve.
        
        Args:
            point_store: PointDataStore instance with position data
            epc: EPC string to get position data for
            ax_x: matplotlib axes to plot on
            
        Returns:
            bool: True if graph was generated, False if no data
        """
        try:
            # Get XY history for this EPC
            timestamps, x_coords, y_coords = point_store.get_xy_history(epc, all_points=True)
            
            if not timestamps or not x_coords or len(timestamps) == 0:
                # No position data available
                ax_x.text(0.5, 0.5, 'No X coordinate data available for this EPC', 
                          ha='center', va='center', fontsize=11,
                          bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
                ax_x.set_xlim(0, 1)
                ax_x.set_ylim(0, 1)
                ax_x.axis('off')
                return False
            
            # Plot X coordinates
            ax_x.plot(timestamps, x_coords, 'b-', linewidth=0.5, marker='o', markersize=2, label='X Coordinate', alpha=0.3)

            # Calculate and plot trend line - Design choice --> not significant
            # trend_info = self._calculate_trend_line(timestamps, x_coords)
            # if trend_info:
            #     ax_x.plot(trend_info['trend_timestamps'], trend_info['trend_coords'], 
            #              'navy', linewidth=2, linestyle='--', label='X Trend', alpha=0.9)
            
            # Calculate and plot smooth curve
            # Savitzky-Golay Filter
            smooth_info = self._calculate_smooth_curve_savgol(timestamps, x_coords)
            
            if smooth_info:
                ax_x.plot(smooth_info['timestamps'], smooth_info['coordinates'], 
                         'green', linewidth=2, linestyle='-', label='X Smooth', alpha=1)
            
            ax_x.set_ylabel('X Coordinate (meters)', fontsize=10)
            ax_x.set_title('X Position Variations Over Time', fontsize=11, fontweight='bold')
            ax_x.grid(True, alpha=0.3)
            ax_x.legend(fontsize=9)
            
            # Format x-axis with adaptive interval based on timestamps time span
            ax_x.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            
            # Calculate time span to choose appropriate locator (time axis markers)
            try:
                time_span_seconds = (max(timestamps) - min(timestamps)).total_seconds()
                
                # Choose appropriate time axis interval based on position data duration
                if time_span_seconds <= 10:  # ≤ 10 seconds: show every second
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
                elif time_span_seconds <= 30:  # ≤ 30 seconds: show every 5 seconds
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
                elif time_span_seconds <= 60:  # ≤ 1 minute: show every 10 seconds
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
                elif time_span_seconds <= 120:  # ≤ 2 minutes: show every 15 seconds
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=15))
                elif time_span_seconds <= 300:  # ≤ 5 minutes: show every 30 seconds
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
                elif time_span_seconds <= 900:  # ≤ 15 minutes: show every minute
                    ax_x.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
                elif time_span_seconds <= 3600:  # ≤ 1 hour: show every 5 minutes
                    ax_x.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
                else:  # > 1 hour: show every 15 minutes
                    ax_x.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
                    
            except (ValueError, TypeError, AttributeError):
                # Fallback to data point based approach if timestamp calculation fails
                if len(timestamps) > 10:
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=max(1, len(timestamps)//8)))
                else:
                    ax_x.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
            
            ax_x.tick_params(axis='x', labelsize=8)
            ax_x.tick_params(axis='y', labelsize=9)
            
            # Don't show x-axis labels (will be shown only on bottom graph)
            ax_x.set_xticklabels([])
            
            # Set time range
            if len(timestamps) > 1:
                time_range = [min(timestamps), max(timestamps)]
                ax_x.set_xlim(time_range)
            
            # Add statistics info box
            if len(x_coords) > 0:
                x_range = max(x_coords) - min(x_coords)
                x_mean = sum(x_coords) / len(x_coords)
                stats_text = f'Points: {len(x_coords)}\nRange: {x_range:.2f}m\nMean: {x_mean:.2f}m'
                
                # Add trend information if available - Design choice --> not significant
                # if trend_info:
                #     slope_per_second = trend_info['slope']
                #     direction = trend_info['direction']
                    
                #     # Convert slope to more meaningful units (meters per minute if time span > 60s)
                #     time_span = trend_info['time_span_seconds']
                #     if time_span > 60:
                #         slope_per_minute = slope_per_second * 60
                #         stats_text += f'\nTrend: {direction}\nSlope: {slope_per_minute:.3f}m/min'
                #     else:
                #         stats_text += f'\nTrend: {direction}\nSlope: {slope_per_second:.3f}m/s'
                
                ax_x.text(0.02, 0.98, stats_text, transform=ax_x.transAxes, fontsize=8,
                         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
            
            return True
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error generating X position graph: {e}")
            return False

    def _generate_y_position_graph(self, point_store, epc: str, ax_y):
        """
        Generates Y position variation graph for ATR7000 readers with smooth curve.
        
        Args:
            point_store: PointDataStore instance with position data
            epc: EPC string to get position data for
            ax_y: matplotlib axes to plot on
            
        Returns:
            bool: True if graph was generated, False if no data
        """
        try:
            # Get XY history for this EPC
            timestamps, x_coords, y_coords = point_store.get_xy_history(epc, all_points=True)
            
            if not timestamps or not y_coords or len(timestamps) == 0:
                # No position data available
                ax_y.text(0.5, 0.5, 'No Y coordinate data available for this EPC', 
                          ha='center', va='center', fontsize=11,
                          bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
                ax_y.set_xlim(0, 1)
                ax_y.set_ylim(0, 1)
                ax_y.axis('off')
                return False
            
            # Plot Y coordinates
            ax_y.plot(timestamps, y_coords, 'r-', linewidth=0.5, marker='o', markersize=2, label='Y Coordinate', alpha=0.3)
            
            # Calculate and plot trend line - Design choice --> not significant
            # trend_info = self._calculate_trend_line(timestamps, y_coords)
            # if trend_info:
            #     ax_y.plot(trend_info['trend_timestamps'], trend_info['trend_coords'], 
            #              'darkred', linewidth=2, linestyle='--', label='Y Trend', alpha=0.9)
            
            # Calculate and plot smooth curve
            # Savitzky-Golay Filter
            smooth_info = self._calculate_smooth_curve_savgol(timestamps, y_coords)

            if smooth_info:
                ax_y.plot(smooth_info['timestamps'], smooth_info['coordinates'], 
                         'green', linewidth=2, linestyle='-', label='Y Smooth', alpha=1)
            
            ax_y.set_ylabel('Y Coordinate (meters)', fontsize=10)
            ax_y.set_xlabel('Time', fontsize=10)
            ax_y.set_title('Y Position Variations Over Time', fontsize=11, fontweight='bold')
            ax_y.grid(True, alpha=0.3)
            ax_y.legend(fontsize=9)
            
            # Format x-axis with adaptive interval based on timestamps time span
            ax_y.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            
            # Calculate time span to choose appropriate locator (time axis markers)
            try:
                time_span_seconds = (max(timestamps) - min(timestamps)).total_seconds()
                
                # Choose appropriate time axis interval based on position data duration
                if time_span_seconds <= 10:  # ≤ 10 seconds: show every second
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
                elif time_span_seconds <= 30:  # ≤ 30 seconds: show every 5 seconds
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
                elif time_span_seconds <= 60:  # ≤ 1 minute: show every 10 seconds
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
                elif time_span_seconds <= 120:  # ≤ 2 minutes: show every 15 seconds
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=15))
                elif time_span_seconds <= 300:  # ≤ 5 minutes: show every 30 seconds
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
                elif time_span_seconds <= 900:  # ≤ 15 minutes: show every minute
                    ax_y.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
                elif time_span_seconds <= 3600:  # ≤ 1 hour: show every 5 minutes
                    ax_y.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
                else:  # > 1 hour: show every 15 minutes
                    ax_y.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
                    
            except (ValueError, TypeError, AttributeError):
                # Fallback to data point based approach if timestamp calculation fails
                if len(timestamps) > 10:
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=max(1, len(timestamps)//8)))
                else:
                    ax_y.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
            
            plt.setp(ax_y.xaxis.get_majorticklabels(), rotation=45, fontsize=8)
            ax_y.tick_params(axis='y', labelsize=9)
            
            # Set time range
            if len(timestamps) > 1:
                time_range = [min(timestamps), max(timestamps)]
                ax_y.set_xlim(time_range)
            
            # Add statistics info box
            if len(y_coords) > 0:
                y_range = max(y_coords) - min(y_coords)
                y_mean = sum(y_coords) / len(y_coords)
                stats_text = f'Points: {len(y_coords)}\nRange: {y_range:.2f}m\nMean: {y_mean:.2f}m'
                
                # Add trend information if available - Design choice --> not significant
                # if trend_info:
                #     slope_per_second = trend_info['slope']
                #     direction = trend_info['direction']
                    
                #     # Convert slope to more meaningful units (meters per minute if time span > 60s)
                #     time_span = trend_info['time_span_seconds']
                #     if time_span > 60:
                #         slope_per_minute = slope_per_second * 60
                #         stats_text += f'\nTrend: {direction}\nSlope: {slope_per_minute:.3f}m/min'
                #     else:
                #         stats_text += f'\nTrend: {direction}\nSlope: {slope_per_second:.3f}m/s'
                
                ax_y.text(0.02, 0.98, stats_text, transform=ax_y.transAxes, fontsize=8,
                         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.8))
            
            return True
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error generating Y position graph: {e}")
            return False

    def _is_messages_csv_from_atr(self, csv_file_path: str) -> bool:
        """
        Checks if a messages_read CSV file is from an ATR7000 reader or a standard RFID reader.
        
        Args:
            csv_file_path: Full path to the messages_read CSV file
            
        Returns:
            True if the CSV is from an ATR7000 reader, False if from a standard RFID reader
        """
        try:           
            # Validate file exists
            if not os.path.exists(csv_file_path):
                if self.debug:
                    print(f"⚠️  File not found: {csv_file_path}")
                return False
            
            # Check if it's a messages_read CSV file by filename
            filename = os.path.basename(csv_file_path)
            if not filename.startswith('messages_read_') or not filename.endswith('.csv'):
                if self.debug:
                    print(f"⚠️  Not a messages_read CSV file: {filename}")
                return False
            
            atr_indicators = 0
            standard_rfid_indicators = 0
            rows_analyzed = 0
            max_rows_to_analyze = 10  # Analyze first 10 data rows for reliable detection
            
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                # Check if CSV has expected columns
                if 'Raw_JSON' not in csv_reader.fieldnames:
                    if self.debug:
                        print(f"⚠️  CSV missing Raw_JSON column")
                    return False
                
                for row in csv_reader:
                    if rows_analyzed >= max_rows_to_analyze:
                        break
                    
                    try:
                        # Parse the JSON message
                        raw_json = row.get('Raw_JSON', '')
                        if not raw_json:
                            continue
                            
                        message_data = json.loads(raw_json)
                        message_type = message_data.get('type', '')
                        data_section = message_data.get('data', {})
                        
                        # Check for ATR7000 indicators
                        if message_type in ['DIRECTIONALITY_RAW', 'DIRECTIONALITY']:
                            atr_indicators += 2  # Strong indicator
                            
                        # Check for ATR-specific fields in data section
                        atr_fields = ['azimuth', 'elevation', 'azimuthConf', 'elevationConf', 'zone', 'zoneName']
                        for field in atr_fields:
                            if field in data_section:
                                atr_indicators += 1
                        
                        # Check RSSI field type (ATR uses "rssi", standard uses "peakRssi")
                        if 'rssi' in data_section and 'peakRssi' not in data_section:
                            atr_indicators += 1
                        elif 'peakRssi' in data_section and 'rssi' not in data_section:
                            standard_rfid_indicators += 1
                        
                        # Check for standard RFID indicators
                        if message_type == 'CUSTOM':
                            standard_rfid_indicators += 1
                            
                        # Check for standard RFID-specific fields
                        standard_fields = ['CRC', 'PC', 'channel', 'eventNum', 'phase', 'reads']
                        for field in standard_fields:
                            if field in data_section:
                                standard_rfid_indicators += 1
                        
                        rows_analyzed += 1
                        
                    except (json.JSONDecodeError, KeyError) as e:
                        if self.debug:
                            print(f"⚠️  Error parsing JSON in row {rows_analyzed + 1}: {e}")
                        continue
            
            if self.debug:
                print(f"🔍 Analysis results for {filename}:")
                print(f"   Rows analyzed: {rows_analyzed}")
                print(f"   ATR indicators: {atr_indicators}")
                print(f"   Standard RFID indicators: {standard_rfid_indicators}")
            
            # Decision logic: ATR if more ATR indicators than standard RFID indicators
            is_atr = atr_indicators > standard_rfid_indicators
            
            if self.debug:
                reader_type = "ATR7000" if is_atr else "Standard RFID"
                print(f"✅ Detected: {reader_type} reader")
            
            return is_atr
            
        except Exception as e:
            if self.debug:
                print(f"❌ Error analyzing CSV file: {e}")
            return False

    def process_atr7000_message(
            self,
            message: str,
            position_point_record: PointDataStore = None,
            position_calculator: ATR7000PositionCalculator = ATR7000PositionCalculator()) -> PointDataStore:
        try:
            if isinstance(message, dict):
                data = message
            else:
                data = json.loads(message)

            # Extract timestamp from the JSON message
            message_timestamp = None
            timestamp_str = data.get('timestamp', '')
            if timestamp_str:
                try:
                    # Parse ISO 8601 timestamp format: "2025-09-11T10:17:02.227+0000"
                    # Remove timezone info and parse
                    timestamp_clean = timestamp_str.replace('+0000', '').replace('Z', '')
                    message_timestamp = datetime.strptime(timestamp_clean, '%Y-%m-%dT%H:%M:%S.%f')
                except ValueError:
                    try:
                        # Try without microseconds
                        timestamp_clean = timestamp_str.replace('+0000', '').replace('Z', '')
                        message_timestamp = datetime.strptime(timestamp_clean, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        if hasattr(self, 'debug') and self.debug:
                            print(f"[DEBUG]⚠️  Could not parse message timestamp: {timestamp_str}")
                        # Will use datetime.now() as fallback

            # Search for RAW_DIRECTIONALITY or DIRECTIONALITY_RAW messages
            if data.get('type') in ['RAW_DIRECTIONALITY', 'DIRECTIONALITY_RAW']:
                # Extract message data
                msg_data = data.get('data', {})
                
                epc = msg_data.get('idHex') or msg_data.get('epc', '') or msg_data.get('EPC', '')
                azimuth = msg_data.get('azimuth') or msg_data.get('Azimuth')
                elevation = msg_data.get('elevation') or msg_data.get('Elevation')
                rssi = msg_data.get('rssi') or msg_data.get('peakRssi') or msg_data.get('RSSI')
                antenna = msg_data.get('antenna') or msg_data.get('Antenna')

                if azimuth is None:
                    azimuth = 0.0
                    if self.debug:
                        print(f"[DEBUG] Azimuth None set to: 0.0")
                if elevation is None:
                    elevation = 0.0
                    if self.debug:
                        print(f"[DEBUG] Elevation None set to: 0.0")

                if epc and azimuth is not None and elevation is not None:
                    # Use extracted timestamp from JSON message or current time as fallback
                    timestamp_to_use = message_timestamp or datetime.now()
                    
                    # Create RAW_DIRECTIONALITY message
                    raw_message = RawDirectionalityMessage(
                        epc=epc,
                        azimuth=float(azimuth),
                        elevation=float(elevation),
                        timestamp=timestamp_to_use,
                        rssi=rssi,
                        antenna=antenna
                    )
                    
                    # Calculate position
                    # The position is calculated based on
                    position = position_calculator.calculate_position(raw_message)

                    # Add to point store
                    position_point_record.add_position_point(position)
                else:
                    print(f"⚠️  Incomplete RAW_DIRECTIONALITY message: {msg_data}")

            # Also handle CUSTOM messages that may contain ATR7000 localization data
            elif data.get('type') == 'CUSTOM':
                msg_data = data.get('data', {})
                epc = msg_data.get('idHex', '')
                
                # Look for azimuth/elevation data in CUSTOM messages
                azimuth = msg_data.get('azimuth')
                elevation = msg_data.get('elevation')
                location_x = msg_data.get('x')
                location_y = msg_data.get('y')
                
                # Check if it has localization data
                if azimuth is not None and elevation is not None:
                    # Use extracted timestamp from JSON message or current time as fallback
                    timestamp_to_use = message_timestamp or datetime.now()
                    
                    rssi = msg_data.get('peakRssi') or msg_data.get('rssi')
                    antenna = msg_data.get('antenna')
                    
                    # Create RAW_DIRECTIONALITY message
                    raw_message = RawDirectionalityMessage(
                        epc=epc,
                        azimuth=float(azimuth),
                        elevation=float(elevation),
                        timestamp=timestamp_to_use,
                        rssi=rssi,
                        antenna=antenna
                    )
                    
                    # Calculate position
                    position = position_calculator.calculate_position(raw_message)
                    
                    # Add to point store
                    position_point_record.add_position_point(position)

                elif location_x is not None and location_y is not None:
                    # Use extracted timestamp from JSON message or current time as fallback
                    timestamp_to_use = message_timestamp or datetime.now()
                    
                    # Use coordinates directly if available
                    position = PositionPoint(
                        epc=epc,
                        x=float(location_x),
                        y=float(location_y),
                        z=0.0,
                        timestamp=timestamp_to_use,
                        is_significant=True
                    )

                    position_point_record.add_position_point(position)
        
        except json.JSONDecodeError:
            # Non-JSON message, silently ignore unless useful
            print(f"⚠️  Non-JSON message received: {data}")
        except Exception as e:
            print(f"⚠️  Error processing ATR7000 message: {e}")

        return position_point_record

    def process_atr7000_messages_csv(self, messages_csv_file_path: str) -> PointDataStore:
        """
        Processes all messages in an ATR7000 CSV file and populates a PointDataStore.
        
        Args:
            messages_csv_file_path: Full path to the messages_read CSV file from ATR7000 reader
            
        Returns:
            PointDataStore populated with position points calculated from all messages
        """
        try:
            # Create PointDataStore with specified parameters
            point_store = PointDataStore(
                max_series_count=1000,
                max_points_per_series=10000,
                max_all_points_per_series=10000000
            )
            
            # Create position calculator
            # With no parameters given the defaults are --> tag height = 3.0m, reader height = 15.0m
            position_calculator = ATR7000PositionCalculator()
            
            # Validate file exists
            if not os.path.exists(messages_csv_file_path):
                print(f"❌ Messages file not found: {messages_csv_file_path}")
                return point_store
            
            # Validate it's a messages CSV file
            filename = os.path.basename(messages_csv_file_path)
            if not filename.startswith('messages_read_') or not filename.endswith('.csv'):
                print(f"❌ Invalid file format. Expected messages_read_*.csv, got: {filename}")
                return point_store
            
            if self.debug:
                print(f"[DEBUG]📍 Processing ATR7000 messages from: {filename}")
                print(f"[DEBUG]🔧 PointDataStore limits: {point_store.max_series_count} series, {point_store.max_points_per_series} points/series")
            
            messages_processed = 0
            messages_with_position_data = 0
            errors_encountered = 0
            
            with open(messages_csv_file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                # Validate CSV has expected columns
                if 'Raw_JSON' not in csv_reader.fieldnames:
                    print(f"❌ Invalid CSV format. Missing 'Raw_JSON' column")
                    return point_store
                
                if self.debug:
                    print("[DEBUG]🔄 Processing messages...")

                for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 because row 1 is header
                    try:
                        raw_json = row.get('Raw_JSON', '')
                        if not raw_json:
                            continue
                        
                        # Store initial point count to check if new points were added
                        initial_point_count = sum(len(points_deque) for points_deque in point_store.all_points_dict.values())
                        
                        # Process the message (timestamp will be extracted from JSON message itself)
                        point_store = self.process_atr7000_message(
                            message=raw_json,
                            position_point_record=point_store,
                            position_calculator=position_calculator
                        )
                        
                        messages_processed += 1
                        
                        # Check if new points were added
                        final_point_count = sum(len(points_deque) for points_deque in point_store.all_points_dict.values())
                        if final_point_count > initial_point_count:
                            messages_with_position_data += 1
                        
                        # Progress feedback every 50 messages
                        if messages_processed % 50 == 0 and self.debug:
                            print(f"[DEBUG]   📊 Processed {messages_processed} messages, {messages_with_position_data} with position data")
                        
                    except Exception as e:
                        errors_encountered += 1
                        if self.debug:
                            print(f"[DEBUG]⚠️  Error processing message at row {row_num}: {e}")
                        
                        # Don't stop processing for individual message errors
                        continue
            
            # Final summary
            total_position_points = sum(len(points_deque) for points_deque in point_store.all_points_dict.values())
            unique_tags = len(point_store.series_dict)
            
            if self.debug:
                print(f"[DEBUG]✅ ATR7000 message processing completed!")
                print(f"[DEBUG]📊 Summary:")
                print(f"[DEBUG]   • Total messages processed: {messages_processed}")
                print(f"[DEBUG]   • Messages with position data: {messages_with_position_data}")
                print(f"[DEBUG]   • Total position points calculated: {total_position_points}")
                print(f"[DEBUG]   • Unique tags tracked: {unique_tags}")
                if errors_encountered > 0:
                    print(f"[DEBUG]   • Errors encountered: {errors_encountered}")

                if unique_tags > 0:
                    print(f"[DEBUG]📍 Tag series in PointDataStore:")
                    for epc, series in point_store.series_dict.items():
                        point_count = len(point_store.all_points_dict.get(epc, []))
                        print(f"[DEBUG]   • {epc[:16]}...: {point_count} points")
            
            return point_store
            
        except Exception as e:
            print(f"❌ Error processing ATR7000 messages CSV: {e}")
            if self.debug:                
                traceback.print_exc()
            
            # Return empty PointDataStore on error
            return PointDataStore(
                max_series_count=1000,
                max_points_per_series=10000,
                max_all_points_per_series=10000000
            )

    # Not used but kept for eventual future use
    def _calculate_trend_line(self, timestamps, coordinates):
        """
        Calculate linear trend line for position coordinate data.
        
        Args:
            timestamps: List of datetime objects
            coordinates: List of coordinate values (x or y)
            
        Returns:
            dict: Contains slope, intercept, direction, and trend points, or None if calculation fails
        """
        try:            
            if len(timestamps) < 2 or len(coordinates) < 2:
                return None
                
            # Convert timestamps to numeric seconds since first timestamp
            first_time = timestamps[0]
            time_numeric = [(t - first_time).total_seconds() for t in timestamps]
            
            # Calculate linear regression (degree=1 for linear trend)
            coefficients = np.polyfit(time_numeric, coordinates, 1)
            slope, intercept = coefficients
            
            # Calculate trend line endpoints for the time range
            time_range = [min(time_numeric), max(time_numeric)]
            trend_coords = [slope * t + intercept for t in time_range]
            trend_timestamps = [timestamps[0], timestamps[-1]]
            
            # Determine trend direction
            slope_threshold = 0.001  # Threshold for considering trend "stable"
            if abs(slope) < slope_threshold:
                direction = "Stable"
            elif slope > 0:
                direction = "Increasing"
            else:
                direction = "Decreasing"
            
            return {
                'slope': slope,
                'intercept': intercept,
                'direction': direction,
                'trend_timestamps': trend_timestamps,
                'trend_coords': trend_coords,
                'time_span_seconds': max(time_numeric)
            }
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error calculating trend line: {e}")
            return None

    # SMOOTHING ALGORITHM
    # We use Savitzky-Golay Filter (savgol), but kept for eventual future use
    def _calculate_smooth_curve_spline(self, timestamps, coordinates):
        """
        Calculate smooth interpolated curve for position coordinate data using cubic splines.
        
        Args:
            timestamps: List of datetime objects
            coordinates: List of coordinate values (x or y)
            
        Returns:
            dict: Contains smooth curve timestamps and coordinates, or None if calculation fails
        """
        try:
            # Import scipy.interpolate for cubic spline
            try:
                from scipy.interpolate import make_interp_spline
            except ImportError:
                if hasattr(self, 'debug') and self.debug:
                    print("⚠️  scipy.interpolate not available for cubic spline smoothing")
                return None
                    
            if len(timestamps) < 4 or len(coordinates) < 4:
                # Need at least 4 points for cubic spline
                return None
                
            # Convert timestamps to numeric seconds since first timestamp
            first_time = timestamps[0]
            time_numeric = np.array([(t - first_time).total_seconds() for t in timestamps])
            coordinates_array = np.array(coordinates)
            
            # Create cubic spline interpolator
            spline = make_interp_spline(time_numeric, coordinates_array, k=3)
            
            # Generate more time points for smooth curve visualization (3x density)
            time_span = max(time_numeric) - min(time_numeric)
            num_points = max(100, len(timestamps) * 3)  # At least 100 points for smoothness
            time_smooth = np.linspace(min(time_numeric), max(time_numeric), num_points)
            
            # Evaluate spline at smooth time points
            coords_smooth = spline(time_smooth)
            
            # Convert back to datetime objects
            timestamps_smooth = [first_time + np.timedelta64(int(t * 1000), 'ms') for t in time_smooth]
            
            return {
                'timestamps': timestamps_smooth,
                'coordinates': coords_smooth.tolist()
            }
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error calculating smooth curve: {e}")
            return None

    def _calculate_smooth_curve_savgol(self, timestamps, coordinates):
        """
        Calculate smooth curve for position coordinate data using Savitzky-Golay filter.
        
        Args:
            timestamps: List of datetime objects
            coordinates: List of coordinate values (x or y)
            
        Returns:
            dict: Contains smooth curve timestamps and coordinates, or None if calculation fails
        """
        try:
            # Import scipy.signal for Savitzky-Golay filter
            try:
                from scipy.signal import savgol_filter
            except ImportError:
                if hasattr(self, 'debug') and self.debug:
                    print("⚠️  scipy.signal not available for Savitzky-Golay smoothing")
                return None
                
            if len(timestamps) < 5 or len(coordinates) < 5:
                # Need at least 5 points for reasonable Savitzky-Golay filtering
                return None
                
            coordinates_array = np.array(coordinates)
            
            # Choose appropriate window length and polynomial order for position data
            data_length = len(coordinates)
            
            # Window length should be odd and much smaller than data length
            # For position data, we want to preserve features while smoothing noise
            if data_length >= 15:
                window_length = 7  # Good balance for most position tracking data
                polyorder = 3      # Cubic polynomial preserves curvature well
            elif data_length >= 9:
                window_length = 5  # Smaller window for limited data
                polyorder = 2      # Quadratic for simpler curves
            else:
                window_length = data_length if data_length % 2 == 1 else data_length - 1
                polyorder = min(2, window_length - 1)
            
            # Ensure window_length is odd and >= polyorder + 1
            if window_length % 2 == 0:
                window_length += 1
            if window_length > data_length:
                window_length = data_length if data_length % 2 == 1 else data_length - 1
            if polyorder >= window_length:
                polyorder = window_length - 1
                
            # Apply Savitzky-Golay filter for smoothing
            # Use 'nearest' mode for boundary handling to avoid edge artifacts
            coords_smooth = savgol_filter(coordinates_array, 
                                        window_length=window_length, 
                                        polyorder=polyorder,
                                        mode='nearest')
            
            return {
                'timestamps': timestamps.copy(),  # Same timestamps as input
                'coordinates': coords_smooth.tolist()
            }
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error calculating Savitzky-Golay smooth curve: {e}")
            return None

    def _calculate_smooth_curve_gaussian(self, timestamps, coordinates):
        """
        Calculate smooth curve for position coordinate data using Gaussian filter.
        
        Args:
            timestamps: List of datetime objects
            coordinates: List of coordinate values (x or y)
            
        Returns:
            dict: Contains smooth curve timestamps and coordinates, or None if calculation fails
        """
        try:
            # Import scipy.ndimage for Gaussian filtering
            try:
                from scipy.ndimage import gaussian_filter1d
            except ImportError:
                if hasattr(self, 'debug') and self.debug:
                    print("⚠️  scipy.ndimage not available for Gaussian smoothing")
                return None
                
            if len(timestamps) < 3 or len(coordinates) < 3:
                # Need at least 3 points for Gaussian filtering
                return None
                
            coordinates_array = np.array(coordinates)
            
            # Choose appropriate sigma based on data length
            # Sigma controls the amount of smoothing - larger values = more smoothing
            data_length = len(coordinates)
            
            if data_length >= 20:
                sigma = 2.0  # Moderate smoothing for larger datasets
            elif data_length >= 10:
                sigma = 1.5  # Lighter smoothing for medium datasets
            else:
                sigma = 1.0  # Minimal smoothing for small datasets
            
            # Apply Gaussian filter for smoothing
            # Use 'reflect' mode for boundary handling to avoid edge artifacts
            coords_smooth = gaussian_filter1d(coordinates_array, 
                                            sigma=sigma,
                                            mode='reflect')
            
            return {
                'timestamps': timestamps.copy(),  # Same timestamps as input
                'coordinates': coords_smooth.tolist()
            }
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error calculating Gaussian smooth curve: {e}")
            return None

    def _calculate_smooth_curve_ema(self, timestamps, coordinates):
        """
        Calculate smooth curve for position coordinate data using Exponential Moving Average.
        
        Args:
            timestamps: List of datetime objects
            coordinates: List of coordinate values (x or y)
            
        Returns:
            dict: Contains smooth curve timestamps and coordinates, or None if calculation fails
        """
        try:
            if len(timestamps) < 2 or len(coordinates) < 2:
                # Need at least 2 points for EMA
                return None
                
            coordinates_array = np.array(coordinates)
            
            # Choose appropriate alpha (smoothing factor) based on data length
            # Alpha determines responsiveness: higher alpha = less smoothing, lower alpha = more smoothing
            data_length = len(coordinates)
            
            if data_length >= 20:
                alpha = 0.3  # More smoothing for larger datasets
            elif data_length >= 10:
                alpha = 0.4  # Moderate smoothing for medium datasets
            else:
                alpha = 0.5  # Less smoothing for small datasets to preserve detail
            
            # Calculate Exponential Moving Average
            coords_smooth = np.zeros_like(coordinates_array)
            coords_smooth[0] = coordinates_array[0]  # First value unchanged
            
            for i in range(1, len(coordinates_array)):
                coords_smooth[i] = alpha * coordinates_array[i] + (1 - alpha) * coords_smooth[i - 1]
            
            return {
                'timestamps': timestamps.copy(),  # Same timestamps as input
                'coordinates': coords_smooth.tolist()
            }
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error calculating EMA smooth curve: {e}")
            return None

    def _calculate_smooth_curve_polynomial(self, timestamps, coordinates):
        """
        Calculate smooth curve for position coordinate data using Polynomial Regression.
        
        Args:
            timestamps: List of datetime objects
            coordinates: List of coordinate values (x or y)
            
        Returns:
            dict: Contains smooth curve timestamps and coordinates, or None if calculation fails
        """
        try:
            if len(timestamps) < 3 or len(coordinates) < 3:
                # Need at least 3 points for polynomial fitting
                return None
                
            # Convert timestamps to numeric seconds since first timestamp
            first_time = timestamps[0]
            time_numeric = np.array([(t - first_time).total_seconds() for t in timestamps])
            coordinates_array = np.array(coordinates)
            
            # Choose appropriate polynomial degree based on data length
            data_length = len(coordinates)
            
            if data_length >= 20:
                degree = min(5, data_length - 1)  # Higher order for complex curves, but not too high
            elif data_length >= 10:
                degree = min(3, data_length - 1)  # Cubic for moderate complexity
            elif data_length >= 6:
                degree = min(2, data_length - 1)  # Quadratic for simple curves
            else:
                degree = 1  # Linear for very small datasets
            
            # Fit polynomial to the data
            try:
                coefficients = np.polyfit(time_numeric, coordinates_array, degree)
            except np.RankWarning:
                # Fallback to lower degree if rank warning occurs
                degree = max(1, degree - 1)
                coefficients = np.polyfit(time_numeric, coordinates_array, degree)
            
            # Generate more time points for smooth curve visualization (2x density)
            time_span = max(time_numeric) - min(time_numeric)
            num_points = max(50, len(timestamps) * 2)  # At least 50 points for smoothness
            time_smooth = np.linspace(min(time_numeric), max(time_numeric), num_points)
            
            # Evaluate polynomial at smooth time points
            coords_smooth = np.polyval(coefficients, time_smooth)
            
            # Convert back to datetime objects
            timestamps_smooth = [first_time + np.timedelta64(int(t * 1000), 'ms') for t in time_smooth]
            
            return {
                'timestamps': timestamps_smooth,
                'coordinates': coords_smooth.tolist()
            }
            
        except Exception as e:
            if hasattr(self, 'debug') and self.debug:
                print(f"⚠️  Error calculating polynomial smooth curve: {e}")
            return None

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
            
            # Verify IOTC disconnection with reader-specific timing
            max_attempts = 6 if self.app_context.is_atr7000 else 5
            check_interval = 30 if self.app_context.is_atr7000 else 10
            reader_type = "ATR7000" if self.app_context.is_atr7000 else "non-ATR7000"
            
            print(f"🔍 Verifying {reader_type} disconnection from IOTC...")
            print(f"⏳ Will check up to {max_attempts} times with {check_interval}s intervals")
            
            current_connection_status = None
            for attempt in range(1, max_attempts + 1):
                current_connection_status = client.is_iotc_connected(session_id)
                
                if not current_connection_status:
                    print(f"✅ {reader_type} successfully disconnected from IOTC (attempt {attempt}/{max_attempts})")
                    break
                
                print(f"ℹ️  Attempt {attempt}/{max_attempts}: {reader_type} still connected to IOTC")
                
                if attempt < max_attempts:  # Don't sleep after the last attempt
                    print(f"⏳ Waiting {check_interval} seconds before next check...")
                    time.sleep(check_interval)
            
            # Final status assessment
            if current_connection_status:
                print(f"⚠️  {reader_type} still connected to IOTC after {max_attempts} attempts. Proceeding anyway.")
                print("💡 IOTC service may need additional time to complete disconnection")
            else:
                print(f"🎯 Disconnection verification completed successfully for {reader_type}")

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
            # This might not be needed if reader is fast enough to connect to IOTC but added for safety
            if self.app_context.is_atr7000:
                # ATR7000 takes a long time to complete a connection after the command is given
                print("ℹ️  Detected ATR7000 reader, waiting additional time after IOTC connection.")
                stabilization_time = 60  # This value may need adjustment based on testing
            else:
                stabilization_time = 30  # This value may need adjustment based on testing
            print(f"⏳ Waiting {stabilization_time} seconds to allow the IOTC service to finish initializing after connection...")
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
            
            # IMPORTANT: Verify reader is still responsive after IOTC setup with retry logic
            print(f"🔍 Verifying reader responsiveness after IOTC activation...")
            reader_status = None
            max_retries = 5
            retry_delay = 60  # seconds
            
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"📡 Attempt {attempt}/{max_retries}: Checking reader status...")
                    reader_status = self.app_context.get_status()
                    
                    if reader_status:
                        print(f"✅ Reader is responsive and operational (attempt {attempt})")
                        break  # Success - exit retry loop
                    else:
                        print(f"⚠️  Attempt {attempt}/{max_retries}: Reader returned empty status")
                        if attempt < max_retries:
                            print(f"⏳ Waiting {retry_delay} seconds before retry {attempt + 1}...")
                            time.sleep(retry_delay)
                        else:
                            print(f"⚠️  All {max_retries} attempts returned empty status - proceeding anyway")
                            
                except Exception as e:
                    print(f"❌ Attempt {attempt}/{max_retries}: Reader status check failed - {e}")
                    if attempt < max_retries:
                        print(f"⏳ Waiting {retry_delay} seconds before retry {attempt + 1}...")
                        time.sleep(retry_delay)
                    else:
                        print(f"⚠️  All {max_retries} attempts failed - proceeding with caution...")
            
            # Final status summary
            if reader_status:
                print(f"🎯 Reader status verification completed successfully")
            else:
                print(f"⚠️  Reader status verification completed with issues - IOTC setup may need more time to stabilize")
            
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
  
            # Verify IOTC disconnection with reader-specific timing
            max_attempts = 6 if self.app_context.is_atr7000 else 5
            check_interval = 30 if self.app_context.is_atr7000 else 10
            reader_type = "ATR7000" if self.app_context.is_atr7000 else "non-ATR7000"
            
            print(f"🔍 Verifying {reader_type} disconnection from IOTC...")
            print(f"⏳ Will check up to {max_attempts} times with {check_interval}s intervals")
            
            current_connection_status = None
            for attempt in range(1, max_attempts + 1):
                current_connection_status = client.is_iotc_connected(session_id)
                
                if not current_connection_status:
                    print(f"✅ {reader_type} successfully disconnected from IOTC (attempt {attempt}/{max_attempts})")
                    break
                
                print(f"ℹ️  Attempt {attempt}/{max_attempts}: {reader_type} still connected to IOTC")
                
                if attempt < max_attempts:  # Don't sleep after the last attempt
                    print(f"⏳ Waiting {check_interval} seconds before next check...")
                    time.sleep(check_interval)

            # Final status assessment
            if current_connection_status:
                print(f"⚠️  {reader_type} still connected to IOTC after {max_attempts} attempts. Proceeding anyway.")
                print("💡 IOTC service may need additional time to complete disconnection")
            else:
                print(f"🎯 Disconnection verification completed successfully for {reader_type}")

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
            # This might not be needed if reader is fast enough to connect to IOTC but added for safety
            if self.app_context.is_atr7000:
                print("ℹ️  Detected ATR7000 reader, waiting additional time.")
                stabilization_time = 60  # This value may need adjustment based on testing
            else:
                stabilization_time = 30  # This value may need adjustment based on testing
            print(f"⏳ Waiting {stabilization_time} seconds to allow the IOTC service to finish initializing after connection...")
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
            print(f"🔗 Client ID: {reader_name}")
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

        # STEP 2: SET ENDPOINT CONFIG (only if changes were made)
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
