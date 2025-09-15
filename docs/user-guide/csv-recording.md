# WebSocket CSV Recording Feature

This document describes the CSV recording functionality added to the WebSocket listener in the Zebra RFID CLI application.

## Overview

The WebSocket listener automatically records RFID tag data and all WebSocket messages to CSV files when recording is active. This feature enables data analysis, debugging, and historical tracking of RFID events.

## Features

### Two CSV Files Created

When recording is active, two CSV files are created in organized directories:

1. **`record/messages/messages_read_<timestamp>.csv`** - Contains all raw WebSocket messages (created immediately when recording starts)
2. **`record/tag_reads/tags_read_<timestamp>.csv`** - Contains processed tag statistics (created when recording stops)

Note: The IOTC WebSocket setup of this CLI will set only the TagData interface as WebSocket, so only tag reads data messages will be received.

**ATR7000 Reader Limitation**: For ATR7000 readers, only the `messages_read_<timestamp>.csv` file is generated during CSV recording. The tag statistics CSV (`tags_read_<timestamp>.csv`) is not currently supported for ATR7000 readers due to different message format processing requirements.

### File Organization

CSV files are automatically organized in the project directory structure:
- **Tag reads**: `<project_root>/record/tag_reads/tags_read_<timestamp>.csv`
- **Messages**: `<project_root>/record/messages/messages_read_<timestamp>.csv`

The directories are created automatically when recording starts if they don't already exist.

### File Naming

Files use the timestamp format: `YYYYMMDD_HHMMSS`
- Example: `record/tag_reads/tags_read_20240908_143022.csv`
- Example: `record/messages/messages_read_20240908_143022.csv`

### CSV File Formats

#### Tags CSV (`tags_read_<timestamp>.csv`)
Contains aggregated RFID tag statistics with the following columns (identical to TagTableWindow export):
- **EPC**: Tag EPC/ID in hexadecimal format
- **Reads**: Total number of times the tag was detected
- **Avg_RSSI**: Average signal strength in dBm
- **Min_RSSI**: Minimum signal strength recorded
- **Max_RSSI**: Maximum signal strength recorded  
- **First_Seen**: Timestamp when tag was first detected
- **Last_Seen**: Timestamp when tag was last detected
- **Rate_Per_Minute**: Average detection rate per minute

#### Messages CSV (`messages_read_<timestamp>.csv`)
Contains all WebSocket messages with the following columns:
- **Timestamp**: When the message was processed (YYYY-MM-DD HH:MM:SS.mmm)
- **Message_Type**: Type of message (tagRead, heartbeat, gpo, RAW_DIRECTIONALITY, etc.)
- **Raw_JSON**: Complete JSON message as received

## Behavior

### Recording Process

**When `start_recording()` is called:**
- Creates and opens `messages_read_<timestamp>.csv` immediately
- Starts collecting tag data in memory (like TagTableWindow)
- All WebSocket messages are written to messages CSV in real-time

**During recording:**
- Tag data is processed and aggregated in memory
- Statistics are calculated and updated for each tag
- No tag CSV file is created yet

**When `stop_recording()` is called:**
- Exports collected tag statistics to `tags_read_<timestamp>.csv`
- Closes the messages CSV file
- Clears memory and resets for next recording session

### Tag Data Processing

The tag data processing follows the exact same logic as `TagTableWindow`:
- RSSI values are collected and averaged
- Read counts are accumulated
- Location data (azimuth/elevation) is preserved when available
- Multiple reads per message are handled correctly
- Invalid RSSI values default to -50.0 dBm

### File Creation
- **Messages CSV**: Created immediately when recording starts
- **Tags CSV**: Created only when recording stops (contains complete statistics)
- **Fresh files**: Each recording session gets new files with new timestamps
- **No appending**: Previous recording data is never modified

## Integration with CLI

The CSV recording feature integrates seamlessly with the existing CLI interface and replicates the TagTableWindow export functionality:

1. Use any WebSocket monitoring option (7, 8, 9, t)
2. Recording can be controlled through the recording flag
3. Tag CSV provides identical data to "Export CSV" button in TagTableWindow
4. Files are saved in the record/messages and record/tag_reads folders (generated at runtime if not existent)

## Example Data

### Tags CSV Sample (Aggregated Statistics)
```csv
EPC,Reads,Avg_RSSI,Min_RSSI,Max_RSSI,First_Seen,Last_Seen,Rate_Per_Minute
E280116060000020394C3F25,145,-42.3,-45.2,-38.1,2024-09-08 14:30:15,2024-09-08 14:32:45,58.7
E280116060000020394C3F26,87,-48.7,-52.1,-44.3,2024-09-08 14:30:16,2024-09-08 14:32:40,35.2
```

### Messages CSV Sample (Real-time Log)
```csv
Timestamp,Message_Type,Raw_JSON
2024-09-08 14:30:15.123,tagRead,"{""type"":""tagRead"",""data"":{""idHex"":""E280116060000020394C3F25"",""peakRssi"":-45.2}}"
2024-09-08 14:30:16.000,heartbeat,"{""type"":""heartbeat""}"
```