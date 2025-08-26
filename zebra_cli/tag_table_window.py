"""
Separate window with real-time RFID tag table
"""
# Standard library imports
import time
import queue

# Third-party imports
import tkinter as tk
from tkinter import ttk
import threading

# Local imports
from typing import Dict, Optional

class TagData:
    """Class for storing RFID tag data"""

    def __init__(self, epc: str, rssi: float, extra_data: Optional[dict] = None):
        self.epc = epc
        self.read_count = 1
        self.rssi_values = [rssi]
        self.first_seen = time.time()
        self.last_seen = time.time()
        self.extra_data = extra_data or {}  # For azimuth, elevation, etc.
        
    def add_reading(self, rssi: float, extra_data: Optional[dict] = None, reads: int = 1):
        """Adds one or more readings for this tag"""
        self.read_count += reads
        # Add as many RSSI as there are reads (if >1, duplicate the last value)
        if reads > 1:
            self.rssi_values.extend([rssi] * reads)
        else:
            self.rssi_values.append(rssi)
        self.last_seen = time.time()
        # Update extra data if provided
        if extra_data:
            self.extra_data.update(extra_data)
        # Keep only the last 100 readings to avoid excessive memory consumption
        if len(self.rssi_values) > 100:
            self.rssi_values = self.rssi_values[-100:]
    
    @property
    def average_rssi(self) -> float:
        """Calculates the average RSSI"""
        if not self.rssi_values:
            return 0.0
        return sum(self.rssi_values) / len(self.rssi_values)
    
    @property
    def time_since_first(self) -> float:
        """Seconds elapsed since the first reading"""
        return time.time() - self.first_seen
    
    @property
    def time_since_last(self) -> float:
        """Seconds elapsed since the last reading"""
        return time.time() - self.last_seen
    
    @property
    def has_location_data(self) -> bool:
        """True if the tag has location data (azimuth/elevation)"""
        return 'azimuth' in self.extra_data and 'elevation' in self.extra_data

