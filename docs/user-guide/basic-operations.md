# 🎯 Basic Operations Guide

Essential commands and workflows for daily use of Zebra RFID CLI.

## Getting Connected

### Initial Connection
```bash
# Start the CLI with your reader details
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change

# The interactive menu will appear
📋 XRFID CLI - Main Menu:
┌─────────────────────────────────────────────────────────────┐
│ CONNECTION:                                                 │
│ l / login      🔐 Login and automatic connection            │
│ d / disconnect 🔌 Disconnect                                │
└─────────────────────────────────────────────────────────────┘
```

### Alternative Login Methods
```bash
# Interactive login (prompts for credentials)
l

# Login with stored credentials (from config.yaml)
l
```

### Connection Status
- ✅ **Connected**: Green indicators and full menu available
- ❌ **Disconnected**: Limited menu options, connection commands only
- ⚠️ **Connection Issues**: Yellow warnings with suggested fixes

## Core Tag Reading Operations

### Start/Stop Scanning

#### Start Scanning
```bash
# Basic scan start
s
# or
start

# Verify scanning started
✅ Scan started successfully
```

#### Stop Scanning
```bash
# Stop current scan
x
# or  
stop

# Verify scanning stopped
✅ Scan stopped successfully
```

### Reading Workflow
1. **Connect** to reader (`l`)
2. **Start scanning** (`s`)
3. **Monitor tags** (see monitoring section)
4. **Stop scanning** (`x`) when done
5. **Disconnect** (`d`) to close session

## Tag Monitoring

### Real-Time Tag Table
```bash
# Open tag monitoring window
m
# or
monitoring
```

**Tag Table Features:**
- **Live updates** every second
- **Tag statistics**: EPC, read count, RSSI min/max/avg
- **Timestamps**: First seen, last seen
- **Status indicators**: Active (green), inactive (gray)
- **Export functionality**: Save data to CSV

### WebSocket Listener
```bash
# Simple WebSocket connection
w
# or
websocket

# Shows real-time tag events in console
🏷️ Tag: E20000123456789012345678 | RSSI: -45 dBm | Antenna: 1
🏷️ Tag: E20000987654321098765432 | RSSI: -52 dBm | Antenna: 2
```

### RSSI Signal Visualization
```bash
# Terminal-based RSSI plot
p
# or
plot

# Shows signal strength over time in terminal
```

## IoT Connector (IOTC) Setup

### WebSocket Setup for CLI
```bash
# Basic WebSocket setup
i
# or
iotc

# Explicit WebSocket setup
i -type ws
```

**What This Does:**
- ✅ Enrolls reader with IOTC service
- ✅ Configures WebSocket endpoint on data interface
- ✅ Maps WebSocket to tag events
- ✅ Starts IOTC service

### MQTT Setup for External Systems
```bash
# MQTT broker integration
i -type mqtt -hostname 192.168.1.200 -readername FXR9001234 -endpointname mqtt-prod
```

**MQTT Topics Created:**
- `tevents/FXR9001234` - Tag events
- `ccmds/FXR9001234` - Control commands
- `crsp/FXR9001234` - Control responses
- `mcmds/FXR9001234` - Management commands
- `mrsp/FXR9001234` - Management responses
- `mevents/FXR9001234` - Management events

### Disconnect from IOTC
```bash
# Disconnect IOTC service
di
# or
disconnectIOTC
```

## Advanced Reader Operations

### REST API Submenu
```bash
# Access advanced API features
r
# or
restApi

# Opens API submenu with advanced operations
# See API-SUBMENU-README.md for details
```

### ATR7000 Localization
```bash
# Enter ATR7000 submenu (only for ATR7000 readers)
a
# or
atr

# ATR submenu options:
# r - Real-time position chart
# h - Position heatmap
# c - Configure reader/tag heights
# s - Localization statistics
```

## Session Management

### Session State
The CLI maintains state between commands:
- **Connection details** are preserved
- **WebSocket status** is maintained
- **Configuration** is auto-saved

### Graceful Exit
```bash
# Proper exit
q
# or
quit

# Emergency exit
Ctrl+C
```

### Session Recovery
If connection is lost:
```bash
# Automatic reconnection attempt
# CLI will show reconnection status

# Manual reconnection
d  # Disconnect first
l  # Then reconnect
```

## Common Workflows

### Daily Tag Monitoring
```bash
1. python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
2. l      # Login
3. i      # Setup IOTC if needed
4. s      # Start scanning
5. m      # Open tag monitoring table
6. # Let it run...
7. x      # Stop scanning when done
8. q      # Exit
```

### Quick Tag Check
```bash
1. python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
2. l      # Login
3. s      # Start scanning
4. w      # Watch WebSocket console
5. x      # Stop after checking tags
6. q      # Exit
```

### IOTC Setup and Testing
```bash
1. python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
2. l      # Login
3. i      # Setup IOTC WebSocket
4. s      # Start scanning
5. m      # Verify tags appear in table
6. x      # Stop scanning
7. q      # Exit
```

### Position Tracking (ATR7000)
```bash
1. python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
2. l      # Login
3. a      # Enter ATR submenu
4. c      # Configure heights
5. r      # Start real-time position chart
6. # Move tags around...
7. h      # View position heatmap
8. b      # Back to main menu
9. q      # Exit
```

## Error Handling

### Common Issues and Solutions

#### Connection Refused
```bash
❌ Connection refused
🔧 Solution: Check reader IP and network connectivity
ping 192.168.1.100
```

#### Authentication Failed
```bash
❌ Authentication failed
🔧 Solution: Verify credentials (default: admin/change)
```

#### WebSocket Connection Failed
```bash
❌ WebSocket connection failed
🔧 Solution: Run IOTC setup
i  # Run IOTC setup command
```

#### No Tags Detected
```bash
❌ No tags detected during scan
🔧 Solutions:
1. Check antenna connections
2. Verify tag placement in read range
3. Check antenna power settings via API submenu (r)
```

### Debug Mode
Enable detailed logging for troubleshooting:
```bash
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change --debug
```

## Tips for Efficient Operation

### Performance Tips
- **Use tag monitoring table** (`m`) for best overview
- **WebSocket console** (`w`) for quick tag verification
- **Terminal plots** (`p`) for signal analysis
- **Close unused windows** to free resources

### Workflow Tips
- **Save frequently used IPs** in config.yaml
- **Use IOTC setup once** per reader, then just connect
- **Monitor connection status** indicators
- **Use debug mode** for troubleshooting

### Multi-Reader Management
- **One CLI instance per reader** recommended
- **Use different terminal windows** for multiple readers
- **Save reader profiles** in separate config files

## Keyboard Shortcuts

### In Main Menu
- **Letters**: Command shortcuts (s, x, m, p, etc.)
- **Tab**: Command completion (if available)
- **Ctrl+C**: Interrupt current operation
- **Ctrl+D**: Alternative exit

### In Monitoring Windows
- **Ctrl+C**: Close monitoring window
- **Esc**: Close monitoring window (GUI)
- **Alt+F4**: Close window (Windows)

---

**Ready for advanced features?** Check out:
- [IoT Connector Setup](iotc-setup.md) - Advanced connectivity
- [Tag Monitoring](tag-monitoring.md) - Detailed monitoring features  
- [API Integration](../advanced/api-integration.md) - REST API automation

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
