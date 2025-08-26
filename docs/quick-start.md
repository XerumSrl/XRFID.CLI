# ⚡ Quick Start Guide

Get up and running with Zebra RFID CLI in under 5 minutes!

## Prerequisites

- ✅ Python 3.9+ installed
- ✅ Git installed
- ✅ Zebra RFID reader (FX9600, FXR90, or ATR7000) on your network
- ✅ Reader credentials (usually `admin`/`admin`)

## 🚀 5-Minute Setup

### Step 1: Clone and Install (2 minutes)

**Windows (PowerShell):**
```powershell
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Connect to Your Reader (1 minute)

```bash
# Replace 192.168.1.100 with your reader's IP address
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
```

You should see the interactive CLI menu:

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
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Start Reading Tags (2 minutes)

1. **Start scanning**: Type `s` or `start`
2. **Monitor tags**: Type `m` or `monitoring` to see a real-time tag table
3. **View RSSI graph**: Type `p` or `plot` for signal strength visualization
4. **Stop scanning**: Type `x` or `stop`

## 🎯 Essential Commands

| Command | Action | Description |
|---------|--------|-------------|
| `s` | Start scan | Begin reading RFID tags |
| `x` | Stop scan | Stop reading tags |
| `m` | Tag table | Open tag monitoring window with statistics |
| `p` | RSSI plot | Open signal strength graph |
| `w` | WebSocket | Start simple WebSocket listener |
| `i` | IOTC setup | Configure IoT Connector for advanced features |
| `h` | Help | Show command help |
| `q` | Quit | Exit the application |

## 🔧 Common First-Time Setup

### Set up IoT Connector for Real-Time Data

```bash
# In the CLI menu, type:
i
# or
iotc
```

This configures WebSocket connectivity for real-time tag streaming.

### Configure for MQTT Integration

```bash
# For MQTT broker integration:
i -type mqtt -hostname 192.168.1.200 -readername FXR9001234 -endpointname mqtt-prod
```

## 📊 Quick Data Visualization

### Real-Time Tag Table
- Type `m` to open a live tag statistics window
- Shows EPC, read count, RSSI statistics, and timestamps
- Export data to CSV with the export button

### RSSI Signal Graphs
- Type `p` for terminal-based plotting
- Type `9` for GUI-based plotting with matplotlib

### ATR7000 Localization (if applicable)
- Type `a` to enter ATR submenu
- Type `r` for real-time position tracking
- Type `h` for position heatmap

## 🛠️ Troubleshooting Quick Fixes

### Can't Connect to Reader?
```bash
# Check reader is reachable
ping 192.168.1.100

# Try with debug logging
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p admin --debug
```

### WebSocket Issues?
- The CLI automatically tries multiple ports (80, 443, 8080, 8443)
- Run IOTC setup: type `i` in the CLI menu

### Wrong Credentials?
- Default is usually `admin`/`change`
- Check reader's web interface for correct credentials

## 📚 What's Next?

After your quick start:

1. **[Basic Operations Guide](user-guide/basic-operations.md)** - Learn all essential features
2. **[IoT Connector Setup](user-guide/iotc-setup.md)** - Advanced connectivity options
3. **[Tag Monitoring](user-guide/tag-monitoring.md)** - Master data visualization
4. **[API Integration](advanced/api-integration.md)** - Automate with REST API

## 💡 Pro Tips

- **Protocol Auto-Detection**: The CLI automatically detects HTTP/HTTPS
- **Session Persistence**: Connection settings are remembered between sessions
- **Multi-Window Support**: Tag table and plots open in separate windows
- **Background Processing**: WebSocket runs in background thread for smooth performance
- **Error Recovery**: Robust error handling with automatic reconnection

---

**Need Help?** Check the [troubleshooting guide](advanced/troubleshooting.md) or [open an issue](https://github.com/XerumSrl/XRFID.CLI/issues).

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
