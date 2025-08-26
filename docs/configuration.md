# ⚙️ Configuration Guide

Complete guide to configuring Zebra RFID CLI for optimal performance and persistent settings.

## Configuration File Location

The Zebra RFID CLI uses a JSON configuration file to store connection settings and session data.

The configuration file is automatically created and managed at:
- **Linux/macOS**: `~/.zebra_cli/config.json`
- **Windows**: `%USERPROFILE%\.zebra_cli\config.json`

## Configuration Structure

The CLI automatically saves connection settings when you successfully connect to a reader:

```json
{
  "ip_address": "192.168.1.100",
  "token": "your-bearer-token-here",
  "protocol": "https",
  "ws_uri": "ws://192.168.1.100/ws"
}
```

## Configuration Management

### Automatic Configuration

The CLI automatically manages configuration through the interactive interface:

1. **First Connection**: When you connect to a reader for the first time, the CLI saves your connection details
2. **Session Persistence**: Settings are automatically loaded on subsequent runs
3. **Protocol Detection**: The CLI tests both HTTP and HTTPS, saving the working protocol
4. **WebSocket URI**: Automatically generated based on the IP address

### Configuration Options

| Field | Type | Description |
|-------|------|-------------|
| `ip_address` | string | IP address of the Zebra IoT Connector |
| `token` | string | Bearer token obtained during authentication |
| `protocol` | string | Working protocol ("http" or "https") |
| `ws_uri` | string | WebSocket URI for real-time tag events |

### Manual Configuration

While the CLI manages configuration automatically, you can manually edit the JSON file if needed:

```json
{
  "ip_address": "192.168.1.100",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "protocol": "https",
  "ws_uri": "ws://192.168.1.100/ws"
}
```

**⚠️ Note**: Manual edits will be overwritten when you reconnect through the CLI interface.

## Default Settings

### Default Credentials
- **Username**: `admin`
- **Password**: `change`

### Connection Timeouts
- **HTTP/HTTPS requests**: 30 seconds
- **WebSocket connection**: 10 seconds
- **Authentication**: 15 seconds

### WebSocket Configuration
The CLI automatically attempts multiple WebSocket URIs for robust connections:
- Primary: `ws://{ip}/ws`
- Fallback URIs tested automatically on connection failure

## Configuration Commands

### Through CLI Interface
1. Start the CLI: `python xrcli_entrypoint.py`
2. Use option **1** to configure connection settings
3. Settings are automatically saved on successful connection

### Clearing Configuration
To reset all settings, delete the configuration file:

```bash
# Linux/macOS
rm ~/.zebra_cli/config.json

# Windows PowerShell
Remove-Item "$env:USERPROFILE\.zebra_cli\config.json"
```

## Troubleshooting Configuration

### Common Issues

**Configuration Not Loading**
- Check if `~/.zebra_cli/` directory exists
- Verify JSON syntax in `config.json`
- Check file permissions

**Connection Settings Not Saved**
- Ensure successful authentication before expecting persistence
- Check write permissions to home directory
- Verify the CLI completed the login process

**WebSocket Issues**
- WebSocket URI is auto-generated from IP address
- Protocol detection happens independently for HTTP/HTTPS vs WebSocket
- Multiple fallback URIs are attempted automatically

### Debug Mode
For configuration troubleshooting, check the source code:
- Configuration logic: `zebra_cli/config.py`
- Interactive interface: `zebra_cli/interactive_cli.py`
- Connection management: `zebra_cli/iotc_client.py`

## Advanced Configuration

### Development Mode
For development purposes, you can inspect the configuration:

```python
from zebra_cli.config import ConfigManager

config_manager = ConfigManager()
config = config_manager.load_config()
print(config)
```

### Custom Configuration Location
The configuration directory is currently fixed to `~/.zebra_cli/` but can be modified in the `ConfigManager` class constructor.

## Security Considerations

- **Bearer tokens** are stored in plain text in the configuration file
- Ensure proper file system permissions on the `.zebra_cli` directory
- Consider the security implications of storing authentication tokens
- The configuration file should not be shared or committed to version control

---

**Need help with configuration?** Check the [troubleshooting guide](advanced/troubleshooting.md) or [command reference](reference/commands.md).

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
