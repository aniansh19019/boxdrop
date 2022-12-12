import os
class Config:
    test_mode = False
    # TODO: make the root dir before accessing
    ROOT_DIR = os.path.abspath("~/BoxDrop")
    # ROOT_DIR = "../example_sync_dir"
    # ROOT_DIR = "client_one"
    # ROOT_DIR = "client_two"
    RABBIT_MQ_IP = "34.224.214.95"
    # RABBIT_MQ_IP = "localhost"
    MAX_CHUNK_SIZE = 1048576 # Max chunk size in bytes
    MIN_CHUNK_SIZE = 1024 # Minimum chunk size in bytes
    CACHE_SIZE = 1024 # Number of chunks to store in the offline cache
    SKIP_FILES = ['.DS_Store', '__pycache__', '.vscode']