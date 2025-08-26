# 🔧 Troubleshooting Guide

Common issues and their solutions for Zebra RFID CLI.

## Connection Issues

### Cannot Connect to Reader

**Symptoms:**
- Connection timeout errors
- "Reader not reachable" messages
- Authentication failures

**Solutions:**

1. **Check Network Connectivity**
   ```bash
   # Test basic connectivity
   ping 192.168.1.100
   
   # Test specific ports
   telnet 192.168.1.100 80
   telnet 192.168.1.100 443
   ```

2. **Verify Reader Status**
   - Ensure reader is powered on and boots completely
   - Check status LEDs (usually solid green when ready)
   - Access reader's web interface in browser

3. **Check Credentials**
   ```bash
   # Try default credentials
   python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
   
   # Enable debug logging
   python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change --debug
   ```

4. **Network Configuration**
   - Ensure CLI machine and reader are on same subnet
   - Check firewall settings
   - Verify no proxy interference

### Protocol Detection Issues

**Symptoms:**
- Mixed HTTP/HTTPS errors
- SSL certificate warnings
- Protocol mismatch errors

**Solutions:**

1. **Manual Protocol Override**
   ```bash
   # Force HTTP
   python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p admin --debug
   # Then in CLI, disconnect and reconnect
   
   # The CLI auto-detects and saves the working protocol
   ```

2. **SSL Certificate Issues**
   - CLI automatically handles self-signed certificates
   - If issues persist, check reader's certificate configuration

## WebSocket Issues

### WebSocket Connection Failures

**Symptoms:**
- "WebSocket connection failed" errors
- No real-time tag updates
- Connection drops frequently

**Solutions:**

1. **Check IOTC Configuration**
   ```bash
   # In CLI menu, run IOTC setup
   i
   # or
   iotc
   ```

2. **Manual Port Testing**
   - CLI automatically tries ports: 80, 443, 8080, 8443
   - Check reader's WebSocket configuration via web interface

3. **Firewall Issues**
   ```bash
   # Test WebSocket ports
   telnet 192.168.1.100 8080
   telnet 192.168.1.100 8443
   ```

4. **Reset WebSocket Connection**
   ```bash
   # In CLI menu:
   rs  # Force WebSocket reset
   ```

### No Tag Data in WebSocket

**Symptoms:**
- WebSocket connects but no tag events
- Empty tag table
- No RSSI data

**Solutions:**

1. **Verify Reader is Scanning**
   ```bash
   # In CLI menu:
   s  # Start scan
   # Verify via reader web interface that scan is active
   ```

2. **Check IOTC Mapping**
   - IOTC setup may need to be run again
   - Verify data interface mapping in reader configuration

3. **Antenna Configuration**
   - Ensure antennas are enabled
   - Check antenna connections and positioning

## Performance Issues

### Slow Response or High CPU Usage

**Symptoms:**
- CLI becomes unresponsive
- High CPU usage
- Delayed command execution

**Solutions:**

1. **Check Tag Volume**
   - High tag density can overwhelm the CLI
   - Consider filtering tags or reducing scan rate

2. **Virtual Environment Issues**
   ```bash
   # Recreate virtual environment
   deactivate
   rm -rf .venv  # or Remove-Item .venv -Recurse -Force on Windows
   python -m venv .venv
   # Reactivate and reinstall
   pip install -r requirements.txt
   ```

3. **Memory Issues**
   - CLI maintains tag history
   - Restart CLI periodically for very long sessions

### Plotting/Visualization Issues

**Symptoms:**
- Plots not displaying
- GUI windows not opening
- Graph rendering errors

**Solutions:**

1. **GUI Dependencies (Linux)**
   ```bash
   # Install GUI libraries
   sudo apt install python3-tk
   sudo apt install python3-matplotlib
   ```

2. **Display Issues (Remote/SSH)**
   ```bash
   # Enable X11 forwarding
   ssh -X user@hostname
   
   # Or use terminal-based plotting only
   # In CLI: Use option 8 instead of 9 for RSSI plots
   ```

3. **Windows Display Issues**
   ```powershell
   # Ensure tkinter is available
   python -c "import tkinter; print('tkinter works')"
   
   # If missing, reinstall Python with tkinter support
   ```

## API Integration Issues

### REST API Submenu Not Working

**Symptoms:**
- API submenu won't open
- API requests fail
- Authentication errors in API calls

**Solutions:**

1. **Ensure Connected**
   - API submenu only works when connected to reader
   - Use `l` to login first

2. **Check Generated Client**
   ```bash
   # Verify API client files exist
   ls zebra_cli/rest_client/
   
   # Regenerate if needed (advanced)
   # Check API-SUBMENU-README.md for instructions
   ```

## Configuration Issues

### Settings Not Persisting

**Symptoms:**
- Have to re-enter IP/credentials every time
- Configuration not saved
- Settings reset on restart

**Solutions:**

1. **Check Configuration File**
   ```bash
   # Verify config.yaml exists and is writable
   ls -la config.yaml
   
   # Check permissions
   chmod 644 config.yaml  # Linux/macOS
   ```

2. **File Permission Issues**
   ```bash
   # Remove corrupt config file
   rm config.yaml  # Linux/macOS
   # or
   Remove-Item config.yaml  # Windows PowerShell
   
   # CLI will recreate on next run
   ```

### Virtual Environment Issues

**Symptoms:**
- Import errors
- Module not found errors
- Dependency conflicts

**Solutions:**

1. **Clean Reinstall**
   ```bash
   # Deactivate and remove virtual environment
   deactivate
   rm -rf .venv
   
   # Recreate and reinstall
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or .venv\Scripts\Activate.ps1  # Windows
   
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Hardware-Specific Issues

### ATR7000 Localization Not Working

**Symptoms:**
- ATR submenu available but no position data
- Directionality messages not received
- Position calculations failing

**Solutions:**

1. **Verify ATR7000 Configuration**
   - Ensure reader is configured for RAW_DIRECTIONALITY messages
   - Check antenna configuration for direction-finding

2. **Height Configuration**
   ```bash
   # In ATR submenu:
   c  # Configure reader and tag heights
   ```

### FXR90 vs FX9600 Issues

**Symptoms:**
- Some features not working
- Different API behavior
- IOTC setup failures

**Solutions:**

1. **Reader Type Detection**
   - CLI automatically detects reader type
   - FXR90 uses different API endpoints

2. **Check Reader Model**
   ```bash
   # Enable debug logging to see detected reader type
   python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p admin --debug
   ```

## Getting Help

### Debug Information

When reporting issues, include:

```bash
# System information
python --version
pip list

# CLI debug output
python xrcli_entrypoint.py --ip YOUR_IP -u admin -p change --debug

# Reader information
# Model, firmware version, network configuration
```

### Log Files

Check for additional error information:
- Configuration errors: `config.yaml`
- Python errors: Enable debug mode
- Network errors: Use ping/telnet diagnostics

### Support Channels

1. **GitHub Issues**: [Report bugs and feature requests](https://github.com/XerumSrl/XRFID.CLI/issues)
2. **GitHub Discussions**: [Community support](https://github.com/XerumSrl/XRFID.CLI/discussions)
3. **Documentation**: Check other guides in the [docs folder](../README.md)

---

**Still having issues?** [Open an issue](https://github.com/XerumSrl/XRFID.CLI/issues) on GitHub with:
- Your system information
- Complete error messages
- Steps to reproduce the issue

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
