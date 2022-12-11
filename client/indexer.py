from config import Config
import os
import shutil
import chunker
import metadata_db
import store

def handle_update_message(message, watcher_ref):

    print("Pausing the watcher before applying received updates!")
    # Pause the watcher
    watcher_ref.stop()

    src_path = message['src_path']

    if message['event_type'] == 'created':
        if message['is_dir']:
            create_dir(src_path)
        else:
            create_file(src_path)

    elif message['event_type'] == 'modified':
        if message['is_dir']:
            modify_dir(src_path)
        else:
            modify_file(src_path)

    elif message['event_type'] == 'moved':
        dest_path = message['dest_path']
        if message['is_dir']:
            move_dir(src_path, dest_path)
        else:
            move_file(src_path, dest_path)
        pass
    elif message['event_type'] == 'deleted':
        if message['is_dir']:
            delete_dir(src_path)
        else:
            delete_file(src_path)
        pass
    # resume the watcher
    watcher_ref.start()
    print("Resuming Watcher")
    



# ! updates might be slow
def create_file(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)
    file_record = metadata_db.get_file_record_from_path(rel_path)
    hash_str = file_record['chunks'][-1]
    hashes = str(hash_str).splitlines()
    chunker.build_file_from_chunks(hashes, abs_path)
    print("New File {} created successfully!".format(rel_path))
    pass

# ! updates might be slow
def create_dir(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)
    # make directory
    os.makedirs(abs_path, exist_ok=True)
    print("Directory {} created successfully!".format(abs_path))
    pass

# ! updates might be slow
def modify_file(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)
    old_chunks = chunker.get_chunks(abs_path)
    chunk_map = {}
    for chunk in old_chunks:
        chunk_map[chunk.hash] = chunk.data
    old_hash_str = chunker.get_hashes(old_chunks)


    # get new file metadata
    new_file_record = metadata_db.get_file_record_from_path(rel_path)
    new_hash_str = new_file_record['chunks'][-1]
    new_hashes = str(new_hash_str).splitlines()
    for hash in new_hashes:
        if hash not in chunk_map.keys():
            if store.chunk_exists(hash):
                chunk_map[hash] = store.get_chunk(hash)
            else:
                print("Chunk {} not found!".format(hash))
    
    # remove old file
    os.remove(abs_path)

    # write the new file
    with open(abs_path, "ab") as out_ref:
        total_hashes = len(new_hashes)
        current_hash = 1
        for hash in new_hashes:
            print("\rRetrieving Chunk {} of {}".format(current_hash, total_hashes), end="")
            out_ref.write(chunk_map[hash])
            current_hash += 1
        print()
    print("File {} modified sucessfully!".format(rel_path))
    
    pass

def modify_dir(rel_path):
    pass


def move_file(rel_src, rel_dest):
    abs_src = os.path.join(Config.ROOT_DIR, rel_src)
    abs_dest = os.path.join(Config.ROOT_DIR, rel_dest)
    # move file
    shutil.move(abs_src, abs_dest)
    print("Moved file {} to {}".format(rel_src, rel_dest))

    pass

def move_dir(rel_src, rel_dest):
    abs_src = os.path.join(Config.ROOT_DIR, rel_src)
    abs_dest = os.path.join(Config.ROOT_DIR, rel_dest)
    # move directory
    shutil.move(abs_src, abs_dest)
    print("Moved directory {} to {}".format(rel_src, rel_dest))
    pass


def delete_file(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)
    # delete the file
    if os.path.exists(abs_path):
        os.remove(abs_path)
        print("Removed file {}".format(rel_path))
    else:
        print("File {} already removed".format(rel_path))


    pass

def delete_dir(rel_path):
    abs_path = os.path.join(Config.ROOT_DIR, rel_path)

    # delete the folder with all the contents
    shutil.rmtree(abs_path, ignore_errors=True)
    print("Removed file {}".format(rel_path))


    pass

