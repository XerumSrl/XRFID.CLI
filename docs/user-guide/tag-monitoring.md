# 📋 Tag Monitoring Guide

Complete guide to real-time tag monitoring, visualization, and data export features.

## Overview of Monitoring Options

The CLI provides multiple ways to monitor RFID tags in real-time:

| Method | Command | Best For | Features |
|--------|---------|----------|----------|
| **Tag Table** | `m` | Complete overview | Statistics, export, GUI |
| **WebSocket Console** | `w` | Quick verification | Real-time console output |
| **RSSI Plotting** | `p` | Signal analysis | Terminal/GUI graphs |

## Tag Table Monitoring

### Opening the Tag Table
```bash
# In CLI main menu (after starting scan)
m
# or
monitoring
```

**Opens a dedicated tkinter window with live tag data.**

### Tag Table Features

#### Real-Time Updates
- **Update frequency**: Every 1 second
- **Live data**: Tag count, RSSI, timestamps
- **Status indicators**: Color-coded tag activity

#### Displayed Information

| Column | Description | Example |
|--------|-------------|---------|
| **EPC** | Tag Electronic Product Code | E20000123456789012345678 |
| **Read Count** | Total number of reads | 156 |
| **RSSI Min** | Minimum signal strength | -65 dBm |
| **RSSI Max** | Maximum signal strength | -42 dBm |
| **RSSI Avg** | Average signal strength | -48.5 dBm |
| **First Seen** | First detection timestamp | 2025-08-26 10:30:15 |
| **Last Seen** | Most recent detection | 2025-08-26 10:35:42 |
| **Status** | Tag activity status | Active/Inactive |

#### Visual Status Indicators
- 🟢 **Green**: Active tags (recently seen)
- 🟡 **Yellow**: Recently active tags
- 🔴 **Red**: Inactive tags (not seen recently)

### Tag Table Operations

#### Export Data
```bash
# Click "Export CSV" button in tag table window
# Saves complete tag statistics to timestamped CSV file
# Format: tag_data_YYYYMMDD_HHMMSS.csv
```

**CSV Export Contents:**
```csv
EPC,ReadCount,RSSI_Min,RSSI_Max,RSSI_Avg,FirstSeen,LastSeen,Status
E20000123456789012345678,156,-65,-42,-48.5,2025-08-26 10:30:15,2025-08-26 10:35:42,Active
E20000987654321098765432,89,-58,-45,-51.2,2025-08-26 10:31:20,2025-08-26 10:35:40,Active
```

#### Refresh and Clear
- **Auto-refresh**: Automatic every second
- **Manual refresh**: Click refresh button
- **Clear data**: Restart CLI or clear via menu

#### Window Management
- **Resizable window**: Adjust to fit your screen
- **Scrollable table**: Handles hundreds of tags
- **Always on top**: Option to keep window visible

## WebSocket Console Monitoring

### Starting WebSocket Listener
```bash
# In CLI main menu (after starting scan)
w
# or
websocket
```

### Console Output Format
```
🎧 WebSocket Listener Active - Press Ctrl+C to stop
🏷️ Tag: E20000123456789012345678 | RSSI: -45 dBm | Antenna: 1 | Time: 10:30:15
🏷️ Tag: E20000987654321098765432 | RSSI: -52 dBm | Antenna: 2 | Time: 10:30:16
🏷️ Tag: E20000555666777888999000 | RSSI: -48 dBm | Antenna: 1 | Time: 10:30:17
```

### WebSocket Features
- **Real-time streaming**: No delays or buffering
- **Minimal overhead**: Lightweight console output
- **Raw data display**: Unprocessed tag events
- **Continuous operation**: Runs until manually stopped

### Stopping WebSocket Listener
```bash
# Press Ctrl+C in the console
# Returns to main CLI menu
```

## RSSI Signal Plotting

### Terminal-Based Plotting
```bash
# In CLI main menu (after starting scan)
p
# or
plot
```

**Features:**
- **ASCII graphs** directly in terminal
- **Multiple tags** on same plot
- **Real-time updates** every 2 seconds
- **Signal strength over time**

**Example Terminal Plot:**
```
                    RSSI Signal Strength
    -40 ┤                                    ╭─╮
    -42 ┤                              ╭─╮   │ │    ╭─╮
    -44 ┤                        ╭─╮   │ │   │ │    │ │
    -46 ┤                  ╭─╮   │ │   │ │   │ │    │ │
    -48 ┤            ╭─╮   │ │   │ │   │ │   │ │    │ │
    -50 ┤      ╭─╮   │ │   │ │   │ │   │ │   │ │    │ │
    -52 ┤╭─╮   │ │   │ │   │ │   │ │   │ │   │ │    │ │
    -54 ┼│ │   │ │   │ │   │ │   │ │   │ │   │ │    │ │
        └┬─┬───┬─┬───┬─┬───┬─┬───┬─┬───┬─┬───┬─┬────┬─┬
         1   2   3   4   5   6   7   8   9  10  11   12
                            Time (seconds)
```

### GUI-Based Plotting
```bash
# Advanced plotting in separate matplotlib window
# Available through menu option 9 or advanced plotting command
```

