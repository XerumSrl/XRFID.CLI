# 📍 ATR7000 Localization Guide

Complete guide to position tracking and localization features with Zebra ATR7000 readers.

## Overview

The ATR7000 reader provides advanced directionality capabilities for precise tag positioning. The CLI includes specialized tools for:
- **Real-time position tracking** with 3D coordinate calculation
- **Position visualization** with multiple chart types
- **Heatmap analysis** for zone detection patterns
- **Statistical analysis** of tag movement and positioning

## Core Technology

### RAW_DIRECTIONALITY Processing
- **Azimuth and elevation angles** from reader's direction-finding antennas
- **Cartesian coordinate conversion** using reader and tag heights
- **3D positioning** with X, Y, Z coordinates
- **Temporal aggregation** for position smoothing

### Position Calculation
```
X = distance * cos(elevation) * sin(azimuth)
Y = distance * cos(elevation) * cos(azimuth)  
Z = reader_height - tag_height - distance * sin(elevation)
```

Where:
- **Distance**: Calculated from RSSI and angle data
- **Reader Height**: Configurable mounting height (default: 3.0m)
- **Tag Height**: Configurable tag height above ground (default: 0.0m)

## Accessing ATR Submenu

### Prerequisites
- **ATR7000 reader** connected and operational
- **IOTC setup** completed for real-time data streaming
- **RAW_DIRECTIONALITY** messages enabled on reader

### Enter ATR Submenu
```bash
# From main CLI menu
a
# or
atr

# ATR7000 Submenu appears:
📍 ATR7000 - Localization Menu:
┌─────────────────────────────────────────────────────────────┐
│ VISUALIZATION:                                              │
│ r / realtime   📊 Real-time position chart (matplotlib)     │
│ x / xy         📈 X/Y variations over time (per tag)        │
│ h / heatmap    🌡️ Heatmap of detected zones (13x13 grid)   │
├─────────────────────────────────────────────────────────────┤
│ CONFIGURATION:                                              │
│ c / config     🔧 Height configuration (reader/tag)         │
├─────────────────────────────────────────────────────────────┤
│ DATA MANAGEMENT:                                            │
│ cl / clear     🧹 Clear all localization data              │
│ s / stat       📊 Localization statistics                   │
├─────────────────────────────────────────────────────────────┤
│ NAVIGATION:                                                 │
│ b / back       ◀️ Return to main menu                       │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### Height Configuration
```bash
# In ATR submenu
c
# or
config
```

**Configuration Options:**
- **Reader Height**: Physical mounting height above ground (meters)
- **Tag Height**: Expected tag height above ground (meters)

**Example Configuration:**
```
📍 Height Configuration:
Current Settings:
- Reader Height: 3.0m (mounted on ceiling)
- Tag Height: 0.0m (ground level)

Enter new reader height (current: 3.0): 2.5
Enter new tag height (current: 0.0): 1.0

✅ Configuration updated:
- Reader Height: 2.5m
- Tag Height: 1.0m
```

### Grid Resolution
- **Default**: 13x13 grid (169 zones)
- **Grid size**: 1 meter per cell
- **Coverage area**: 13m x 13m centered on reader
- **Configurable**: Via configuration files

## Visualization Modes

### Real-Time Position Chart
```bash
# In ATR submenu
r
# or
realtime
```

**Features:**
- **Live matplotlib window** with real-time updates
- **Multi-tag tracking** with color-coded positions
- **3D scatter plot** showing X, Y, Z coordinates
- **Interactive zoom and pan** capabilities
- **Tag legends** with EPC identification

**Chart Elements:**
- **Reader position**: Center point (0, 0, reader_height)
- **Tag positions**: Colored dots for each detected tag
- **Movement trails**: Optional path visualization
- **Grid overlay**: Reference grid for distance estimation

### X/Y Variations Over Time
```bash
# In ATR submenu
x
# or
xy
```

**Features:**
- **Time-series plotting** of position changes
- **Per-tag analysis** with separate lines for each tag
- **High-precision timestamps** (millisecond accuracy)
- **Position stability analysis** over time
- **Movement pattern detection**

**Plot Types:**
- **X-coordinate vs Time**: Horizontal movement patterns
- **Y-coordinate vs Time**: Depth movement patterns
- **Distance from reader**: Radial movement analysis

### Position Heatmap
```bash
# In ATR submenu
h
# or
heatmap
```

**Features:**
- **13x13 grid visualization** showing detection density
- **Color-coded zones**: Hot (red) to cold (blue) detection areas
- **Detection count overlay**: Numbers showing total detections per zone
- **Zone analysis**: Identification of high-traffic areas

**Heatmap Interpretation:**
- 🔴 **Red zones**: High tag detection frequency
- 🟡 **Yellow zones**: Moderate detection frequency  
- 🔵 **Blue zones**: Low detection frequency
- ⚫ **Black zones**: No detections recorded

## Data Management

### Localization Statistics
```bash
# In ATR submenu
s
# or
stat
```

**Statistics Provided:**
```
📊 ATR7000 Localization Statistics:

Global Statistics:
- Total tags tracked: 15
- Total position points: 1,247
- Session duration: 00:15:32
- Average points per tag: 83.1

Per-Tag Statistics:
┌──────────────────────────────────┬─────────┬──────────┬─────────────┬─────────────┐
│ EPC                              │ Points  │ Duration │ Avg X (m)   │ Avg Y (m)   │
├──────────────────────────────────┼─────────┼──────────┼─────────────┼─────────────┤
│ E20000123456789012345678         │ 156     │ 00:08:45 │ 2.3         │ -1.7        │
│ E20000987654321098765432         │ 89      │ 00:05:20 │ -0.8        │ 3.2         │
└──────────────────────────────────┴─────────┴──────────┴─────────────┴─────────────┘

