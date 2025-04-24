
## Background

This project aims to implement a simple, reliable folder synchronization tool between a client and a server. The use case involves scenarios where content from a selected folder on the server should always be up-to-date on the client side. The system is designed for Linux environments initially, focusing on maintaining a consistent mirror of a chosen folder in real time or near real time.

The project may evolve to support multiple server nodes and a command-capable UI client. But the immediate scope is focused on a robust MVP for synchronizing one folder out of several preconfigured directories from server to client.

## Requirements

### Must Have
- Two-way synchronization of a single chosen folder between client and server
- Synchronization must include all text-based files and ignore non-text files
- The folder to synchronize is chosen from a set of predefined folders on the server
- Configurable synchronization interval, with a minimum of 5 seconds latency
- Initial implementation for Linux-based environments on both server and client
- Conflict resolution strategy (e.g., last-write-wins or timestamp-based)

### Should Have
- Efficient transfer using file diffs or hash-based change detection
- Logging of synchronization activity
- Ability to restart synchronization after a crash/resume

### Could Have
- Support for multiple server nodes (future)
- Client-side UI to choose folder and run commands on server (future)

### Won't Have (for now)
- Support for binary or non-text files
- Cross-platform (Windows/macOS) support

## Method

### Architecture Overview

```
Client                Server
------                ------
[Watcher]             [Watcher]
    |                     |
[SyncMgr] <--------> [SyncMgr]
    |                     |
[Socket]   <------->   [Socket]
```

- Both server and client run local `inotify` watchers.
- When a file is created, modified, or deleted, the watcher triggers a sync event.
- Each side has a Sync Manager that handles:
  - Change detection
  - File filtering (text files only)
  - Timestamp-based conflict resolution
  - Efficient file transfer
- Sync communication is over TCP sockets using a custom lightweight protocol with JSON metadata and raw file chunks.

### Sync Rules and Event Semantics

- **Server**:
  - Full control: create, update, delete, rename, move
  - Watches all inotify events
- **Client**:
  - Edit-only: only modify file content
  - Only `IN_MODIFY` is a valid trigger
- **Conflict Resolution**:
  - Timestamp-based
  - If timestamps match, server wins

### Folder and File Rules

- One active folder from a predefined list (server config)
- Only text files included:
  - `.txt`, `.md`, `.json`, `.csv`, `.yaml`, `.py`, etc.
- Binary files and hidden files are ignored
- MIME or content-based validation may be used

### Synchronization Protocol

#### Message Format

All messages are JSON strings with a 4-byte length prefix. File content (if present) follows.

#### Types

| Type          | Description                         |
|---------------|-------------------------------------|
| FILE_UPDATE   | Sync file create/modify with content |
| FILE_DELETE   | Remove file                         |
| FILE_MOVE     | Rename or move                      |
| PING          | Heartbeat                           |
| ERROR         | Protocol or sync error              |

#### File Content Transfer

- Sent right after JSON metadata
- Receiver checks MIME type, timestamp, hash
- Prevents unnecessary overwrites

### Sync State Tracking

#### SQLite Schema

```sql
CREATE TABLE file_state (
    path TEXT PRIMARY KEY,
    last_modified TEXT,
    sha256 TEXT,
    origin TEXT
);
```

- Tracks last known state of each file
- Used for sync decision-making and resync after restart
- `origin` prevents sync loops

### Startup Behavior

- Full folder scan
- DB comparison
- Apply deltas based on conflict rules

## Implementation

### Project Structure

```
folder_sync/
├── client/
│   ├── watcher.py
│   ├── sync_manager.py
│   ├── transport.py
│   └── main.py
├── server/
│   ├── watcher.py
│   ├── sync_manager.py
│   ├── transport.py
│   └── main.py
├── common/
│   ├── protocol.py
│   ├── file_utils.py
│   └── logger.py
```

### Component Roles

- `watcher.py`: inotify monitor
- `sync_manager.py`: state manager, conflict resolution
- `transport.py`: TCP socket comms
- `protocol.py`: message definitions
- `file_utils.py`: hashing, filtering
- `logger.py`: unified logging

### Development Phases

1. Setup project, folders, and config
2. Implement transport & JSON protocol
3. Integrate inotify via `watchdog` or `pyinotify`
4. Develop sync manager with SQLite
5. Build startup scan logic
6. Add retry logic and tests

## Milestones

### Milestone 1: Project Initialization (Week 1)
- Define structure, config, and logging

### Milestone 2: Protocol and Transport (Week 2)
- TCP socket with JSON + file stream

### Milestone 3: Inotify and Sync Manager (Week 3)
- Real-time event handling and DB tracking

### Milestone 4: Two-Way Sync Logic (Week 4)
- Edit-only client
- Full control server
- Conflict resolution

### Milestone 5: Testing and Verification (Week 5)
- Validate correctness, deletions, renames

### Milestone 6: Production Hardening (Week 6)
- Add retries, error logs, config tuning
