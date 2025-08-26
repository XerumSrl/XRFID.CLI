# Zebra RFID CLI - API Submenu Documentation

## Overview

The API Submenu is a comprehensive interface for interacting with Zebra RFID readers via REST API endpoints. It provides both GET operations for retrieving information and PUT operations for updating reader configurations using JSON payloads.

## Access


## Access

The correct way to access the API submenu is from the main CLI menu when you are already connected to a reader.

- From the main menu, select `r` or `restApi` while connected: the API submenu will open for the same reader and session.

It is not possible to access the API submenu directly without an active connection. All API operations will refer to the currently connected reader.

## Main Features

- **Automatic Authentication**: JWT token management with auto-login
- **Reader Model Detection**: Automatic detection and caching of reader model
- **File Organization**: Automatic saving of responses in reader-specific folders
- **JSON-based Configuration**: PUT operations using organized JSON files
- **Comprehensive Error Handling**: Clear feedback for all error scenarios

---

## Getting Started

### First Time Setup


When you first access the API submenu **without arguments**, you'll be prompted for:

```
📝 First time setup - Enter reader credentials for API requests:

📍 Reader IP: [Enter reader IP address]
👤 Username [admin]: [Enter username or press ENTER for admin]
🔑 Password [admin]: [Enter password or press ENTER for admin]
```

**Note**: You should provide valid reader credentials, because except rare cases the default admin/admin won't be correct.

If you use the CLI arguments (`-t`, `-u`, `-p`), the submenu will use those values directly and skip the prompts. If any argument is missing, you will be prompted for the missing value(s).

### Automatic Initialization

Upon entering the API submenu, the system automatically:

1. **Auto-Login**: Attempts to obtain JWT token using provided credentials
   - Tries both HTTPS and HTTP protocols automatically
   - Detects working protocol and remembers it for future requests
   - Displays login success/failure status

2. **Reader Model Detection**: Queries `/cloud/version` endpoint
   - Detects reader model (e.g., FXR90, ATR7000)
   - Caches model information for file organization
   - Uses "UNKNOWN" if detection fails

3. **Session Persistence**: Maintains credentials and token throughout session
   - Shows token timestamp when obtained
   - Automatically resets credentials when exiting submenu

---

## Menu Structure

```
🔧==========================================================
   ZEBRA RFID API REQUESTS - Interactive Mode
============================================================
📍 Reader IP: 192.168.2.46
👤 Username: admin
🔑 Password: ****
------------------------------------------------------------

🔧 API Requests Menu:
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ 📍 Target Reader: 192.168.2.46                                                          │
│ 🏷️  Reader Model: FXR90                                                                  │
│ 🕒 Token obtained: 2025-07-24 16:30:47                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ GET ENDPOINTS:                                      │ 💾 SAVE OPTIONS:                  │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ gl / getLogin   🔐 Get JWT token                    │ (none)                            │
│ gs / getStatus  📊 Get reader status                │ [-y] [-n](default)                │
│ gv / getVersion 🏷️  Get reader version               │ [-y] [-n](default)                │
│ gn / getNetwork 🌐 Get network config               │ [-y] [-n](default)                │
│ gr / getRegion  🌍 Get region config                │ [-y] [-n](default)                │
│ gm / getMode    ⚙️  Get operating mode               │ [-y] [-n](default)                │
│ gc / getConfig  🔧 Get reader config                │ [-y] [-n](default)                │
│ gi / getGpi     📥 Get GPI status                   │ [-y] [-n](default)                │
│ go / getGpo     📤 Get GPO status                   │ [-y] [-n](default)                │
│ gp / getCaps    🎯 Get reader capabilities          │ [-y] [-n](default)                │
│ gz / getTimezone 🕐 Get timezone config             │ [-y] [-n](default)                │
│ gx / getCableLoss 📡 Get cable loss compensation    │ [-y] [-n](default)                │
│ ge / getCerts   🔒 Get certificates                 │ [-y] [-n](default)                │
│ gw / getLogs    📄 Get logs configuration           │ [-y] [-n](default)                │
│ gy / getSyslog  📋 Get system log                   │ [-y] [-n](default)                │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ PUT ENDPOINTS (File-based):                         │ 📁 FILE PATH OPTIONS:             │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ sn / setNetwork 🌐 Update network config            │ -p <file> OR --path <file>        │
│ sr / setRegion  🌍 Update region info               │ -p <file> OR --path <file>        │
│ sm / setMode    ⚙️  Update operating mode            │ -p <file> OR --path <file>        │
│ sc / setConfig  🔧 Update reader config             │ -p <file> OR --path <file>        │
│ so / setGpo     📤 Update GPO port state            │ -p <file> OR --path <file>        │
│ st / setTimezone 🕐 Set time zone                   │ -p <file> OR --path <file>        │
│ sl / setLogs    📄 Set logs config                  │ -p <file> OR --path <file>        │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ PUT ENDPOINTS (Special):                            │ 🔧 COMMAND FLAGS:                 │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ sp / setPassword 🔑 Change reader password          │ -u/-c/-n OR --username/--current/--new │
│ rb / reboot     🔄 Reboot reader                    │ (none)                            │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ UTILITIES:                                          │ 🛠️ ACTIONS:                       │
├─────────────────────────────────────────────────────┼───────────────────────────────────┤
│ c / clear      🧹 Clear screen                      │ (none)                            │
│ b / back       ↩️  Back to main menu                 │ (none)                            │
└─────────────────────────────────────────────────────┴───────────────────────────────────┘

🎯 API command or shortcut:
```

