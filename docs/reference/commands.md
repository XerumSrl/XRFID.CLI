# 📋 Command Reference

Complete reference of all available commands in Zebra RFID CLI.

## Main Menu Commands

### Connection Management

| Command | Shortcut | Description | Usage |
|---------|----------|-------------|-------|
| `login` | `l` | Login and automatic connection | Interactive prompt for credentials |
| `disconnect` | `d` | Disconnect from reader | Closes current session |

**Examples:**
```bash
# Interactive login
l

# Disconnect current session  
d
```

### Reader Operations

| Command | Shortcut | Description | Usage |
|---------|----------|-------------|-------|
| `start` | `s` | Start RFID scan | Begins reading tags |
| `stop` | `x` | Stop RFID scan | Stops reading tags |
| `restApi` | `r` | Open REST API submenu | Access advanced API features |

**Examples:**
```bash
# Start scanning for tags
s

# Stop scanning
x

# Open API submenu
r
```

### Monitoring and Visualization

| Command | Shortcut | Description | Usage |
|---------|----------|-------------|-------|
| `websocket` | `w` | Simple WebSocket connection | Basic real-time tag listener |
| `monitoring` | `m` | Tag table window | Full tag statistics in GUI |
| `plot` | `p` | RSSI graph (terminal) | Signal strength visualization |
| `atr` | `a` | ATR7000 localization submenu | Position tracking features |

**Examples:**
```bash
# Open tag monitoring table
m

# Show RSSI plot in terminal
p

# Enter ATR7000 submenu
a
```

### IoT Connector (IOTC)

| Command | Shortcut | Description | Parameters |
|---------|----------|-------------|------------|
| `iotc` | `i` | Setup IoT Connector | `-type ws|mqtt` `-hostname` `-readername` `-endpointname` |
| `disconnectIOTC` | `di` | Disconnect from IOTC | None |

**Examples:**
```bash
# WebSocket setup (default)
i
i -type ws

# MQTT setup
i -type mqtt -hostname 192.168.1.200 -readername FXR9001234 -endpointname mqtt-prod

# Disconnect IOTC
di
```

### Utility Commands

| Command | Shortcut | Description | Usage |
|---------|----------|-------------|-------|
| `clear` | `c` | Clear screen | Clears terminal output |
| `reset` | `rs` | Force WebSocket reset | Resets WebSocket connection |
| `help` | `h` | Command help | Shows available commands |
| `quit` | `q` | Exit application | Closes CLI |

**Examples:**
```bash
# Clear screen
c

# Reset WebSocket connection
rs

# Show help
h

# Exit application
q
```

## CLI Startup Parameters

### Required Parameters

| Parameter | Short | Description | Example |
|-----------|-------|-------------|---------|
| `--ip` | `-i` | Reader IP address | `--ip 192.168.1.100` |
| `--username` | `-u` | Username | `--username admin` |
| `--password` | `-p` | Password | `--password admin` |

### Optional Parameters

| Parameter | Short | Description | Default | Example |
|-----------|-------|-------------|---------|---------|
| `--ip` | - | Reader IP address | - | `--ip 192.168.1.100` |
| `-u` | `--username` | Login username | - | `-u admin` |
| `-p` | `--password` | Login password | - | `-p change` |
| `--debug` | - | Enable debug logging | `False` | `--debug` |
| `--table` | - | Batch mode: start scan + tag table | `False` | `--table` |
| `--rssi` | - | Batch mode: start scan + RSSI plot | `False` | `--rssi` |
| `--help` | `-h` | Show help message | - | `--help` |

**Complete Startup Examples:**
```bash
# Basic connection
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change

# With debug logging
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change --debug

# Batch mode: automatic login + scan + tag table
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change --table

# Batch mode: automatic login + scan + RSSI plot
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change --rssi

# Show help
python xrcli_entrypoint.py --help
```

### Batch Mode