class TagTableWindow:
    """Separate window for displaying the RFID tag table"""

    def clear_queue(self) -> None:
        """Empties the data queue in a thread-safe manner"""
        try:
            while not self.data_queue.empty():
                self.data_queue.get_nowait()
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][TagTableWindow] Error during queue cleanup: {e}")

    def __init__(self, data_queue: queue.Queue, stop_event: threading.Event, debug: bool = False) -> None:
        self.data_queue = data_queue
        self.stop_event = stop_event
        self.tags: Dict[str, TagData] = {}
        self.root = None
        self.window = None
        self.tree = None
        self.update_interval = 1000  # Update every second
        self.running = False
        self.debug = debug  # Enable detailed logging if True
        
    def create_window(self):
        """Creates the main window with the table"""
        # Create a root window and hide it immediately
        self.root = tk.Tk()
        self.root.withdraw()  # Hides the root window
        
        # Now create the main window as Toplevel
        self.window = tk.Toplevel(self.root)
        self.window.title("🏷️ RFID Tag Table - Live")
        self.window.geometry("1000x600")  # Slightly wider for the new column
        self.window.configure(bg='white')
        
        # Prevent the window from being closed accidentally
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🏷️ Detected RFID Tags - Live Table", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))

        # (REMOVED) No warning for CLI closure: window can now be closed normally
        
        # Frame for statistics
        stats_frame = ttk.LabelFrame(main_frame, text="📊 General Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Labels for statistics
        self.stats_labels = {}
        stats_row1 = ttk.Frame(stats_frame)
        stats_row1.pack(fill=tk.X)
        
        self.stats_labels['total_tags'] = ttk.Label(stats_row1, text="Unique Tags: 0", font=('Arial', 10, 'bold'))
        self.stats_labels['total_tags'].pack(side=tk.LEFT, padx=(0, 20))
        
        self.stats_labels['total_reads'] = ttk.Label(stats_row1, text="Total Reads: 0", font=('Arial', 10, 'bold'))
        self.stats_labels['total_reads'].pack(side=tk.LEFT, padx=(0, 20))
        
        self.stats_labels['avg_rssi'] = ttk.Label(stats_row1, text="Avg RSSI: N/A", font=('Arial', 10, 'bold'))
        self.stats_labels['avg_rssi'].pack(side=tk.LEFT)
        
                # Frame for the table with scrollbar
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the Treeview (table)
        columns = ('EPC', 'Reads', 'Avg RSSI', 'Min RSSI', 'Max RSSI', 'First Seen', 'Last Seen', 'Rate/min', 'Type')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure the columns
        column_configs = {
            'EPC': {'width': 180, 'anchor': 'w'},
            'Reads': {'width': 70, 'anchor': 'center'},
            'Avg RSSI': {'width': 90, 'anchor': 'center'},
            'Min RSSI': {'width': 70, 'anchor': 'center'},
            'Max RSSI': {'width': 70, 'anchor': 'center'},
            'First Seen': {'width': 90, 'anchor': 'center'},
            'Last Seen': {'width': 90, 'anchor': 'center'},
            'Rate/min': {'width': 70, 'anchor': 'center'},
            'Type': {'width': 80, 'anchor': 'center'}
        }
        
        for col, config in column_configs.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=config['width'], anchor=config['anchor'])
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Pack the table and scrollbar
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Frame for controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Button to clear the table
        clear_button = ttk.Button(controls_frame, text="🗑️ Clear Table", command=self.clear_table)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Button to export data
        export_button = ttk.Button(controls_frame, text="💾 Export CSV", command=self.export_csv)
        export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Label to show the last update
        self.last_update_label = ttk.Label(controls_frame, text="Last update: Never")
        self.last_update_label.pack(side=tk.RIGHT)
        
        return self.window
    
    def process_data(self):
        """Processes data from the WebSocket queue"""
        try:
            while not self.data_queue.empty():
                data = self.data_queue.get_nowait()
                if self.debug:
                    print(f"[DEBUG][TagTableWindow] Tag message received from queue: {data}")
                if isinstance(data, dict) and 'data' in data:
                    tag_data = data['data']
                    if isinstance(tag_data, dict) and 'idHex' in tag_data:
                        epc = tag_data['idHex']
                        rssi = tag_data.get('peakRssi', 0)
                        try:
                            if rssi is None or rssi == 'N/A' or rssi == '':
                                rssi = -50.0
                            else:
                                rssi = float(rssi)
                        except (ValueError, TypeError):
                            rssi = -50.0
                        extra_data = {}
                        if 'azimuth' in tag_data:
                            extra_data['azimuth'] = tag_data['azimuth']
                        if 'elevation' in tag_data:
                            extra_data['elevation'] = tag_data['elevation']
                        if 'antenna' in tag_data:
                            extra_data['antenna'] = tag_data['antenna']
                        if self.debug:
                            print(f"[DEBUG][TagTableWindow] Updating tag {epc} with RSSI {rssi} and extra {extra_data}")
                        if epc in self.tags:
                            self.tags[epc].add_reading(rssi, extra_data)
                        else:
                            self.tags[epc] = TagData(epc, rssi, extra_data)
                elif isinstance(data, dict):
                    epc = data.get('epc', data.get('EPC', data.get('idHex', '')))
                    if epc:
                        rssi = data.get('RSSI', data.get('rssi', data.get('peakRSSI', data.get('peakRssi', 0))))
                        try:
                            if rssi is None or rssi == 'N/A' or rssi == '':
                                rssi = -50.0
                            else:
                                rssi = float(rssi)
                        except (ValueError, TypeError):
                            rssi = -50.0
                        extra_data = {}
                        for key in ['azimuth', 'elevation', 'antenna']:
                            if key in data:
                                extra_data[key] = data[key]
                        reads = 1
                        if 'reads' in data:
                            try:
                                reads = int(data['reads'])
                                if reads < 1:
                                    reads = 1
                            except Exception:
                                reads = 1
                        if self.debug:
                            print(f"[DEBUG][TagTableWindow] Updating tag {epc} with RSSI {rssi}, reads={reads}, extra={extra_data}")
                        if epc in self.tags:
                            self.tags[epc].add_reading(rssi, extra_data, reads=reads)
                        else:
                            tag = TagData(epc, rssi, extra_data)
                            tag.read_count = reads
                            if reads > 1:
                                tag.rssi_values = [rssi] * reads
                            self.tags[epc] = tag
        except queue.Empty:
            if self.debug:
                print("[DEBUG][TagTableWindow] Data queue empty during process_data")
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][TagTableWindow] Table data processing error: {e}")
            print(f"⚠️ Table data processing error: {e}")
    
    def update_table(self):
        """Updates the table display"""
        if not self.running or not self.window:
            return
        if self.stop_event and self.stop_event.is_set():
            self.on_closing()
            return
        try:
            if self.debug:
                print("[DEBUG][TagTableWindow] Table update in progress...")
            self.process_data()
            if self.tree is not None:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                total_tags = len(self.tags)
                total_reads = sum(tag.read_count for tag in self.tags.values())
                if self.tags:
                    all_rssi_values = []
                    for tag in self.tags.values():
                        all_rssi_values.extend(tag.rssi_values)
                    avg_rssi = sum(all_rssi_values) / len(all_rssi_values) if all_rssi_values else 0
                else:
                    avg_rssi = 0
                self.stats_labels['total_tags'].config(text=f"Unique Tags: {total_tags}")
                self.stats_labels['total_reads'].config(text=f"Total Reads: {total_reads}")
                self.stats_labels['avg_rssi'].config(text=f"Avg RSSI: {avg_rssi:.1f} dBm" if avg_rssi != 0 else "Avg RSSI: N/A")
                sorted_tags = sorted(self.tags.items(), key=lambda x: x[1].read_count, reverse=True)
                for epc, tag_data in sorted_tags:
                    time_elapsed = tag_data.time_since_first
                    rate_per_minute = (tag_data.read_count / time_elapsed * 60) if time_elapsed > 0 else 0
                    first_seen_str = self.format_time_ago(tag_data.time_since_first)
                    last_seen_str = self.format_time_ago(tag_data.time_since_last)
                    rssi_min = min(tag_data.rssi_values) if tag_data.rssi_values else 0
                    rssi_max = max(tag_data.rssi_values) if tag_data.rssi_values else 0
                    tag_type = "📍 ATR7000" if tag_data.has_location_data else "🏷️ Standard"
                    values = (
                        epc,
                        tag_data.read_count,
                        f"{tag_data.average_rssi:.1f} dBm",
                        f"{rssi_min:.1f} dBm",
                        f"{rssi_max:.1f} dBm",
                        first_seen_str,
                        last_seen_str,
                        f"{rate_per_minute:.1f}/min",
                        tag_type
                    )
                    item_id = self.tree.insert('', tk.END, values=values)
                    if tag_data.time_since_last < 2:
                        self.tree.set(item_id, 'EPC', f"🟢 {epc}")
                    elif tag_data.time_since_last < 10:
                        self.tree.set(item_id, 'EPC', f"🟡 {epc}")
                    else:
                        self.tree.set(item_id, 'EPC', f"🔴 {epc}")
                current_time = time.strftime("%H:%M:%S")
                self.last_update_label.config(text=f"Last update: {current_time}")
                if self.debug:
                    print(f"[DEBUG][TagTableWindow] Table updated: {total_tags} tags, {total_reads} reads, average RSSI {avg_rssi:.1f}")
            else:
                raise(Exception("Tree widget not initialized"))
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][TagTableWindow] Table update error: {e}")
            print(f"⚠️ Table update error: {e}")
        if self.running:
            self.window.after(self.update_interval, self.update_table)
    
    def format_time_ago(self, seconds: float) -> str:
        """Formats elapsed time in a readable way"""
        if seconds < 60:
            return f"{int(seconds)}s ago"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m ago"
        else:
            hours = int(seconds / 3600)
            return f"{hours}h ago"
    
    def clear_table(self):
        """Clears all table data"""
        self.tags.clear()
        if self.tree is not None:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.stats_labels['total_tags'].config(text="Unique Tags: 0")
            self.stats_labels['total_reads'].config(text="Total Reads: 0")
            self.stats_labels['avg_rssi'].config(text="Avg RSSI: N/A")
            if self.debug:
                print("[DEBUG][TagTableWindow] Tag table cleaned by user")
            print("🗑️ Tag table cleaned")
        else:
            print("⚠️ Tree widget not initialized")

    def export_csv(self):
        """Exports data in CSV format"""
        try:
            import csv
            from tkinter import filedialog
            
            # Ask the user where to save the file
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save tag data as CSV"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Header
                    writer.writerow(['EPC', 'Reads', 'Avg_RSSI', 'Min_RSSI', 'Max_RSSI', 
                                   'First_Seen', 'Last_Seen', 'Rate_Per_Minute'])
                    
                    # Data
                    for epc, tag_data in self.tags.items():
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
                
                print(f"💾 Data exported to: {filename}")
                
        except Exception as e:
            print(f"❌ CSV export error: {e}")
    
    def on_closing(self):
        """Handles window closure, complete cleanup and monitoring stop"""
        self.running = False
        # Signal monitoring stop (like for graphs)
        if self.stop_event and not self.stop_event.is_set():
            self.stop_event.set()
        def cleanup_tk_objects():
            try:
                # Clear Treeview
                if self.tree:
                    for item in self.tree.get_children():
                        self.tree.delete(item)
                    self.tree = None
                # Clear stats labels
                if hasattr(self, 'stats_labels'):
                    for key in self.stats_labels:
                        self.stats_labels[key].destroy()
                    self.stats_labels = {}
                # Clear last update label
                if hasattr(self, 'last_update_label') and self.last_update_label:
                    self.last_update_label.destroy()
                    self.last_update_label = None
            except Exception as e:
                print(f"❌ Tkinter objects cleanup error: {e}")
            # Destroy window
            if self.window:
                try:
                    self.window.destroy()
                except Exception as e:
                    print(f"❌ Window close error: {e}")
            self.window = None
            # Destroy root window to prevent empty 'tk' window
            if hasattr(self, 'root') and self.root:
                try:
                    self.root.destroy()
                except Exception as e:
                    print(f"❌ Root window close error: {e}")
            self.root = None
        # Schedule cleanup on main thread
        if self.window:
            self.window.after(0, cleanup_tk_objects)
        print("🗑️ Tag table window closed and monitoring stopped")
    
    def run(self):
        """Starts the table window in a separate thread with Windows threading management"""
        import sys
        
        def _run_window():
            # Empty the data queue before starting monitoring
            self.clear_queue()
            try:
                # On Windows, force COM initialization in this thread
                if sys.platform.startswith('win'):
                    try:
                        import ctypes
                        # Initialize COM for this thread (avoid apartment issues)
                        ctypes.windll.ole32.CoInitialize(None)
                    except:
                        pass  # Ignore COM errors
                
                # Create the window
                self.create_window()
                self.running = True
                
                
                if self.window is not None:
                    # Start periodic update
                    self.window.after(100, self.update_table)  # First update after 100ms
                else:
                    raise Exception("Window not initialized")

                if self.root is not None:
                    # Start tkinter main loop on the root window
                    self.root.mainloop()
                else:
                    raise Exception("Root window not initialized")

            except Exception as e:
                print(f"❌ Tag table window error: {e}")
            finally:
                self.running = False
                # Cleanup COM on Windows
                if sys.platform.startswith('win'):
                    try:
                        import ctypes
                        ctypes.windll.ole32.CoUninitialize()
                    except:
                        pass
        
        # Start in a separate thread
        thread = threading.Thread(target=_run_window, daemon=True)
        thread.start()
        
        return thread