---

## GET Operations

### Available GET Commands

| Command | Endpoint | Description |
|---------|----------|-------------|
| `gl / getLogin` | `/cloud/localRestLogin` | Get JWT token |
| `gs / getStatus` | `/cloud/status` | Get reader status |
| `gv / getVersion` | `/cloud/version` | Get reader version |
| `gn / getNetwork` | `/cloud/network` | Get network config |
| `gr / getRegion` | `/cloud/region` | Get region config |
| `gm / getMode` | `/cloud/mode` | Get operating mode |
| `gc / getConfig` | `/cloud/config` | Get reader config |
| `gi / getGpi` | `/cloud/gpi` | Get GPI status |
| `go / getGpo` | `/cloud/gpo` | Get GPO status |
| `gp / getCaps` | `/cloud/readerCapabilities` | Get reader capabilities |
| `gz / getTimezone` | `/cloud/timeZone` | Get timezone config |
| `gx / getCableLoss` | `/cloud/cableLossCompensation` | Get cable loss compensation |
| `ge / getCerts` | `/cloud/certificates` | Get certificates |
| `gw / getLogs` | `/cloud/logs` | Get logs configuration |
| `gy / getSyslog` | `/cloud/logs/syslog` | Get system log |

### GET Command Arguments

All GET commands (except `getLogin`) support optional arguments to control response saving:

| Argument | Description | Example |
|----------|-------------|---------|
| *(none)* | Show response, don't save | `getStatus` |
| `-n` or `--no` | Show response, don't save | `getStatus -n` |
| `-y` or `--yes` | Show response and save to file | `getStatus -y` |

**Important Notes:**
- Invalid arguments abort command execution with helpful error messages
- Multiple arguments are not allowed (e.g., `getStatus -y -n` will abort)
- `getLogin` responses are never saved (sensitive token data)
- `getSyslog -y` saves only `.tar.gz` files (not JSON responses)

### GET Operation Flow

GET commands now support argument-based control for saving responses:

1. **Command Format**: `<command> [argument]`
   - **No argument**: Shows response, doesn't save (e.g., `getStatus`)
   - **`-n` or `--no`**: Shows response, doesn't save (e.g., `getStatus -n`)
   - **`-y` or `--yes`**: Shows response and saves to file (e.g., `getStatus -y`)

2. **Execution Flow**:
   - System validates argument (if provided)
   - Makes authenticated request using JWT token
   - Response is displayed in formatted JSON
   - If `-y`/`--yes` was specified, automatically saves to file
   - User presses ENTER to continue

3. **Error Handling**:
   - Invalid arguments (e.g., `getStatus -invalid`) abort command execution
   - Multiple arguments (e.g., `getStatus -y -n`) abort command execution
   - Clear error messages guide users to correct usage

**File Saving Details:**
- **Most Commands**: Save as JSON files in `api-responses/{IP}_{MODEL}/{command}/` folders
- **Special Case - getSyslog**: Saves binary data as `.tar.gz` compressed archive (never JSON)
- **Excluded**: `getLogin` command responses are never saved (sensitive token data)

### Example GET Response Display

**Example 1: Basic Command (No Saving)**
```
🎯 API command or shortcut: getStatus

� GET READER STATUS
-------------------
📍 Target: 192.168.2.46
🌐 Endpoint: /cloud/status
🔑 Authentication: Bearer Token

�📡 API RESPONSE - /cloud/status
==================================================
✅ Status: 200
📄 Response Data:
------------------------------
{
  "radioActivity": "active",
  "uptime": 12345
}
==================================================

⏸️  Press ENTER to continue...
```

**Example 2: Command with Save Argument**
```
🎯 API command or shortcut: getStatus -y

📊 GET READER STATUS
-------------------
📍 Target: 192.168.2.46
🌐 Endpoint: /cloud/status
🔑 Authentication: Bearer Token

� API RESPONSE - /cloud/status
==================================================
✅ Status: 200
📄 Response Data:
------------------------------
{
  "radioActivity": "active", 
  "uptime": 12345
}
==================================================

💾 SAVING STATUS RESPONSE
-------------------------
🔍 Detecting reader model...
📡 Reader: FXR90
📁 Saving to: api-responses/192.168.2.46_FXR90/status/status-FXR90-20250728-163047.json
🔄 Preparing JSON data...
✅ SUCCESS!
==================================================
📄 File saved: status-FXR90-20250728-163047.json
📁 Location: api-responses/192.168.2.46_FXR90/status/status-FXR90-20250728-163047.json
📡 Reader: 192.168.2.46 (FXR90)
📏 Size: 0.15 KB (156 bytes)
📦 Format: Clean JSON response data
==================================================
💡 File contains:
   • Raw API response data only
   • Organized by reader IP and model

⏸️  Press ENTER to continue...
```

