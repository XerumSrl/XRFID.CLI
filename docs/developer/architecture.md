# 🏗️ Architecture Overview

Technical architecture and design documentation for Zebra RFID CLI.

## 📋 Project Overview

The Zebra RFID CLI is an interactive Python application designed for seamless integration with Zebra IoT Connector to control RFID readers and visualize real-time tag data streams.

### Core Architecture Principles

- **Interactive CLI Design**: Persistent session management with menu-driven interface
- **Thread-Safe Communication**: Robust multi-threaded architecture for real-time data processing
- **Modular Design**: Clean separation of concerns across functional modules
- **Cross-Platform Compatibility**: Windows, Linux, and macOS support
- **Extensible Framework**: Easy addition of new reader types and visualization modes

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                        │
├─────────────────────────────────────────────────────────────────────┤
│  Interactive CLI (Typer) │  GUI Windows (tkinter/matplotlib)       │
│  - Menu System           │  - Tag Tables                           │
│  - Command Processing    │  - RSSI Plots                           │
│  - User Input/Output     │  - Localization Charts                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                       Application Logic Layer                      │
├─────────────────────────────────────────────────────────────────────┤
│  Session Management     │  Data Processing      │  Visualization    │
│  - Connection State     │  - Tag Aggregation    │  - Real-time Plots │
│  - Config Persistence  │  - RSSI Statistics    │  - Terminal Charts │
│  - Protocol Detection  │  - Position Calc      │  - Data Export     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                      Communication Layer                           │
├─────────────────────────────────────────────────────────────────────┤
│  REST API Client        │  WebSocket Client     │  IOTC Integration │
│  - HTTP/HTTPS          │  - Real-time Events   │  - Service Setup  │
│  - Authentication      │  - Multiple URIs      │  - MQTT Config    │
│  - Reader Control      │  - Fallback Logic     │  - Data Mapping   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                         Hardware Layer                             │
├─────────────────────────────────────────────────────────────────────┤
│  Zebra RFID Readers     │  IoT Connector        │  Network          │
│  - FX9600, FXR90       │  - WebSocket Server    │  - HTTP/HTTPS     │
│  - ATR7000              │  - MQTT Broker        │  - TCP/IP          │
│  - Reader APIs          │  - Data Interfaces    │  - WebSocket       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. Interactive CLI (`interactive_cli.py`)

**Purpose**: Main application controller and user interface

**Key Responsibilities:**
- Persistent session management
- Command routing and execution
- Menu display and user interaction
- Resource lifecycle management

**Threading Model:**
- **Main Thread**: CLI interface and user interaction
- **Background Threads**: WebSocket listener, GUI windows
- **Communication**: Thread-safe queues for data exchange

```python
class InteractiveCLI:
    """Persistent interactive CLI for Zebra RFID"""
    
    def __init__(self, debug: bool = False):
        self.app_context = AppContext(debug=debug)
        self.running = True
        self.listener = None
        self.data_queue = None
        self.stop_event = None
        
    def run(self):
        """Main event loop with command processing"""
        command_map = {
            'l': self.handle_login_connect,
            's': self.handle_start_scan,
            'w': self.startWebsocket,
            # ... other commands
        }
```

### 2. Application Context (`context.py`)

**Purpose**: Centralized state management and reader communication

**Key Responsibilities:**
- Connection state management
- WebSocket lifecycle
- Data aggregation and storage
- Configuration persistence

```python
class AppContext:
    """Central context for reader connection and data management"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.reader_client = None
        self.websocket_listener = None
        self.config_manager = ConfigManager()
        self.tag_data = {}
```

### 3. Configuration Management (`config.py`)

**Purpose**: Persistent configuration storage and retrieval

**Architecture:**
- **File Location**: `~/.zebra_cli/config.json`
- **Format**: JSON for simplicity and cross-platform compatibility
- **Thread Safety**: File-based persistence with atomic writes

```python
class ConfigManager:
    """Manages CLI configuration persistence"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".zebra_cli"
        self.config_file = self.config_dir / "config.json"
        
    def save_config(self, ip_address: str, token: str, protocol: str):
        """Saves configuration with atomic write"""
```

### 4. WebSocket Listener (`websocket_listener.py`)

**Purpose**: Real-time tag event processing

**Architecture:**
- **Event-Driven**: Asynchronous WebSocket client
- **Data Queuing**: Thread-safe queue.Queue for data distribution
- **Reconnection Logic**: Automatic retry with multiple URI fallbacks
- **Error Handling**: Graceful degradation and recovery

```python
class WebSocketListener:
    """Thread-safe WebSocket client for real-time tag events"""
    
    def __init__(self, uri: str, data_queue: queue.Queue):
        self.uri = uri
        self.data_queue = data_queue
        self.stop_event = threading.Event()
        
    def start_listening(self):
        """Main listening loop with reconnection logic"""
```

### 5. Data Visualization (`plotter.py`, `tag_table_window.py`)

**Purpose**: Real-time data visualization and analysis

**Components:**
- **Terminal Plotting**: plotext for in-console visualization
- **GUI Plotting**: matplotlib for advanced charting
- **Tag Tables**: tkinter for tabular data display
- **Export Functions**: CSV export for data analysis

## 🔄 Data Flow Architecture

### Tag Event Processing Pipeline

```
1. Tag Detection (Hardware)
   ↓
2. WebSocket Event (JSON)
   ↓
3. Data Queue (Thread-Safe)
   ↓
4. Context Processing (Aggregation)
   ↓
5. Visualization Updates (Real-Time)
   ↓
6. User Interface Display
```

### Session Management Flow

