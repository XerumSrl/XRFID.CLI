# 🤝 Contributing Guide

Welcome to the Zebra RFID CLI project! We appreciate your interest in contributing.

## 📋 Project Information

**Project**: Zebra RFID CLI  
**Developer**: [Xerum Srl](https://xerum.it)  
**License**: MIT License  
**Repository**: [XerumSrl/XRFID.CLI](https://github.com/XerumSrl/XRFID.CLI)

## 🎯 How to Contribute

### 🐛 Bug Reports

Found a bug? Help us improve by reporting it!

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Python version and OS
   - Reader model (FX9600, FXR90, ATR7000)
   - Steps to reproduce
   - Expected vs actual behavior
   - CLI output with `--debug` flag

**Example Bug Report:**
```
**Bug Description**: WebSocket connection fails on FXR90
**Environment**: Python 3.11, Windows 11, FXR90 reader
**Steps to Reproduce**:
1. Connect to FXR90 with `l` command
2. Try WebSocket with `w` command
3. Connection fails with timeout

**Debug Output**:
[DEBUG] WebSocket attempting connection to ws://192.168.1.100/ws
[ERROR] Connection failed: timeout after 10 seconds
```

### 💡 Feature Requests

Have an idea for improvement? We'd love to hear it!

1. **Check the roadmap** to see if it's already planned
2. **Open an issue** with the enhancement label
3. **Describe the use case** and expected behavior
4. **Consider backward compatibility** implications

### 🔧 Code Contributions

#### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/XRFID.CLI.git
   cd XRFID.CLI
   ```

3. **Set up development environment**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Windows)
   .venv\Scripts\Activate.ps1
   # Activate (Linux/macOS)
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies (if available)
   pip install -r requirements-dev.txt  # if exists
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

#### Development Guidelines

##### Code Style

- **Follow PEP 8** Python style guidelines
- **Use type hints** for all function parameters and return values
- **Prefer f-strings** for string formatting
- **Use descriptive variable names** (Italian names are acceptable for domain-specific terms)
- **Include docstrings** for all classes and public methods

**Example:**
```python
def calculate_tag_position(
    rssi: float, 
    azimuth: float, 
    elevation: float, 
    reader_height: float = 3.0
) -> Position3D:
    """
    Calculate 3D position from RSSI and angle data.
    
    Args:
        rssi: Signal strength in dBm
        azimuth: Horizontal angle in degrees
        elevation: Vertical angle in degrees
        reader_height: Reader mounting height in meters
        
    Returns:
        Position3D object with X, Y, Z coordinates
    """
```

##### Threading Considerations

- **Use thread-safe communication** via `queue.Queue`
- **Implement proper cleanup** with `threading.Event`
- **Test concurrent operations** thoroughly
- **Document thread ownership** of resources

##### Error Handling

- **Handle exceptions gracefully** with user-friendly messages
- **Use emoji indicators** for status (✅, ❌, ⚠️)
- **Provide debugging information** when `--debug` is enabled
- **Maintain application stability** - don't crash on network errors

##### Testing

- **Test with real hardware** when possible
- **Include unit tests** for core logic
- **Test error conditions** and recovery scenarios
- **Verify backward compatibility**

#### Commit Guidelines

We use **Conventional Commits** for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(websocket): add automatic reconnection with exponential backoff

Implements robust reconnection logic for WebSocket connections
with configurable retry intervals and maximum attempts.

Closes #123

fix(atr7000): correct position calculation for negative elevations

The position calculation was incorrectly handling negative elevation
angles, causing inverted Z coordinates in some scenarios.

docs(readme): update installation instructions for Python 3.12

Add specific notes about potential compatibility issues and
workarounds for newer Python versions.
```

#### Pull Request Process

1. **Ensure your code follows** the style guidelines
2. **Test thoroughly** with real hardware if possible
3. **Update documentation** if needed
4. **Create a clear PR description**:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested with FX9600 reader
- [ ] Tested with FXR90 reader  
- [ ] Tested with ATR7000 reader
- [ ] Tested on Windows
- [ ] Tested on Linux/macOS

## Checklist
- [ ] Code follows PEP 8 style guidelines
- [ ] Self-review of code completed
- [ ] Documentation updated if needed
- [ ] No breaking changes without discussion
```

5. **Ensure CI passes** (when available)
6. **Respond to review feedback** promptly
7. **Maintain commit history** or squash as requested

## 🧪 Testing Guidelines

### Manual Testing Checklist

#### Basic Functionality
- [ ] CLI starts without errors
- [ ] Connection to reader succeeds
- [ ] Start/stop scanning works
- [ ] WebSocket connection establishes
- [ ] Tag data appears correctly
- [ ] GUI windows open and function

#### Advanced Features
- [ ] IOTC setup completes successfully
- [ ] Real-time plotting works
- [ ] Tag table updates correctly
- [ ] Export functionality works
- [ ] ATR7000 localization (if available)

#### Error Scenarios
- [ ] Network disconnection handling
- [ ] Invalid credentials handling
- [ ] Reader power cycle recovery
- [ ] WebSocket reconnection
- [ ] Configuration file corruption

### Hardware Testing

**Recommended Test Setup:**
- Multiple reader types (FX9600, FXR90, ATR7000)
- Various network configurations
- Different Python versions (3.9, 3.10, 3.11, 3.12)
- Multiple operating systems

## 📚 Documentation Contributions

### Documentation Structure
```
docs/
├── README.md                    # Documentation index
├── installation.md              # Setup instructions
├── quick-start.md              # Getting started guide
├── configuration.md            # Configuration options
├── user-guide/                 # User documentation
├── developer/                  # Technical documentation
├── advanced/                   # Advanced topics
└── reference/                  # API and command reference
```

### Documentation Guidelines

- **Keep examples current** and tested
- **Use clear, concise language**
- **Include screenshots** for GUI features (when relevant)
- **Provide complete code examples**
- **Test all commands and procedures**

## 🚨 Code of Conduct

### Our Commitment

This project is maintained by **Xerum Srl** and we're committed to providing a welcoming, professional environment for all contributors.

### Expected Behavior

- **Be respectful** in all interactions
- **Focus on constructive feedback**
- **Help others learn and contribute**
- **Acknowledge contributions** from others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Spam or off-topic discussions
- Violating intellectual property rights

## 🏢 Xerum Srl Attribution

### Copyright and Attribution

This project is developed and maintained by **[Xerum Srl](https://xerum.it)**.

**Important**: When contributing code or documentation:
- **Maintain original attribution** to Xerum Srl
- **Respect the MIT License** terms
- **Keep copyright notices** intact
- **Credit Xerum Srl** in derivative works

### Commercial Use

This project is available under the MIT License, allowing commercial use. However:
- **Give appropriate credit** to Xerum Srl
- **Include the original license** in derivative works
- **Respect trademark rights** (if any)

## 📞 Getting Help

### Community Support

- **GitHub Issues**: [Report bugs and ask questions](https://github.com/XerumSrl/XRFID.CLI/issues)
- **GitHub Discussions**: [Community discussions](https://github.com/XerumSrl/XRFID.CLI/discussions)
- **Documentation**: [Comprehensive guides](https://github.com/XerumSrl/XRFID.CLI/tree/master/docs)

### Professional Support

For professional support, integration services, or custom development:

**Contact Xerum Srl:**
- Website: [xerum.it](https://xerum.it)
- Email: Available on website
- Professional Services: Custom RFID solutions and integration

## 🎉 Recognition

### Contributors

All contributors are recognized in our project documentation. Significant contributions may be highlighted in:
- Release notes
- Project README
- Documentation credits

### Contribution Types

We value all types of contributions:
- **Code contributions** (features, fixes, optimizations)
- **Documentation improvements** (guides, examples, translations)
- **Testing and validation** (hardware testing, bug reproduction)
- **Community support** (helping other users, answering questions)
- **Design and UX** (interface improvements, workflow optimization)

## 📅 Release Process

### Versioning

We follow **Semantic Versioning** (SemVer):
- `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Cycle

- **Regular releases**: Monthly or as needed
- **Hotfix releases**: Critical bug fixes
- **Feature releases**: Major new functionality

---

## 🙏 Thank You

Thank you for your interest in contributing to Zebra RFID CLI! Your contributions help make this tool better for the entire RFID community.

**Questions?** Feel free to open an issue or start a discussion.

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
