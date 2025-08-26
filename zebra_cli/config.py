import json
from pathlib import Path

class ConfigManager:
    """Manages CLI configuration persistence."""

    def __init__(self):
        self.config_dir = Path.home() / ".zebra_cli"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
    
    def save_config(self, ip_address: str, token: str, protocol: str = "https"):
        """Saves configuration to disk."""
        config = {
            "ip_address": ip_address,
            "token": token,
            "protocol": protocol,
            "ws_uri": f"ws://{ip_address}/ws"
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def save_config_dict(self, config_data: dict):
        """Saves a complete configuration dictionary to disk."""
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def load_config(self):
        """Loads configuration from disk."""
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def clear_config(self):
        """Removes saved configuration."""
        if self.config_file.exists():
            self.config_file.unlink()