```
1. User Login Request
   ↓
2. Protocol Detection (HTTP/HTTPS)
   ↓
3. Authentication & Token Storage
   ↓
4. WebSocket Connection Setup
   ↓
5. Session Persistence (Config Save)
   ↓
6. Interactive Menu Access
```

## 🗄️ Data Models

### Tag Data Structure

```python
class TagData:
    """Core tag data model"""
    epc: str                    # Electronic Product Code
    read_count: int             # Total read occurrences
    rssi_values: List[float]    # Signal strength history
    first_seen: datetime        # Initial detection timestamp
    last_seen: datetime         # Most recent detection
    antenna: int                # Reader antenna number
    
    # ATR7000 specific
    position: Optional[Position3D]  # X, Y, Z coordinates
    azimuth: Optional[float]        # Direction angle
    elevation: Optional[float]      # Elevation angle
```

### Configuration Schema

```python
class Config:
    """Configuration data model"""
    ip_address: str         # Reader IP address
    token: str              # Bearer authentication token
    protocol: str           # "http" or "https"
    ws_uri: str             # WebSocket connection URI
```

## 🧵 Threading Architecture

### Thread Responsibilities

| Thread | Purpose | Lifecycle | Communication |
|--------|---------|-----------|---------------|
| **Main** | CLI interface, user interaction | Application lifetime | Direct method calls |
| **WebSocket** | Real-time tag event processing | Connection lifetime | queue.Queue |
| **GUI Windows** | Matplotlib plots, tkinter tables | Window lifetime | queue.Queue |
| **Background Tasks** | File I/O, configuration saves | Task lifetime | threading.Event |

### Thread Safety Mechanisms

- **Data Queues**: `queue.Queue` for thread-safe data exchange
- **Event Coordination**: `threading.Event` for graceful shutdown
- **Atomic Operations**: File-based configuration with atomic writes
- **Resource Cleanup**: Proper thread join and resource disposal

## 🔌 Integration Points

### Zebra IoT Connector (IOTC)

**Purpose**: Bridge between readers and external systems

**Integration Patterns:**
- **WebSocket Setup**: Automated endpoint creation and mapping
- **MQTT Configuration**: Multi-interface topic mapping
- **Service Management**: Start/stop of IOTC services
- **Fallback URIs**: Multiple connection attempts for robustness

### Reader API Integration

**Supported Readers:**
- **FX9600**: Standard IOTC XML configuration
- **FXR90**: Direct REST API with optimized setup
- **ATR7000**: Enhanced with directionality processing

**API Patterns:**
- **Authentication**: Bearer token with automatic renewal
- **Command Execution**: Synchronous REST API calls
- **Status Monitoring**: Real-time WebSocket events
- **Error Handling**: Graceful degradation and retry logic

## 🛡️ Error Handling Strategy

### Layered Error Handling

1. **Network Level**: Connection timeouts, protocol errors
2. **Application Level**: Invalid commands, state errors
3. **User Level**: Friendly error messages with emoji indicators
4. **Debug Level**: Detailed stack traces and logging

### Recovery Mechanisms

- **Automatic Reconnection**: WebSocket and HTTP client recovery
- **Protocol Fallback**: HTTP/HTTPS automatic detection
- **Session Recovery**: Configuration-based reconnection
- **Graceful Degradation**: Partial functionality on connection loss

## 🔧 Development Patterns

### Code Organization

```
zebra_cli/
├── interactive_cli.py          # Main CLI controller
├── context.py                  # Application state management
├── config.py                   # Configuration persistence
├── websocket_listener.py       # Real-time event processing
├── plotter.py                  # Data visualization
├── tag_table_window.py         # GUI table display
├── iotc_client.py              # IoT Connector integration
├── api_submenu.py              # REST API operations
├── atr_submenu.py              # ATR7000 specific features
├── atr7000_locationing.py      # Position calculation logic
└── rest_client/                # Generated API client
    └── io_t_connector_local_rest_ap_is_client/
```

### Design Patterns Used

- **Command Pattern**: CLI command mapping and execution
- **Observer Pattern**: Real-time data updates and notifications
- **Factory Pattern**: Reader-specific client creation
- **Singleton Pattern**: Application context and configuration
- **Strategy Pattern**: Multiple visualization modes

### Testing Strategy

- **Unit Tests**: Core logic and data processing
- **Integration Tests**: Reader communication and WebSocket
- **Manual Testing**: Interactive CLI workflows
- **Error Simulation**: Network failures and recovery

## 🚀 Performance Considerations

### Memory Management

- **Limited RSSI History**: Configurable per-tag storage limits
- **Data Aggregation**: Efficient tag data structures
- **GUI Resource Cleanup**: Proper window and thread disposal
- **Configuration Caching**: Minimal file I/O operations

### Real-Time Performance

- **Asynchronous Processing**: Non-blocking WebSocket handling
- **Queue Management**: Bounded queues to prevent memory growth
- **Update Batching**: Efficient GUI refresh rates
- **Background Processing**: Non-blocking data aggregation

## 🔮 Extensibility Points

### Adding New Reader Support

1. **Create Reader Client**: Implement reader-specific API calls
2. **Add Command Handlers**: Extend CLI command mapping
3. **Update Context Logic**: Add reader detection and initialization
4. **Test Integration**: Verify WebSocket and API functionality

### Adding New Visualization Modes

1. **Create Plotter Class**: Implement visualization logic
2. **Add CLI Commands**: Extend command mapping
3. **Update Data Models**: Add required data fields
4. **Thread Integration**: Ensure thread-safe operation

### Adding New Export Formats

1. **Extend Export Logic**: Add format-specific writers
2. **Update GUI Controls**: Add format selection options
3. **Configuration Options**: Add format preferences
4. **Validation Logic**: Ensure data integrity

---

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
