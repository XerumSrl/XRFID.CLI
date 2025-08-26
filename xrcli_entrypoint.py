# Standard library imports
import argparse

# Local imports
from zebra_cli.interactive_cli import InteractiveCLI

def main() -> None:
    """
    Entry point for the Zebra RFID CLI.
    - Standard interactive mode: shows the CLI menu.
    - Batch/one-shot mode: with --table or --rssi, after automatic login executes the sequence directly (login → start scanning → table/plot) without showing the menu between steps.
      The menu is only shown in case of error in one of the steps.
    """
    parser = argparse.ArgumentParser(
        description="Entry point for the Zebra RFID CLI. Allows optional automatic login and batch mode."
    )
    parser.add_argument("--ip", type=str, help="Zebra reader IP address (optional)")
    parser.add_argument("-u", "--username", type=str, help="Username for login (optional)")
    parser.add_argument("-p", "--password", type=str, help="Password for login (optional)")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable detailed logging and advanced printing for CLI debugging"
    )
    parser.add_argument(
        "--table",
        action="store_true",
        help="After automatic connection, start scanning and open tag table"
    )
    parser.add_argument(
        "--rssi",
        action="store_true",
        help="After automatic connection, start scanning and open RSSI graph"
    )
    args = parser.parse_args()

    # Batch/one-shot mode: execute automatic sequence without showing menu, show menu only in case of error
    batch_mode = args.table or args.rssi
    cli = InteractiveCLI(debug=args.debug)
    def fallback_to_menu():
        print("\n➡️  Switching to interactive menu...")
        cli.run()

    if args.ip and args.username and args.password:
        if args.debug:
            print(f"\n[DEBUG] Entrypoint - Starting automatic login sequence")
            print(f"[DEBUG] Entrypoint - IP: {args.ip}, Username: {args.username}")
            print(f"[DEBUG] Entrypoint - Batch mode: {batch_mode}")
            print(f"[DEBUG] Entrypoint - Args.table: {args.table}, Args.rssi: {args.rssi}")
        
        print(f"\n🔐 Automatic login to {args.ip} with user {args.username}...")
        try:
            if args.debug:
                print(f"[DEBUG] Entrypoint - Calling login_and_connect...")
            success = cli.app_context.login_and_connect(args.ip, args.username, args.password)
            if not success:
                print("❌ Automatic login failed. Continue with manual login from CLI.")
                fallback_to_menu()
                return
            if args.debug:
                print(f"[DEBUG] Entrypoint - Login successful")
                print(f"[DEBUG] Entrypoint - Connected: {cli.app_context.is_connected()}")
                print(f"[DEBUG] Entrypoint - WebSocket running: {cli.app_context.is_websocket_running()}")
                print("✅ Automatic login successful!\n")
            
            # For batch mode, only check that the WebSocket is active (without additional attempts)
            if batch_mode and not cli.app_context.is_websocket_running():
                print("⚠️  WebSocket not active after login.")
                print("💡 This is normal for IOTC connections - WebSocket may need more time to activate.")
                print("💡 Switching to interactive mode where you can manually activate WebSocket.")
                fallback_to_menu()
                return
            
            if batch_mode:
                if args.debug:
                    print(f"[DEBUG] Entrypoint - Starting batch mode sequence")
                    print(f"[DEBUG] Entrypoint - Pre-scan connection status: {cli.app_context.is_connected()}")
                    print(f"[DEBUG] Entrypoint - Pre-scan WebSocket status: {cli.app_context.is_websocket_running()}")
                try:
                    # Start scanning
                    if args.debug:
                        print(f"[DEBUG] Entrypoint - Calling handle_start_scan...")
                    scan_result = cli.handle_start_scan()
                    if args.debug:
                        print(f"[DEBUG] Entrypoint - handle_start_scan completed")
                        print(f"[DEBUG] Entrypoint - Post-scan connection status: {cli.app_context.is_connected()}")
                        print(f"[DEBUG] Entrypoint - Post-scan WebSocket status: {cli.app_context.is_websocket_running()}")
                    # handle_start_scan already prints errors, but if no connection or exception, fallback
                    if not cli.app_context.is_connected():
                        print("❌ Connection lost after login. Switching to menu.")
                        fallback_to_menu()
                        return
                    # Start table or plot
                    if args.table:
                        if args.debug:
                            print(f"[DEBUG] Entrypoint - Starting tag table...")
                        cli.handle_tag_table()
                    elif args.rssi:
                        if args.debug:
                            print(f"[DEBUG] Entrypoint - Starting RSSI plot...")
                        cli.handle_plot_live_gui_enhanced()
                    # After window closure, always show CLI menu
                    if args.debug:
                        print(f"[DEBUG] Entrypoint - Batch operations completed, starting CLI menu...")                    

                    cli.run()
                    return
                except Exception as e:
                    print(f"❌ Error during automatic startup: {e}\n")
                    fallback_to_menu()
                    return
                
            input("\n⏸️  Press ENTER to continue...")
        except Exception as e:
            print(f"❌ Automatic login error: {e}\nContinue with manual login from CLI.")
            fallback_to_menu()
            return
    elif any([args.ip, args.username, args.password]):
        print("⚠️  For automatic login all parameters are required: --ip, -u, -p. Starting CLI without automatic login.\n")
    # If not batch, or if batch but login not requested, show menu
    cli.run()

if __name__ == "__main__":
    main()