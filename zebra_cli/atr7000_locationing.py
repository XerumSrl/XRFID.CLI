"""
Module for managing ATR7000 localization with RAW_DIRECTIONALITY messages
"""
import math
import queue
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import numpy as np

 # Import matplotlib with fallback
try:
    import matplotlib
    # Set non-interactive backend to avoid threading conflicts with tkinter
    matplotlib.use('Qt5Agg')  # Use Qt backend if available, otherwise fallback
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.dates import DateFormatter
    import matplotlib.patches as patches
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    try:
        # Fallback to TkAgg backend if Qt is not available
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        from matplotlib.dates import DateFormatter
        import matplotlib.patches as patches
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        MATPLOTLIB_AVAILABLE = True
    except ImportError:
        MATPLOTLIB_AVAILABLE = False

@dataclass
class RawDirectionalityMessage:
    """Represents a RAW_DIRECTIONALITY message from the ATR7000 reader"""
    epc: str
    azimuth: float  # degrees
    elevation: float  # degrees
    timestamp: datetime
    rssi: Optional[float] = None
    antenna: Optional[int] = None

@dataclass
class PositionPoint:
    """Calculated Cartesian position point"""
    epc: str
    x: float  # meters
    y: float  # meters
    z: float  # meters
    timestamp: datetime
    is_significant: bool = False
    azimuth: float = 0.0
    elevation: float = 0.0

@dataclass
class PlotDataSerie:
    """Data series for a specific tag"""
    epc: str
    points: deque = field(default_factory=lambda: deque(maxlen=100))
    color: str = 'blue'
    first_timestamp: Optional[datetime] = None
    last_timestamp: Optional[datetime] = None

class ATR7000PositionCalculator:
    """Position calculator based on RAW_DIRECTIONALITY messages"""
    
    def __init__(self, reader_height: float = 15.0, tag_height: float = 3.0):
        """
        Args:
            reader_height: Reader height in meters (default 15.0m)
            tag_height: Tag height in meters (default 3.0m)
        """
        self.reader_height = reader_height
        self.tag_height = tag_height
        
    def feet_to_meters(self, feet: float) -> float:
        """Converts feet to meters"""
        return feet * 0.3048
    
    def calculate_position(self, raw_data: RawDirectionalityMessage) -> PositionPoint:
        """
        Calculates the Cartesian position from RAW_DIRECTIONALITY data
        """
        # Calculate the object's height
        object_height = self.reader_height - self.tag_height

        azimuth = raw_data.azimuth  # Azimuth in degrees
        elevation = raw_data.elevation  # Elevation in degrees

        # Convert angles to radians
        azimuth_radians = math.radians(azimuth)
        elevation_radians = math.radians(elevation)

        # Project onto the XY plane the object's distance using tangent
        projection_on_plane = object_height * math.tan(elevation_radians)

        # Calculate Cartesian coordinates
        result_x = projection_on_plane * math.sin(azimuth_radians)
        result_y = projection_on_plane * math.cos(azimuth_radians)
        result_z = self.tag_height

        return PositionPoint(
            epc=raw_data.epc,
            x=result_x,
            y=result_y,
            z=result_z,
            timestamp=raw_data.timestamp,
            azimuth=azimuth,
            elevation=elevation
        )