The `--table` and `--rssi` parameters enable batch mode for automated workflows:

1. **Automatic Login**: Connects using provided credentials
2. **Start Scanning**: Automatically begins RFID scanning
3. **Open Visualization**: Launches requested monitoring window
4. **Interactive Menu**: Shows CLI menu after window closes

**Batch Mode Requirements:**
- All connection parameters must be provided (`--ip`, `-u`, `-p`)
- WebSocket connectivity must be working
- Reader must be properly configured

## ATR7000 Submenu Commands

Available when connected to ATR7000 reader via `a` command:

| Command | Shortcut | Description | Usage |
|---------|----------|-------------|-------|
| `realtime` | `r` | Real-time position chart | Opens matplotlib window |
| `xy` | `x` | X/Y variations over time | Per-tag position tracking |
| `heatmap` | `h` | Position heatmap | 13x13 grid visualization |
| `config` | `c` | Height configuration | Set reader/tag heights |
| `clear` | `cl` | Clear localization data | Reset all position data |
| `stat` | `s` | Localization statistics | Show tracking metrics |
| `back` | `b` | Return to main menu | Exit ATR submenu |

**Examples:**
```bash
# In ATR submenu:
r  # Real-time position chart
h  # Position heatmap
c  # Configure heights
s  # Show statistics
```

## REST API Submenu Commands

Available via `r` command from main menu. See [API-SUBMENU-README.md](../../API-SUBMENU-README.md) for complete details.

### Common API Operations

| Category | Description | Examples |
|----------|-------------|----------|
| Reader Info | Get reader details | Model, firmware, status |
| Antenna Control | Manage antennas | Enable/disable, power settings |
| Tag Operations | Tag filtering and control | Start/stop, filters |
| Configuration | Reader settings | Network, protocols, features |

## Interactive Menu Navigation

### Menu Structure
```
Main Menu
├── Connection (l, d)
├── Reader Operations (s, x, r)
├── Monitoring (w, m, p, a)
├── IOTC (i, di)
└── Utilities (c, rs, h, q)

ATR Submenu (from 'a')
├── Visualization (r, x, h)
├── Configuration (c)
├── Data Management (cl, s)
└── Navigation (b)

API Submenu (from 'r')
├── Reader Management
├── Antenna Control  
├── Tag Operations
└── Advanced Features
```

### Input Methods

- **Command Name**: Type full command name (e.g., `monitoring`)
- **Shortcut**: Type single letter (e.g., `m`)
- **Case Insensitive**: Both `M` and `m` work
- **Tab Completion**: Available for command names

### Session Management

- **Persistent Connection**: Connection maintained between commands
- **Auto-reconnect**: Automatic reconnection on network issues
- **State Preservation**: Settings saved across sessions
- **Graceful Exit**: `Ctrl+C` or `q` command

## Command Timing and Behavior

### Synchronous Commands
- Connection operations (`l`, `d`)
- Reader control (`s`, `x`)
- Configuration commands

### Asynchronous Commands  
- WebSocket listener (`w`)
- Tag monitoring (`m`)
- Plotting (`p`)
- Real-time visualization

### Background Operations
- Tag data collection
- WebSocket maintenance
- Configuration persistence

## Error Handling

### Common Error Responses

| Error Type | Description | Solution |
|------------|-------------|----------|
| Connection Error | Reader not reachable | Check IP, network, credentials |
| Authentication Error | Invalid credentials | Verify username/password |
| Command Error | Invalid command | Use `h` for help |
| State Error | Invalid operation for current state | Connect first, then try command |

### Debug Mode

Enable with `--debug` for detailed logging:
```bash
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change --debug
```

**Debug Output Includes:**
- HTTP request/response details
- WebSocket message logging
- Configuration file operations
- Error stack traces

---

**Need more help?** Check the [troubleshooting guide](../advanced/troubleshooting.md) or [user guides](../user-guide/).

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
