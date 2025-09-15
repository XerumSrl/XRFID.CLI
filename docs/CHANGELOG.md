# 📝 Changelog

All notable changes to Zebra RFID CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release preparation
- Comprehensive documentation structure
- MIT License with Xerum Srl attribution

### Changed
- Repository structure for open source publication
- Updated README with installation instructions

## [1.0.0] - 2025-08-26 - Initial Release 🎉

### Added

#### Core Features
- **Interactive CLI Interface** with persistent session management
- **Multi-Reader Support**: FX9600, FXR90, and ATR7000 compatibility
- **Real-Time Tag Monitoring** with WebSocket connectivity
- **Data Visualization** in terminal and GUI windows
- **Configuration Persistence** with automatic protocol detection

#### Reader Operations
- **Connection Management**: Automatic HTTP/HTTPS protocol detection
- **Start/Stop Scanning**: Basic RFID tag reading control
- **Authentication**: Bearer token management with persistent sessions
- **WebSocket Integration**: Real-time tag event streaming

#### Visualization and Monitoring
- **Tag Table Window**: Real-time tkinter-based tag statistics display
  - Read count, RSSI min/max/avg, timestamps
  - Color-coded status indicators
  - CSV export functionality
- **RSSI Plotting**: Terminal and GUI-based signal strength visualization
- **WebSocket Console**: Simple real-time tag event display
- **Data Export**: CSV export for tag statistics and analysis

#### IoT Connector (IOTC) Integration
- **WebSocket Setup**: Automated IOTC configuration for real-time streaming
- **MQTT Configuration**: Multi-interface topic mapping for external systems
- **Service Management**: Start/stop IOTC services on readers
- **Multi-URI Fallback**: Robust WebSocket connection with multiple fallback URIs

#### ATR7000 Localization Features
- **Position Calculation**: 3D coordinate calculation from directionality data
- **Real-Time Position Tracking**: Live matplotlib-based position visualization
- **Heatmap Analysis**: 13x13 grid position heatmap
- **X/Y Variations**: Per-tag position tracking over time
- **Configuration**: Adjustable reader and tag heights
- **Statistics**: Position tracking metrics and data management

#### API and REST Client
- **Generated API Client**: OpenAPI-based REST client for Zebra readers
- **API Submenu**: Interactive REST API testing and exploration
- **Multiple Reader Support**: Optimized handling for different reader types
- **Error Handling**: Graceful API error handling and recovery

#### Platform Support
- **Cross-Platform**: Windows, Linux, and macOS compatibility
- **Python 3.9+**: Modern Python version support
- **Virtual Environment**: Isolated dependency management
- **Package Management**: Complete requirements specification

### Technical Architecture

#### Threading Model
- **Main Thread**: CLI interface and user interaction
- **Background Thread**: WebSocket listener for real-time events
- **GUI Threads**: Separate threads for matplotlib and tkinter windows
- **Thread-Safe Communication**: queue.Queue for data exchange
- **Lifecycle Management**: threading.Event for clean shutdown

#### Configuration System
- **JSON Configuration**: Simple, cross-platform configuration storage
- **Location**: `~/.zebra_cli/config.json`
- **Automatic Management**: Session persistence and protocol detection
- **Manual Override**: Support for manual configuration editing

#### Data Processing
- **Real-Time Aggregation**: Efficient tag data collection and statistics
- **Memory Management**: Configurable data retention limits
- **Export Functionality**: CSV export for external analysis
- **Position Calculation**: Advanced 3D positioning for ATR7000

#### Error Handling
- **Graceful Degradation**: Continues operation on partial failures
- **User-Friendly Messages**: Clear error reporting with emoji indicators
- **Debug Mode**: Detailed logging for troubleshooting
- **Automatic Recovery**: WebSocket reconnection and session restoration

### Developer Features

#### Code Quality
- **Type Hints**: Comprehensive type annotations throughout
- **PEP 8 Compliance**: Professional Python code standards
- **Modular Design**: Clean separation of concerns
- **Documentation**: Comprehensive inline and external documentation

#### Extensibility
- **Plugin Architecture**: Easy addition of new reader types
- **Visualization Framework**: Extensible plotting and display system
- **Command System**: Simple addition of new CLI commands
- **Configuration**: Flexible configuration management

### Command Reference