**Example 3: Invalid Argument (Command Aborts)**
```
🎯 API command or shortcut: getStatus -invalid

❌ Invalid argument: -invalid

Valid arguments for GET commands:
  • No argument: Show response, don't save
  • -n or --no: Show response, don't save  
  • -y or --yes: Show response and save to file

💡 Examples:
  getStatus        (show only)
  getStatus -n     (show only)
  getStatus -y     (show and save)

⏸️  Press ENTER to continue...
```

**Special Case - getSyslog Command:**

The `getSyslog` command has special handling for binary syslog data. Unlike other GET commands, it **only saves the decoded binary tar.gz file** (never the JSON response itself) when `-y`/`--yes` is specified.

**Example: getSyslog with Save Argument**
```
🎯 API command or shortcut: getSyslog -y

📋 GET SYSTEM LOG (FXR90)
-------------------------
📍 Target: 192.168.2.46
🌐 Endpoint: /cloud/logs/syslog
� Authentication: Bearer Token
🏷️  Reader: FXR90 specific endpoint

�📡 API RESPONSE - /cloud/logs/syslog
==================================================
✅ Status: 200
📄 Response Data:
------------------------------
{
  "binary": "[base64 encoded tar.gz data]"
}
==================================================

💾 SAVING SYSLOG TO FILE
------------------------
📄 Binary syslog data detected in response
🔍 Detecting reader model...
📡 Reader: FXR90
📁 Saving to: api-responses/192.168.2.46_FXR90/syslog/syslog-FXR90-20250728-163047.tar.gz
🔄 Decoding binary data...
✅ SUCCESS!
==================================================
📄 File saved: syslog-FXR90-20250728-163047.tar.gz
📁 Location: api-responses/192.168.2.46_FXR90/syslog/syslog-FXR90-20250728-163047.tar.gz
📡 Reader: 192.168.2.46 (FXR90)
📏 Size: 125.34 KB (128,349 bytes)
🗜️  Format: tar.gz compressed archive
==================================================
💡 You can extract this file with:
   tar -xzf "api-responses/192.168.2.46_FXR90/syslog/syslog-FXR90-20250728-163047.tar.gz"
💡 File organized by reader IP and model

⏸️  Press ENTER to continue...
```

**Note**: `getSyslog` (without `-y`) shows the response but saves nothing, just like other GET commands.

---

## PUT Operations

### Available PUT Commands

| Command | Endpoint | Description | File Path Support |
|---------|----------|-------------|-------------------|
| `sn / setNetwork` | `/cloud/network` | Update reader network configuration | ✅ `-p <file>` |
| `sr / setRegion` | `/cloud/region` | Update region information | ✅ `-p <file>` |
| `sm / setMode` | `/cloud/mode` | Update operating mode | ✅ `-p <file>` |
| `sc / setConfig` | `/cloud/config` | Update reader config | ✅ `-p <file>` |
| `so / setGpo` | `/cloud/gpo` | Updates GPO port state | ✅ `-p <file>` |
| `st / setTimezone` | `/cloud/timeZone` | Set time zone | ✅ `-p <file>` |
| `sl / setLogs` | `/cloud/logs` | Set logs configuration | ✅ `-p <file>` |
| `sp / setPassword` | `/cloud/updatePassword` | Change reader password | ❌ Uses flags |
| `rb / reboot` | `/cloud/reboot` | Reboot reader | ❌ No arguments |

### JSON File Organization

PUT operations require JSON files organized in specific folders:

```
requests-json/
├── config/          # JSON files for setConfig
├── mode/            # JSON files for setMode
├── gpo/             # JSON files for setGpo
├── network/         # JSON files for setNetwork
├── region/          # JSON files for setRegion
├── timezone/        # JSON files for setTimezone
└── logs/            # JSON files for setLogs
```

## ⚠️  **CRITICAL IMPORTANT NOTE** ⚠️

**The CLI assumes you provide correctly structured JSON files that match the expected API schema for each endpoint. The system performs basic JSON syntax validation (checking for valid JSON format) but does NOT validate the content against specific API schemas or required fields.**

**This means:**
- ✅ **JSON Syntax Validation**: The CLI will catch malformed JSON (missing commas, brackets, etc.)
- ❌ **Schema Validation**: The CLI will NOT catch incorrect field names, missing required fields, or invalid values
- 🚨 **Your Responsibility**: You must ensure your JSON files contain the correct structure and data expected by each API endpoint

**Recommendation**: Test JSON files with non-critical settings first and verify results using corresponding GET commands.

### PUT Command Usage Modes

Most PUT commands now support **two execution modes**:

#### 1. **Interactive Mode** (Default)
Execute command without arguments to use the traditional interactive file selection:

```
🎯 API command or shortcut: setNetwork
🎯 API command or shortcut: sc
```

#### 2. **Direct File Path Mode** (New)
Execute command with `-p` or `--path` flag to specify JSON file directly:

