"""
Persistent Interactive CLI for API Submenu
"""
# Standard library imports
import os
import time
import json
import base64
import getpass
from pathlib import Path
from datetime import datetime

# Third-party imports
import httpx

# Local imports
from typing import Optional
from zebra_cli.context import AppContext

class ApiSubmenu:
  
    def __init__(self, app_context: Optional[AppContext] = None) -> None:
        self.app_context = app_context
        # API credentials storage
        if app_context:
            self.api_reader_ip = app_context.ip_address
            self.api_username = app_context.username
            self.api_password = app_context.password
            self.api_jwt_token = app_context.token
            self.api_protocol = app_context.protocol
        else:
            raise ValueError("ApiSubmenu initialization failed, App Context cannot be None")
  
    def handle_api_submenu(self) -> None:
        """
        Main entry point for the API requests submenu.
        
        This method:
        1. Prompts for credentials if not already stored
        2. Performs automatic login and model detection
        3. Shows the interactive API menu
        4. Handles all API command processing
        5. Cleans up credentials on exit
        """
        print("\n🔧 API REQUESTS SETUP")
        print("-" * 25)
        if self.app_context:
            self.api_reader_ip = self.app_context.ip_address
            self.api_username = self.app_context.username
            self.api_password = self.app_context.password
            self.api_jwt_token = self.app_context.token
            self.api_protocol = self.app_context.protocol
        else:
            raise ValueError("ApiSubmenu initialization failed, App Context cannot be None")

        # Check if credentials are already stored
        if not self.api_reader_ip or not self.api_username or not self.api_password:
            print("📝 First time setup - Enter reader credentials for API requests:")
            print()
            
            try:
                ip = input("📍 Reader IP: ").strip()
                if not ip:
                    print("❌ IP required")
                    input("\n⏸️  Press ENTER to continue...")
                    return
                
                username = input("👤 Username [admin]: ").strip() or "admin"
                
                # Obfuscated password input
                password = getpass.getpass("🔑 Password [admin]: ") or "admin"
                
                # Store credentials
                self.api_reader_ip = ip
                self.api_username = username
                self.api_password = password
                
                print("✅ Credentials saved for API requests")
                print()
                
            except Exception as e:
                print(f"❌ Error setting up credentials: {e}")
                input("\n⏸️  Press ENTER to continue...")
                return
        
        # Automatic initialization when entering API menu
        initialization_success = self._auto_initialize_api()
        
        # If initialization failed, clear credentials and return to main menu
        if not initialization_success:
            print("\n❌ Auto-login failed: Please check IP address, username, and password")
            print("🧹 Clearing stored credentials...")
            
            # Clear all API credentials
            self.api_reader_ip = None
            self.api_username = None
            self.api_password = None
            self.api_jwt_token = None
            self.api_token_timestamp = None
            self.api_reader_model = None
            
            input("\n⏸️  Press ENTER to return to main menu...")
            return
        
        # Show API requests submenu only if initialization was successful
        self._show_api_submenu()
    
    def _auto_initialize_api(self) -> bool:
        """Automatically performs login and model detection when entering API menu"""
        print("\n🔄 AUTOMATIC API INITIALIZATION")
        print("-" * 37)
        print("🤖 Performing automatic setup...")
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"👤 User: {self.api_username}")
        print()
        
        # Step 1: Automatic login
        login_success = self._auto_login()
        
        # Step 2: Automatic model detection (only if login successful)
        if login_success:
            self._get_reader_info()
        else:
            print("⚠️  Skipping model detection due to login failure")
        
        print("\n✅ Initialization completed - Results:")
        print(f"   🔐 Login: {'✅ Success' if login_success else '❌ Failed'}")
        print(f"   🏷️  Model: {getattr(self, 'api_reader_model', 'Not detected')}")
        print(f"   🔑 Token: {'✅ Available' if hasattr(self, 'api_jwt_token') and self.api_jwt_token else '❌ None'}")
        
        if login_success:
            input("\n⏸️  Press ENTER to continue to API menu...")  # Wait for user to see results
        
        return login_success  # Return the success status
    
    def _auto_login(self) -> bool:
        """Silently attempts to obtain JWT token automatically"""
        print("🔐 Attempting automatic login...")
        
        try:
            # Try both HTTPS and HTTP protocols
            protocol = self.api_protocol
 
            try:
                if protocol in ['http', 'https']:
                    print(f"   🔍 Trying {protocol.upper()} protocol...")
                else:
                    print(f"   🔍 Trying UNKNOWN protocol...")
                
                try:

                    token = self.api_jwt_token

                    if token:
                        # Store token and timestamp
                        self.api_jwt_token = token
                        self.api_token_timestamp = time.time()
                        if self.app_context and self.app_context.debug:
                            if protocol in ['http', 'https']:
                                print(f"   ✅ Token obtained via {protocol.upper()}")
                            else:
                                print(f"   ✅ Token obtained via UNKNOWN protocol")
                            print(f"   🔑 Token length: {len(token)} characters")
                        return True
                    else:
                        print(f"   ⚠️  No token found in any expected field")
                        return False                  
                except Exception as e:
                    print(f"   ❌ JSON parsing error: {e}")
                    return False            
            except Exception as e:
                # If we reach here, all attempts failed
                print("   ❌ Auto-login failed - manual login may be required")
                print("   💡 Use 'l / login' command for detailed error information")
                return False
            
        except Exception as e:
            print(f"   ❌ Auto-login error: {e}")
            return False
    
    def _get_reader_info(self) -> None:
        """Silently detects and stores reader model information"""
        print("🏷️  Detecting reader model...")
        
        try:
            # Try to get model information from version endpoint (silent)
            headers = {
                "Authorization": f"Bearer {self.api_jwt_token}",
                "Accept": "application/json"
            }
            
            protocol = self.api_protocol
            
            
            try:
                if self.app_context and self.app_context.debug:
                    if protocol in ['http', 'https']:
                        print(f"   🔍 Trying {protocol.upper()} for version endpoint...")
                    else:
                        print(f"   🔍 Trying UNKNOWN protocol for version endpoint...")
                
                response = httpx.get(
                    f"{protocol}://{self.api_reader_ip}/cloud/version",
                    headers=headers,
                    verify=False,
                    timeout=10.0
                )

                if self.app_context and self.app_context.debug:
                    print(f"   📡 Version response status: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    if self.app_context and self.app_context.debug:
                        print(f"   📄 Version response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Not a dict'}")
                    
                    if isinstance(response_data, dict) and 'model' in response_data:
                        model = str(response_data['model']).strip()
                        self.api_reader_model = model
                        if self.app_context and self.app_context.debug:
                            print(f"   ✅ Reader model: {model}")
                        return
                    else:
                        print(f"   ⚠️  No 'model' field in version response")
                else:
                    print(f"   ❌ Version HTTP {response.status_code}: {response.text[:100]}...")
                        
            except Exception as e:
                if protocol in ['http', 'https']:
                    print(f"   ❌ {protocol.upper()} version error: {e}")
                else:
                    print(f"   ❌ UNKNOWN protocol version error: {e}")
        
        except Exception as e:
            self.api_reader_model = "UNKNOWN"
            print(f"   ⚠️  Model detection error: {e}")
        
    def _reset_api_credentials(self) -> None:
        """Resets all API session credentials and data"""
        self.api_reader_ip = None
        self.api_username = None
        self.api_password = None
        self.api_jwt_token = None
        self.api_token_timestamp = None
        self.api_reader_model = None
        print("✅ API session reset - credentials cleared")
    
    def _show_api_submenu(self) -> None:
        """Shows the API requests submenu with persistent loop"""
        # Define wcwidth function with fallback
        try:
            from wcwidth import wcwidth as _wcwidth
        except ImportError:
            _wcwidth = None
        
        def wcwidth(c):
            if _wcwidth is not None:
                try:
                    width = _wcwidth(c)
                    # Handle None, -1, 0 by defaulting to 1
                    if width is None or width < 1:
                        return 1
                    # Cap all widths to maximum of 2 to prevent table breakage
                    elif width > 2:
                        return 2
                    else:
                        return width
                except (TypeError, ValueError):
                    # Handle composite characters by treating them as width 2
                    return 2
            else:
                # Fallback: Simple approach - all non-ASCII is width 2
                try:
                    char_ord = ord(c)
                    if char_ord > 127:
                        return 2
                    else:
                        return 1
                except (TypeError, ValueError):
                    # Handle composite characters
                    return 2
        
        left_width = 50  # Width for command column (increased to accommodate longer commands)
        right_width = 43  # Width for arguments column (50 + 43 = 93 total content width)
        
        def visual_len(text):
            return sum(wcwidth(c) for c in text)
        def row(text):
            # Match the inner content width of two-column rows
            content_width = left_width + right_width + 3
            pad = content_width - visual_len(text)
            return f"│ {text}{' ' * pad} │"
        def two_col_row(left_text, right_text):
            """Create a two-column row with left and right text"""
            left_pad = left_width - visual_len(left_text)
            right_pad = right_width - visual_len(right_text)
            return f"│ {left_text}{' ' * left_pad} │ {right_text}{' ' * right_pad} │"
        def separator_row():
            """Create separator row between columns"""
            return f"├{('─' * (left_width + 2))}┼{('─' * (right_width + 2))}┤"
        
        api_command_map = {
            'gl': self.handle_api_login, 'getlogin': self.handle_api_login,
            'gs': self.handle_api_status, 'getstatus': self.handle_api_status,
            'gv': self.handle_api_version, 'getversion': self.handle_api_version,
            'gn': self.handle_api_network, 'getnetwork': self.handle_api_network,
            'gr': self.handle_api_region, 'getregion': self.handle_api_region,
            'gm': self.handle_api_mode, 'getmode': self.handle_api_mode,
            'gc': self.handle_api_config, 'getconfig': self.handle_api_config,
            'gi': self.handle_api_gpi, 'getgpi': self.handle_api_gpi,
            'go': self.handle_api_gpo, 'getgpo': self.handle_api_gpo,
            'gp': self.handle_api_caps, 'getcaps': self.handle_api_caps,
            'gz': self.handle_api_timezone, 'gettimezone': self.handle_api_timezone,
            'gx': self.handle_api_cableloss, 'getcableloss': self.handle_api_cableloss,
            'ge': self.handle_api_certs, 'getcerts': self.handle_api_certs,
            'gw': self.handle_api_logs, 'getlogs': self.handle_api_logs,
            'gy': self.handle_api_syslog, 'getsyslog': self.handle_api_syslog,
            # PUT commands
            'sc': self.handle_api_set_config, 'setconfig': self.handle_api_set_config,
            'sm': self.handle_api_set_mode, 'setmode': self.handle_api_set_mode,
            'sn': self.handle_api_set_network, 'setnetwork': self.handle_api_set_network,
            'sr': self.handle_api_set_region, 'setregion': self.handle_api_set_region,
            'so': self.handle_api_set_gpo, 'setgpo': self.handle_api_set_gpo,
            'st': self.handle_api_set_timezone, 'settimezone': self.handle_api_set_timezone,
            'sl': self.handle_api_set_logs, 'setlogs': self.handle_api_set_logs,
            'rb': self.handle_api_reboot, 'reboot': self.handle_api_reboot,
            # Utilities
            'c': self.clear_screen,
            'h': self.show_help, 'help': self.show_help,
            'back': None, 'b': None
        }
        
        try:
            while True:
                try:
                    self.clear_screen()
                    print("🔧" + "=" * 58)
                    print("   ZEBRA RFID API REQUESTS - Interactive Mode")
                    print("=" * 60)
                    print(f"📍 Reader IP: {self.api_reader_ip}")
                    print(f"👤 Username: {self.api_username}")
                    print(f"🔑 Password: {'*' * len(self.api_password or '')}")
                    print("-" * 60)
                    
                    print("\n🔧 API Requests Menu:")
                    print("┌" + "─" * (left_width + right_width + 5) + "┐")
                    print(row(f"📍 Target Reader: {self.api_reader_ip}"))
                    
                    # Display reader model if available
                    if hasattr(self, 'api_reader_model') and self.api_reader_model:
                        print(row(f"📋 Reader Model: {self.api_reader_model}"))
                    
                    if hasattr(self, 'api_token_timestamp') and self.api_token_timestamp:
                        from datetime import datetime
                        timestamp_str = datetime.fromtimestamp(self.api_token_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        print(row(f"⏰ Token obtained: {timestamp_str}"))
                    print("├" + "─" * (left_width + right_width + 5) + "┤")
                    
                    # GET ENDPOINTS section with two columns
                    print(two_col_row("GET ENDPOINTS:", "💾 SAVE RESPONSE OPTIONS:"))
                    print(separator_row())
                    print(two_col_row("gl / getLogin    🔐 Get JWT token", "(none)"))
                    print(two_col_row("gs / getStatus   📊 Get reader status", "[-y] [-n](default)"))
                    print(two_col_row("gv / getVersion  📋 Get reader version", "[-y] [-n](default)"))
                    print(two_col_row("gn / getNetwork  🌐 Get network config", "[-y] [-n](default)"))
                    print(two_col_row("gr / getRegion   🌍 Get region config", "[-y] [-n](default)"))
                    print(two_col_row("gm / getMode     📋 Get operating mode", "[-y] [-n](default)"))
                    print(two_col_row("gc / getConfig   🔧 Get reader config", "[-y] [-n](default)"))
                    print(two_col_row("gi / getGpi      📥 Get GPI status", "[-y] [-n](default)"))
                    print(two_col_row("go / getGpo      📤 Get GPO status", "[-y] [-n](default)"))
                    print(two_col_row("gp / getCaps     🎯 Get reader capabilities", "[-y] [-n](default)"))
                    print(two_col_row("gz / getTimezone ⏰ Get timezone config", "[-y] [-n](default)"))
                    print(two_col_row("gx / getCableLoss📡 Get cable loss compensation", "[-y] [-n](default)"))
                    print(two_col_row("ge / getCerts    🔒 Get certificates", "[-y] [-n](default)"))
                    print(two_col_row("gw / getLogs     📄 Get logs configuration", "[-y] [-n](default)"))
                    print(two_col_row("gy / getSyslog   📋 Get system log", "[-y] [-n](default)"))
                    
                    print(separator_row())
                    # PUT ENDPOINTS - File-based section
                    print(two_col_row("PUT ENDPOINTS (File-based):", "📁 SAVE RESPONSE FILE PATH OPTIONS:"))
                    print(separator_row())
                    print(two_col_row("sn / setNetwork  🌐 Update network config", "-p <file> OR --path <file>"))
                    print(two_col_row("sr / setRegion   🌍 Update region info", "-p <file> OR --path <file>"))
                    print(two_col_row("sm / setMode     📋 Update operating mode", "-p <file> OR --path <file>"))
                    print(two_col_row("sc / setConfig   🔧 Update reader config", "-p <file> OR --path <file>"))
                    print(two_col_row("so / setGpo      📤 Update GPO port state", "-p <file> OR --path <file>"))
                    print(two_col_row("st / setTimezone ⏰ Set time zone", "-p <file> OR --path <file>"))
                    print(two_col_row("sl / setLogs     📄 Set logs config", "-p <file> OR --path <file>"))
                    
                    print(separator_row())
                    # PUT ENDPOINTS - Special commands section
                    print(two_col_row("PUT ENDPOINTS (Special):", "🔧 COMMAND FLAGS:"))
                    print(separator_row())
                    print(two_col_row("sp / setPassword 🔑 Change reader password", "-u/-c/-n OR --username/--current/--new"))
                    print(two_col_row("rb / reboot      🔄 Reboot reader", "(none)"))
                    
                    print(separator_row())
                    # UTILITIES section with two columns
                    print(two_col_row("UTILITIES:", "🔧 ACTIONS:"))
                    print(separator_row())
                    print(two_col_row("c / clear       🧹 Clear screen", "(none)"))
                    print(two_col_row("h / help        ❓ Show API submenu help", "(none)"))
                    print(two_col_row("b / back        📋 Back to main menu", "(none)"))
                    print("└" + "─" * (left_width + right_width + 5) + "┘")
                    
                    choice = input("\n🎯 API command or shortcut: ").strip()
                    
                    if choice.lower() in ('b', 'back'):
                        break
                    elif choice.lower() in ('c', 'clear'):
                        continue  # Clear screen by continuing the loop
                    else:
                        # Parse command and arguments
                        parts = choice.split()
                        cmd = parts[0].lower() if parts else ''
                        arg = parts[1] if len(parts) > 1 else None

                        # Help command (h/help) triggers help output
                        if cmd in ('h', 'help'):
                            self.show_help()
                            continue

                        # Define GET commands that support argument-based saving
                        get_commands_with_saving = [
                            'gs', 'getstatus', 'gv', 'getversion', 'gn', 'getnetwork', 'gr', 'getregion',
                            'gm', 'getmode', 'gc', 'getconfig', 'gi', 'getgpi', 'go', 'getgpo', 'gp', 'getcaps',
                            'gz', 'gettimezone', 'gx', 'getcableloss', 'ge', 'getcerts', 'gw', 'getlogs', 'gy', 'getsyslog'
                        ]

                        if cmd in get_commands_with_saving:
                            # Validate argument for GET commands that support saving
                            valid_args = [None, '-y', '--yes', '-n', '--no']
                            if arg not in valid_args:
                                print(f"\n❌ Invalid argument '{arg}' for command '{cmd}'")
                                print("💡 Valid arguments: -y/--yes (save), -n/--no (don't save), or no argument (don't save)")
                                input("⏸️  Press ENTER to continue...")
                                continue

                            # Determine save behavior
                            save_response = arg in ['-y', '--yes']

                            # Execute GET command with save parameter
                            handler_map = {
                                'gs': self.handle_api_status, 'getstatus': self.handle_api_status,
                                'gv': self.handle_api_version, 'getversion': self.handle_api_version,
                                'gn': self.handle_api_network, 'getnetwork': self.handle_api_network,
                                'gr': self.handle_api_region, 'getregion': self.handle_api_region,
                                'gm': self.handle_api_mode, 'getmode': self.handle_api_mode,
                                'gc': self.handle_api_config, 'getconfig': self.handle_api_config,
                                'gi': self.handle_api_gpi, 'getgpi': self.handle_api_gpi,
                                'go': self.handle_api_gpo, 'getgpo': self.handle_api_gpo,
                                'gp': self.handle_api_caps, 'getcaps': self.handle_api_caps,
                                'gz': self.handle_api_timezone, 'gettimezone': self.handle_api_timezone,
                                'gx': self.handle_api_cableloss, 'getcableloss': self.handle_api_cableloss,
                                'ge': self.handle_api_certs, 'getcerts': self.handle_api_certs,
                                'gw': self.handle_api_logs, 'getlogs': self.handle_api_logs,
                                'gy': self.handle_api_syslog, 'getsyslog': self.handle_api_syslog
                            }
                            
                            handler = handler_map.get(cmd)
                            if handler:
                                handler(save_response)
                            else:
                                print(f"\n❌ Invalid command '{cmd}'")
                                input("⏸️  Press ENTER to continue...")
                        
                        elif cmd in ('gl', 'getlogin'):
                            # getLogin never saves, no argument validation needed
                            if arg is not None:
                                print(f"\n❌ Command '{cmd}' does not accept arguments")
                                input("⏸️  Press ENTER to continue...")
                                continue
                            self.handle_api_login()
                        
                        elif cmd in ('sp', 'setpassword'):
                            # setPassword requires three specific flags: -u/-c/-n or --username/--current/--new
                            # Check if there's a simple argument (not starting with -) instead of flags
                            if arg is not None and not arg.startswith('-'):
                                print(f"\n❌ Command '{cmd}' does not accept simple arguments")
                                print("💡 Usage: sp -u <username> -c <current_password> -n <new_password>")
                                print("💡 Or: setpassword --username <username> --current <current_password> --new <new_password>")
                                input("⏸️  Press ENTER to continue...")
                                continue
                            
                            # Parse flags from the full command line
                            full_command = choice.strip()
                            parts = full_command.split()
                            if len(parts) < 7:  # cmd + 6 flag+value pairs minimum
                                print(f"\n❌ Missing required flags for '{cmd}'")
                                print("💡 Usage: sp -u <username> -c <current_password> -n <new_password>")
                                print("💡 Or: setpassword --username <username> --current <current_password> --new <new_password>")
                                input("⏸️  Press ENTER to continue...")
                                continue
                            
                            # Parse flags with argument validation
                            parsed_args = self._parse_setpassword_flags(parts[1:])  # Skip command name
                            if parsed_args is None:
                                continue  # Error already shown in parse function
                            
                            # Execute setPassword with parsed arguments
                            self.handle_api_set_password(
                                username=parsed_args['username'],
                                current_password=parsed_args['current_password'],
                                new_password=parsed_args['new_password']
                            )
                        
                        else:
                            # Define PUT commands that support -p/--path flags
                            put_commands_with_path = [
                                'sn', 'setnetwork', 'sr', 'setregion', 'sm', 'setmode', 
                                'sc', 'setconfig', 'so', 'setgpo', 'st', 'settimezone', 
                                'sl', 'setlogs'  
                            ]
                            
                            # Define commands that don't accept any arguments
                            no_arg_commands = ['rb', 'reboot']
                            
                            if cmd in put_commands_with_path:
                                # Parse PUT command arguments for -p/--path flag
                                full_command = choice.strip()
                                parts = full_command.split()
                                args = parts[1:] if len(parts) > 1 else []
                                
                                # Execute PUT command with arguments
                                handler_map = {
                                    'sn': self.handle_api_set_network, 'setnetwork': self.handle_api_set_network,
                                    'sr': self.handle_api_set_region, 'setregion': self.handle_api_set_region,
                                    'sm': self.handle_api_set_mode, 'setmode': self.handle_api_set_mode,
                                    'sc': self.handle_api_set_config, 'setconfig': self.handle_api_set_config,
                                    'so': self.handle_api_set_gpo, 'setgpo': self.handle_api_set_gpo,
                                    'st': self.handle_api_set_timezone, 'settimezone': self.handle_api_set_timezone,
                                    'sl': self.handle_api_set_logs, 'setlogs': self.handle_api_set_logs
                                }
                                
                                handler = handler_map.get(cmd)
                                if handler:
                                    handler(args)
                                else:
                                    print(f"\n❌ Invalid command '{cmd}'")
                                    input("⏸️  Press ENTER to continue...")
                            
                            elif cmd in no_arg_commands:
                                # Handle commands that don't accept arguments
                                action = api_command_map.get(cmd)
                                if action:
                                    if arg is not None:
                                        print(f"\n❌ Command '{cmd}' does not accept arguments")
                                        input("⏸️  Press ENTER to continue...")
                                        continue
                                    action()
                                else:
                                    print(f"\n❌ Invalid command '{cmd}'")
                                    input("⏸️  Press ENTER to continue...")
                            
                            else:
                                # Handle other utility commands
                                action = api_command_map.get(cmd)
                                if action:
                                    if arg is not None:
                                        print(f"\n❌ Command '{cmd}' does not accept arguments")
                                        input("⏸️  Press ENTER to continue...")
                                        continue
                                    action()
                                else:
                                    print(f"\n❌ Invalid command '{cmd}'")
                                    print("💡 GET commands: gl, gs, gv, gn, gr, gm, gc, gi, go, gp, gz, gx, ge, gw, gy")
                                    print("💡 PUT commands: sn, sr, sm, sc, so, st, sl, rb")
                                    print("💡 PUT with -p flag: sn -p <file>, sr -p <file>, etc.")
                                    print("💡 Special: sp (requires flags: -u -c -n or --username --current --new)")
                                    print("💡 Utilities: c, t, b")
                                    input("⏸️  Press ENTER to continue...")
                        
                except KeyboardInterrupt:
                    print("\n\n👋 Returning to main menu")
                    break
                except Exception as e:
                    print(f"\n❌ Unexpected error: {e}")
                    input("⏸️  Press ENTER to continue...")
                    break
        finally:
            # Always reset credentials when exiting API menu (any exit method)
            self._reset_api_credentials()

    def _check_jwt_token(self) -> bool:
        """Checks if a valid JWT token is available for API requests"""
        if not hasattr(self, 'api_jwt_token') or not self.api_jwt_token:
            print("\n⚠️  JWT TOKEN REQUIRED")
            print("-" * 25)
            print("❌ No JWT token available for API requests")
            print("💡 Use 'l / login' command first to obtain a JWT token")
            input("\n⏸️  Press ENTER to continue...")
            return False
        
        # Optional: Check if token is not expired (basic validation)
        try:
            # JWT tokens have 3 parts separated by dots
            if self.api_jwt_token.count('.') != 2:
                print("\n⚠️  INVALID JWT TOKEN FORMAT")
                print("-" * 30)
                print("❌ Stored token doesn't appear to be a valid JWT")
                print("💡 Use 'l / login' command to obtain a new token")
                input("\n⏸️  Press ENTER to continue...")
                return False
        except Exception:
            print("\n⚠️  TOKEN VALIDATION ERROR")
            print("-" * 27)
            print("❌ Error validating stored token")
            print("💡 Use 'l / login' command to obtain a new token")
            input("\n⏸️  Press ENTER to continue...")
            return False
        
        return True
    
    def _get_api_headers(self) -> dict:
        """Returns headers with JWT Bearer token for API requests"""
        if not self._check_jwt_token():
            return {}
        
        return {
            "Authorization": f"Bearer {self.api_jwt_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _handle_auth_error(self) -> bool:
        """Handle authorization errors and display user guidance. Returns True if error occurred."""
        print("\n🚨 AUTHORIZATION ERROR")
        print("=" * 25)
        print("❌ Request unauthorized - JWT token may be expired or invalid")
        print("⚠️  Please refresh your authentication!")
        print("💡 Use 'l / login' command to obtain a fresh JWT token")
        print("🔄 Then try this command again")
        print("=" * 25)
        input("\n⏸️  Press ENTER to continue...")
        return True

    def _make_silent_api_request(self, endpoint: str, method: str = "GET", data: Optional[dict] = None, params: Optional[dict] = None) -> tuple:
        """
        Makes an authenticated API request to the Zebra reader without user interaction
        
        Args:
            endpoint: API endpoint (e.g., "/cloud/status")
            method: HTTP method (GET, POST, PUT, DELETE)
            data: JSON data for POST/PUT requests
            params: Query parameters
            
        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        # Silent token check - no user interaction
        if not hasattr(self, 'api_jwt_token') or not self.api_jwt_token:
            return False, {"error": "No JWT token available"}, 0
        
        try:

            protocol = self.api_protocol

            headers = {
                "Authorization": f"Bearer {self.api_jwt_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            url = f"{protocol}://{self.api_reader_ip}{endpoint}"
            
            # Make the request based on method
            if method.upper() == "GET":
                response = httpx.get(url, headers=headers, params=params, verify=False, timeout=10.0)
            elif method.upper() == "POST":
                response = httpx.post(url, headers=headers, json=data, params=params, verify=False, timeout=10.0)
            elif method.upper() == "PUT":
                response = httpx.put(url, headers=headers, json=data, params=params, verify=False, timeout=10.0)
            elif method.upper() == "DELETE":
                response = httpx.delete(url, headers=headers, params=params, verify=False, timeout=10.0)
            else:
                return False, {"error": f"Unsupported method: {method}"}, 0
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except:
                response_data = {"message": response.text}
            
            # Check if the request was successful (2xx status codes)
            success = 200 <= response.status_code < 300
            return success, response_data, response.status_code
            
        except Exception as e:
            return False, {"error": f"Request error: {e}"}, 0

    def _make_api_request(self, endpoint: str, method: str = "GET", data: Optional[dict] = None, params: Optional[dict] = None) -> tuple:
        """
        Makes an authenticated API request to the Zebra reader
        
        Args:
            endpoint: API endpoint (e.g., "/cloud/status")
            method: HTTP method (GET, POST, PUT, DELETE)
            data: JSON data for POST/PUT requests
            params: Query parameters
            
        Returns:
            tuple: (success: bool, response_data: dict, status_code: int)
        """
        if not self._check_jwt_token():
            return False, {"error": "No JWT token available"}, 0
        
        try:

            protocol = self.api_protocol

            headers = self._get_api_headers()

            url = f"{protocol}://{self.api_reader_ip}{endpoint}"
            
            # Make the request based on method
            if method.upper() == "GET":
                response = httpx.get(url, headers=headers, params=params, verify=False, timeout=10.0)
            elif method.upper() == "POST":
                response = httpx.post(url, headers=headers, json=data, params=params, verify=False, timeout=10.0)
            elif method.upper() == "PUT":
                response = httpx.put(url, headers=headers, json=data, params=params, verify=False, timeout=10.0)
            elif method.upper() == "DELETE":
                response = httpx.delete(url, headers=headers, params=params, verify=False, timeout=10.0)
            else:
                return False, {"error": f"Unsupported method: {method}"}, 0
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except:
                response_data = {"message": response.text}
            
            # Check if the request was successful (2xx status codes)
            success = 200 <= response.status_code < 300
            return success, response_data, response.status_code
        
        except Exception as e:
            return False, {"error": f"Request error: {e}"}, 0
    
    def _get_reader_model(self) -> str:
        """Gets reader model for file organization (uses cached value if available)"""
        try:
            # Use cached model if available from automatic initialization
            if hasattr(self, 'api_reader_model') and self.api_reader_model and self.api_reader_model != "UNKNOWN":
                # Clean model name for safe filename usage
                model = str(self.api_reader_model).replace(' ', '_').replace('/', '_').replace('\\', '_')
                return model
            
            # Fallback: Try to get model from version endpoint (without showing output)
            # Check token silently without user interaction
            if not hasattr(self, 'api_jwt_token') or not self.api_jwt_token:
                return "UNKNOWN"
            
            success, data, status_code = self._make_silent_api_request("/cloud/version", "GET")
            
            if success and isinstance(data, dict) and 'model' in data:
                model = str(data['model']).strip()
                # Clean model name for safe filename usage and cache it
                model = model.replace(' ', '_').replace('/', '_').replace('\\', '_')
                self.api_reader_model = model  # Cache for future use
                return model
            
            # Fallback if version endpoint fails or model not found
            return "UNKNOWN"
            
        except Exception as e:
            # Return UNKNOWN if any error occurs during model detection
            return "UNKNOWN"
    
    def _discover_json_files(self, command: str) -> list[str]:
        """Discovers available JSON files for a PUT command"""
        try:
            folder_path = Path(f"requests-json/{command}")
            if not folder_path.exists():
                return []
            
            json_files = []
            for file_path in folder_path.glob("*.json"):
                if file_path.is_file():
                    # Validate that it's actually a JSON file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            json.load(f)  # Try to parse JSON
                        json_files.append(file_path.name)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        # Skip invalid JSON files
                        continue
            
            return sorted(json_files)
        except Exception:
            return []
    
    def _select_json_file(self, command: str) -> Optional[dict]:
        """Interactive JSON file selection with preview option"""
        try:
            # Check if folder exists
            folder_path = Path(f"requests-json/{command}")
            if not folder_path.exists():
                print(f"\n❌ FOLDER NOT FOUND")
                print(f"📂 Expected folder: requests-json/{command}/")
                print("🛠️  Please create the folder structure:")
                print(f"   1. Create folder: requests-json/{command}/")
                print(f"   2. Add JSON files to the folder")
                print(f"   3. Try the command again")
                return None
            
            # Discover JSON files
            json_files = self._discover_json_files(command)
            
            if not json_files:
                print(f"\n❌ NO JSON FILES FOUND")
                print(f"📂 Folder exists but no valid JSON files found: requests-json/{command}/")
                print("🛠️  Please add valid JSON files to the folder and try again")
                return None
            
            # Show file selection menu
            print(f"\n📋 AVAILABLE JSON FILES FOR {command.upper()}:")
            print("-" * 50)
            for i, filename in enumerate(json_files, 1):
                print(f"  {i}. {filename}")
            print(f"  0. ❌ Abort operation")
            
            # Get user selection
            while True:
                try:
                    choice = input(f"\n🔢 Select JSON file (1-{len(json_files)}, 0 to abort): ").strip()
                    if not choice.isdigit():
                        print("❌ Invalid input. Please enter a number.")
                        continue
                    if choice == '0':
                        print("❌ Operation aborted by user")
                        return None
                    file_index = int(choice) - 1
                    if 0 <= file_index < len(json_files):
                        selected_file = json_files[file_index]
                        break
                    else:
                        print(f"❌ Invalid selection. Please enter a number between 1 and {len(json_files)}, or 0 to abort")
                except KeyboardInterrupt:
                    print("\n❌ Selection cancelled")
                    return None
            
            # Load and validate selected JSON file
            file_path = folder_path / selected_file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"\n❌ MALFORMED JSON FILE")
                print(f"📁 File: {selected_file}")
                print(f"🚫 Error: {e}")
                print("🛠️  Please fix the JSON syntax and try again")
                return None
            except Exception as e:
                print(f"\n❌ ERROR READING FILE")
                print(f"📁 File: {selected_file}")
                print(f"🚫 Error: {e}")
                return None
            
            # Ask for preview
            preview_choice = input(f"\n🔍 Do you want to preview the JSON content before sending? (y/N): ").strip().lower()
            
            if preview_choice == 'y':
                print(f"\n📄 JSON CONTENT PREVIEW - {selected_file}:")
                print("=" * 60)
                formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                print(formatted_json)
                print("=" * 60)
                input("\n⏸️  Press ENTER to proceed with sending the request...")
            
            print(f"✅ Selected: {selected_file}")
            return json_data
            
        except Exception as e:
            print(f"\n❌ Unexpected error during file selection: {e}")
            return None

    def _handle_put_request(self, endpoint: str, command: str, description: str, json_data: Optional[dict] = None, file_path: Optional[str] = None) -> None:
        """Generic handler for PUT requests with JSON body selection or direct data"""
        print(f"\n⚙️  {description}")
        print("-" * 50)
        print(f"🌐 Endpoint: PUT {endpoint}")
        
        # Check token
        if not self._check_jwt_token():
            return
        
        # Use provided JSON data or select from file
        if json_data is not None:
            print(f"📁 JSON Source: {file_path}")
            print(f"📏 JSON Size: {len(str(json_data))} characters")
            print()
        else:
            print(f"📂 JSON Source: requests-json/{command}/")
            print()
            # Select JSON file interactively
            json_data = self._select_json_file(command)
            if json_data is None:
                input("\n⏸️  Press ENTER to continue...")
                return
        
        # Make PUT request
        try:
            print(f"\n🚀 Sending PUT request to {endpoint}...")
            success, response_data, status_code = self._make_api_request(endpoint, "PUT", data=json_data)
            
            if success:
                print(f"✅ Request successful! (Status: {status_code})")
                self._show_api_response(success, response_data, status_code, endpoint, f"PUT {command}")
            else:
                print(f"❌ Request failed!")
                print(f"📊 Status Code: {status_code}")
                print(f"🚫 Response: {response_data}")
                
        except Exception as e:
            print(f"❌ Request error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def _show_api_response(self, success: bool, data: dict, status_code: int, endpoint: str, command_name: Optional[str] = None, save_response: bool = False) -> None:
        """Shows formatted API response to user and optionally saves to file"""
        print(f"\n📡 API RESPONSE - {endpoint}")
        print("=" * 50)
        
        if success:
            print(f"✅ Status: {status_code}")
            print(f"📄 Response Data:")
            print("-" * 30)
            
            # Format JSON response nicely
            try:
                formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
                print(formatted_json)
            except:
                print(str(data))
        else:
            print(f"❌ Request Failed - Status: {status_code}")
            print(f"📄 Error Details:")
            print("-" * 30)
            print(str(data))
        
        print("=" * 50)
        
        # Save response to file if requested (skip for login)
        if command_name and command_name != 'login' and save_response:
            self._save_response_to_file(success, data, status_code, endpoint, command_name)
    
    def _save_response_to_file(self, success: bool, data: dict, status_code: int, endpoint: str, command_name: str) -> None:
        """Saves API response to a JSON file without user interaction"""
        try:
            print(f"\n💾 SAVING {command_name.upper()} RESPONSE")
            print("-" * (13 + len(command_name)))
            
            # Get reader model for directory and filename organization
            print("🔍 Detecting reader model...")
            reader_model = self._get_reader_model()
            
            # Create timestamp for filename (format: YYYYMMDD-HHMMSS)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            # Create reader-specific filename: command-MODEL-timestamp.json
            filename = f"{command_name}-{reader_model}-{timestamp}.json"
            
            # Create reader-specific directory: api-responses/IP_MODEL/command/
            import os
            reader_id = f"{self.api_reader_ip}_{reader_model}"
            response_dir = os.path.join(os.getcwd(), "api-responses", reader_id, command_name)
            os.makedirs(response_dir, exist_ok=True)
            
            # Full file path
            file_path = os.path.join(response_dir, filename)
            
            print(f"📡 Reader: {reader_model}")
            print(f"📁 Saving to: {file_path}")
            print("🔄 Preparing JSON data...")
            
            # Save only the actual response data (without metadata wrapper)
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Get file size for confirmation
            file_size = os.path.getsize(file_path)
            file_size_kb = file_size / 1024
            
            print("✅ SUCCESS!")
            print("=" * 50)
            print(f"📄 File saved: {filename}")
            print(f"📁 Location: {file_path}")
            print(f"📡 Reader: {self.api_reader_ip} ({reader_model})")
            print(f"📏 Size: {file_size_kb:.2f} KB ({file_size} bytes)")
            print(f"📦 Format: Clean JSON response data")
            print("=" * 50)
            print("💡 File contains:")
            print("   • Raw API response data only")
            print("   • No metadata or wrapper information")
            print("   • Ready for direct data processing")
            print("   • Organized by reader IP and model")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            print("🔍 Check if you have write permissions in the project directory")

    def _parse_put_command_flags(self, args) -> Optional[dict]:
        """
        Parses PUT command flags for -p/--path argument.
        
        Args:
            args: List of arguments after the command name
            
        Returns:
            dict with 'file_path' key if successful, None if error
        """
        import os
        import json
        from pathlib import Path
        
        if not args:
            return {}  # No arguments, use interactive mode
        
        # Check for -p or --path flag
        if len(args) >= 2 and args[0] in ['-p', '--path']:
            file_path = args[1]
            
            # Convert to absolute path if relative
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            
            # Validate file exists
            if not os.path.exists(file_path):
                print(f"\n❌ FILE NOT FOUND")
                print(f"📁 Specified file does not exist: {file_path}")
                input("⏸️  Press ENTER to continue...")
                return None
            
            # Validate it's a file (not directory)
            if not os.path.isfile(file_path):
                print(f"\n❌ INVALID FILE")
                print(f"📁 Path exists but is not a file: {file_path}")
                input("⏸️  Press ENTER to continue...")
                return None
            
            # Validate JSON content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                print(f"✅ JSON file validated: {file_path}")
                return {'file_path': file_path, 'json_data': json_data}
            except json.JSONDecodeError as e:
                print(f"\n❌ INVALID JSON")
                print(f"📁 File: {file_path}")
                print(f"🚫 JSON Error: {e}")
                input("⏸️  Press ENTER to continue...")
                return None
            except Exception as e:
                print(f"\n❌ FILE READ ERROR")
                print(f"📁 File: {file_path}")
                print(f"🚫 Error: {e}")
                input("⏸️  Press ENTER to continue...")
                return None
        else:
            # Invalid arguments
            print(f"\n❌ INVALID ARGUMENTS")
            print("💡 Valid usage: -p <file_path> or --path <file_path>")
            print("💡 Or use command without arguments for interactive mode")
            input("⏸️  Press ENTER to continue...")
            return None

    def _parse_setpassword_flags(self, args) -> Optional[dict]:
        """
        Parses setPassword command flags and validates them.
        
        Args:
            args: List of arguments after the command name
            
        Returns:
            dict with username, current_password, new_password keys or None if invalid
        """
        # Initialize result dictionary
        result = {
            'username': None,
            'current_password': None,
            'new_password': None
        }
        
        # Check if we have short or long flags - no mixing allowed
        has_short = any(arg.startswith('-') and not arg.startswith('--') for arg in args)
        has_long = any(arg.startswith('--') for arg in args)
        
        if has_short and has_long:
            print("\n❌ Cannot mix short (-u, -c, -n) and long (--username, --current, --new) flags")
            print("💡 Use either: sp -u <username> -c <current_password> -n <new_password>")
            print("💡 Or: setpassword --username <username> --current <current_password> --new <new_password>")
            input("⏸️  Press ENTER to continue...")
            return None
        
        # Parse arguments
        i = 0
        while i < len(args):
            arg = args[i]
            
            # Check if we have a value for this flag
            if i + 1 >= len(args):
                print(f"\n❌ Missing value for flag '{arg}'")
                print("💡 Each flag requires a value")
                input("⏸️  Press ENTER to continue...")
                return None
            
            value = args[i + 1]
            
            # Parse short flags
            if arg == '-u':
                if result['username'] is not None:
                    print(f"\n❌ Duplicate username flag")
                    input("⏸️  Press ENTER to continue...")
                    return None
                result['username'] = value
            elif arg == '-c':
                if result['current_password'] is not None:
                    print(f"\n❌ Duplicate current password flag")
                    input("⏸️  Press ENTER to continue...")
                    return None
                result['current_password'] = value
            elif arg == '-n':
                if result['new_password'] is not None:
                    print(f"\n❌ Duplicate new password flag")
                    input("⏸️  Press ENTER to continue...")
                    return None
                result['new_password'] = value
            
            # Parse long flags
            elif arg == '--username':
                if result['username'] is not None:
                    print(f"\n❌ Duplicate username flag")
                    input("⏸️  Press ENTER to continue...")
                    return None
                result['username'] = value
            elif arg == '--current':
                if result['current_password'] is not None:
                    print(f"\n❌ Duplicate current password flag")
                    input("⏸️  Press ENTER to continue...")
                    return None
                result['current_password'] = value
            elif arg == '--new':
                if result['new_password'] is not None:
                    print(f"\n❌ Duplicate new password flag")
                    input("⏸️  Press ENTER to continue...")
                    return None
                result['new_password'] = value
            
            else:
                print(f"\n❌ Invalid flag '{arg}'")
                print("💡 Valid flags: -u, -c, -n or --username, --current, --new")
                input("⏸️  Press ENTER to continue...")
                return None
            
            i += 2  # Skip flag and its value
        
        # Validate all required flags are present
        missing = []
        if result['username'] is None:
            missing.append('username (-u or --username)')
        if result['current_password'] is None:
            missing.append('current password (-c or --current)')
        if result['new_password'] is None:
            missing.append('new password (-n or --new)')
        
        if missing:
            print(f"\n❌ Missing required flags: {', '.join(missing)}")
            print("💡 All three flags are required")
            input("⏸️  Press ENTER to continue...")
            return None
        
        # Validate arguments are not empty
        if result['username'] is None or not str(result['username']).strip():
            print(f"\n❌ Username cannot be empty")
            input("⏸️  Press ENTER to continue...")
            return None
        if result['current_password'] is None or not str(result['current_password']).strip():
            print(f"\n❌ Current password cannot be empty")
            input("⏸️  Press ENTER to continue...")
            return None
        if result['new_password'] is None or not str(result['new_password']).strip():
            print(f"\n❌ New password cannot be empty")
            input("⏸️  Press ENTER to continue...")
            return None
        
        return result

    def _update_credentials_after_password_change(self, new_password: str, username: str) -> None:
        """Updates stored credentials and refreshes JWT token after successful password change"""
        try:
            # Update stored password
            self.api_password = new_password
            
            # Update username if it was changed
            if username != self.api_username:
                self.api_username = username
            
            # Clear current token
            self.api_jwt_token = None
            self.api_token_timestamp = None
            
            print("✅ Stored credentials updated")
            print("🔄 Refreshing JWT token with new password...")
            
            # Auto-refresh token with new credentials
            login_success = self._auto_login()
            
            if login_success:
                print("✅ JWT token refreshed successfully!")
                print("🎉 Password change completed and session active")
                print()
                print("=" * 50)
                print("✅ PASSWORD CHANGE SUCCESSFUL")
                print("=" * 50)
                print(f"📍 Reader: {self.api_reader_ip}")
                print(f"👤 Username: {self.api_username}")
                print(f"🔑 Password: Updated successfully")
                print(f"🔑 Token: {'✅ Active' if self.api_jwt_token else '❌ None'}")
                print("=" * 50)
            else:
                print("⚠️  Password change successful but session refresh failed")
                print("🔄 Please reconnect to the reader using one of these options:")
                print("   • Return to main menu and use 'r / restApi' command")
                
        except Exception as e:
            print(f"⚠️  Password change successful but credential update failed: {e}")
            print("🔄 Please reconnect to the reader using one of these options:")
            print("   • Return to main menu and use 'r / restApi' command")

    # GET HANDLERS

    def handle_api_login(self) -> None:
        """Handles API login to get JWT token from /cloud/localRestLogin endpoint"""
        print("\n🔐 API LOGIN - GET JWT TOKEN")
        print("-" * 35)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/localRestLogin")
        print(f"👤 Username: {self.api_username}")
        print(f"🔐 Authentication: Basic Auth")
        print()
        
        try:
            token = None  # Ensure token is always defined
            protocol = self.api_protocol

            if protocol in ['http', 'https']:
                print(f"🔍 Trying {protocol.upper()} protocol...")
            else:
                print(f"🔍 Trying UNKNOWN protocol for version endpoint...")

            # Prepare Basic Auth
            credentials = f"{self.api_username}:{self.api_password}"
            basic_auth_header = f"Basic {base64.b64encode(credentials.encode('utf-8')).decode('utf-8')}"
            
            # Make GET request with Basic Auth
            response = httpx.get(
                f"{protocol}://{self.api_reader_ip}/cloud/localRestLogin",
                headers={
                    "Authorization": basic_auth_header,
                    "Accept": "application/json"
                },
                verify=False,
                timeout=10.0
            )
            
            if response.status_code == 200:
                if protocol in ['http', 'https']:
                    print(f"✅ {protocol.upper()} request successful!")
                else:
                    print(f"✅ UNKNOWN protocol request successful!")
                
                # Parse response
                try:
                    data = response.json()
                    print(f"📥 Response received: {len(str(data))} characters")
                    
                    # Extract JWT token from response
                    # Zebra typically puts JWT in the 'message' field
                    token = (data.get('token') or data.get('bearerToken') or 
                            data.get('access_token') or data.get('accessToken') or
                            data.get('jwt') or data.get('JWT') or
                            data.get('message'))
                    
                    if token and isinstance(token, str) and token.count('.') == 2:
                        print("✅ JWT token extracted successfully!")
                        self.api_jwt_token = token
                        import time
                        self.api_token_timestamp = time.time()
                    else:
                        print("⚠️  No valid JWT token found in response")
                        print(f"📄 Raw response: {data}")
                        
                except Exception as e:
                    print(f"❌ Error parsing response: {e}")
                    print(f"📄 Raw response: {response.text}")
                    
            else:
                if protocol in ['http', 'https']:
                    print(f"❌ {protocol.upper()} failed - Status: {response.status_code}")
                else:
                    print(f"❌ UNKNOWN protocol failed - Status: {response.status_code}")
                if response.text:
                    print(f"📄 Error response: {response.text}")
                
            # Display results
            if token:
                print("\n🎉 SUCCESS!")
                print("=" * 50)
                print(f"🔑 JWT Token Retrieved:")
                print(f"   {token}")
                print("=" * 50)
                print(f"📏 Token length: {len(token)} characters")
                print(f"🔍 Token preview: {token[:30]}...{token[-20:]}")
                print("\n💡 Token is now stored and will be displayed in the menu")
            else:
                print("\n❌ FAILED!")
                print("🔍 Unable to retrieve JWT token from any protocol")
                print("💡 Check IP address, username, and password")
                
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        
        input("\n⏸️  Press ENTER to continue...")  

    def handle_api_status(self, save_response: bool = False) -> None:
        """Handles GET /cloud/status API endpoint"""
        print("\n📊 GET READER STATUS")
        print("-" * 25)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/status")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/status", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/status", "status", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_version(self, save_response: bool = False) -> None:
        """Handles GET /cloud/version API endpoint"""
        print("\n🏷️  GET READER VERSION")
        print("-" * 25)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/version")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/version", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/version", "version", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_network(self, save_response: bool = False) -> None:
        """Handles GET /cloud/network API endpoint"""
        print("\n🌐 GET NETWORK CONFIGURATION")
        print("-" * 31)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/network")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/network", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/network", "network", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_region(self, save_response: bool = False) -> None:
        """Handles GET /cloud/region API endpoint"""
        print("\n🌍 GET REGION CONFIGURATION")
        print("-" * 29)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/region")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/region", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/region", "region", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_mode(self, save_response: bool = False) -> None:
        """Handles GET /cloud/mode API endpoint"""
        print("\n⚙️  GET OPERATING MODE")
        print("-" * 23)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/mode")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/mode", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/mode", "mode", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_config(self, save_response: bool = False) -> None:
        """Handles GET /cloud/config API endpoint"""
        print("\n🔧 GET READER CONFIG")
        print("-" * 22)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/config")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/config", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/config", "config", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_gpi(self, save_response: bool = False) -> None:
        """Handles GET /cloud/gpi API endpoint"""
        print("\n� GET GPI STATUS")
        print("-" * 19)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/gpi")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/gpi", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/gpi", "gpi", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_gpo(self, save_response: bool = False) -> None:
        """Handles GET /cloud/gpo API endpoint"""
        print("\n📤 GET GPO STATUS")
        print("-" * 19)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/gpo")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/gpo", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/gpo", "gpo", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_caps(self, save_response: bool = False) -> None:
        """Handles GET /cloud/readerCapabilities API endpoint"""
        print("\n🎯 GET READER CAPABILITIES")
        print("-" * 30)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/readerCapabilities")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/readerCapabilities", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/readerCapabilities", "caps", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_timezone(self, save_response: bool = False) -> None:
        """Handles GET /cloud/timeZone API endpoint"""
        print("\n🕐 GET TIMEZONE CONFIG")
        print("-" * 24)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/timeZone")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/timeZone", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/timeZone", "timezone", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_cableloss(self, save_response: bool = False) -> None:
        """Handles GET /cloud/cableLossCompensation API endpoint"""
        print("\n📡 GET CABLE LOSS COMPENSATION")
        print("-" * 35)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/cableLossCompensation")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/cableLossCompensation", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/cableLossCompensation", "cableloss", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_certs(self, save_response: bool = False) -> None:
        """Handles GET /cloud/certificates API endpoint"""
        print("\n🔒 GET CERTIFICATES")
        print("-" * 21)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/certificates")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/certificates", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/certificates", "certs", save_response)
        
        input("\n⏸️  Press ENTER to continue...")
    
    def handle_api_logs(self, save_response: bool = False) -> None:
        """Handles GET /cloud/logs API endpoint"""
        print("\n📄 GET LOGS CONFIGURATION")
        print("-" * 28)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/logs")
        print(f"🔑 Authentication: Bearer Token")
        
        success, data, status_code = self._make_api_request("/cloud/logs", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        self._show_api_response(success, data, status_code, "/cloud/logs", "logs", save_response)
        
        input("\n⏸️  Press ENTER to continue...")

    def handle_api_syslog(self, save_response: bool = False) -> None:
        """Handles GET /cloud/logs/syslog API endpoint (FXR90 specific)"""
        print("\n📋 GET SYSTEM LOG (FXR90)")
        print("-" * 26)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: /cloud/logs/syslog")
        print(f"🔑 Authentication: Bearer Token")
        print(f"🏷️  Reader: FXR90 specific endpoint")
        
        success, data, status_code = self._make_api_request("/cloud/logs/syslog", "GET")
        
        # Check for authorization errors
        if not success and status_code in [401, 403]:
            self._handle_auth_error()
            return
        
        # Show API response (never save as JSON for syslog)
        self._show_api_response(success, data, status_code, "/cloud/logs/syslog", "syslog", False)
        
        # If successful and contains binary data, save to file if requested
        if success and isinstance(data, dict) and 'binary' in data and save_response:
            print("\n💾 SAVING SYSLOG TO FILE")
            print("-" * 24)
            print("📄 Binary syslog data detected in response")
            
            try:
                # Get reader model for directory and filename organization
                print("🔍 Detecting reader model...")
                reader_model = self._get_reader_model()
                
                # Create timestamp for filename (format: YYYYMMDD-HHMMSS)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                
                # Create reader-specific filename: syslog-MODEL-timestamp.tar.gz
                filename = f"syslog-{reader_model}-{timestamp}.tar.gz"
                
                # Create reader-specific directory: api-responses/IP_MODEL/syslog/
                reader_id = f"{self.api_reader_ip}_{reader_model}"
                syslog_dir = os.path.join(os.getcwd(), "api-responses", reader_id, "syslog")
                os.makedirs(syslog_dir, exist_ok=True)
                
                # Full file path
                file_path = os.path.join(syslog_dir, filename)
                
                print(f"📡 Reader: {reader_model}")
                print(f"📁 Saving to: {file_path}")
                print("🔄 Decoding binary data...")
                
                # Decode base64 binary data
                binary_data = data['binary']
                decoded_data = base64.b64decode(binary_data)
                
                # Save the decoded tar.gz file
                with open(file_path, 'wb') as f:
                    f.write(decoded_data)
                
                # Get file size for confirmation
                file_size = os.path.getsize(file_path)
                file_size_kb = file_size / 1024
                
                print(f"✅ SUCCESS!")
                print("=" * 50)
                print(f"📄 File saved: {filename}")
                print(f"📁 Location: {file_path}")
                print(f"📡 Reader: {self.api_reader_ip} ({reader_model})")
                print(f"📏 Size: {file_size_kb:.2f} KB ({file_size} bytes)")
                print(f"🗜️  Format: tar.gz compressed archive")
                print("=" * 50)
                print("💡 You can extract this file with:")
                print(f"   tar -xzf \"{file_path}\"")
                print("💡 File organized by reader IP and model")
                
            except Exception as e:
                    print(f"❌ Error saving file: {e}")
                    print("🔍 Check if you have write permissions in the project directory")
        elif success and save_response:
            print("\n⚠️  No binary data found in response")
            print("💡 The response doesn't contain the expected 'binary' field")
        
        input("\n⏸️  Press ENTER to continue...")

    # PUT HANDLERS

    def handle_api_set_config(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/config API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/config", "config", "UPDATE READER CONFIGURATION", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/config", "config", "UPDATE READER CONFIGURATION")

    def handle_api_set_mode(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/mode API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/mode", "mode", "UPDATE OPERATING MODE", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/mode", "mode", "UPDATE OPERATING MODE")

    def handle_api_set_network(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/network API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/network", "network", "UPDATE READER NETWORK CONFIGURATION", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/network", "network", "UPDATE READER NETWORK CONFIGURATION")

    def handle_api_set_region(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/region API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/region", "region", "UPDATE REGION INFORMATION", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/region", "region", "UPDATE REGION INFORMATION")

    def handle_api_set_gpo(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/gpo API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/gpo", "gpo", "UPDATES GPO PORT STATE", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/gpo", "gpo", "UPDATES GPO PORT STATE")

    def handle_api_set_timezone(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/timeZone API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/timeZone", "timezone", "SET TIME ZONE", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/timeZone", "timezone", "SET TIME ZONE")

    def handle_api_set_logs(self, file_path_args: Optional[list] = None) -> None:
        """Handles PUT /cloud/logs API endpoint with JSON file selection"""
        if file_path_args:
            parsed = self._parse_put_command_flags(file_path_args)
            if parsed is None:
                return
            if 'json_data' in parsed:
                self._handle_put_request("/cloud/logs", "logs", "SET LOGS CONFIGURATION", 
                                       parsed['json_data'], parsed['file_path'])
                return
        self._handle_put_request("/cloud/logs", "logs", "SET LOGS CONFIGURATION")

    def handle_api_set_password(self, username: Optional[str] = None, current_password: Optional[str] = None, new_password: Optional[str] = None) -> None:
        """
        Handles PUT /cloud/updatePassword API endpoint with argument-based input.
        
        Args:
            username: Target username for password change
            current_password: Current password for authentication
            new_password: New password to set
        """
        print("\n🔑 CHANGE READER PASSWORD")
        print("-" * 25)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: PUT /cloud/updatePassword")
        print(f"🔑 Authentication: Bearer Token")
        print()
        
        # Check token first
        if not self._check_jwt_token():
            return
        
        # If no arguments provided, fall back to interactive mode (for backwards compatibility)
        if username is None or current_password is None or new_password is None:
            print("❌ Missing required arguments for password change")
            print("💡 Use: sp -u <username> -c <current_password> -n <new_password>")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        try:
            # Display the arguments (without showing passwords)
            print("📝 Password change details:")
            print(f"👤 Username: {username}")
            print(f"🔑 Current Password: {'*' * len(current_password)}")
            print(f"🆕 New Password: {'*' * len(new_password)}")
            print()
            
            # Confirmation prompt (still required for safety)
            print(
                f"⚠️  Are you sure you want to change the password for user '{username}'? [y/N]: ",
                end=""
            )
            confirm = input().strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ Password change cancelled")
                input("\n⏸️  Press ENTER to continue...")
                return
            
            # Construct JSON payload
            payload = {
                "currentPassword": current_password,
                "newPassword": new_password,
                "userName": username
            }
            
            # Send request
            print(f"\n🚀 Sending password change request...")
            try:
                success, response_data, status_code = self._make_api_request("/cloud/updatePassword", "PUT", data=payload)
                
                if success:
                    print(f"✅ Password change successful! (Status: {status_code})")
                    print("🔄 Updating stored credentials and refreshing session...")
                    
                    # Update credentials and refresh token
                    self._update_credentials_after_password_change(new_password, username)
                    
                else:
                    print(f"❌ Password change failed!")
                    print(f"📊 Status Code: {status_code}")
                    
                    # Display error message from API response
                    error_message = "Unknown error"
                    if isinstance(response_data, dict):
                        error_message = (response_data.get('error') or 
                                       response_data.get('message') or 
                                       response_data.get('details') or 
                                       str(response_data))
                    else:
                        error_message = str(response_data)
                    
                    print(f"🚫 Error: {error_message}")
                        
            except Exception as e:
                print(f"❌ Request error: {e}")
                print("� Please check your network connection and try again")
            
        except Exception as e:
            print(f"❌ Unexpected error during password change: {e}")
        
        input("\n⏸️  Press ENTER to continue...")

    def handle_api_reboot(self) -> None:
        """Handles PUT /cloud/reboot API endpoint"""
        print("\n🔄 REBOOT READER")
        print("-" * 18)
        print(f"📍 Target: {self.api_reader_ip}")
        print(f"🌐 Endpoint: PUT /cloud/reboot")
        print(f"🔑 Authentication: Bearer Token")
        print()
        
        # Check token first
        if not self._check_jwt_token():
            return
        
        # More explicit confirmation prompt for dangerous operation
        print("⚠️  WARNING: This will restart the reader!")
        print("📡 All active connections will be lost")
        print("⏱️  Reader will be unavailable for ~30-60 seconds")
        print("🔌 Any ongoing operations will be interrupted")
        print()
        
        confirm = input(
            "❓ Are you absolutely sure you want to reboot the reader? (yes/no): "
        ).strip().lower()
        
        if confirm not in ['yes', 'y']:
            print("❌ Reboot cancelled")
            input("\n⏸️  Press ENTER to continue...")
            return
        
        # Send reboot request with empty body
        print("\n🔄 Sending reboot command...")
        try:
            success, response_data, status_code = self._make_api_request("/cloud/reboot", "PUT", data={})
            
            # Show detailed response information
            print(f"\n📡 REBOOT REQUEST RESPONSE")
            print("=" * 50)
            
            if success:
                print(f"✅ Reboot command sent successfully!")
                print(f"📊 HTTP Status Code: {status_code}")
                
                # Show all response data
                if response_data:
                    print(f"📄 Response Data:")
                    print("-" * 30)
                    try:
                        formatted_json = json.dumps(response_data, indent=2, ensure_ascii=False)
                        print(formatted_json)
                    except:
                        print(str(response_data))
                else:
                    print(f"📄 Response: Empty (expected for reboot command)")
                
                print("=" * 50)
                print("\n💡 NEXT STEPS:")
                print("  1. Wait 30-60 seconds for reader to restart")
                print("  2. Use 'l / login' to reconnect to the reader")
                print("  3. Verify connection with 's / status'")
                
            else:
                print(f"❌ Reboot command failed!")
                print(f"📊 HTTP Status Code: {status_code}")
                
                # Show detailed error information
                if response_data:
                    print(f"📄 Error Response:")
                    print("-" * 30)
                    try:
                        formatted_json = json.dumps(response_data, indent=2, ensure_ascii=False)
                        print(formatted_json)
                    except:
                        print(str(response_data))
                else:
                    print(f"📄 Error: No response data received")
                
                print("=" * 50)
                print(f"💡 Reboot failed - check reader connectivity and try again")
                
        except Exception as e:
            print(f"\n❌ REBOOT REQUEST ERROR")
            print("=" * 50)
            print(f"🚫 Network/Request Error: {e}")
            print("💡 Check network connection and reader availability")
            print("=" * 50)
        
        input("\n⏸️  Press ENTER to continue...")

    # UTILITIES HANDLERS

    def clear_screen(self) -> None:
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
  
    def show_help(self) -> None:
        """Displays help and usage tips for the API submenu."""
        print("\n🆘 API SUBMENU HELP")
        print("=" * 60)
        print("This submenu lets you interact directly with Zebra reader REST API endpoints.")
        print("You can GET or PUT configuration, status, and control data.")
        print("\nUSAGE:")
        print("  • Enter a command shortcut (e.g. 'gs', 'setnetwork') or full command name.")
        print("  • For GET commands, add '-y' to save the response as a JSON file.")
        print("  • For PUT commands, provide a file path with '-p <file>' or '--path <file>'.")
        print("  • Use 'b' or 'back' to return to the main menu.")
        print("  • Use 'c' or 'clear' to clear the screen.")
        print("  • Use 'h' or 'help' to show this help message.")
        print("\nTIPS:")
        print("  • You must be authenticated (JWT token) to use most API commands.")
        print("  • If you see AUTHORIZATION ERROR, use 'l' or 'login' to refresh your token.")
        print("  • File-based PUT commands require a valid JSON file with correct structure.")
        print("  • Saved GET responses are organized by reader IP and model in 'api-responses/'.")
        print("  • Use the main menu 'status' or 'help' for overall CLI troubleshooting.")
        print("\nTROUBLESHOOTING:")
        print("  • Connection errors: Check reader IP, network, and protocol (HTTP/HTTPS).")
        print("  • Auth errors: JWT token may be expired or invalid. Re-login if needed.")
        print("  • File errors: Ensure you have write permissions and valid file paths.")
        print("  • API errors: Check the reader's firmware version and API compatibility.")
        print("\nFor more details, see 'API-SUBMENU-README.md'.")
        input("\n⏸️  Press ENTER to return to the API menu...")