class Config:
    test_mode = True
    # ROOT_DIR = "~/BoxDrop"
    ROOT_DIR = "../example_sync_dir"
    RABBIT_MQ_IP = "34.224.214.95"
    MAX_CHUNK_SIZE = 4096 # Max chunk size in bytes
    MIN_CHUNK_SIZE = 256 # Minimum chunk size in bytes
    CACHE_SIZE = 1024 # Number of chunks to store in the offline cache
    SKIP_FILES = ['.DS_Store', '__pycache__']