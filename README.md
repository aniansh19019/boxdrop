# BoxDrop - An Efficient File Synchronization Service

BoxDrop is a Dropbox-like file synchronization service that enables users to sync files across multiple devices. It uses advanced techniques for efficient storage and bandwidth usage.

## Key Features

- **Efficient File Chunking**: Uses FastCDC (Fast Content-Defined Chunking) algorithm to break files into chunks
  - Only uploads new/modified chunks, saving bandwidth
  - Deduplicates data by storing identical chunks only once
  - Optimizes storage usage across all users' files

- **Real-time Synchronization**
  - Watches for file system changes (create/modify/delete/move)
  - Automatically syncs changes across all user devices
  - Uses message queues for reliable cross-device communication
  - Maintains file consistency across devices

- **Cloud Storage Backend**
  - Uses Amazon S3 for reliable chunk storage
  - Metadata stored separately from file chunks
  - Efficient chunk-level retrieval and storage

- **User Management**
  - User authentication and authorization
  - Per-user storage quota management
  - Multiple device support per user

## Architecture

The system consists of several key components:

1. **File Chunker (chunker.py)**
   - Breaks files into variable-sized chunks using FastCDC
   - Manages chunk metadata and file versioning
   - Handles file operations (create/update/delete/move)

2. **Storage Manager (store.py)**
   - Interfaces with Amazon S3 for chunk storage
   - Handles chunk upload/download operations
   - Manages chunk existence verification

3. **File Watcher (watcher.py)**
   - Monitors file system changes in real-time
   - Triggers appropriate handlers for file events
   - Manages synchronization across devices

4. **Message Queue System (mq_sender.py, mq_receiver.py)**
   - Handles cross-device communication
   - Ensures reliable message delivery
   - Maintains synchronization order

5. **Metadata Database (metadata_db.py)**
   - Stores file and chunk metadata
   - Manages file versioning
   - Tracks user information and quotas

## Usage Instructions

### Prerequisites
- Python 3
- virtualenv
- MacOS or Linux system

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd boxdrop
```

2. Run the installation script:
```bash
chmod u+x install.sh
./install.sh
```

3. Start the BoxDrop client:
```bash
./run.sh
```

4. Follow the prompts to:
   - Create an account or login
   - A new BoxDrop folder will be created in your home directory
   - The folder name will include a unique identifier: `BoxDrop<random_id>`

### Using BoxDrop

1. **Adding Files**
   - Simply copy or save files into your BoxDrop folder
   - Files will automatically sync to the cloud
   - Only new/changed chunks are uploaded

2. **Multi-device Setup**
   - Install BoxDrop on other devices
   - Login with the same account
   - Files will automatically sync across devices

3. **File Operations**
   - Create, modify, delete, or move files normally
   - All changes sync automatically
   - Conflicts are handled based on timestamp

## Implementation Details

### Chunking Algorithm

BoxDrop uses FastCDC for content-defined chunking, which:
- Creates variable-sized chunks based on content
- Ensures efficient handling of insertions/deletions
- Maintains chunk boundaries based on content, not fixed positions

### Storage Optimization

The system optimizes storage by:
- Storing each unique chunk only once
- Using content-based addressing (SHA-256 hashing)
- Tracking chunk usage across files
- Only uploading modified chunks during updates

### Synchronization Process

1. File system changes are detected by the watcher
2. Changed files are chunked and analyzed
3. New/modified chunks are uploaded to S3
4. Metadata is updated in the database
5. Change notifications are sent via message queue
6. Other devices receive updates and sync accordingly

## Future Improvements

- [ ] Add chunk database to track chunk usage count
- [ ] Implement deleted file restoration
- [ ] Increase chunk count for better deduplication
- [ ] Improve file metadata updates during restoration
- [ ] Add concurrent chunk upload/download support
- [ ] Implement proper change queue management
