# 🏷️ Zebra RFID CLI - Interactive Interface for Zebra RFID Readers

A powerful interactive CLI to control Zebra RFID readers and visualize real-time data using the Zebra IoT Connector.

## 📄 Open Source License

**This is an open source project developed by [Xerum Srl](https://xerum.it)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Copyright © 2025 Xerum Srl. This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**If you modify this code, please keep the original credits and attribution to Xerum Srl.**

## 🚀 Installation & Quick Start

### 1. System Requirements
- **Python 3.9+** (check with `python --version`)
- **Git** to clone the repository
- **Zebra FX9600, FXR90, or ATR7000** connected to the network
- **Network access** to the reader (same subnet or proper routing)

### 2. Clone and Setup

#### Windows (PowerShell)
```powershell
# Clone the repository
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI

# Create a virtual environment (recommended)
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Launch CLI with your reader details
python xrcli_entrypoint.py --ip <READER-IP> -u <USERNAME> -p <PASSWORD>

# Example: Launch CLI (default credentials)
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change

# Launch CLI with debug logging
python xrcli_entrypoint.py --ip <READER-IP> -u <USERNAME> -p <PASSWORD> --debug
```

#### Linux/macOS (Bash)
```bash
# Clone the repository
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI

# Create a virtual environment (recommended)
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch CLI with your reader details
python xrcli_entrypoint.py --ip <READER-IP> -u <USERNAME> -p <PASSWORD>

# Example: Launch CLI (default credentials)
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change

# Launch CLI with debug logging
python xrcli_entrypoint.py --ip <READER-IP> -u <USERNAME> -p <PASSWORD> --debug
```

#### Alternative: Quick Start Script (Windows)
```powershell
# Quick setup script for Windows users
# Save this as setup.ps1 and run: .\setup.ps1

# Check Python version
python --version

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Setup complete! Run the CLI with:" -ForegroundColor Green
Write-Host "python xrcli_entrypoint.py --ip YOUR_READER_IP -u admin -p change" -ForegroundColor Yellow
```

### 3. Main Dependencies
Below are the main dependencies used in this project. For the full list and exact versions, see `requirements.txt` and `requirements-freeze.txt`.

```
websocket-client>=1.8.0        # WebSocket client for real-time tag events
plotext>=5.3.2                # Terminal-based plotting
matplotlib>=3.9.0             # GUI plotting
numpy>=1.26.4                 # Numerical operations
httpx>=0.28.1                 # HTTP client for REST API
attrs>=25.3.0                 # Class attribute management
typer>=0.16.0                 # Modern CLI framework
rich>=14.0.0                  # Colored terminal output
wcwidth>=0.2.13               # Unicode width support
colorama>=0.4.6               # Terminal color support
python-dateutil>=2.9.0.post0  # Date/time utilities
ruamel.yaml>=0.18.14          # YAML parsing
shellingham>=1.5.4            # Shell detection
six>=1.17.0                   # Python 2/3 compatibility
sniffio>=1.3.1                # Async context detection
typing_extensions>=4.14.1     # Type hint extensions
pydantic>=2.11.7              # Data validation
Jinja2>=3.1.6                 # Templating engine
markdown-it-py>=3.0.0         # Markdown parser
MarkupSafe>=3.0.2             # Safe string handling
mdurl>=0.1.2                  # Markdown URL support
openapi-python-client>=0.25.2 # OpenAPI client generator
packaging>=25.0               # Package version handling
pluggy>=1.6.0                 # Plugin management
pydantic_core>=2.33.2         # Pydantic core
Pygments>=2.19.2              # Syntax highlighting
pytest>=8.4.1                 # Testing framework
iniconfig>=2.1.0              # INI file parsing
ruff>=0.12.2                  # Linter
requests                      # HTTP requests
urllib3>=1.26.0               # HTTP library
tkinter                       # GUI (included with Python)
```

For development and testing, all dependencies are pinned in `requirements-freeze.txt`.

## 🎯 Main Features

- **🔐 Automatic Connection**: Auto-login with protocol detection (HTTP/HTTPS)
- **📡 Reader Control**: Start/stop RFID scans via REST API
- **🌐 IoT Connector (IOTC)**: Complete setup and cloud connection management for both WebSocket or MQTT endpoints
- **📋 Real-Time Monitoring**: Tag table with full statistics and export
- **📊 Data Visualization**: Real-time RSSI graphs (terminal and GUI)
- **📍 ATR7000 Localization**: Complete positional tracking system
- **🎧 WebSocket Listener**: Real-time tag events with robust fallback
- **🔧 REST API Submenu**: Interact directly with the main reader API endpoint for advanced operations and diagnostics

## 🎛️ Main Menu

```
📋 XRFID CLI - Main Menu:
┌─────────────────────────────────────────────────────────────┐
│ CONNECTION:                                                 │
│ l / login      🔐 Login and automatic connection            │
│ d / disconnect 🔌 Disconnect                                │
├─────────────────────────────────────────────────────────────┤
│ READER OPERATIONS:                                          │
│ s / start      🟢 Start scan                                │
│ x / stop       🔴 Stop scan                                 │
│ r / restApi    🔧 API Requests (submenu)                    │
├─────────────────────────────────────────────────────────────┤
│ MONITORING:                                                 │
│ w / websocket  🎧 Simple WebSocket connection               │
│ m / monitoring 📋 Tag table                                 │
│ p / plot       📊 RSSI graph                                │
│ a / atr        📍 ATR7000 - Localization (submenu)          │
├─────────────────────────────────────────────────────────────┤
│ IOT CONNECTOR (IOTC):                                       │
│ i / iotc       🌐 Setup IoT Connector                       │
│ di / disconnectIOTC 🔌 Disconnect from IOTC                 │
├─────────────────────────────────────────────────────────────┤
│ UTILITIES:                                                  │
│ c / clear      🧹 Clear screen                              │
│ rs / reset     💥 Force WebSocket reset                     │
│ h / help       ❓ Command help                              │
│ q / quit       🚪 Exit                                      │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 IoT Connector (IOTC)

The IOTC system allows the reader to connect to the Zebra cloud for advanced features. The CLI provides intelligent setup for both WebSocket and MQTT endpoints.

### Automatic Setup (Command `i` / `iotc`)

The IOTC setup command supports two connection types with different parameters:

#### **WebSocket Setup (for CLI communication)**

```bash
iotc -type ws
# or simply: iotc
```

or with the shortcut command:

```bash
i -type ws
# or simply: i
```

**Purpose**: Sets up WebSocket endpoint on the reader's data interface specifically for CLI communication with real-time tag events.

**What it does:**
- ✅ Check reader enrollment status
- ✅ Configure WebSocket endpoint on data interface
- ✅ Map WebSocket endpoint to data events
- ✅ Start IOTC service and establish connection

#### **MQTT Setup (for general integrations)**
```bash
iotc -type mqtt -hostname <BROKER-IP> -readername <READER-NAME> -endpointname <ENDPOINT-NAME>
```
or with the shortcut command:

```bash
i -type mqtt -hostname <BROKER-IP> -readername <READER-NAME> -endpointname <ENDPOINT-NAME>
```
**Purpose**: Sets up MQTT endpoints on all reader interfaces for external system integration with brokers.

**Required Parameters:**
- `-hostname`: MQTT broker IP address (e.g., `192.168.1.100`)
- `-readername`: Reader identifier for topic naming (e.g., `FXR9001234`)
- `-endpointname`: Endpoint configuration name (e.g., `mqtt-prod`)

**What it does:**
- ✅ Check reader enrollment status
- ✅ Configure MQTT endpoints on **all interfaces**:
  - **Data Interface**: Tag events → `tevents/{reader_name}`
  - **Control Interface**: Commands ↔ `ccmds/{reader_name}` / `crsp/{reader_name}`
  - **Management Interface**: Commands ↔ `mcmds/{reader_name}` / `mrsp/{reader_name}`
  - **Management Events Interface**: Status events → `mevents/{reader_name}`
- ✅ Configure data-level batching and retention policies
- ✅ Map all endpoints to their respective interfaces
- ✅ Start IOTC service

#### **FXR90 Readers**
For FXR90 readers, the CLI automatically detects the reader type and uses direct REST API configuration instead of the standard IOTC XML commands.

## 📍 ATR7000 Localization

Advanced positional tracking system using RAW_DIRECTIONALITY messages from ATR7000 readers to calculate precise tag positions in Cartesian coordinates (X, Y, Z).

### **🎯 Core Technology**
- **RAW_DIRECTIONALITY Processing**: Converts azimuth/elevation angles to Cartesian coordinates
- **Position Calculation**: Uses reader height and tag height for accurate 3D positioning
- **Smart Aggregation**: Significant point detection with temporal averaging
- **Real-time Visualization**: Multiple plotting modes for position analysis

### **📊 Available Commands**

| Command     | Shortcut | Action                                 |
|-------------|----------|----------------------------------------|
| realtime    | r        | Real-time position chart (matplotlib)  |
| xy          | x        | X/Y variations over time (per tag)      |
| heatmap     | h        | Heatmap of detected zones (13x13 grid) |
| config      | c        | Height configuration (reader/tag)       |
| clear       | cl       | Clear all localization data            |
| stat        | s        | Localization statistics                 |
| back        | b        | Return to main menu                     |

### **🔧 Configuration Options**
- **Reader Height**: Configurable reader mounting height (default: 3.0m)
- **Tag Height**: Configurable tag height above ground (default: 0.0m)
- **Grid Resolution**: 13x13 grid for heatmap with 1m per cell
- **Point Storage**: Up to 100 significant points per tag, 1000 total points (FIFO)

### **📈 Visualization Features**
- **Real-time Chart**: Live position updates with color-coded tags
- **X/Y Variations**: High-precision timestamp plotting (milliseconds)
- **Heatmap**: Detection density visualization with configurable grid
- **Statistics**: Complete tracking metrics per tag and totals

## 🧩 API Submenu

Access to the API submenu is only available from the main CLI menu when already connected to a reader. Select `r` or `restApi` from the main menu while connected: the API submenu will open for the same reader and session.

For full details on available features and commands, see [API-SUBMENU-README.md](API-SUBMENU-README.md).

## 🎯 Typical Workflow

1. **Connect**: `l` for automatic login or `k` for manual connection
2. **Setup IOTC** (if needed): `i` for complete configuration
3. **Start Scan**: `v` to begin reading tags
4. **Monitor**:
   - `t` for complete table with statistics
   - `p` for RSSI graph in window
   - `a` for ATR7000 localization
5. **Stop**: `f` to stop scanning
6. **Disconnect**: `d` to close the session

## 🏗️ Technical Architecture

- **🐍 Python 3.9+** with full type hints
- **🔌 websocket-client**: Robust WebSocket connections
- **📊 plotext + matplotlib**: Terminal + GUI plotting
- **🖼️ tkinter**: Separate windows for tables
- **🧵 Multi-threading**: Background WebSocket listener
- **📦 queue.Queue**: Thread-safe communication
- **⚙️ Typer**: Modern CLI framework with auto-completion

## 📚 Documentation

### 🚀 Quick Start
- **[5-Minute Quick Start](docs/quick-start.md)** - Get up and running immediately
- **[Complete Installation Guide](docs/installation.md)** - Platform-specific setup instructions
- **[Command Reference](docs/reference/commands.md)** - All available commands and parameters

### 📖 User Guides
- **[Basic Operations](docs/user-guide/basic-operations.md)** - Essential workflows and commands
- **[IoT Connector Setup](docs/user-guide/iotc-setup.md)** - WebSocket and MQTT configuration
- **[Tag Monitoring](docs/user-guide/tag-monitoring.md)** - Real-time visualization and data export
- **[ATR7000 Localization](docs/user-guide/atr7000-localization.md)** - Advanced position tracking

### 🔧 Advanced Topics
- **[API Integration](docs/advanced/api-integration.md)** - REST API automation and scripting
- **[Troubleshooting](docs/advanced/troubleshooting.md)** - Common issues and solutions
- **[Architecture Overview](docs/developer/architecture.md)** - Technical design and structure

### 📋 Complete Documentation Index
**[📚 Browse All Documentation](docs/README.md)** - Complete organized documentation with navigation

---

## 📚 Further Information and Documentation

For detailed information on advanced configuration and API usage:
- [API-SUBMENU-README.md](API-SUBMENU-README.md) — Detailed API submenu documentation and advanced usage

## 🛠️ Quick Troubleshooting

### Connection Issues
- Ensure the reader is powered on and reachable
- Check credentials (usually admin/admin)
- The CLI automatically detects HTTP/HTTPS

### WebSocket
- Automatic fallback on multiple ports (80, 443, 8080, 8443)
- Check firewall and network configuration

### IOTC
- Restart setup with `i` / `iotc` if needed

## 📁 Project Structure

```
XRFID-Test-CLI/
├── zebra_cli/                      # Main CLI package
│   ├── interactive_cli.py           # Main interactive CLI
│   ├── websocket_listener.py        # WebSocket listener (background thread)
│   ├── tag_table_window.py          # Tag table GUI window
│   ├── plotter.py                   # RSSI plotting (terminal/GUI)
│   ├── atr_submenu.py               # ATR submenu logic
│   ├── atr7000_locationing.py       # ATR7000 localization features
│   ├── api_submenu.py               # REST API submenu logic
│   ├── config.py                    # Configuration management
│   ├── context.py                   # Session/context management
│   ├── rest_client/                 # Generated REST API client
│   ├── iotc_client.py               # IoT Connector client (move here for consistency)
│   └── __pycache__/                 # Python bytecode cache
├── tests/                           # Test suite
│   ├── test_api_submenu.py          # API submenu tests
│   └── __pycache__/                 # Test bytecode cache
├── main.py                          # Main entry point (if present)
├── xrcli_entrypoint.py              # CLI entrypoint
├── requirements.txt                 # Python dependencies
├── requirements-freeze.txt          # Pinned dependencies for dev/test
├── config.yaml                      # Persistent configuration
├── directionality.html              # Directionality visualization (HTML resource)
├── README.md                        # Main documentation
├── API-SUBMENU-README.md            # API submenu documentation
├── ...                              # Other supporting files/folders
```
### ❓ HELP - Tips and Troubleshooting

**TIPS:**
- Protocol (HTTP/HTTPS) is auto-detected and remembered after login
- WebSocket adapts to chosen protocol
- Use Ctrl+C to interrupt monitoring or plotting
- Tag table and RSSI plot open in separate windows
- Most commands require an active connection
- For ATR7000 features, use the ATR submenu (a / atr)
- For API requests, use the REST API submenu (r / restApi)

**TROUBLESHOOTING:**
- Ensure the reader is powered on and reachable
- Default credentials are usually admin/change
- When trying to setup the reader for a WebSocket connection and the procedure fails, run IOTC setup again
- If you encounter errors, try disconnecting and logging in again

## 🤝 Contributions

**This is an open source project by Xerum Srl.** We welcome contributions!

To contribute:
1. Fork the repository
2. Create a branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

**Please maintain the original attribution to Xerum Srl in your contributions.**

## 📜 License & Credits

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for complete details.

**Developed by [Xerum Srl](https://xerum.it)**  
Copyright © 2025 Xerum Srl

If you use or modify this code, please keep the original credits and attribution.

---

**🎉 Ready to use!** The CLI automatically manages connection, protocols, and WebSocket with robust fallback.
