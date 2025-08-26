# 🌐 IoT Connector (IOTC) Setup Guide

Comprehensive guide to setting up and configuring Zebra IoT Connector for real-time tag data streaming.

## What is IoT Connector (IOTC)?

IoT Connector is Zebra's cloud connectivity service that enables:
- **Real-time tag streaming** via WebSocket or MQTT
- **Multiple interface mapping** for different data types
- **Cloud integration** with external systems
- **Advanced data processing** and filtering

## Setup Types

### WebSocket Setup (Recommended for CLI)

**Purpose**: Direct real-time communication between reader and CLI.

#### Basic WebSocket Setup
```bash
# In CLI main menu
i
# or
iotc
# or explicitly
i -type ws
```

**What Happens During Setup:**
1. ✅ **Reader Enrollment Check** - Verifies reader is registered with IOTC
2. ✅ **WebSocket Endpoint Creation** - Creates endpoint on data interface
3. ✅ **Data Mapping** - Maps tag events to WebSocket stream
4. ✅ **Service Startup** - Starts IOTC service on reader
5. ✅ **Connection Test** - Verifies WebSocket connectivity

**Expected Output:**
```
🌐 IOTC Setup Starting...
✅ Reader enrollment verified
✅ WebSocket endpoint configured on data interface
✅ Data interface mapped to tag events
✅ IOTC service started successfully
🎯 WebSocket ready for real-time tag streaming
```

### MQTT Setup (For External Integration)

**Purpose**: Integration with external MQTT brokers and systems.

#### MQTT Broker Setup
```bash
# Full MQTT configuration
i -type mqtt -hostname 192.168.1.200 -readername FXR9001234 -endpointname mqtt-prod
```

**Required Parameters:**
- `-hostname`: MQTT broker IP address
- `-readername`: Unique reader identifier for topic naming
- `-endpointname`: Configuration name for this MQTT setup

**What Happens During MQTT Setup:**
1. ✅ **Reader Enrollment Check**
2. ✅ **MQTT Endpoints Creation** on all interfaces:
   - **Data Interface** → Tag events
   - **Control Interface** → Commands and responses
   - **Management Interface** → Management commands and events
3. ✅ **Topic Mapping** with reader name
4. ✅ **Service Configuration** and startup

**MQTT Topics Created:**
```
tevents/{readername}    # Tag event stream
ccmds/{readername}      # Control commands (incoming)
crsp/{readername}       # Control responses (outgoing)
mcmds/{readername}      # Management commands (incoming)
mrsp/{readername}       # Management responses (outgoing)
mevents/{readername}    # Management events (outgoing)
```

**Expected Output:**
```
🌐 IOTC MQTT Setup Starting...
✅ Reader enrollment verified  
✅ MQTT endpoints configured on all interfaces
✅ Topics mapped: tevents/FXR9001234, ccmds/FXR9001234, etc.
✅ IOTC service started successfully
🎯 MQTT ready for external system integration
```

## Reader-Specific Behavior

### FX9600 and Standard Readers
- Uses **IOTC XML configuration** commands
- Full interface mapping support
- Standard setup process

### FXR90 Readers
- Uses **direct REST API** configuration
- Automatic reader type detection
- Optimized setup process for FXR90 architecture

## Verification and Testing

### WebSocket Connection Test
After WebSocket setup:
```bash
# Start tag monitoring to test
s  # Start scanning
w  # Start WebSocket listener

# You should see real-time tag events:
🏷️ Tag: E20000123456789012345678 | RSSI: -45 dBm | Antenna: 1
🏷️ Tag: E20000987654321098765432 | RSSI: -52 dBm | Antenna: 2
```

### MQTT Connection Test
After MQTT setup, use an MQTT client:
```bash
# Subscribe to tag events (external MQTT client)
mosquitto_sub -h 192.168.1.200 -t "tevents/FXR9001234"

# Should show JSON tag events:
{"epc":"E20000123456789012345678","rssi":-45,"antenna":1,"timestamp":"2025-08-26T10:30:00Z"}
```

## Advanced Configuration

### Custom WebSocket Ports
```bash
# The CLI automatically tries these ports in order:
# 80, 443, 8080, 8443

# Successful port is saved in config.yaml for future connections
```