#### Main Menu Commands
- `l` / `login`: Login and automatic connection
- `d` / `disconnect`: Disconnect from reader
- `s` / `start`: Start RFID scanning
- `x` / `stop`: Stop RFID scanning
- `w` / `websocket`: Simple WebSocket listener
- `m` / `monitoring`: Tag table window
- `p` / `plot`: RSSI visualization
- `r` / `restapi`: REST API submenu
- `a` / `atr`: ATR7000 localization submenu
- `ex` / `export`: Export collected data to PDF
- `i` / `iotc`: IoT Connector setup
- `di` / `disconnectIOTC`: Disconnect IOTC
- `c` / `clear`: Clear screen
- `rs` / `reset`: Reset WebSocket connection
- `h` / `help`: Show help
- `q` / `quit`: Exit application

#### Command Line Parameters
- `--ip`: Reader IP address
- `-u` / `--username`: Login username
- `-p` / `--password`: Login password
- `--debug`: Enable debug logging
- `--table`: Batch mode with tag table
- `--rssi`: Batch mode with RSSI plot

#### ATR7000 Submenu Commands
- `r` / `realtime`: Real-time position chart
- `x` / `xy`: X/Y variations over time
- `h` / `heatmap`: Position heatmap
- `c` / `config`: Height configuration
- `cl` / `clear`: Clear localization data
- `s` / `stat`: Localization statistics
- `b` / `back`: Return to main menu

### Installation and Setup

#### System Requirements
- Python 3.9 or higher
- Network access to Zebra RFID reader
- Git for repository cloning

#### Supported Readers
- **Zebra FX9600**: Fixed and portable RFID readers
- **Zebra FXR90**: Rugged fixed RFID readers
- **Zebra ATR7000**: Advanced directionality-enabled readers

#### Quick Installation
```bash
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python xrcli_entrypoint.py --ip <READER-IP> -u admin -p change
```

### Dependencies

#### Core Dependencies
- **websocket-client**: WebSocket connectivity for real-time events
- **plotext**: Terminal-based plotting and visualization
- **matplotlib**: Advanced GUI plotting and charting
- **tkinter**: Built-in GUI toolkit for tag tables
- **httpx**: Modern HTTP client for REST API communication
- **requests**: HTTP library for reader communication

#### Development Dependencies
- **Type annotations**: Full typing support
- **Cross-platform**: Windows, Linux, macOS compatibility

### Known Issues and Limitations

#### Version 1.0.0 Limitations
- **Configuration**: Currently limited to single reader configuration
- **Networking**: WebSocket requires specific network configurations
- **Platform**: Some GUI features may behave differently across platforms
- **Memory**: Long-running sessions may accumulate tag data

#### Workarounds
- **Multiple Readers**: Manual configuration switching required
- **Network Issues**: Manual WebSocket reset available (`rs` command)
- **Memory Management**: Restart CLI for long sessions

### Migration Notes

This is the initial release, so no migration is required.

Future versions will include migration guides for configuration and data formats.

---

## 📊 Release Statistics

### Version 1.0.0 Metrics
- **Total Files**: 50+ Python and documentation files
- **Lines of Code**: 5,000+ lines of Python code
- **Documentation**: 20+ documentation files
- **Features**: 15+ major features implemented
- **Commands**: 20+ CLI commands available
- **Reader Support**: 3 reader families supported

### Development Timeline
- **Project Start**: Early 2025
- **Core Development**: 6+ months
- **Testing Phase**: Extensive hardware testing
- **Documentation**: Comprehensive user and developer guides
- **Open Source Release**: August 26, 2025

---

## 🏢 Credits and Attribution

**Developed by**: [Xerum Srl](https://xerum.it)  
**Copyright**: © 2025 Xerum Srl  
**License**: MIT License  
**Repository**: [XerumSrl/XRFID.CLI](https://github.com/XerumSrl/XRFID.CLI)

### Special Thanks
- Zebra Technologies for excellent RFID hardware and APIs
- Open source community for foundational libraries
- Beta testers for feedback and validation

---

## 🔗 Links and Resources

- **GitHub Repository**: [XerumSrl/XRFID.CLI](https://github.com/XerumSrl/XRFID.CLI)
- **Documentation**: [Complete User and Developer Guides](docs/)
- **Issues**: [Bug Reports and Feature Requests](https://github.com/XerumSrl/XRFID.CLI/issues)
- **Discussions**: [Community Discussion Forum](https://github.com/XerumSrl/XRFID.CLI/discussions)
- **Xerum Srl**: [Company Website](https://xerum.it)

---

*This changelog is maintained following the [Keep a Changelog](https://keepachangelog.com/) format.*