```
🎯 API command or shortcut: setNetwork -p ./requests-json/network/my-config.json
🎯 API command or shortcut: sc --path /absolute/path/to/config.json
🎯 API command or shortcut: setRegion -p ../configs/region-setup.json
```

**Path Flag Support:**
- **Short flag**: `-p <file_path>`
- **Long flag**: `--path <file_path>`
- **Path types**: Both relative and absolute paths are supported
- **Validation**: File existence and JSON syntax are validated before sending
- **No preview**: When using flags, no preview prompt is shown

**Error Behavior:**
- **File not found**: Shows error and returns to menu (no fallback to interactive mode)
- **Invalid JSON**: Shows parsing error and returns to menu
- **Invalid arguments**: Shows usage help and returns to menu

### PUT Operation Flow

#### Step-by-Step Walkthrough

**Example: Using `sc / setConfig`**

1. **Command Selection**
   ```
   🎯 API command or shortcut: sc
   ```

2. **Operation Header**
   ```
   ⚙️  UPDATE READER CONFIGURATION
   --------------------------------------------------
   🌐 Endpoint: PUT /cloud/config
   📂 JSON Source: requests-json/config/
   ```

3. **File Discovery and Selection**
   ```
   📋 AVAILABLE JSON FILES FOR CONFIG:
   --------------------------------------------------
     1. basic-config.json
     2. advanced-config.json
     3. test-config.json
     0. ❌ Abort operation
   
   🔢 Select JSON file (1-3, 0 to abort):
   ```

4. **User Selection** (e.g., selecting `1`)
   ```
   🔢 Select JSON file (1-3, 0 to abort): 1
   ```

5. **Preview Option**
   ```
   🔍 Do you want to preview the JSON content before sending? (y/N): y
   ```

6. **JSON Preview** (if requested)
   ```
   📄 JSON CONTENT PREVIEW - basic-config.json:
   ============================================================
   {
     "setting1": "value1",
     "setting2": {
       "nested": "value"
     }
   }
   ============================================================
   
   ⏸️  Press ENTER to proceed with sending the request...
   ```

7. **Request Execution**
   ```
   ✅ Selected: basic-config.json
   
   🚀 Sending PUT request to /cloud/config...
   ✅ Request successful! (Status: 200)
   ```

8. **Response Display**
   ```
   📡 API RESPONSE - /cloud/config
   ==================================================
   ✅ Status: 200
   📄 Response Data:
   ------------------------------
   {
     "status": "success",
     "message": "Configuration updated"
   }
   ```

#### Abort Operation

Users can abort at file selection:
```
🔢 Select JSON file (1-3, 0 to abort): 0
❌ Operation aborted by user

⏸️  Press ENTER to continue...
```

---

## Password Change Operation (`sp / setPassword`)

The password change command is a special PUT operation that works differently from other configuration commands. Instead of using JSON files or interactive prompts, it uses **command-line flags** to collect credentials and change the reader's password.

### Command: `sp / setPassword`

**Endpoint**: `PUT /cloud/updatePassword`

**Authentication**: Requires valid JWT token

**Workflow**: Flag-based arguments (no JSON files, no interactive prompts)

### Command Syntax

The setPassword command requires **all three flags** to be provided:

#### **Short Flags Format**
```
sp -u <username> -c <current_password> -n <new_password>
```

#### **Long Flags Format**
```
setpassword --username <username> --current <current_password> --new <new_password>
```

### Flag Requirements

| Flag | Long Flag | Description | Required |
|------|-----------|-------------|----------|
| `-u` | `--username` | Target username for password change | ✅ Yes |
| `-c` | `--current` | Current password for authentication | ✅ Yes |
| `-n` | `--new` | New password to set | ✅ Yes |

### Important Rules

1. **All three flags are required** - Missing any flag will abort the command
2. **No mixing flag formats** - Cannot mix short (`-u`) and long (`--username`) flags in same command
3. **No duplicate flags** - Each flag can only be used once per command
4. **No empty values** - All flag values must be non-empty strings
5. **Flag validation** - Invalid flags will abort the command with usage help

### Step-by-Step Password Change Process

#### **Step 1: Command with Flags**
```
🎯 API command or shortcut: sp -u admin -c oldpassword -n newpassword
```

**Alternative with long flags:**
```
🎯 API command or shortcut: setpassword --username admin --current oldpassword --new newpassword
```

#### **Step 2: Operation Header**
```
🔑 CHANGE READER PASSWORD
-------------------------
📍 Target: 192.168.2.46
🌐 Endpoint: PUT /cloud/updatePassword
🔑 Authentication: Bearer Token
```

#### **Step 3: Argument Display (Passwords Masked)**
```
📝 Password change details:
👤 Username: admin
🔑 Current Password: ***********
🆕 New Password: ***********
```

**Security Features**:
- ✅ **Password masking**: Passwords are masked with `*` characters in display
- ✅ **No password logging**: Passwords never appear in logs or output files
- ✅ **Input validation**: All arguments are validated before confirmation

#### **Step 4: Confirmation Dialog (Still Required)**
```
⚠️  Are you sure you want to change the password for user 'admin'? [y/N]: y
```

