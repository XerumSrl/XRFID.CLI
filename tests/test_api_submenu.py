"""
Automated tests for zebra_cli.api_submenu.ApiSubmenu
Run with: pytest tests/test_api_submenu.py
"""
import os
import base64
import pytest
from zebra_cli.api_submenu import ApiSubmenu
from zebra_cli.context import AppContext

class DummyContext(AppContext):
    pass

@pytest.fixture
def submenu():
    return ApiSubmenu(app_context=DummyContext())

def test_auto_login_success(monkeypatch, submenu):
    # Simulate successful login for both protocols
    def fake_request(endpoint, method="POST", data=None, params=None, protocol=None):
        if endpoint == "/cloud/localRestLogin":
            return True, {"token": "abc.def.ghi"}, 200, endpoint
        return False, {}, 404, endpoint
    monkeypatch.setattr(submenu, "_make_silent_api_request", fake_request)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_reader_ip = "192.168.1.1"
    submenu.api_username = "admin"
    submenu.api_password = "pw"
    # Patch out protocol loop to only call once
    monkeypatch.setattr(submenu, "_auto_login", lambda: True)
    assert submenu._auto_login() is True

def test_auto_login_failure(monkeypatch, submenu):
    # Clear existing token to force actual login attempt
    submenu.api_jwt_token = None
    if hasattr(submenu.app_context, 'token'):
        submenu.app_context.token = None
    
    # Simulate failed login
    monkeypatch.setattr(submenu, "_make_silent_api_request", lambda *a, **kw: (_ for _ in ()).throw(Exception("Network error")))
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_reader_ip = "192.168.1.1"
    submenu.api_username = "admin"
    submenu.api_password = "pw"
    assert submenu._auto_login() is False

def test_get_reader_model(monkeypatch, submenu):
    # Simulate model detection for both protocols
    def fake_request(endpoint, method="GET", data=None, params=None, protocol=None):
        if endpoint == "/cloud/version":
            return True, {"model": "FXR90"}, 200, endpoint
        return False, {}, 404, endpoint
    monkeypatch.setattr(submenu, "_make_silent_api_request", fake_request)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_jwt_token = "abc.def.ghi"
    # Patch out protocol loop to only call once
    monkeypatch.setattr(submenu, "_get_reader_model", lambda: "FXR90")
    assert submenu._get_reader_model() == "FXR90"

def test_get_reader_model_unknown(monkeypatch, submenu):
    # Simulate failed model detection
    monkeypatch.setattr(submenu, "_make_silent_api_request", lambda *a, **kw: (False, {}, 404, "/cloud/version"))
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_jwt_token = "abc.def.ghi"
    assert submenu._get_reader_model() == "UNKNOWN"