### MQTT Quality of Service
```bash
# Default QoS settings applied:
# - QoS 1 for tag events (at least once delivery)
# - QoS 0 for management events (best effort)
# - Retained messages: false
```

### Data Interface Batching
```bash
# Automatic batching configuration:
# - Batch size: 100 tags
# - Batch timeout: 1 second
# - Retention: 24 hours
```

## Troubleshooting IOTC Setup

### Reader Not Enrolled
```
❌ Reader enrollment failed
```
**Solutions:**
1. Check reader internet connectivity
2. Verify reader can reach Zebra cloud services
3. Ensure reader firmware supports IOTC
4. Check network firewall settings

### WebSocket Endpoint Creation Failed
```
❌ Failed to create WebSocket endpoint
```
**Solutions:**
1. Run setup again: `rs` (reset WebSocket) then `i`
2. Check reader available memory and resources
3. Verify no conflicting IOTC configurations
4. Restart reader if necessary

### MQTT Broker Connection Failed
```
❌ MQTT broker connection failed
```
**Solutions:**
1. Verify MQTT broker is running: `telnet 192.168.1.200 1883`
2. Check broker authentication requirements
3. Verify network connectivity between reader and broker
4. Check broker logs for connection attempts

### Service Startup Failed
```
❌ IOTC service failed to start
```
**Solutions:**
1. Check reader system resources
2. Verify no conflicting services
3. Restart reader and try again
4. Check reader logs for detailed errors

## IOTC Service Management

### Check IOTC Status
```bash
# In API submenu (r)
# Use management interface calls to check IOTC status
```

### Restart IOTC Service
```bash
# Disconnect and reconnect IOTC
di  # Disconnect IOTC
i   # Setup IOTC again
```

### Clean IOTC Configuration
```bash
# Complete IOTC reset
di  # Disconnect IOTC first
rs  # Reset WebSocket connection
i   # Setup fresh IOTC configuration
```

## Integration Examples

### Real-Time Dashboard Integration
```bash
# 1. Setup WebSocket for CLI monitoring
i -type ws

# 2. Setup MQTT for dashboard integration  
i -type mqtt -hostname dashboard-server.local -readername LOBBY01 -endpointname dashboard

# 3. Dashboard subscribes to: tevents/LOBBY01
```

### Multi-System Integration
```bash
# Reader with multiple MQTT endpoints
i -type mqtt -hostname warehouse-system.local -readername WH01 -endpointname warehouse
i -type mqtt -hostname analytics-server.local -readername WH01 -endpointname analytics
i -type mqtt -hostname alert-system.local -readername WH01 -endpointname alerts
```

### Development vs Production
```bash
# Development environment
i -type mqtt -hostname dev-broker.local -readername DEV01 -endpointname development

# Production environment  
i -type mqtt -hostname prod-broker.local -readername PROD01 -endpointname production
```

## Security Considerations

### Network Security
- **TLS encryption** for MQTT connections (when supported by broker)
- **WebSocket over HTTPS** when reader supports SSL
- **Network isolation** for IOTC traffic

### Access Control
- **MQTT broker authentication** configuration
- **Topic-based access control** on MQTT broker
- **Reader access management** via web interface

### Data Privacy
- **Tag data encryption** in transit
- **Secure broker configuration** with authentication
- **Regular security updates** for reader firmware

## Performance Optimization

### WebSocket Performance
- **Connection pooling** handled automatically
- **Reconnection logic** with exponential backoff
- **Message queuing** during temporary disconnections

### MQTT Performance
- **Batch processing** for high-volume tag streams
- **QoS optimization** based on use case
- **Connection persistence** with keep-alive

### Resource Management
- **Memory monitoring** on reader
- **Network bandwidth** considerations for high tag volumes
- **CPU usage** optimization for real-time processing

---

**Next Steps:**
- [Tag Monitoring](tag-monitoring.md) - Use IOTC for real-time monitoring
- [API Integration](../advanced/api-integration.md) - Advanced IOTC management
- [Troubleshooting](../advanced/troubleshooting.md) - IOTC issue resolution

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