**User can**:
- **Confirm** (`y`): Proceed with password change
- **Cancel** (`N` or any other key): Abort the operation

#### **Step 5: Request Execution**
```
🚀 Sending password change request...
✅ Password change successful! (Status: 200)
🔄 Updating stored credentials and refreshing session...
```

**API Request Format**:
```json
{
  "currentPassword": "<current_password>",
  "newPassword": "<new_password>",
  "userName": "<username>"
}
```

#### **Step 6: Automatic Credential Update**
```
✅ Stored credentials updated
🔄 Refreshing JWT token with new password...
✅ JWT token refreshed successfully!
🎉 Password change completed and session active

==================================================
✅ PASSWORD CHANGE SUCCESSFUL
==================================================
📍 Reader: 192.168.2.46
👤 Username: admin
🔑 Password: Updated successfully
🔑 Token: ✅ Active
==================================================
```

**Automatic Actions After Success**:
1. **Update stored password**: CLI saves new password for future operations
2. **Clear old JWT token**: Invalidates the current token
3. **Auto-refresh token**: Automatically obtains new JWT token with new password
4. **Session continuity**: No need to manually reconnect

### Error Handling & Validation

#### **Missing Required Flags**
```
🎯 API command or shortcut: sp -u admin -c oldpass

❌ Missing required flags for 'sp'
� Usage: sp -u <username> -c <current_password> -n <new_password>
� Or: setpassword --username <username> --current <current_password> --new <new_password>
⏸️  Press ENTER to continue...
```

#### **Invalid Flag**
```
🎯 API command or shortcut: sp -u admin -x invalid -n newpass

❌ Invalid flag '-x'
💡 Valid flags: -u, -c, -n or --username, --current, --new
⏸️  Press ENTER to continue...
```

#### **Mixed Flag Formats**
```
🎯 API command or shortcut: sp -u admin --current oldpass -n newpass

❌ Cannot mix short (-u, -c, -n) and long (--username, --current, --new) flags
💡 Use either: sp -u <username> -c <current_password> -n <new_password>
💡 Or: setpassword --username <username> --current <current_password> --new <new_password>
⏸️  Press ENTER to continue...
```

#### **Duplicate Flags**
```
🎯 API command or shortcut: sp -u admin -u duplicate -c oldpass -n newpass

❌ Duplicate username flag
⏸️  Press ENTER to continue...
```

#### **Empty Values**
```
🎯 API command or shortcut: sp -u "" -c oldpass -n newpass

❌ Username cannot be empty
⏸️  Press ENTER to continue...
```

#### **Simple Arguments (Not Flags)**
```
🎯 API command or shortcut: sp someargument

❌ Command 'sp' does not accept simple arguments
💡 Usage: sp -u <username> -c <current_password> -n <new_password>
💡 Or: setpassword --username <username> --current <current_password> --new <new_password>
⏸️  Press ENTER to continue...
```

#### **API Request Failures**
```
❌ Password change failed!
📊 Status Code: 401
🚫 Error: Current password is incorrect
```

#### **Network Errors**
```
❌ Request error: ConnectTimeout
🔍 Please check your network connection and try again
```

### Command Examples

#### **Valid Commands**
```bash
# Short flags
sp -u admin -c myoldpass -n mynewpass
sp -u user123 -c current123 -n secure456

# Long flags  
setpassword --username admin --current myoldpass --new mynewpass
setpassword --username user123 --current current123 --new secure456
```

#### **Invalid Commands**
```bash
# Missing flags
sp -u admin -c oldpass                    # Missing -n flag

# Mixed formats
sp -u admin --current oldpass -n newpass  # Mixed short/long flags

# Duplicate flags
sp -u admin -u duplicate -c old -n new    # Duplicate -u flag

# Simple arguments
sp myargument                             # Not using flags

# Invalid flags
sp -u admin -x invalid -n newpass         # Invalid -x flag
```

### Security Considerations

- **🔒 No credential exposure**: Passwords are masked in all displays and never logged
- **🔄 Token management**: Old JWT tokens are cleared and new ones obtained automatically
- **🎯 Targeted operation**: Password change only affects the currently targeted reader
- **⚡ Immediate refresh**: New JWT token obtained immediately after successful change
- **🛡️ Validation**: Comprehensive input validation before any API requests
- **⚠️ Confirmation required**: User must still confirm the operation for safety

### Integration with Existing Session

**Before Password Change**:
- User has active session with old password
- JWT token valid for current password

**After Successful Password Change**:
- ✅ New password stored and active
- ✅ New JWT token obtained automatically
- ✅ All subsequent API calls use new credentials
- ✅ No manual reconnection required

**After Failed Password Change**:
- ❌ Old password and token remain unchanged
- ❌ Session continues with original credentials
- ❌ No disruption to existing functionality

### Benefits of Flag-Based Approach

1. **Scriptable**: Can be used in automation scripts and batch operations
2. **Consistent**: Matches the pattern used by GET commands with save flags
3. **Error Prevention**: Validates all inputs before confirmation prompt
4. **No Retry Loops**: Clean single-execution flow with upfront validation
5. **Clear Syntax**: Explicit flag names make commands self-documenting
6. **Flexible Format**: Supports both short and long flag formats

