"""
ATR7000 Localization Submenu for Zebra RFID CLI
"""
# Standard library imports
import os
import time
import queue
import threading
import json
from datetime import datetime

# Third-party imports
try:
    from wcwidth import wcwidth as _wcwidth
except ImportError:
    _wcwidth = None

# Local imports
from zebra_cli.atr7000_locationing import (
    ATR7000LocationPlotter, ATR7000PositionCalculator, PointDataStore, PositionPoint, RawDirectionalityMessage
)

class AtrSubmenu:
    """Handles the ATR7000 localization submenu with text commands and shortcuts"""
    
    def __init__(self, cli) -> None:
        self.cli = cli  # Reference to InteractiveCLI for context and methods
        self.position_calculator = ATR7000PositionCalculator()
        self.point_store = PointDataStore()
        self.location_plotter = ATR7000LocationPlotter(self.point_store, debug=self.cli.debug)
        self.data_queue = None
        self.command_map = {
            'r': self.handle_atr7000_realtime_plot, 'realtime': self.handle_atr7000_realtime_plot,
            'x': self.handle_atr7000_xy_variations, 'xy': self.handle_atr7000_xy_variations,
            'h': self.handle_atr7000_heatmap, 'heatmap': self.handle_atr7000_heatmap,
            'c': self.handle_atr7000_configuration, 'config': self.handle_atr7000_configuration,
            'cl': self.handle_atr7000_clear_data, 'clear': self.handle_atr7000_clear_data,
            's': self.handle_atr7000_statistics, 'stat': self.handle_atr7000_statistics,
            'b': None, 'back': None
        }

    def show_menu(self) -> None:
        # Handle wcwidth import and normalize return values
        
        def wcwidth(c):
            if _wcwidth is not None:
                try:
                    width = _wcwidth(c)
                    # Handle None, -1, 0 by defaulting to 1
                    if width is None or width < 1:
                        return 1
                    # Cap all widths to maximum of 2 to prevent table breakage
                    elif width > 2:
                        return 2
                    else:
                        return width
                except (TypeError, ValueError):
                    # Handle composite characters by treating them as width 2
                    return 2
            else:
                # Fallback: Simple approach - all non-ASCII is width 2
                try:
                    char_ord = ord(c)
                    if char_ord > 127:
                        return 2
                    else:
                        return 1
                except (TypeError, ValueError):
                    # Handle composite characters
                    return 2
            
        width = 60
        def visual_len(text):
            return sum(wcwidth(c) for c in text)
        def atr_row(text):
            pad = width - visual_len(text)
            return f"│ {text}{' ' * pad} │"
        print("\n📍 Localization - ATR7000:")
        print("┌" + "─" * (width + 2) + "┐")
        print(atr_row("r  / realtime   📊 Real-time positions chart"))
        print(atr_row("x  / xy         📈 X/Y variations over time (per tag)"))
        print(atr_row("h  / heatmap    🔥 Detected zones heatmap"))
        print(atr_row("c  / config     🔧 Height configuration"))
        print(atr_row("cl / clear      🚮 Clear location data"))
        print(atr_row("s  / stat       📋 Localization statistics"))
        print(atr_row("b  / back       🔙 Back to main menu"))
        print("└" + "─" * (width + 2) + "┘")

    def handle_submenu(self) -> None:
        if not self.cli.app_context.is_connected():
            print("❌ You must first connect to the reader")
            input("⏸️  Press ENTER to continue...")
            return
        while True:
            self.clear_screen()
            self.show_menu()
            choice = input("\n🔹 ATR command or shortcut: ").strip().lower()
            action = self.command_map.get(choice)
            if action:
                action()
            elif choice in ('b', 'back'):
                break
            else:
                print(f"\n❌ Invalid command or shortcut '{choice}'")
                input("⏸️  Press ENTER to continue...")
    
    def start_atr7000_websocket_listener(self, location_queue: queue.Queue, location_stop_event: threading.Event) -> None:
        """Uses permanent WebSocket for ATR7000 RAW_DIRECTIONALITY messages"""
        if self.cli.debug:
            print(f"🔍 [DEBUG] start_atr7000_websocket_listener called with queue: {location_queue}, stop_event: {location_stop_event}")

        if not self.cli.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            return
        
        # Check if permanent WebSocket is running
        if not self.cli.app_context.is_websocket_running():
            print("❌ WebSocket connection not active. Please reconnect to the reader.")
            return
        
        # Debug: Show WebSocket status
        ws_status = self.cli.app_context.get_websocket_status()
        if self.cli.debug:
            print(f"🔍 [DEBUG] WebSocket Status: {ws_status}")
        
        # Clear any buffered data from WebSocket to ensure only fresh data
        self.cli.app_context.clear_websocket_buffer()
        
        print(f"📡 Using permanent WebSocket connection")
        
        # Start listener thread that processes permanent WebSocket data
        listener_thread = threading.Thread(
            target=self._run_atr7000_listener,
            args=(location_queue, location_stop_event),
            daemon=True
        )
        listener_thread.start()
        if self.cli.debug:
            print(f"🔍 [DEBUG] ATR7000 listener thread started: {listener_thread.name}")

        print("✅ ATR7000 listener configured and started with permanent WebSocket")
        print("💡 Monitoring RAW_DIRECTIONALITY messages...")
    
    def _run_atr7000_listener(self, location_queue: queue.Queue, location_stop_event: threading.Event) -> None:
        """Processes ATR7000 messages from permanent WebSocket"""
        
        if self.cli.debug:
            print("🔍 [DEBUG] ATR7000 listener started, waiting for messages...")
        message_count = 0
        
        while not location_stop_event.is_set():
            try:
                # Get message from permanent WebSocket
                message = self.cli.app_context.get_websocket_data()
                
                if message is None:
                    time.sleep(0.1)  # Small delay when no data
                    continue
                
                message_count += 1
                if message_count % 10 == 1 and self.cli.debug:  # Show every 10th message
                    print(f"🔍 [DEBUG] ATR7000 received message #{message_count}: {type(message)} - {str(message)[:100]}...")
                
                # Process the message for RAW_DIRECTIONALITY data
                if isinstance(message, str):
                    self.process_atr7000_message(message, location_queue)
                elif isinstance(message, dict):
                    # Convert to JSON string if necessary
                    self.process_atr7000_message(json.dumps(message), location_queue)
                    
            except Exception as e:
                if self.cli.debug:
                    print(f"⚠️  Error in ATR7000 listener: {e}")
                time.sleep(0.1)

        if self.cli.debug:
            print(f"🔍 [DEBUG] ATR7000 listener stopped after processing {message_count} messages")

    def process_atr7000_message(self, message: str, location_queue: queue.Queue) -> None:
        """Processes WebSocket messages to extract RAW_DIRECTIONALITY data"""
        try:
            if isinstance(message, dict):
                data = message
            else:
                data = json.loads(message)
            
            # Debug: show all message types to see what arrives
            msg_type = data.get('type', 'UNKNOWN')
            if self.cli.debug:
                print(f"🔍 [DEBUG] ATR7000 processing message type: '{msg_type}'")

            # Search for RAW_DIRECTIONALITY or DIRECTIONALITY_RAW messages
            if data.get('type') in ['RAW_DIRECTIONALITY', 'DIRECTIONALITY_RAW']:
                # Extract message data
                msg_data = data.get('data', {})
                
                epc = msg_data.get('idHex') or msg_data.get('epc', '') or msg_data.get('EPC', '')
                azimuth = msg_data.get('azimuth') or msg_data.get('Azimuth')
                elevation = msg_data.get('elevation') or msg_data.get('Elevation')
                rssi = msg_data.get('rssi') or msg_data.get('peakRssi') or msg_data.get('RSSI')
                antenna = msg_data.get('antenna') or msg_data.get('Antenna')
                
                if epc and azimuth is not None and elevation is not None:
                    # Create RAW_DIRECTIONALITY message
                    raw_message = RawDirectionalityMessage(
                        epc=epc,
                        azimuth=float(azimuth),
                        elevation=float(elevation),
                        timestamp=datetime.now(),
                        rssi=rssi,
                        antenna=antenna
                    )
                    
                    # Calculate position
                    position = self.position_calculator.calculate_position(raw_message)
                    
                    # Add to point store
                    significant_point = self.point_store.add_position_point(position)
                    
                    # Concise log: only EPC and Cartesian position
                    if significant_point:
                        print(f"📍 {significant_point.epc}... -> X:{significant_point.x:.2f}m Y:{significant_point.y:.2f}m")
                    
                    # NEW: Also forward to tag table if active
                    # Create a message compatible with TagTableWindow
                    if hasattr(self.cli, 'data_queue') and self.data_queue:
                        tag_message = {
                            'type': 'TagRead',
                            'data': {
                                'idHex': epc,
                                'peakRssi': rssi if rssi is not None else -50,  # Default RSSI if missing
                                'antenna': antenna if antenna is not None else 1,
                                'azimuth': azimuth,
                                'elevation': elevation
                            },
                            'timestamp': datetime.now().isoformat()
                        }
                        try:
                            self.data_queue.put_nowait(tag_message)
                        except queue.Full:
                            pass  # Ignore if queue is full
                else:
                    # Debug only: print some fields that may contain the data we're looking for
                    if any(x in str(msg_data).lower() for x in ['epc', 'id', 'hex', 'azim', 'elev']):
                        for key, value in msg_data.items():
                            if any(x in key.lower() for x in ['epc', 'id', 'hex', 'azim', 'elev', 'angle', 'bearing']):
                                print(f"   🔹 {key}: {value}")
            
            # NEW: Also handle CUSTOM messages that may contain ATR7000 localization data
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
                    rssi = msg_data.get('peakRssi') or msg_data.get('rssi')
                    antenna = msg_data.get('antenna')
                    
                    # Create RAW_DIRECTIONALITY message
                    raw_message = RawDirectionalityMessage(
                        epc=epc,
                        azimuth=float(azimuth),
                        elevation=float(elevation),
                        timestamp=datetime.now(),
                        rssi=rssi,
                        antenna=antenna
                    )
                    
                    # Calculate position
                    position = self.position_calculator.calculate_position(raw_message)
                    
                    # Add to point store
                    significant_point = self.point_store.add_position_point(position)
                    
                    if significant_point:
                        print(f"📍 {significant_point.epc[:12]}... -> X:{significant_point.x:.2f}m Y:{significant_point.y:.2f}m")
                
                elif location_x is not None and location_y is not None:
                    # Use coordinates directly if available
                    position = PositionPoint(
                        epc=epc,
                        x=float(location_x),
                        y=float(location_y),
                        z=0.0,
                        timestamp=datetime.now(),
                        is_significant=True
                    )
                    
                    significant_point = self.point_store.add_position_point(position)
                    if significant_point:
                        print(f"📍 {significant_point.epc[:12]}... -> X:{significant_point.x:.2f}m Y:{significant_point.y:.2f}m")
        
        except json.JSONDecodeError:
            # Non-JSON message, silently ignore unless useful
            pass
        except Exception as e:
            print(f"⚠️  Error processing ATR7000 message: {e}")
  
    def handle_atr7000_realtime_plot(self) -> None:
        """Starts the real-time positions chart using permanent WebSocket"""
        if not self.cli.app_context.is_connected():
            print("❌ Connection required. Use command 'l' first.")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        print("\n📊 Starting real-time positions chart...")
        print("⚠️  This chart displays positions calculated from RAW_DIRECTIONALITY messages")
        print("💡 Close the chart window to return to the menu")
        
        # Check if permanent WebSocket is running
        if not self.cli.app_context.is_websocket_running():
            print("❌ WebSocket connection not active. Please reconnect to the reader.")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        # Debug: Show WebSocket status
        ws_status = self.cli.app_context.get_websocket_status()
        if self.cli.debug:
            print(f"🔍 [DEBUG] WebSocket Status: {ws_status}")

        # Clear any buffered data from WebSocket to ensure only fresh data
        self.cli.app_context.clear_websocket_buffer()
        
        # Ensure no active listeners before starting
        self.cli.ensure_no_background_listeners()
        
        # Prepare queue and stop event
        location_queue = queue.Queue()
        location_stop_event = threading.Event()

        if self.cli.debug:
            print(f"🔍 [DEBUG] Starting ATR7000 with queue: {location_queue}, stop_event: {location_stop_event}")

        # Start listener using permanent WebSocket
        try:
            self.start_atr7000_websocket_listener(location_queue, location_stop_event)
            
            print("✅ Chart started! Close the window to return to the menu...")
            self.location_plotter.plot_realtime_positions(location_queue, location_stop_event)
        except Exception as e:
            print(f"❌ Error starting chart: {e}")
            import traceback
            traceback.print_exc()
        
        # Cleanup after plot closure
        try:
            import matplotlib.pyplot as plt
            plt.ioff()
            plt.close('all')
            time.sleep(1)
        except Exception as e:
            print(f"⚠️  Error closing matplotlib: {e}")
        
        # Set stop event to clean up the monitoring thread
        location_stop_event.set()
        
        print("⏹️  Chart stopped")
        input("⏸️  Press ENTER to continue...")
    
    def handle_atr7000_xy_variations(self) -> None:
        """Shows X/Y variations over time for a specific tag"""
        # Get the list of tags with localization data
        all_series = self.point_store.get_all_series()
        
        if not all_series:
            print("❌ No localization data available")
            print("💡 Start the real-time chart first to collect data")
            input("⏸️  Press ENTER to continue...")
            return
        
        print("\n📈 Available tags for variation analysis:")
        for i, series in enumerate(all_series, 1):
            significant_count = sum(1 for p in series.points if p.is_significant)
            print(f"{i}. {series.epc} (Significant points: {significant_count})")
        
        try:
            choice = int(input("\n🔹 Select tag number: ")) - 1
            if 0 <= choice < len(all_series):
                selected_epc = all_series[choice].epc
                print(f"\n📊 Generating chart for {selected_epc}...")
                self.location_plotter.plot_xy_variations(selected_epc)
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Enter a valid number")
        except Exception as e:
            print(f"❌ Error generating chart: {e}")
        
        input("⏸️  Press ENTER to continue...")
    
    def handle_atr7000_heatmap(self) -> None:
        """Generates and displays the detected zones heatmap"""
        print("\n🔥 Generating heatmap...")
        print("💡 The heatmap shows the number of detections per zone")
        
        try:
            # Heatmap configuration
            grid_size = 13  # 13x13 grid as in the C# code
            meter_per_cell = 1.0  # 1 meter per cell
            
            print(f"🔧 Configuration: Grid {grid_size}x{grid_size}, {meter_per_cell}m per cell")
            
            # Generate and show heatmap
            self.location_plotter.plot_heatmap(grid_size, meter_per_cell)
            
        except Exception as e:
            print(f"❌ Error generating heatmap: {e}")
        
        input("⏸️  Press ENTER to continue...")
    
    def handle_atr7000_configuration(self) -> None:
        """Configure ATR7000 localization parameters"""
        print("\n⚙️  ATR7000 LOCALIZATION CONFIGURATION")
        print(f"📏 Current reader height: {self.position_calculator.reader_height:.2f}m")
        print(f"📏 Current tag height: {self.position_calculator.tag_height:.2f}m")
        
        try:
            new_reader_height = input(f"\n🔹 New reader height (m) [{self.position_calculator.reader_height:.2f}]: ").strip()
            if new_reader_height:
                self.position_calculator.reader_height = float(new_reader_height)
                print(f"✅ Reader height updated: {self.position_calculator.reader_height:.2f}m")
            
            new_tag_height = input(f"🔹 New tag height (m) [{self.position_calculator.tag_height:.2f}]: ").strip()
            if new_tag_height:
                self.position_calculator.tag_height = float(new_tag_height)
                print(f"✅ Tag height updated: {self.position_calculator.tag_height:.2f}m")
            
        except ValueError:
            print("❌ Please enter valid numeric values")
        except Exception as e:
            print(f"❌ Error during configuration: {e}")
        
        input("⏸️  Press ENTER to continue...")
    
    def handle_atr7000_clear_data(self) -> None:
        """Clears all localization data"""
        confirm = input("\n⚠️  Are you sure you want to clear all localization data? (y/N): ").strip().lower()
        
        if confirm == 'y':
            self.point_store.clear()
            print("✅ Localization data cleared")
        else:
            print("❌ Operation cancelled")
        
        input("⏸️  Press ENTER to continue...")
    
    def handle_atr7000_statistics(self) -> None:
        """Shows statistics on localization data"""
        all_series = self.point_store.get_all_series()
        all_points_dict = getattr(self.point_store, 'all_points_dict', {})

        if not all_series:
            print("❌ No localization data available")
            input("⏸️  Press ENTER to continue...")
            return

        print("\n📊 LOCALIZATION STATISTICS:")
        print("=" * 50)
        print(f"🏷️  Tracked tags: {len(all_series)}")

        total_points = 0
        total_significant = 0

        for series in all_series:
            # Use all_points_dict for total points (FIFO, up to 1000)
            epc = series.epc
            points_count = len(all_points_dict.get(epc, []))
            significant_count = sum(1 for p in series.points if p.is_significant)
            total_points += points_count
            total_significant += significant_count

            duration = "N/A"
            if series.first_timestamp and series.last_timestamp:
                delta = series.last_timestamp - series.first_timestamp
                duration = f"{delta.total_seconds():.1f}s"

            print(f"\n📍 {epc}")
            print(f"   📊 Total points: {points_count}")
            print(f"   ⭐ Significant points: {significant_count}")
            print(f"   ⏱️  Tracking duration: {duration}")

        print(f"\n📈 TOTALS:")
        print(f"   📊 Total points: {total_points}")
        print(f"   ⭐ Significant points: {total_significant}")

        input("⏸️  Press ENTER to continue...")

    def clear_screen(self) -> None:
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')