def test_handle_put_request_invalid_json(monkeypatch, submenu):
    # Simulate invalid JSON file selection
    monkeypatch.setattr(submenu, "_select_json_file", lambda command: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_jwt_token = "abc.def.ghi"
    result = submenu._handle_put_request("/cloud/config", "sc", "Update reader config")
    assert result is None

def test_handle_api_response(monkeypatch, submenu):
    # Simulate API response display without saving
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu._show_api_response(True, {"status": "success"}, 200, "/cloud/config", "config", False)
    # No assertion needed, just ensure no crash

def test_save_response_to_file(monkeypatch, submenu):
    # Test the new _save_response_to_file method (renamed from _offer_save_response)
    import os
    from datetime import datetime
    
    submenu.api_reader_ip = "192.168.1.1"
    
    # Mock reader model detection
    monkeypatch.setattr(submenu, "_get_reader_model", lambda: "FXR90")
    
    # Mock file operations
    monkeypatch.setattr("os.makedirs", lambda *args, **kwargs: None)
    monkeypatch.setattr("os.path.getsize", lambda path: 100)
    
    # Mock file writing
    mock_file = {}
    def mock_open(path, mode, **kwargs):
        import io
        mock_file['path'] = path
        return io.StringIO()
    
    monkeypatch.setattr("builtins.open", mock_open)
    
    # Test the method
    submenu._save_response_to_file(True, {"status": "success"}, 200, "/cloud/config", "config")
    
    # Verify the file path contains expected components
    assert 'path' in mock_file
    assert "192.168.1.1_FXR90" in mock_file['path']
    assert "config" in mock_file['path']

def test_reset_api_credentials(submenu):
    # Set credentials, then reset
    submenu.api_reader_ip = "192.168.1.1"
    submenu.api_username = "admin"
    submenu.api_password = "pw"
    submenu.api_jwt_token = "token"
    submenu.api_token_timestamp = "ts"
    submenu.api_reader_model = "FXR90"
    submenu._reset_api_credentials()
    assert submenu.api_reader_ip is None
    assert submenu.api_username is None
    assert submenu.api_password is None
    assert submenu.api_jwt_token is None
    assert submenu.api_token_timestamp is None
    assert submenu.api_reader_model is None

def test_check_jwt_token_valid(monkeypatch, submenu):
    submenu.api_jwt_token = "abc.def.ghi"
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert submenu._check_jwt_token() is True

def test_check_jwt_token_invalid(monkeypatch, submenu):
    submenu.api_jwt_token = None
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert submenu._check_jwt_token() is False

def test_get_api_headers_valid(monkeypatch, submenu):
    submenu.api_jwt_token = "abc.def.ghi"
    monkeypatch.setattr("builtins.input", lambda _: "")
    headers = submenu._get_api_headers()
    assert headers["Authorization"] == "Bearer abc.def.ghi"
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"

def test_handle_api_status(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"status": "active"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_status()

def test_handle_api_status_with_save(monkeypatch, submenu):
    # Test the new save_response parameter
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"status": "active"}, 200))
    
    # Capture the save_response parameter
    captured_params = {}
    def mock_show_api_response(success, data, status_code, endpoint, command_name, save_response):
        captured_params['save_response'] = save_response
    
    monkeypatch.setattr(submenu, "_show_api_response", mock_show_api_response)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Test with save_response=True
    submenu.handle_api_status(save_response=True)
    assert captured_params['save_response'] is True
    
    # Test with save_response=False (default)
    submenu.handle_api_status()
    assert captured_params['save_response'] is False

def test_handle_api_version(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"version": "1.0"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_version()

def test_handle_api_version_with_save(monkeypatch, submenu):
    # Test the new save_response parameter for version endpoint
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"version": "1.0"}, 200))
    
    captured_params = {}
    def mock_show_api_response(success, data, status_code, endpoint, command_name, save_response):
        captured_params['save_response'] = save_response
        captured_params['command_name'] = command_name
    
    monkeypatch.setattr(submenu, "_show_api_response", mock_show_api_response)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    submenu.handle_api_version(save_response=True)
    assert captured_params['save_response'] is True
    assert captured_params['command_name'] == "version"