class PointDataStore:
    """Store for managing tag position data"""
    
    def __init__(self, max_series_count: int = 50, max_points_per_series: int = 100, max_all_points_per_series: int = 1000):
        self.max_series_count = max_series_count
        self.max_points_per_series = max_points_per_series
        self.max_all_points_per_series = max_all_points_per_series  # new: max total FIFO points
        self.series_dict: Dict[str, PlotDataSerie] = {}
        self.all_points_dict: Dict[str, deque] = {}  # new: save all FIFO points
        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        self._lock = threading.Lock()
        
    def add_position_point(self, point: PositionPoint) -> Optional[PositionPoint]:
        """Adds a position point and returns the significant point if created"""
        with self._lock:
            # Save ALL points (FIFO)
            if point.epc not in self.all_points_dict:
                self.all_points_dict[point.epc] = deque(maxlen=self.max_all_points_per_series)
            self.all_points_dict[point.epc].append(point)
            # Create or get the series for this EPC
            if point.epc not in self.series_dict:
                if len(self.series_dict) >= self.max_series_count:
                    self._remove_oldest_series()
                
                color_index = len(self.series_dict) % len(self.colors)
                self.series_dict[point.epc] = PlotDataSerie(
                    epc=point.epc,
                    color=self.colors[color_index],
                    first_timestamp=point.timestamp
                )
            
            series = self.series_dict[point.epc]
            series.last_timestamp = point.timestamp
            
            # Aggregation logic based on the provided C# code
            latest_significant_point = None
            for p in reversed(list(series.points)):
                if p.is_significant:
                    latest_significant_point = p
                    break
            
            return_point = None
            
            if latest_significant_point is not None:
                # Check if we have enough recent points to create a new significant point
                non_significant_after_last = [
                    p for p in series.points 
                    if p.timestamp >= latest_significant_point.timestamp and not p.is_significant
                ]
                
                if (len(non_significant_after_last) > 0 and 
                    point.timestamp > latest_significant_point.timestamp + timedelta(milliseconds=500)):
                    
                    # Create new significant point as average
                    avg_x = sum(p.x for p in non_significant_after_last) / len(non_significant_after_last)
                    avg_y = sum(p.y for p in non_significant_after_last) / len(non_significant_after_last)
                    
                    significant_point = PositionPoint(
                        epc=point.epc,
                        x=avg_x,
                        y=avg_y,
                        z=point.z,
                        timestamp=point.timestamp,
                        is_significant=True,
                        azimuth=point.azimuth,
                        elevation=point.elevation
                    )
                    
                    series.points.append(significant_point)
                    return_point = significant_point
                else:
                    # Add non-significant point
                    point.is_significant = False
                    series.points.append(point)
            
            elif len(series.points) == 0:
                # First point of the series - always significant
                point.is_significant = True
                series.points.append(point)
                return_point = point
            else:
                # Create significant point as average of all existing points
                avg_x = sum(p.x for p in series.points) / len(series.points)
                avg_y = sum(p.y for p in series.points) / len(series.points)
                
                significant_point = PositionPoint(
                    epc=point.epc,
                    x=avg_x,
                    y=avg_y,
                    z=point.z,
                    timestamp=point.timestamp,
                    is_significant=True,
                    azimuth=point.azimuth,
                    elevation=point.elevation
                )
                
                series.points.append(significant_point)
                return_point = significant_point
            
            # Remove old points if necessary
            while len(series.points) > self.max_points_per_series:
                series.points.popleft()
                
            return return_point
    
    def _remove_oldest_series(self):
        """Removes the oldest series"""
        if not self.series_dict:
            return
            
        oldest_epc = min(self.series_dict.keys(), 
                        key=lambda epc: self.series_dict[epc].first_timestamp or datetime.now())
        del self.series_dict[oldest_epc]
    
    def get_all_series(self) -> List[PlotDataSerie]:
        """Returns all series"""
        with self._lock:
            return list(self.series_dict.values())
    
    def get_significant_points(self, epc: Optional[str] = None) -> List[PositionPoint]:
        """Returns all significant points, optionally filtered by EPC"""
        with self._lock:
            points = []
            series_to_check = [self.series_dict[epc]] if epc and epc in self.series_dict else self.series_dict.values()
            
            for series in series_to_check:
                points.extend([p for p in series.points if p.is_significant])
            
            return sorted(points, key=lambda p: p.timestamp)
    
    def get_xy_history(self, epc: str, all_points: bool = True) -> Tuple[List[datetime], List[float], List[float]]:
        """Returns the history of X and Y coordinates for an EPC. If all_points=True, returns ALL read points (FIFO), otherwise only significant ones."""
        with self._lock:
            if all_points:
                if epc not in self.all_points_dict:
                    return [], [], []
                points = list(self.all_points_dict[epc])
            else:
                if epc not in self.series_dict:
                    return [], [], []
                series = self.series_dict[epc]
                points = [p for p in series.points if p.is_significant]
            timestamps = [p.timestamp for p in points]
            x_coords = [p.x for p in points]
            y_coords = [p.y for p in points]
            return timestamps, x_coords, y_coords
    
    def generate_heatmap_matrix(self, grid_size: int = 13, meter_per_cell: float = 1.0) -> np.ndarray:
        """
        Generates a heatmap matrix with the number of detected positions per area, using ALL points (FIFO)
        grid_size: grid size (default 13x13)
        meter_per_cell: meters per cell (default 1 meter)
        """
        matrix = np.zeros((grid_size, grid_size), dtype=int)
        center = grid_size // 2
        
        with self._lock:
            for points_deque in self.all_points_dict.values():
                for point in points_deque:
                    # Calculate matrix indices
                    x_idx = int(round(point.x / meter_per_cell)) + center
                    y_idx = int(round(point.y / meter_per_cell)) + center
                    # Check that indices are valid
                    if 0 <= x_idx < grid_size and 0 <= y_idx < grid_size:
                        matrix[y_idx, x_idx] += 1  # Note: y before x for correct visualization
        return matrix
    
    def clear(self):
        """Clears all data (both significant points and all FIFO points)"""
        with self._lock:
            self.series_dict.clear()
            self.all_points_dict.clear()