---

## Reboot Operation (`rb / reboot`)

The reboot command is a special PUT operation that restarts the RFID reader. Unlike other PUT commands, it requires no JSON files and sends an empty request body.

### Command: `rb / reboot`

**Endpoint**: `PUT /cloud/reboot`

**Authentication**: Requires valid JWT token

**Request Body**: Empty (no JSON required)

### Step-by-Step Reboot Process

#### **Step 1: Command Selection**
```
🎯 API command or shortcut: rb
```

#### **Step 2: Operation Header & Warning**
```
🔄 REBOOT READER
------------------
📍 Target: 192.168.2.46
🌐 Endpoint: /cloud/reboot
🔑 Authentication: Bearer Token

⚠️  WARNING: This will restart the reader!
📡 All active connections will be lost
⏱️  Reader will be unavailable for ~30-60 seconds
🔌 Any ongoing operations will be interrupted
```

#### **Step 3: Explicit Confirmation**
```
❓ Are you absolutely sure you want to reboot the reader? (yes/no): yes
```

**Security Features**:
- ✅ **Explicit confirmation**: Requires typing "yes" or "y" (not just "y")
- ✅ **Clear warnings**: Multiple warnings about consequences
- ✅ **Cancellation option**: Any response other than "yes" or "y" cancels

#### **Step 4: Request Execution & Response**
```
🔄 Sending reboot command...

📡 REBOOT REQUEST RESPONSE
==================================================
✅ Reboot command sent successfully!
📊 HTTP Status Code: 200
📄 Response Data:
------------------------------
{
  "status": "rebooting",
  "message": "Reader restart initiated"
}
==================================================

💡 NEXT STEPS:
  1. Wait 30-60 seconds for reader to restart
  2. Use 'gl / getlogin' to reconnect to the reader
  3. Verify connection with 'gs / getstatus'
```

### Error Handling

**API Failure Example**:
```
❌ Reboot command failed!
📊 HTTP Status Code: 403
📄 Error Response:
------------------------------
{
  "error": "Insufficient privileges",
  "message": "Reboot operation requires administrator access"
}
==================================================
💡 Reboot failed - check reader connectivity and try again
```

**Network Error Example**:
```
❌ REBOOT REQUEST ERROR
==================================================
🚫 Network/Request Error: ConnectTimeout
💡 Check network connection and reader availability
==================================================
```

### Important Notes

- **No JSON Files**: This command doesn't use the requests-json folder structure
- **No Response Saving**: Reboot responses are not saved to files (simple operation)
- **Connection Impact**: All WebSocket and API connections will be terminated
- **Recovery Time**: Allow 30-60 seconds for complete reader restart
- **Reconnection Required**: Must re-establish JWT token after reboot

---

## File Organization System

### Response File Saving

All API responses are automatically saved with the following structure:

```
api-responses/
└── {IP}_{MODEL}/
    ├── status/
    │   └── status-{MODEL}-{TIMESTAMP}.json
    ├── config/
    │   └── config-{MODEL}-{TIMESTAMP}.json
    ├── mode/
    │   └── mode-{MODEL}-{TIMESTAMP}.json
    └── [other-endpoints]/
        └── {endpoint}-{MODEL}-{TIMESTAMP}.json
```

### File Naming Convention

- **Format**: `{endpoint}-{MODEL}-{TIMESTAMP}.{extension}`
- **Timestamp**: `YYYYMMDD-HHMMSS` (e.g., `20250724-163047`)
- **Model**: Reader model detected from `/cloud/version` (e.g., `FXR90`, `ATR7000`)
- **IP**: Reader IP address for folder organization

### Example File Paths

```
api-responses/192.168.1.100_FXR90/
├── status/status-FXR90-20250724-163047.json
├── config/config-FXR90-20250724-163102.json
├── mode/mode-FXR90-20250724-163115.json
└── syslog/syslog-FXR90-20250724-163130.tar.gz
```

### Reader Model Detection

The system detects reader model via:

1. **Primary Method**: Query `/cloud/version` endpoint
   - Extracts `model` field from response
   - Cleans model name for safe filename usage
   - Caches result for session

2. **Fallback**: Uses "UNKNOWN" if detection fails
   - Network errors
   - Missing model field in response
   - Authentication failures

---

## Authentication & Token Management

### JWT Token Lifecycle

1. **Automatic Acquisition**: On submenu entry
   - Uses Basic Auth to call `/cloud/localRestLogin`
   - Tries HTTPS first, falls back to HTTP
   - Stores token with timestamp

2. **Token Usage**: All subsequent requests use Bearer token
   ```
   Authorization: Bearer {jwt_token}
   ```

3. **Token Refresh**: Manual refresh via `gl / getLogin` command

4. **Session Reset**: Credentials cleared on submenu exit

### Authentication Error Handling

If requests fail due to authentication:
```
🚨 AUTHORIZATION ERROR
=========================
❌ Request unauthorized - JWT token may be expired or invalid
⚠️  Please refresh your authentication!
💡 Use 'l / login' command to obtain a fresh JWT token
🔄 Then try this command again
=========================
```