**GUI Plot Features:**
- **High-resolution graphs** with zoom and pan
- **Multiple tag tracking** with different colors
- **Interactive legends** with tag selection
- **Export capabilities** (PNG, PDF, SVG)
- **Customizable time ranges** and RSSI scales

## Advanced Monitoring Features

### Tag Filtering
```bash
# Filter tags by EPC pattern (in development)
# Filter tags by RSSI threshold
# Filter tags by antenna
```

### Statistical Analysis
The tag table provides automatic statistical analysis:

#### RSSI Statistics
- **Minimum RSSI**: Weakest signal detected
- **Maximum RSSI**: Strongest signal detected  
- **Average RSSI**: Mean signal strength over time
- **Standard deviation**: Signal consistency measure

#### Temporal Statistics
- **Read frequency**: Reads per second/minute
- **Presence duration**: Time tag remained in field
- **Gap analysis**: Periods when tag wasn't detected

#### Antenna Distribution
- **Antenna usage**: Which antennas detect each tag
- **Signal comparison**: RSSI differences between antennas
- **Coverage analysis**: Tag detection patterns

### Data Export Options

#### CSV Export
```csv
# Complete tag data with all statistics
EPC,ReadCount,RSSI_Min,RSSI_Max,RSSI_Avg,RSSI_StdDev,FirstSeen,LastSeen,Duration,Antennas
```

#### JSON Export (Advanced)
```json
{
  "export_timestamp": "2025-08-26T10:35:00Z",
  "session_duration": 300,
  "total_tags": 25,
  "tags": [
    {
      "epc": "E20000123456789012345678",
      "statistics": {
        "read_count": 156,
        "rssi": {"min": -65, "max": -42, "avg": -48.5, "stddev": 5.2},
        "timing": {
          "first_seen": "2025-08-26T10:30:15Z",
          "last_seen": "2025-08-26T10:35:42Z",
          "duration": 327
        },
        "antennas": [1, 2],
        "status": "active"
      }
    }
  ]
}
```

## Performance Optimization

### Memory Management
- **Tag history**: Limited to last 50 RSSI values per tag
- **Total tags**: No hard limit, but performance degrades with >1000 tags
- **Data rotation**: Old data automatically cleared

### Update Frequency Tuning
```yaml
# In config.yaml
monitoring:
  update_interval: 1.0      # Seconds between table updates
  max_rssi_history: 50      # RSSI values kept per tag
  gui_refresh_rate: 2.0     # GUI plot update rate
```

### Network Optimization
- **WebSocket buffering**: Handles burst tag reads
- **Efficient updates**: Only changed data transmitted
- **Connection resilience**: Automatic reconnection on network issues

## Monitoring Workflows

### Daily Inventory Check
```bash
1. s     # Start scanning
2. m     # Open tag table
3. # Let scan run for required time
4. # Export CSV when complete
5. x     # Stop scanning
```

### Signal Quality Analysis
```bash
1. s     # Start scanning
2. p     # Start RSSI plotting
3. # Move tags or adjust antennas
4. # Observe signal changes
5. x     # Stop scanning
```

### Real-Time Event Monitoring
```bash
1. s     # Start scanning
2. w     # Start WebSocket console
3. # Watch for specific tag events
4. # Note timestamps and patterns
5. Ctrl+C  # Stop WebSocket
6. x     # Stop scanning
```

### Batch Processing Monitoring
```bash
1. s     # Start scanning
2. m     # Open tag table for overview
3. w     # Also start console for real-time
4. # Process batches of items
5. # Export data between batches
6. x     # Stop scanning when done
```

## Troubleshooting Monitoring

### No Tags Appearing
```
❌ Tag table empty or no WebSocket events
```
**Solutions:**
1. Verify scanning is active: `s`
2. Check IOTC setup: `i`
3. Verify antenna connections and power
4. Check tag placement in read range

### Monitoring Window Not Opening
```
❌ Tag table window fails to open
```
**Solutions:**
1. Check tkinter installation: `python -c "import tkinter"`
2. Verify GUI support (for remote/SSH sessions)
3. Check display settings and permissions

### Performance Issues
```
❌ Slow updates or high CPU usage
```
**Solutions:**
1. Reduce update frequency in config.yaml
2. Clear tag data: restart CLI
3. Reduce RSSI history length
4. Close unused monitoring windows

### Export Failures
```
❌ CSV export fails or file not created
```
**Solutions:**
1. Check file permissions in current directory
2. Ensure sufficient disk space
3. Close any open CSV files with same name
4. Check antivirus/security software

## Integration with External Systems

### Database Integration
```python
# Example: Import CSV data into database
import pandas as pd
df = pd.read_csv('tag_data_20250826_103500.csv')
# Process and insert into database
```

### Real-Time Dashboards
```javascript
// Example: WebSocket integration with web dashboard
const ws = new WebSocket('ws://reader-ip:8080');
ws.onmessage = function(event) {
  const tagData = JSON.parse(event.data);
  updateDashboard(tagData);
};
```

### API Integration
```bash
# Use API submenu to create custom monitoring endpoints
r  # Enter API submenu
# Configure custom data endpoints
```

---

**Related Guides:**
- [Basic Operations](basic-operations.md) - Essential CLI commands
- [IOTC Setup](iotc-setup.md) - Configure real-time data streaming
- [API Integration](../advanced/api-integration.md) - Advanced monitoring automation

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