class ATR7000LocationPlotter:
    """Plotter for ATR7000 localization visualizations"""
    
    def __init__(self, point_store: PointDataStore, debug: bool = False):
        self.point_store = point_store
        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        self.debug = debug
    
    def plot_realtime_positions(self, data_queue: queue.Queue, stop_event: threading.Event):
        """Displays real-time positions"""
        if not MATPLOTLIB_AVAILABLE:
            if self.debug:
                print("[DEBUG][ATR7000LocationPlotter] Matplotlib not available for GUI plotting")
            print("❌ Matplotlib not available for GUI plotting")
            return
        
        try:
            plt.ion()
            fig, ax = plt.subplots(figsize=(12, 10))
            ax.set_title('ATR7000 Tag Positions in Real Time', fontsize=14, fontweight='bold')
            ax.set_xlabel('X (meters)')
            ax.set_ylabel('Y (meters)')
            ax.grid(True, alpha=0.3)
            ax.set_aspect('equal')
            ax.text(0.5, 1.04, "⚠️ Close this window only via the CLI to avoid warnings!", fontsize=11, color='red', ha='center', va='center', transform=ax.transAxes)
            ax.set_xlim(-6, 6)
            ax.set_ylim(-6, 6)
            if self.debug:
                print("[DEBUG][ATR7000LocationPlotter] Plot window opened - monitoring positions...")

            def update_plot(frame):
                if stop_event.is_set():
                    plt.close('all')
                    return []
                try:
                    all_series = self.point_store.get_all_series()
                    ax.clear()
                    ax.set_title('ATR7000 Tag Positions in Real Time', fontsize=14, fontweight='bold')
                    ax.set_xlabel('X (meters)')
                    ax.set_ylabel('Y (meters)')
                    ax.grid(True, alpha=0.3)
                    ax.set_aspect('equal')
                    ax.set_xlim(-6, 6)
                    ax.set_ylim(-6, 6)
                    plots = []
                    for series in all_series:
                        significant_points = [p for p in series.points if p.is_significant]
                        if len(significant_points) > 0:
                            x_coords = [p.x for p in significant_points]
                            y_coords = [p.y for p in significant_points]
                            scatter = ax.scatter(x_coords, y_coords, color=series.color, s=60, alpha=0.8, 
                                               label=f'{series.epc}', edgecolors='white', linewidth=0.5)
                            plots.append(scatter)
                            if len(x_coords) > 0:
                                star = ax.scatter(x_coords[-1], y_coords[-1], color=series.color, 
                                               s=120, marker='*', edgecolors='black', linewidth=1)
                    if all_series:
                        ax.legend(loc='upper right', fontsize=8)
                    if self.debug:
                        print(f"[DEBUG][ATR7000LocationPlotter] Plot update: {len(all_series)} active series")
                    return plots
                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG][ATR7000LocationPlotter] Error updating plot: {e}")
                    print(f"⚠️  Error updating plot: {e}")
                    return []
            # Keep reference to animation to prevent garbage collection
            ani = animation.FuncAnimation(fig, update_plot, interval=2000, blit=False, cache_frame_data=False)
            plt.show(block=False)
            while not stop_event.is_set():
                try:
                    plt.pause(1.0)
                    if not plt.get_fignums():
                        break
                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG][ATR7000LocationPlotter] Error in plot loop: {e}")
                    print(f"⚠️  Error in plot loop: {e}")
                    break
        except Exception as e:
            if self.debug:
                print(f"[DEBUG][ATR7000LocationPlotter] Error during plot initialization: {e}")
            print(f"❌ Error during plot initialization: {e}")
        finally:
            try:
                plt.ioff()
                plt.close('all')
                if self.debug:
                    print("[DEBUG][ATR7000LocationPlotter] Plot window closed")
                else:
                    print("🔄 Plot window closed")
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG][ATR7000LocationPlotter] Error closing plot: {e}")
                print(f"⚠️  Error closing plot: {e}")
    
    def plot_xy_variations(self, epc: str):
        """Shows X and Y variations over time for a specific tag, using ALL read points (FIFO), with high-precision X axis (milliseconds)"""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available for GUI plotting")
            return
        # Use all read points (FIFO)
        timestamps, x_coords, y_coords = self.point_store.get_xy_history(epc, all_points=True)
        if not timestamps:
            print(f"❌ No data available for tag {epc}")
            return
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        # X plot
        ax1.plot(timestamps, x_coords, 'b-', linewidth=2, marker='o', markersize=4, label='X Coordinate')
        ax1.set_ylabel('X (meters)')
        ax1.set_title(f'Tag {epc} Position Variations', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        # Y plot
        ax2.plot(timestamps, y_coords, 'r-', linewidth=2, marker='s', markersize=4, label='Y Coordinate')
        ax2.set_ylabel('Y (meters)')
        ax2.set_xlabel('Time')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        # Format X axis for dates with milliseconds
        ax2.xaxis.set_major_formatter(DateFormatter('%H:%M:%S.%f'))
        # Set X interval to show all data from the start
        if len(timestamps) > 1:
            ax2.set_xlim([min(timestamps), max(timestamps)])
        fig.autofmt_xdate()
        plt.tight_layout()
        plt.show()
    
    def plot_heatmap(self, grid_size: int = 13, meter_per_cell: float = 1.0):
        """Displays the heatmap of detected positions"""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available for GUI plotting")
            return
        
        matrix = self.point_store.generate_heatmap_matrix(grid_size, meter_per_cell)
        
        if np.sum(matrix) == 0:
            print("❌ No data available for the heatmap")
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create the heatmap
        im = ax.imshow(matrix, cmap='hot', interpolation='nearest', origin='lower')
        
        # Add colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        plt.colorbar(im, cax=cax, label='Number of detections')
        
        # Configure axes
        center = grid_size // 2
        ticks = range(0, grid_size, 2)
        labels = [(i - center) * meter_per_cell for i in ticks]

        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels([f'{l:.1f}' for l in labels])
        ax.set_yticklabels([f'{l:.1f}' for l in labels])

        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.set_title(f'Heatmap of Tag Positions (Cells of {meter_per_cell}m)', fontsize=14, fontweight='bold')

        # Add grid
        ax.set_xticks([i - 0.5 for i in range(grid_size + 1)], minor=True)
        ax.set_yticks([i - 0.5 for i in range(grid_size + 1)], minor=True)
        ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5, alpha=0.5)

        plt.tight_layout()
        plt.show()