**Resolution**: Use `gl / getLogin` to refresh the token.

---

## Utility Commands

### Change Target Reader (`t / target`)

Allows switching to a different reader without exiting submenu:

```
🎯 CHANGE TARGET READER
-----------------------
📝 Enter new reader credentials:

📍 New Reader IP: 192.168.1.200
👤 Username [admin]: admin  
🔑 Password: [hidden input]

🔄 Testing connection to new reader...
✅ Connection successful!
🔄 Updating credentials and reinitializing...
✅ Target reader changed successfully!
```

**Features**:
- Automatic credential backup/restore on failure
- Connection validation before switching
- Automatic re-initialization with new reader

### Clear Screen (`c / clear`)

Clears the terminal screen for better visibility.

---

## Integration with Main CLI

### Relationship to WebSocket Functionality

- **Independent Operation**: API submenu operates independently of WebSocket connections
- **Separate Authentication**: Uses its own JWT token system
- **No WebSocket Dependency**: Does not require active WebSocket connection
- **Complementary**: Can be used alongside tag monitoring features

### Main CLI Workflow Integration

1. **Entry Point**: Accessed via `r / restApi` from main menu
2. **Isolated Session**: Maintains separate credential storage
3. **Clean Exit**: Automatically cleans up credentials on return to main menu
4. **No Interference**: Does not affect main CLI WebSocket connections

### Prerequisites

- **Network Connectivity**: Reader must be reachable via HTTP/HTTPS
- **Valid Credentials**: Must have valid username/password for reader
- **Python Dependencies**: `httpx` library for HTTP requests

---

## Error Handling & Validation

### JSON File Validation

```
❌ MALFORMED JSON FILE
📁 File: broken-config.json
🚫 Error: Expecting ',' delimiter: line 5 column 2 (char 45)
🛠️  Please fix the JSON syntax and try again
```

### Missing Folder Structure

```
❌ FOLDER NOT FOUND
📂 Expected folder: requests-json/config/
🛠️  Please create the folder structure:
   1. Create folder: requests-json/config/
   2. Add JSON files to the folder
   3. Try the command again
```

### Empty Folders

```
❌ NO JSON FILES FOUND
📂 Folder exists but no valid JSON files found: requests-json/config/
🛠️  Please add valid JSON files to the folder and try again
```

### API Response Errors

```
❌ Request failed!
📊 Status Code: 400
🚫 Response: {
  "error": "Invalid configuration parameter",
  "details": "Parameter 'invalidField' is not supported"
}
```

---

## Troubleshooting

### Common Network/Connection Issues

**Problem**: Connection timeout or refused
```
❌ HTTP connection error: ConnectTimeout
```
**Solutions**:
- Verify reader IP address is correct
- Check network connectivity (`ping` reader IP)
- Ensure reader is powered on and network interface is active
- Verify firewall settings aren't blocking connections

**Problem**: Protocol issues
```
❌ HTTPS connection error: SSL verification failed
```
**Solutions**:
- Try using HTTP instead of HTTPS (system auto-detects)
- Reader may not have valid SSL certificates
- Check if reader supports HTTPS

### Certificate/HTTPS Problems

**Problem**: SSL certificate errors
```
❌ HTTPS verification failed
```
**Resolution**: The system automatically falls back to HTTP, but you can:
- Check reader's certificate configuration
- Verify reader's HTTPS settings
- Use HTTP if HTTPS is not required

### Authentication Issues

**Problem**: Invalid credentials
```
❌ HTTP 401: Unauthorized
```
**Solutions**:
- Verify username and password
- Check if reader account is not locked
- Ensure credentials have API access permissions

**Problem**: Token expiration
```
🚨 AUTHORIZATION ERROR - JWT token may be expired
```
**Solution**: Use `gl / getLogin` to refresh the token

**Resolution**: Use `gl / getLogin` to refresh the token. If the issue persists, go back to the main menu (`b / back`) and re-enter the API submenu using `r / restApi` command, ensuring you provide the correct reader credentials.

### Password Change Issues

**Problem**: Password change fails after successful API response
```
⚠️  Password change successful but session refresh failed
```
**Solutions**:
- Use `t / target` command to re-enter credentials with new password
- Exit API submenu and re-enter with `r / restApi` using new password
- This typically happens due to network issues during token refresh

**Problem**: Cannot change password - forgot current password
```
❌ Password change failed!
🚫 Error: Current password is incorrect
```
**Solutions**:
- Verify the current password is correct
- If password is truly forgotten, physical access to reader may be required
- Some readers have reset procedures documented in their manuals
- Contact system administrator if reader is managed centrally

