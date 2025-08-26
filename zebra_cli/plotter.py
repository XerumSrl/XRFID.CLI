# Standard library imports
import time
import queue
import threading
from collections import deque

# Third-party imports
import plotext as plt
try:
    import matplotlib.pyplot as plt_gui
    import matplotlib.animation as animation
    from matplotlib.dates import DateFormatter
    import datetime
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class Plotter:
    """
    Handles plotting of RFID tag data.
    """
    def __init__(self, debug: bool = False) -> None:
        self.rssi_values = []
        self.timestamps = []
        self.rssi_data = deque(maxlen=100)  # Circular buffer for performance
        self.time_data = deque(maxlen=100)
        self.gui_active = False
        self.debug = debug
        
    def plot_live_rssi_gui(self, data_queue: queue.Queue, stop_event: threading.Event) -> None:
        """Displays a real-time RSSI chart in a separate window using matplotlib."""
        
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available. Install it with: pip install matplotlib")
            print("🔄 Fallback to terminal graph...")
            return self.plot_live_rssi(data_queue, stop_event)
            
        self.gui_active = True
        print("🖼️  Opening RSSI graph window...")
        print("💡 Close the window or press Ctrl+C to stop")
        
        # Setup matplotlib figure
        fig, ax = plt_gui.subplots(figsize=(12, 6))
        ax.set_title('Real-time RSSI of RFID Tags', fontsize=14, fontweight='bold')
        ax.set_xlabel('Time')
        ax.set_ylabel('RSSI (dBm)')
        ax.grid(True, alpha=0.3)
        
        # Chart line
        line, = ax.plot([], [], 'b-', linewidth=2, label='RSSI')
        ax.legend()
        
        # Statistics
        stats_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                           verticalalignment='top', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        def update_plot(_frame):
            """Update function for animation."""
            if stop_event.is_set():
                plt_gui.close('all')
                return line, stats_text
                
            # Read new data from queue
            while not data_queue.empty():
                try:
                    tag_event = data_queue.get_nowait()
                    rssi_value = self._extract_rssi_from_event(tag_event)
                    
                    if rssi_value is not None:
                        current_time = datetime.datetime.now()
                        self.time_data.append(current_time)
                        self.rssi_data.append(rssi_value)
                        
                except queue.Empty:
                    break
            
            # Update chart only if there's new data
            if len(self.time_data) > 0:
                line.set_data(list(self.time_data), list(self.rssi_data))
                
                # Update axes
                if len(self.time_data) > 1:
                    ax.set_xlim(min(self.time_data), max(self.time_data))
                    ax.set_ylim(min(self.rssi_data) - 5, max(self.rssi_data) + 5)
                    
                    # Format X axis for dates
                    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
                    fig.autofmt_xdate()
                    
                    # Update statistics
                    avg_rssi = sum(self.rssi_data) / len(self.rssi_data)
                    min_rssi = min(self.rssi_data)
                    max_rssi = max(self.rssi_data)
                    count = len(self.rssi_data)
                    
                    stats_text.set_text(
                        f'Samples: {count}\n'
                        f'Average: {avg_rssi:.1f}dBm\n'
                        f'Min: {min_rssi}dBm\n'
                        f'Max: {max_rssi}dBm'
                    )
                else:
                    stats_text.set_text('Waiting for RSSI data...')
            
            return line, stats_text
        
        # Create animation
        ani = animation.FuncAnimation(fig, update_plot, interval=500, blit=False)
        
        try:
            plt_gui.show()
        except KeyboardInterrupt:
            print("\n⏹️  Graph interrupted")
        finally:
            self.gui_active = False
            plt_gui.close('all')
    
    def _extract_rssi_from_event(self, event):
        """Extracts the RSSI value from an event, supporting different formats."""
        if isinstance(event, list):
            events = event
        else:
            events = [event]
            
        for single_event in events:
            if not isinstance(single_event, dict):
                continue
                
            # Formato Zebra: data.peakRssi
            if 'data' in single_event:
                tag_data = single_event['data']
                if isinstance(tag_data, dict):
                    rssi_value = tag_data.get('peakRssi')
                    if rssi_value is not None:
                        try:
                            return float(rssi_value)
                        except (ValueError, TypeError):
                            pass
            
            # Formati alternativi
            for field in ['RSSI', 'rssi', 'peakRSSI', 'peakRssi']:
                rssi_value = single_event.get(field)
                if rssi_value is not None:
                    try:
                        return float(rssi_value)
                    except (ValueError, TypeError):
                        pass
                        
        return None

    def plot_live_rssi(self, data_queue: queue.Queue, stop_event: threading.Event) -> None:
        """Displays a real-time chart of RFID tag RSSI values."""
        
        plt.title("Real-time RSSI of RFID Tags")
        plt.xlabel("Time (last 100 events)")
        plt.ylabel("RSSI (dBm)")

        while not stop_event.is_set():
            try:
                while not data_queue.empty():
                    tag_event = data_queue.get_nowait()
                    events = tag_event if isinstance(tag_event, list) else [tag_event]
                    for event in events:
                        rssi_value = None
                        if isinstance(event, dict) and 'data' in event:
                            tag_data = event['data']
                            if isinstance(tag_data, dict):
                                rssi_value = tag_data.get('peakRssi')
                                if rssi_value is None:
                                    rssi_value = (tag_data.get('RSSI') or 
                                                tag_data.get('rssi') or 
                                                tag_data.get('peakRSSI'))
                        if rssi_value is None:
                            rssi_value = (event.get('RSSI') or 
                                        event.get('rssi') or 
                                        event.get('peakRSSI') or
                                        event.get('peakRssi'))
                        if rssi_value is not None:
                            try:
                                rssi_float = float(rssi_value)
                                self.rssi_values.append(rssi_float)
                                if self.debug:
                                    print(f"[DEBUG][Plotter] RSSI added to chart: {rssi_float}dBm")
                            except (ValueError, TypeError):
                                if self.debug:
                                    print(f"[DEBUG][Plotter] Invalid RSSI value: {rssi_value}")
            except queue.Empty:
                if self.debug:
                    print("[DEBUG][Plotter] Data queue empty during plot_live_rssi")

            plt.clt()  # Clear terminal
            plt.cld()  # Clear previous chart data
            
            # Keep only the last 100 points for display
            display_data = self.rssi_values[-100:]
            
            if display_data:
                # Create X axis with time indices
                x_values = list(range(len(display_data)))
                plt.plot(x_values, display_data, marker="dot", color="blue")
                plt.title("Real-time RSSI of RFID Tags")
                plt.xlabel(f"Time (last {len(display_data)} events)")
                plt.ylabel("RSSI (dBm)")
                
                # Add statistics
                if len(display_data) > 1:
                    avg_rssi = sum(display_data) / len(display_data)
                    min_rssi = min(display_data)
                    max_rssi = max(display_data)
                    plt.text(f"Average: {avg_rssi:.1f}dBm | Min: {min_rssi}dBm | Max: {max_rssi}dBm", 
                           x=0, y=max_rssi + 2)
            else:
                plt.text("No RSSI data received yet...", x=0, y=0)
            
            plt.show()
            
            time.sleep(1.0)  # Update every second for better readability

    def plot_live_rssi_gui_permanent(self, app_context) -> None:
        """Displays a real-time RSSI chart in GUI window using permanent WebSocket."""
        
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available. Install it with: pip install matplotlib")
            return
            
        self.gui_active = True
        print("🖼️  Opening RSSI graph window...")
        
        # Setup matplotlib figure
        fig, ax = plt_gui.subplots(figsize=(12, 8))
        ax.set_title('Real-time RFID Tag RSSI', fontsize=14, fontweight='bold')
        ax.set_xlabel('Time')
        ax.set_ylabel('RSSI (dBm)')
        ax.grid(True, alpha=0.3)
        
        times = []
        rssi_values = []
        
        def update_plot(_frame):
            """Update function for animation."""
            # Get data from permanent WebSocket
            tag_event = app_context.get_websocket_data()
            
            if tag_event is not None:
                # Extract RSSI value
                rssi_value = None
                if isinstance(tag_event, dict) and 'data' in tag_event:
                    tag_data = tag_event['data']
                    if isinstance(tag_data, dict):
                        rssi_value = tag_data.get('peakRssi')
                        if rssi_value is None:
                            rssi_value = (tag_data.get('RSSI') or 
                                        tag_data.get('rssi') or 
                                        tag_data.get('peakRSSI'))
                if rssi_value is None:
                    rssi_value = (tag_event.get('RSSI') or 
                                tag_event.get('rssi') or 
                                tag_event.get('peakRSSI') or
                                tag_event.get('peakRssi'))
                
                if rssi_value is not None:
                    try:
                        rssi_float = float(rssi_value)
                        import datetime
                        current_time = datetime.datetime.now()
                        
                        times.append(current_time)
                        rssi_values.append(rssi_float)
                        
                        # Keep only last 100 points
                        if len(times) > 100:
                            times.pop(0)
                            rssi_values.pop(0)
                            
                    except (ValueError, TypeError):
                        pass
            
            # Update plot
            ax.clear()
            ax.set_title('Real-time RFID Tag RSSI', fontsize=14, fontweight='bold')
            ax.set_xlabel('Time')
            ax.set_ylabel('RSSI (dBm)')
            ax.grid(True, alpha=0.3)
            
            if times and rssi_values:
                ax.plot(times, rssi_values, 'b-', marker='o', markersize=3)
                
                # Add statistics
                avg_rssi = sum(rssi_values) / len(rssi_values)
                min_rssi = min(rssi_values)
                max_rssi = max(rssi_values)
                
                ax.text(0.02, 0.98, f'Avg: {avg_rssi:.1f}dBm | Min: {min_rssi}dBm | Max: {max_rssi}dBm | Count: {len(rssi_values)}', 
                       transform=ax.transAxes, verticalalignment='top', fontsize=10,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
                
                # Auto-adjust time axis
                plt_gui.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                fig.autofmt_xdate()
            else:
                ax.text(0.5, 0.5, 'Waiting for RSSI data...', 
                       transform=ax.transAxes, ha='center', va='center')
            
            return ()
        
        # Create animation
        ani = animation.FuncAnimation(fig, update_plot, interval=500, blit=False, cache_frame_data=True, save_count=100)
        
        try:
            plt_gui.show()
        except KeyboardInterrupt:
            print("\n⏹️  Graph interrupted")
        finally:
            self.gui_active = False
            plt_gui.close('all')

class EnhancedPlotter(Plotter):
    """Enhanced plotter with tag selection and filtering"""
    
    def __init__(self, target_epc: str = 'ALL', debug: bool = False) -> None:
        super().__init__(debug=debug)
        self.target_epc = target_epc
        self.tag_data = {}  # Dictionary to store data for each tag
        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']
        
    def plot_live_rssi_gui(self, data_queue: queue.Queue, stop_event: threading.Event) -> None:
        """Displays RSSI chart filtered for specific tag or all tags"""
        
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available. Install it with: pip install matplotlib")
            return
            
        self.gui_active = True
        print("🖼️  Opening RSSI graph window...")
        
        # Setup matplotlib figure
        fig, ax = plt_gui.subplots(figsize=(14, 8))
        
        if self.target_epc == 'ALL':
            ax.set_title('Real-time RSSI of All RFID Tags', fontsize=14, fontweight='bold')
        else:
            ax.set_title(f'Real-time RSSI of Tag {self.target_epc}', fontsize=14, fontweight='bold')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('RSSI (dBm)')
        ax.grid(True, alpha=0.3)
        
        # Statistics
        stats_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                           verticalalignment='top', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        def update_plot(_frame):
            """Update function for animation."""
            if stop_event.is_set():
                plt_gui.close('all')
                return ()
                
            # Read new data from queue
            while not data_queue.empty():
                try:
                    tag_event = data_queue.get_nowait()
                    epc, rssi_value = self._extract_tag_data_from_event(tag_event)
                    
                    if epc and rssi_value is not None:
                        # Filter for specific tag
                        if self.target_epc != 'ALL' and epc != self.target_epc:
                            continue
                            
                        current_time = datetime.datetime.now()
                        
                        # Initialize data structure for new tag
                        if epc not in self.tag_data:
                            self.tag_data[epc] = {
                                'times': deque(maxlen=100),
                                'rssi': deque(maxlen=100),
                                'color': self.colors[len(self.tag_data) % len(self.colors)]
                            }
                        
                        # Add new data
                        self.tag_data[epc]['times'].append(current_time)
                        self.tag_data[epc]['rssi'].append(rssi_value)
                        
                except queue.Empty:
                    break
            
            # Update chart if there's data
            if self.tag_data:
                # Clear previous lines
                ax.clear()
                ax.set_xlabel('Time')
                ax.set_ylabel('RSSI (dBm)')
                ax.grid(True, alpha=0.3)
                
                if self.target_epc == 'ALL':
                    ax.set_title('Real-time RSSI of All RFID Tags', fontsize=14, fontweight='bold')
                else:
                    ax.set_title(f'Real-time RSSI of Tag {self.target_epc}', fontsize=14, fontweight='bold')
                
                all_times = []
                all_rssi = []
                stats_info = []
                
                # Draw line for each tag
                for epc, data in self.tag_data.items():
                    if len(data['times']) > 0:
                        times_list = list(data['times'])
                        rssi_list = list(data['rssi'])
                        
                        # Draw the line
                        ax.plot(times_list, rssi_list, 
                               color=data['color'], linewidth=2, 
                               label=f'{epc}', marker='o', markersize=3)
                        
                        all_times.extend(times_list)
                        all_rssi.extend(rssi_list)
                        
                        # Calculate statistics for this tag
                        avg_rssi = sum(rssi_list) / len(rssi_list)
                        min_rssi = min(rssi_list)
                        max_rssi = max(rssi_list)
                        count = len(rssi_list)
                        
                        stats_info.append(f'{epc}: {count} samples, Average: {avg_rssi:.1f}dBm')
                
                # Set axis limits
                if all_times and all_rssi:
                    ax.set_xlim(min(all_times), max(all_times))
                    ax.set_ylim(min(all_rssi) - 5, max(all_rssi) + 5)
                    
                    # Format X axis for dates
                    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
                    fig.autofmt_xdate()
                    
                    # Show legend if multiple tags
                    if len(self.tag_data) > 1:
                        ax.legend(loc='upper right')
                    
                    # Update statistics
                    stats_text = ax.text(0.02, 0.98, '\n'.join(stats_info), 
                                       transform=ax.transAxes, 
                                       verticalalignment='top', fontsize=9,
                                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
                else:
                    ax.text(0.5, 0.5, f'Waiting for data for tag: {self.target_epc}', 
                           transform=ax.transAxes, ha='center', va='center')
            
            return ()
        
        # Create animation
        ani = animation.FuncAnimation(fig, update_plot, interval=500, blit=False, cache_frame_data=True, save_count=100)
        
        try:
            plt_gui.show()
        except KeyboardInterrupt:
            print("\n⏹️  Graph interrupted")
        finally:
            self.gui_active = False
            plt_gui.close('all')
    
    def _extract_tag_data_from_event(self, event):
        """Extracts EPC and RSSI from a tag event"""
        epc = None
        rssi_value = None
        
        if isinstance(event, dict):
            # Zebra format: data.idHex, data.peakRssi
            if 'data' in event and isinstance(event['data'], dict):
                tag_data = event['data']
                epc = tag_data.get('idHex')
                rssi_value = tag_data.get('peakRssi')
            else:
                # Alternative formats
                epc = event.get('epc', event.get('EPC'))
                rssi_value = event.get('RSSI', event.get('rssi', event.get('peakRSSI')))
        
        # Convert RSSI to float if possible
        if rssi_value is not None:
            try:
                rssi_value = float(rssi_value)
            except (ValueError, TypeError):
                rssi_value = None
        
        return epc, rssi_value

    def plot_live_rssi_gui_permanent(self, app_context) -> None:
        """Displays RSSI chart filtered for specific tag or all tags using permanent WebSocket"""
        
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available. Install it with: pip install matplotlib")
            return
            
        self.gui_active = True
        print("🖼️  Opening RSSI graph window...")
        
        # Setup matplotlib figure
        fig, ax = plt_gui.subplots(figsize=(14, 8))
        
        if self.target_epc == 'ALL':
            ax.set_title('Real-time RSSI of All RFID Tags', fontsize=14, fontweight='bold')
        else:
            ax.set_title(f'Real-time RSSI of Tag {self.target_epc}', fontsize=14, fontweight='bold')
            
        ax.set_xlabel('Time')
        ax.set_ylabel('RSSI (dBm)')
        ax.grid(True, alpha=0.3)
        
        # Statistics
        stats_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                           verticalalignment='top', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        def update_plot(_frame):
            """Update function for animation."""
            # Read new data from permanent WebSocket
            for _ in range(10):  # Process up to 10 events per update
                tag_event = app_context.get_websocket_data()
                if tag_event is None:
                    break
                    
                epc, rssi_value = self._extract_tag_data_from_event(tag_event)
                
                if epc and rssi_value is not None:
                    # Filter for specific tag
                    if self.target_epc != 'ALL' and epc != self.target_epc:
                        continue
                        
                    current_time = datetime.datetime.now()
                    
                    # Initialize data structure for new tag
                    if epc not in self.tag_data:
                        self.tag_data[epc] = {
                            'times': deque(maxlen=100),
                            'rssi': deque(maxlen=100),
                            'color': self.colors[len(self.tag_data) % len(self.colors)]
                        }
                    
                    # Add new data
                    self.tag_data[epc]['times'].append(current_time)
                    self.tag_data[epc]['rssi'].append(rssi_value)
            
            # Update chart if there's data
            if self.tag_data:
                # Clear previous lines
                ax.clear()
                ax.set_xlabel('Time')
                ax.set_ylabel('RSSI (dBm)')
                ax.grid(True, alpha=0.3)
                
                if self.target_epc == 'ALL':
                    ax.set_title('Real-time RSSI of All RFID Tags', fontsize=14, fontweight='bold')
                else:
                    ax.set_title(f'Real-time RSSI of Tag {self.target_epc}', fontsize=14, fontweight='bold')
                
                # Plot data for each tag
                stats_lines = []
                for epc, data in self.tag_data.items():
                    if data['times'] and data['rssi']:
                        ax.plot(data['times'], data['rssi'], 
                               color=data['color'], label=f'{epc[:8]}...', marker='o', markersize=3)
                        
                        # Statistics for each tag
                        avg_rssi = sum(data['rssi']) / len(data['rssi'])
                        min_rssi = min(data['rssi'])
                        max_rssi = max(data['rssi'])
                        count = len(data['rssi'])
                        stats_lines.append(f"{epc[:8]}: Avg {avg_rssi:.1f}dBm (Min {min_rssi}, Max {max_rssi}, Count {count})")
                
                # Update legend and statistics
                if len(self.tag_data) > 1:
                    ax.legend(loc='upper right')
                
                # Update statistics text
                stats_text.set_text('\n'.join(stats_lines[:5]))  # Show max 5 tags in stats
                
                # Auto-adjust time axis
                plt_gui.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                fig.autofmt_xdate()
            else:
                if self.target_epc == 'ALL':
                    ax.text(0.5, 0.5, 'Waiting for tag data...', 
                           transform=ax.transAxes, ha='center', va='center')
                else:
                    ax.text(0.5, 0.5, f'Waiting for data for tag: {self.target_epc}', 
                           transform=ax.transAxes, ha='center', va='center')
            
            return ()
        
        # Create animation
        ani = animation.FuncAnimation(fig, update_plot, interval=500, blit=False, cache_frame_data=True, save_count=100)
        
        try:
            plt_gui.show()
        except KeyboardInterrupt:
            print("\n⏹️  Graph interrupted")
        finally:
            self.gui_active = False
            plt_gui.close('all')

    def plot_live_rssi_permanent(self, app_context) -> None:
        """Displays a real-time chart of RFID tag RSSI values using permanent WebSocket."""
        
        plt.title("Real-time RFID Tag RSSI")
        plt.xlabel("Time (last 100 events)")
        plt.ylabel("RSSI (dBm)")

        try:
            while True:
                # Get data from permanent WebSocket
                tag_event = app_context.get_websocket_data()
                
                if tag_event is not None:
                    events = tag_event if isinstance(tag_event, list) else [tag_event]
                    for event in events:
                        rssi_value = None
                        if isinstance(event, dict) and 'data' in event:
                            tag_data = event['data']
                            if isinstance(tag_data, dict):
                                rssi_value = tag_data.get('peakRssi')
                                if rssi_value is None:
                                    rssi_value = (tag_data.get('RSSI') or 
                                                tag_data.get('rssi') or 
                                                tag_data.get('peakRSSI'))
                        if rssi_value is None:
                            rssi_value = (event.get('RSSI') or 
                                        event.get('rssi') or 
                                        event.get('peakRSSI') or
                                        event.get('peakRssi'))
                        if rssi_value is not None:
                            try:
                                rssi_float = float(rssi_value)
                                self.rssi_values.append(rssi_float)
                                if self.debug:
                                    print(f"[DEBUG][Plotter] RSSI added to chart: {rssi_float}dBm")
                            except (ValueError, TypeError):
                                if self.debug:
                                    print(f"[DEBUG][Plotter] Invalid RSSI value: {rssi_value}")

                plt.clt()  # Clear terminal
                plt.cld()  # Clear previous chart data
                
                # Keep only the last 100 points for display
                display_data = self.rssi_values[-100:]
                
                if display_data:
                    # Create X axis with time indices
                    x_values = list(range(len(display_data)))
                    
                    # Plot data
                    plt.plot(x_values, display_data, color='blue', marker='o')
                    
                    # Set axis limits
                    plt.ylim(min(display_data) - 5, max(display_data) + 5)
                    
                    # Add statistics
                    avg_rssi = sum(display_data) / len(display_data)
                    min_rssi = min(display_data)
                    max_rssi = max(display_data)
                    plt.text(f"Average: {avg_rssi:.1f}dBm | Min: {min_rssi}dBm | Max: {max_rssi}dBm", 
                           x=0, y=max_rssi + 2)
                else:
                    plt.text("No RSSI data received yet...", x=0, y=0)
                
                plt.show()
                
                time.sleep(1.0)  # Update every second for better readability
                
        except KeyboardInterrupt:
            pass  # Exit gracefully on Ctrl+C