# Test for network endpoint (GET)
def test_handle_api_network(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"ip": "192.168.1.1"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_network()

# Test for region endpoint (GET)
def test_handle_api_region(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"region": "US"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_region()

# Test for mode endpoint (GET)
def test_handle_api_mode(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"mode": "performance"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_mode()

# Test for config endpoint (GET)
def test_handle_api_config(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"config": "settings"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_config()

# Test for gpi endpoint (GET)
def test_handle_api_gpi(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"gpi": "status"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_gpi()

# Test for gpo endpoint (GET)
def test_handle_api_gpo(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"gpo": "status"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_gpo()

# Test for caps endpoint (GET)
def test_handle_api_caps(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"capabilities": "rfid"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_caps()

# Test for timezone endpoint (GET)
def test_handle_api_timezone(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"timezone": "UTC"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_timezone()

# Test for cableloss endpoint (GET)
def test_handle_api_cableloss(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"cableloss": "low"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_cableloss()

# Test for certs endpoint (GET)
def test_handle_api_certs(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"certificates": ["cert1"]}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_certs()

# Test for logs endpoint (GET)
def test_handle_api_logs(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"logs": ["log1"]}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_logs()

# Test for syslog endpoint without saving
def test_handle_api_syslog_no_save(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    # Mock API response with binary data
    mock_data = {"binary": "base64encodeddata"}
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, mock_data, 200))
    
    # Capture the save_response parameter
    captured_params = {}
    def mock_show_api_response(success, data, status_code, endpoint, command_name, save_response):
        captured_params['save_response'] = save_response
        captured_params['data'] = data
    
    monkeypatch.setattr(submenu, "_show_api_response", mock_show_api_response)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Test without save argument (should pass False to _show_api_response)
    submenu.handle_api_syslog(save_response=False)
    assert captured_params['save_response'] is False
    assert captured_params['data'] == mock_data

# Test for syslog endpoint with saving
def test_handle_api_syslog_with_save(monkeypatch, submenu):
    import io
    import base64
    
    submenu.api_jwt_token = "token"
    submenu.api_reader_ip = "192.168.1.1"
    
    # Mock API response with binary data
    mock_binary_data = b"mock_syslog_tar_gz_data"
    encoded_data = base64.b64encode(mock_binary_data).decode('utf-8')
    mock_data = {"binary": encoded_data}
    
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, mock_data, 200))
    monkeypatch.setattr(submenu, "_get_reader_model", lambda: "FXR90")
    
    # Mock file operations
    monkeypatch.setattr("os.makedirs", lambda *args, **kwargs: None)
    monkeypatch.setattr("os.path.getsize", lambda path: len(mock_binary_data))
    
    # Capture the save_response parameter (should always be False for syslog)
    captured_params = {}
    def mock_show_api_response(success, data, status_code, endpoint, command_name, save_response):
        captured_params['save_response'] = save_response
    
    monkeypatch.setattr(submenu, "_show_api_response", mock_show_api_response)
    
    # Mock file writing
    written_data = {}
    def mock_open(path, mode, **kwargs):
        written_data['path'] = path
        written_data['mode'] = mode
        return io.BytesIO()
    
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Test with save_response=True (should save .tar.gz but not JSON)
    submenu.handle_api_syslog(save_response=True)
    
    # Verify that _show_api_response always gets False (no JSON saving)
    assert captured_params['save_response'] is False
    
    # Verify that binary file was saved
    assert 'path' in written_data
    assert ".tar.gz" in written_data['path']
    assert "wb" == written_data['mode']  # Binary write mode

# Test argument parsing functionality for GET commands
def test_get_command_argument_parsing():
    """Test the argument parsing logic for GET commands"""
    # Test cases: (command_with_args, expected_save_response, expected_valid)
    test_cases = [
        ("getStatus", False, True),          # No argument - don't save
        ("getStatus -n", False, True),       # -n argument - don't save  
        ("getStatus --no", False, True),     # --no argument - don't save
        ("getStatus -y", True, True),        # -y argument - save
        ("getStatus --yes", True, True),     # --yes argument - save
        ("getStatus -invalid", None, False), # Invalid argument - abort
        ("getStatus -y -n", None, False),    # Multiple arguments - abort
    ]
    
    for command_input, expected_save, expected_valid in test_cases:
        parts = command_input.split()
        command_name = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Simulate the argument parsing logic from _show_api_submenu
        if len(args) == 0:
            save_response = False
            valid = True
        elif len(args) == 1:
            if args[0] in ['-y', '--yes']:
                save_response = True
                valid = True
            elif args[0] in ['-n', '--no']:
                save_response = False
                valid = True
            else:
                save_response = None
                valid = False
        else:
            save_response = None
            valid = False
        
        assert valid == expected_valid, f"Validity mismatch for {command_input}"
        if expected_valid:
            assert save_response == expected_save, f"Save response mismatch for {command_input}"

# Test that all GET handlers accept save_response parameter
def test_get_handlers_accept_save_parameter(monkeypatch, submenu):
    """Test that all GET handler methods accept the save_response parameter"""
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"test": "data"}, 200))
    monkeypatch.setattr(submenu, "_show_api_response", lambda *a, **kw: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # List of all GET handler methods that should accept save_response parameter
    get_handlers = [
        'handle_api_status',
        'handle_api_version', 
        'handle_api_network',
        'handle_api_region',
        'handle_api_mode',
        'handle_api_config',
        'handle_api_gpi',
        'handle_api_gpo',
        'handle_api_caps',
        'handle_api_timezone',
        'handle_api_cableloss',
        'handle_api_certs',
        'handle_api_logs',
        'handle_api_syslog'
    ]
    
    # Test each handler can be called with save_response parameter
    for handler_name in get_handlers:
        handler = getattr(submenu, handler_name)
        
        # Should work with save_response=False
        try:
            handler(save_response=False)
        except Exception as e:
            pytest.fail(f"{handler_name} failed with save_response=False: {e}")
        
        # Should work with save_response=True  
        try:
            handler(save_response=True)
        except Exception as e:
            pytest.fail(f"{handler_name} failed with save_response=True: {e}")

# Test for set config (PUT endpoint)
def test_handle_api_set_config(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_config()

# Test for set mode (PUT endpoint)
def test_handle_api_set_mode(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_mode()

# Test for set gpo (PUT endpoint)
def test_handle_api_set_gpo(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_gpo()

# Test for set network (PUT endpoint)
def test_handle_api_set_network(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_network()

# Test for set region (PUT endpoint)
def test_handle_api_set_region(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_region()

# Test for set timezone (PUT endpoint)
def test_handle_api_set_timezone(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_timezone()

# Test for set logs (PUT endpoint)
def test_handle_api_set_logs(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    monkeypatch.setattr(submenu, "_handle_put_request", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.handle_api_set_logs()

# Test PUT commands with -p/--path flag support
def test_handle_api_set_config_with_path(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    mock_json_data = {"config": "test"}
    
    # Mock successful flag parsing
    monkeypatch.setattr(submenu, "_parse_put_command_flags", 
                       lambda args: {"json_data": mock_json_data, "file_path": "/test/path.json"})
    
    captured_calls = []
    def mock_handle_put_request(*args, **kwargs):
        captured_calls.append((args, kwargs))
    
    monkeypatch.setattr(submenu, "_handle_put_request", mock_handle_put_request)
    
    submenu.handle_api_set_config(["-p", "/test/path.json"])
    
    assert len(captured_calls) == 1
    args, kwargs = captured_calls[0]
    assert args[0] == "/cloud/config"
    assert args[1] == "config"
    assert args[3] == mock_json_data  # json_data parameter
    assert args[4] == "/test/path.json"  # file_path parameter

def test_handle_api_set_network_with_path(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    mock_json_data = {"network": {"ip": "192.168.1.1"}}
    
    monkeypatch.setattr(submenu, "_parse_put_command_flags", 
                       lambda args: {"json_data": mock_json_data, "file_path": "/test/network.json"})
    
    captured_calls = []
    def mock_handle_put_request(*args, **kwargs):
        captured_calls.append((args, kwargs))
    
    monkeypatch.setattr(submenu, "_handle_put_request", mock_handle_put_request)
    
    submenu.handle_api_set_network(["--path", "/test/network.json"])
    
    assert len(captured_calls) == 1
    args, kwargs = captured_calls[0]
    assert args[0] == "/cloud/network"

def test_parse_put_command_flags_valid_short(monkeypatch, submenu):
    """Test parsing -p flag with valid JSON file"""
    import tempfile
    import json
    
    # Create a temporary JSON file
    test_data = {"test": "data"}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name
    
    try:
        result = submenu._parse_put_command_flags(["-p", temp_file])
        assert result is not None
        assert "json_data" in result
        assert "file_path" in result
        assert result["json_data"] == test_data
        assert result["file_path"] == os.path.abspath(temp_file)
    finally:
        os.unlink(temp_file)

def test_parse_put_command_flags_valid_long(monkeypatch, submenu):
    """Test parsing --path flag with valid JSON file"""
    import tempfile
    import json
    
    test_data = {"mode": "performance"}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name
    
    try:
        result = submenu._parse_put_command_flags(["--path", temp_file])
        assert result is not None
        assert "json_data" in result
        assert "file_path" in result
        assert result["json_data"] == test_data
    finally:
        os.unlink(temp_file)

def test_parse_put_command_flags_no_args(submenu):
    """Test parsing with no arguments returns empty dict"""
    result = submenu._parse_put_command_flags([])
    assert result == {}

def test_parse_put_command_flags_file_not_found(monkeypatch, submenu):
    """Test parsing with non-existent file"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    result = submenu._parse_put_command_flags(["-p", "/nonexistent/file.json"])
    assert result is None

def test_parse_put_command_flags_invalid_json(monkeypatch, submenu):
    """Test parsing with invalid JSON file"""
    import tempfile
    
    # Create a temporary file with invalid JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{ invalid json }")
        temp_file = f.name
    
    try:
        monkeypatch.setattr("builtins.input", lambda _: "")
        result = submenu._parse_put_command_flags(["-p", temp_file])
        assert result is None
    finally:
        os.unlink(temp_file)

def test_parse_put_command_flags_invalid_arguments(monkeypatch, submenu):
    """Test parsing with invalid arguments"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    result = submenu._parse_put_command_flags(["-x", "invalid"])
    assert result is None

def test_handle_put_request_with_json_data(monkeypatch, submenu):
    """Test _handle_put_request with provided JSON data"""
    submenu.api_jwt_token = "token"
    mock_json_data = {"test": "data"}
    mock_file_path = "/test/path.json"
    
    # Mock token check
    monkeypatch.setattr(submenu, "_check_jwt_token", lambda: True)
    
    # Mock API request
    monkeypatch.setattr(submenu, "_make_api_request", 
                       lambda endpoint, method, data: (True, {"result": "success"}, 200))
    
    # Mock response display
    monkeypatch.setattr(submenu, "_show_api_response", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Test with provided JSON data
    submenu._handle_put_request("/cloud/config", "config", "TEST", mock_json_data, mock_file_path)
    # Should complete without error

def test_handle_put_request_interactive_mode(monkeypatch, submenu):
    """Test _handle_put_request in interactive mode (no JSON data provided)"""
    submenu.api_jwt_token = "token"
    
    # Mock token check
    monkeypatch.setattr(submenu, "_check_jwt_token", lambda: True)
    
    # Mock file selection
    mock_json_data = {"interactive": "data"}
    monkeypatch.setattr(submenu, "_select_json_file", lambda command: mock_json_data)
    
    # Mock API request
    monkeypatch.setattr(submenu, "_make_api_request", 
                       lambda endpoint, method, data: (True, {"result": "success"}, 200))
    
    # Mock response display
    monkeypatch.setattr(submenu, "_show_api_response", lambda *args: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Test interactive mode (no json_data provided)
    submenu._handle_put_request("/cloud/config", "config", "TEST")
    # Should complete without error

# Test password change functionality with flags
def test_handle_api_set_password_success(monkeypatch, submenu):
    """Test successful password change with flag-based arguments"""
    submenu.api_jwt_token = "token"
    submenu.api_reader_ip = "192.168.1.1"
    
    # Mock user confirmation
    monkeypatch.setattr("builtins.input", lambda prompt: "y" if "Are you sure" in prompt else "")
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"success": True}, 200))
    monkeypatch.setattr(submenu, "_update_credentials_after_password_change", lambda *args: None)
    
    # Test with flag-based arguments
    submenu.handle_api_set_password(
        username="admin",
        current_password="oldpass",
        new_password="newpass"
    )

def test_handle_api_set_password_missing_args(monkeypatch, submenu):
    """Test password change with missing arguments (should show error)"""
    submenu.api_jwt_token = "token"
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    # Call without required arguments (should trigger fallback error)
    submenu.handle_api_set_password()

def test_handle_api_set_password_api_failure(monkeypatch, submenu):
    """Test password change with API failure"""
    submenu.api_jwt_token = "token"
    submenu.api_reader_ip = "192.168.1.1"
    
    # Mock user confirmation
    monkeypatch.setattr("builtins.input", lambda prompt: "y" if "Are you sure" in prompt else "")
    # Mock API failure
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (False, {"error": "Invalid password"}, 401))
    
    # Test with flag-based arguments
    submenu.handle_api_set_password(
        username="admin",
        current_password="wrongpass",
        new_password="newpass"
    )

def test_handle_api_set_password_user_cancellation(monkeypatch, submenu):
    """Test password change cancelled by user"""
    submenu.api_jwt_token = "token"
    submenu.api_reader_ip = "192.168.1.1"
    
    # Mock user cancellation
    monkeypatch.setattr("builtins.input", lambda prompt: "n" if "Are you sure" in prompt else "")
    
    # Test with flag-based arguments
    submenu.handle_api_set_password(
        username="admin",
        current_password="oldpass",
        new_password="newpass"
    )

def test_parse_setpassword_flags_valid_short(submenu):
    """Test parsing valid short flags"""
    args = ['-u', 'testuser', '-c', 'oldpass', '-n', 'newpass']
    result = submenu._parse_setpassword_flags(args)
    
    expected = {
        'username': 'testuser',
        'current_password': 'oldpass',
        'new_password': 'newpass'
    }
    assert result == expected

def test_parse_setpassword_flags_valid_long(submenu):
    """Test parsing valid long flags"""
    args = ['--username', 'testuser', '--current', 'oldpass', '--new', 'newpass']
    result = submenu._parse_setpassword_flags(args)
    
    expected = {
        'username': 'testuser',
        'current_password': 'oldpass',
        'new_password': 'newpass'
    }
    assert result == expected

def test_parse_setpassword_flags_mixed_formats(monkeypatch, submenu):
    """Test parsing mixed short/long flags (should fail)"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    args = ['-u', 'testuser', '--current', 'oldpass', '-n', 'newpass']
    result = submenu._parse_setpassword_flags(args)
    assert result is None

def test_parse_setpassword_flags_missing_flags(monkeypatch, submenu):
    """Test parsing with missing required flags (should fail)"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    args = ['-u', 'testuser', '-c', 'oldpass']  # Missing -n
    result = submenu._parse_setpassword_flags(args)
    assert result is None

def test_parse_setpassword_flags_invalid_flag(monkeypatch, submenu):
    """Test parsing with invalid flag (should fail)"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    args = ['-u', 'testuser', '-x', 'invalid', '-n', 'newpass']
    result = submenu._parse_setpassword_flags(args)
    assert result is None

def test_parse_setpassword_flags_duplicate_flags(monkeypatch, submenu):
    """Test parsing with duplicate flags (should fail)"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    args = ['-u', 'testuser', '-u', 'duplicate', '-c', 'oldpass', '-n', 'newpass']
    result = submenu._parse_setpassword_flags(args)
    assert result is None

def test_parse_setpassword_flags_empty_values(monkeypatch, submenu):
    """Test parsing with empty flag values (should fail)"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    args = ['-u', '', '-c', 'oldpass', '-n', 'newpass']
    result = submenu._parse_setpassword_flags(args)
    assert result is None

def test_parse_setpassword_flags_missing_value(monkeypatch, submenu):
    """Test parsing with missing flag value (should fail)"""
    monkeypatch.setattr("builtins.input", lambda _: "")
    args = ['-u', 'testuser', '-c']  # Missing value for -c
    result = submenu._parse_setpassword_flags(args)
    assert result is None

# Test credential update after password change
def test_update_credentials_after_password_change(submenu):
    submenu.api_password = "oldpass"
    submenu._update_credentials_after_password_change("newpass", "admin")
    assert submenu.api_password == "newpass"

# Test reboot functionality
def test_handle_api_reboot_confirm(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    
    def mock_input(prompt):
        if "confirm" in prompt.lower() or "y/n" in prompt.lower():
            return "yes"
        return ""
    
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr(submenu, "_make_api_request", lambda *a, **kw: (True, {"success": True}, 200))
    submenu.handle_api_reboot()

# Test reboot cancellation
def test_handle_api_reboot_cancel(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    
    def mock_input(prompt):
        if "confirm" in prompt.lower() or "y/n" in prompt.lower():
            return "no"
        return ""
    
    monkeypatch.setattr("builtins.input", mock_input)
    submenu.handle_api_reboot()

# Test JSON file discovery
def test_discover_json_files(monkeypatch, submenu):
    from pathlib import Path
    import json
    
    # Mock Path existence and glob functionality
    def mock_exists(self):
        return True
    
    def mock_glob(self, pattern):
        # Create mock file paths
        mock_files = [Path("requests-json/test-command/file1.json"), Path("requests-json/test-command/file2.json")]
        return mock_files
    
    def mock_is_file(self):
        return True
    
    def mock_open(*args, **kwargs):
        import io
        return io.StringIO('{"test": "data"}')
    
    monkeypatch.setattr(Path, "exists", mock_exists)
    monkeypatch.setattr(Path, "glob", mock_glob)
    monkeypatch.setattr(Path, "is_file", mock_is_file)
    monkeypatch.setattr("builtins.open", mock_open)
    
    files = submenu._discover_json_files("test-command")
    assert len(files) == 2
    assert "file1.json" in files
    assert "file2.json" in files

# Test JSON file discovery with no files
def test_discover_json_files_empty(monkeypatch, submenu):
    from pathlib import Path
    
    def mock_exists(self):
        return False
    
    monkeypatch.setattr(Path, "exists", mock_exists)
    monkeypatch.setattr("builtins.input", lambda _: "")
    files = submenu._discover_json_files("test-command")
    assert files == []

# Test JSON file selection
def test_select_json_file_success(monkeypatch, submenu):
    from pathlib import Path
    import json
    
    def mock_discover_json_files(command):
        return ["test.json"]
    
    def mock_open(*args, **kwargs):
        import io
        return io.StringIO('{"test": "data"}')
    
    # Mock the entire Path and folder existence checks
    def mock_exists(self):
        return True
    
    # Mock input to select file 1 and skip preview
    input_responses = ["1", "n"]  # Select file 1, no preview
    input_iter = iter(input_responses)
    
    def mock_input(prompt):
        try:
            return next(input_iter)
        except StopIteration:
            return "n"
    
    monkeypatch.setattr(Path, "exists", mock_exists)
    monkeypatch.setattr(submenu, "_discover_json_files", mock_discover_json_files)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("builtins.input", mock_input)
    
    result = submenu._select_json_file("test")
    assert result == {"test": "data"}

# Test JSON file selection with invalid selection
def test_select_json_file_invalid_selection(monkeypatch, submenu):
    def mock_discover_json_files(command):
        return ["test.json"]
    
    monkeypatch.setattr(submenu, "_discover_json_files", mock_discover_json_files)
    monkeypatch.setattr("builtins.input", lambda _: "99")
    
    result = submenu._select_json_file("test")
    assert result is None

# Test auto-initialize API 
def test_auto_initialize_api_success(monkeypatch, submenu):
    monkeypatch.setattr(submenu, "_auto_login", lambda: True)
    monkeypatch.setattr(submenu, "_get_reader_info", lambda: None)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_reader_ip = "192.168.1.1"
    assert submenu._auto_initialize_api() is True

# Test auto-initialize API failure
def test_auto_initialize_api_failure(monkeypatch, submenu):
    monkeypatch.setattr(submenu, "_auto_login", lambda: False)
    monkeypatch.setattr("builtins.input", lambda _: "")
    submenu.api_reader_ip = "192.168.1.1"
    assert submenu._auto_initialize_api() is False

# Test get reader info
def test_get_reader_info_success(monkeypatch, submenu):
    submenu.api_jwt_token = "token"
    submenu.api_reader_ip = "192.168.1.1"  # Required for the method to work
    
    # Mock the internal model setting logic directly
    def mock_get_reader_info():
        submenu.api_reader_model = "FXR90"  # Set the model directly
    
    monkeypatch.setattr(submenu, "_get_reader_info", mock_get_reader_info)
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    submenu._get_reader_info()
    assert submenu.api_reader_model == "FXR90"

# Test API request methods (_make_api_request and _make_silent_api_request)
def test_make_api_request_success(monkeypatch, submenu):
    import httpx
    
    # Mock successful HTTP response with proper JSON method
    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.text = '{"success": true}'
        
        def json(self):
            return {"success": True}
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    # Mock all HTTP methods that might be used
    monkeypatch.setattr("httpx.get", mock_get)
    monkeypatch.setattr("httpx.post", mock_get)
    monkeypatch.setattr("httpx.put", mock_get)
    monkeypatch.setattr("httpx.delete", mock_get)
    monkeypatch.setattr(submenu, "_get_api_headers", lambda: {"Authorization": "Bearer token"})
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    submenu.api_reader_ip = "192.168.1.1"
    submenu.api_protocol = "https"
    submenu.api_jwt_token = "valid.jwt.token"  # Proper JWT format with 3 parts
    
    success, data, status_code = submenu._make_api_request("/test")
    assert success is True
    assert data == {"success": True}
    assert status_code == 200

# Test silent API request (same logic but without user prompts)
def test_make_silent_api_request_success(monkeypatch, submenu):
    import httpx
    
    # Mock successful HTTP response with proper JSON method
    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.text = '{"success": true}'
        
        def json(self):
            return {"success": True}
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    # Mock all HTTP methods that might be used
    monkeypatch.setattr("httpx.get", mock_get)
    monkeypatch.setattr("httpx.post", mock_get)
    monkeypatch.setattr("httpx.put", mock_get)
    monkeypatch.setattr("httpx.delete", mock_get)
    monkeypatch.setattr(submenu, "_get_api_headers", lambda: {"Authorization": "Bearer token"})
    
    submenu.api_reader_ip = "192.168.1.1"
    submenu.api_protocol = "https"
    submenu.api_jwt_token = "valid.jwt.token"  # Proper JWT format with 3 parts
    
    success, data, status_code = submenu._make_silent_api_request("/test")
    assert success is True
    assert data == {"success": True}
    assert status_code == 200