Position Distribution:
- Grid coverage: 87% (146/169 zones with detections)
- Most active zone: (6,8) with 234 detections
- Average position accuracy: ±0.5m
```

### Clear Localization Data
```bash
# In ATR submenu
cl
# or
clear

# Confirmation prompt
⚠️ Clear all localization data? This cannot be undone. (y/N): y
✅ All localization data cleared
```

## Advanced Features

### Position Smoothing
**Automatic smoothing algorithms:**
- **Temporal averaging**: Multiple readings averaged over time windows
- **Outlier detection**: Removes impossible position jumps
- **Kalman filtering**: Predictive smoothing for moving tags

### Significant Point Detection
**Intelligent data collection:**
- **Movement threshold**: Only stores positions with significant change
- **Time-based sampling**: Regular position updates regardless of movement
- **Memory management**: FIFO buffer for position history

### Data Storage Limits
- **Per-tag limit**: 100 significant position points
- **Total limit**: 1,000 position points across all tags
- **Automatic cleanup**: Oldest data removed when limits reached

## Workflows and Use Cases

### Asset Tracking Workflow
```bash
1. a          # Enter ATR submenu
2. c          # Configure heights for your environment
3. s          # Start scanning (from main menu)
4. r          # Start real-time position chart
5. # Move assets around, observe positions
6. h          # Generate heatmap for pattern analysis
7. s          # View statistics
8. b          # Return to main menu
```

### Zone Analysis Workflow
```bash
1. a          # Enter ATR submenu
2. c          # Configure for zone heights
3. s          # Start scanning
4. # Let system collect data over time
5. h          # View heatmap for zone identification
6. s          # Analyze statistics for zone usage
7. # Export data for further analysis
```

### Movement Pattern Analysis
```bash
1. a          # Enter ATR submenu
2. r          # Start real-time tracking
3. x          # Also open X/Y time analysis
4. # Track specific tag movements
5. s          # Review statistical patterns
6. # Document movement behaviors
```

### Calibration and Testing
```bash
1. a          # Enter ATR submenu  
2. c          # Set precise heights
3. # Place tags at known positions
4. r          # Verify position accuracy
5. # Adjust configuration as needed
6. s          # Document accuracy statistics
```

## Troubleshooting

### No Position Data
```
❌ No position data appearing in charts
```
**Solutions:**
1. **Check ATR7000 configuration**: Ensure RAW_DIRECTIONALITY is enabled
2. **Verify IOTC setup**: Position data requires real-time streaming
3. **Check antenna configuration**: Direction-finding antennas must be active
4. **Verify tag placement**: Tags must be in direction-finding range

### Inaccurate Positions
```
❌ Positions appear incorrect or erratic
```
**Solutions:**
1. **Calibrate heights**: Ensure accurate reader and tag height configuration
2. **Check reader mounting**: Reader must be level and properly positioned
3. **Verify environment**: Metal objects can interfere with positioning
4. **Check antenna calibration**: May require professional antenna alignment

### Performance Issues
```
❌ Charts update slowly or freeze
```
**Solutions:**
1. **Reduce update frequency**: Adjust plotting rates in configuration
2. **Clear old data**: Use clear command to free memory
3. **Close unused charts**: Multiple charts consume resources
4. **Check system resources**: Ensure adequate CPU and memory

### Charts Not Opening
```
❌ Matplotlib windows fail to open
```
**Solutions:**
1. **Check matplotlib installation**: `pip install matplotlib`
2. **Verify GUI support**: Required for remote/SSH sessions
3. **Check display settings**: X11 forwarding for Linux/SSH
4. **Update graphics drivers**: May be required for 3D plotting

## Integration and Export

### Data Export
```python
# Position data can be exported via tag monitoring
# Export includes X, Y, Z coordinates when available
# CSV format with position columns added
```

### API Integration
```bash
# Use REST API submenu for programmatic access
r  # Enter API submenu
# Access raw directionality data
# Configure custom position processing
```

### External Visualization
```python
# Example: Export position data for external analysis
import pandas as pd
import matplotlib.pyplot as plt

# Load exported position data
df = pd.read_csv('tag_positions.csv')

# Create custom visualizations
plt.scatter(df['X'], df['Y'], c=df['RSSI'])
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.colorbar(label='RSSI (dBm)')
plt.show()
```

## Best Practices

### Installation Considerations
- **Reader height**: 2.5-4.0m optimal for most applications
- **Clear line of sight**: Minimize obstacles between reader and tags
- **Environmental factors**: Consider temperature, humidity, RF interference
- **Mounting stability**: Ensure reader is securely mounted and level

### Configuration Tips
- **Accurate measurements**: Precise height configuration critical for accuracy
- **Regular calibration**: Verify position accuracy with known reference points
- **Environment mapping**: Document physical layout for interpretation
- **Tag characteristics**: Consider tag type and orientation effects

### Performance Optimization
- **Selective monitoring**: Focus on specific areas or tags when possible
- **Regular data clearing**: Prevent memory buildup in long-running sessions
- **Update rate tuning**: Balance real-time updates with system performance
- **Resource monitoring**: Watch CPU and memory usage during operation

---

**Related Guides:**
- [Basic Operations](basic-operations.md) - Essential CLI commands for ATR7000
- [Tag Monitoring](tag-monitoring.md) - General tag monitoring features
- [API Integration](../advanced/api-integration.md) - Advanced ATR7000 configuration

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