**Problem**: Session becomes unusable after failed password change attempt
**Resolution**: 
- The CLI maintains session integrity - failed password changes don't affect existing session
- Current credentials remain active until successful password change
- If session seems corrupted, use `gl / getLogin` to refresh token
```
**Solution**: Use `gl / getLogin` to refresh the token

### Reader-Specific Endpoint Availability

**Problem**: Endpoint not found
```
❌ Request failed!
📊 Status Code: 404
🚫 Response: {"error": "Endpoint not found"}
```
**Causes**:
- Reader model doesn't support the specific endpoint
- Firmware version doesn't include the feature
- Endpoint path incorrect for reader model

**Solutions**:
- Check reader documentation for supported endpoints
- Verify firmware version supports the feature
- Use `gv / getVersion` to confirm reader model and firmware

### File Access Issues

**Problem**: Permission denied saving files
```
❌ Error saving file: Permission denied
🔍 Check if you have write permissions in the project directory
```
**Solutions**:
- Run CLI with appropriate permissions
- Check folder write permissions
- Ensure disk space is available

**Problem**: JSON file read errors
```
❌ ERROR READING FILE
📁 File: config.json
🚫 Error: [Errno 13] Permission denied
```
**Solutions**:
- Check file permissions
- Ensure file is not locked by another application
- Verify file exists and is accessible

---

## Best Practices

### JSON File Management

- **Descriptive Names**: Use clear, descriptive filenames
- **Version Control**: Consider versioning important configurations
- **Testing**: Test JSON files with non-critical endpoints first
- **Backup**: Keep backups of working configurations

### Safe Testing

- **Non-Production**: Test on development/lab readers first
- **Incremental Changes**: Make small configuration changes
- **Backup Configs**: Save current config before making changes
- **Verification**: Use GET commands to verify changes took effect

### Session Management

- **Token Refresh**: Refresh tokens if experiencing auth errors
- **Clean Exit**: Always exit submenu properly to clean up credentials
- **Network Stability**: Ensure stable network connection for operations

### Password Management

- **Current Password**: Always verify current password before attempting change
- **Strong Passwords**: Use strong passwords for reader security
- **Document Changes**: Keep secure record of password changes
- **Test Access**: After password change, verify all functionality still works
- **Backup Access**: Ensure alternative access methods before changing passwords

---

## Command Reference Quick Guide

### GET Commands (Information Retrieval)
```
gl / getlogin - Get JWT token           | gp / getcaps - Get capabilities
gs / getstatus - Get status             | gz / gettimezone - Get timezone  
gv / getversion - Get version           | gx / getcableloss - Get cable loss
gn / getnetwork - Get network config    | ge / getcerts - Get certificates
gr / getregion - Get region config      | gw / getlogs - Get logs config
gm / getmode - Get mode                 | gy / getsyslog - Get system log
gc / getconfig - Get reader config      | 
gi / getgpi - Get GPI status            |
go / getgpo - Get GPO status            |
```

### PUT Commands (Configuration Updates)
```
sn - Set network config     | st - Set timezone
sr - Set region info        | sl - Set logs config
sm - Set mode               | sp - Set password
sc - Set reader config      | rb - Reboot reader
so - Set GPO state          |
```

### Utilities
```
c  - Clear screen          | b - Back to main menu
t  - Change target reader  |
```

---

## Testing

### Automated Test Suite

The API submenu functionality is covered by a comprehensive automated test suite located in `test_api_submenu.py`. This test suite provides complete coverage for the `ApiSubmenu` class and all its methods.

**Important**: These are unit tests that use mocking and do not require actual RFID reader hardware to run.

### Running the Tests

The tests require the virtual environment to be activated. From the project root directory:

**Windows (PowerShell):**
```powershell
.venv\Scripts\python.exe -m pytest test_api_submenu.py -v
```

**Alternative using pytest directly:**
```powershell
.venv\Scripts\pytest.exe test_api_submenu.py -v
```

**Unix/Linux/macOS:**
```bash
.venv/bin/python -m pytest test_api_submenu.py -v
```

**Alternative using pytest directly:**
```bash
.venv/bin/pytest test_api_submenu.py -v
```

### Test Coverage

The test suite includes comprehensive testing for `api_submenu.py` covering:
- **Authentication and JWT token management**
- **All GET endpoint operations** with argument-based saving (`-y`/`--yes`, `-n`/`--no`, no argument)
- **All PUT endpoint operations** with JSON file selection
- **Argument parsing logic** for GET commands with validation
- **Response saving functionality** with automatic file organization  
- **Special getSyslog handling** (binary .tar.gz files vs JSON responses)
- **File operations and JSON handling** with reader-specific directories
- **Password management functionality** with secure input handling
- **Error handling scenarios** including invalid arguments and network failures
- **User input validation** and command execution prevention
- **Network request mocking** for isolated unit testing

#### New Test Features (Argument-Based Saving)

The updated test suite specifically validates:
- **Argument parsing**: Tests for `-y`, `--yes`, `-n`, `--no`, and invalid arguments
- **Save parameter propagation**: Ensures `save_response` parameter is correctly passed to all GET handlers
- **getSyslog special behavior**: Verifies that binary files are saved while JSON responses are not
- **Command execution prevention**: Tests that invalid arguments abort commands with helpful messages
- **Backward compatibility**: All existing functionality continues to work as expected

### Prerequisites

No additional test dependencies are required - `pytest` is already included in the project's requirements. The tests use Python's built-in mocking capabilities and the existing project dependencies.

---

*This documentation covers the complete API submenu functionality. For main CLI features, refer to the main project README.md.*
