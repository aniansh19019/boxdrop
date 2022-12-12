from fastcdc import fastcdc
import hashlib
import uuid
import os
import queue
import datetime
import store
import metadata_db
import config
import watcher
import sys
import shutil
import auth

# TODO: add chunks database to keep track of the use count of each chunk
# TODO: add the option to restore deleted files
# TODO: consider adding a queue of changes
# TODO: increase chunk count
# TODO: update file metadata when the file is restored
# TODO: File not found on moving file
# TODO: Problem when the same file is being uploaded again after being deleted. Gives duplicate records by file_path

# * set auto commit to False for performance
# file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)
# chunk_db = sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=False, outer_stack= False)

def get_hashes(chunks):
    retval = ""
    for chunk in chunks:
        retval += str(chunk.hash) + "\n"
    return retval

def get_chunks(filename):
    return list(fastcdc(filename, config.Config.MIN_CHUNK_SIZE, config.Config.MAX_CHUNK_SIZE, config.Config.MAX_CHUNK_SIZE, True, hashlib.sha256))


def chunk_and_upload_file(filepath):

    file = os.path.basename(filepath)
    # Check if file is to be skipped
    if file in config.Config.SKIP_FILES:
        print("Skipping {}".format(filepath))
        return
    print("Uploading chunks for {}".format(file))
    chunks = get_chunks(filepath)
    print("Chunks Generated! Uploading Chunks!")
    hash_str = get_hashes(chunks)
    # Upload chunks
    total_chunks = len(chunks)
    current_chunk = 1
    for chunk in chunks:
        print("\rChunk {} of {}".format(current_chunk, total_chunks), end="")
        if not store.chunk_exists(chunk.hash):
            chunk_record = {'hash': chunk.hash, 'use_count': 1}
            # store chunk in s3 store
            store.put_chunk(chunk.hash, chunk.data)
            # store chunk data in metadata_db
            metadata_db.put_chunk_record(chunk_record)

        current_chunk+=1
    print()
    # chunk_db.commit()
    print("Chunks Uploaded!")
    rel_path = os.path.relpath(filepath, config.Config.ROOT_DIR)
    # Add entry for file
    db_data = {
    "id": uuid.uuid4().hex,
    "version": 1,
    "is_dir": False,
    "is_deleted": False,
    "path": rel_path,
    "size": os.path.getsize(filepath),
    "owner": auth.user_email(),
    "date_uploaded": datetime.datetime.now().timestamp(),
    "date_created": os.path.getctime(filepath),
    "date_modified": os.path.getmtime(filepath),
    "chunks": [hash_str],
    "editors": [],
    "viewers": []
    }
    
    # Add to metadata db
    metadata_db.put_file_record(db_data)
    return db_data['id']


def create_directory_record(dir_path):
    dir_path = os.path.abspath(dir_path)
    rel_path = os.path.relpath(dir_path, config.Config.ROOT_DIR)
    # Add entry for directory
    db_data = {
            "id": uuid.uuid4().hex,
            "version": 1,
            "is_dir": True,
            "is_deleted": False,
            "path": rel_path,
            "size": os.path.getsize(dir_path),
            "owner": auth.user_email(),
            "date_uploaded": datetime.datetime.now().timestamp(),
            "date_created": os.path.getctime(dir_path),
            "date_modified": os.path.getmtime(dir_path),
            "children": list(),
            "editors": [],
            "viewers": []
            }
    
    # add to metadata_db
    metadata_db.put_file_record(db_data)
    return db_data['id']
   

def build_directory_tree_metadata(sync_dir):
    abs_path = os.path.abspath(sync_dir)
    assert os.path.isdir(abs_path)
    retval = None
    for (root, dirs, files ) in os.walk(abs_path, topdown=False):
        # Check if the directory is to be skipped
        rel_path = os.path.relpath(root, abs_path)
        if rel_path in config.Config.SKIP_FILES:
            print("Skipping {}".format(root))
            continue

        print("Root: {}".format(root))
        for file in files:
            filepath = os.path.join(root, file)
            chunk_and_upload_file(filepath)


        # Add root directory to db
        dir_id = create_directory_record(root)
        repopulate_parent_directory(root)

        
        if root == abs_path:
            retval = dir_id
        print('------------------------------')
    print("Directory Tree Built Successfully!")
    return retval


def restore_directory_tree(parent_dir, root_id):
     # * open db files
    # file_db = get_file_db()
    # chunk_db = get_chunk_db()

    root_record = metadata_db.get_file_record_from_id(root_id)
    
    assert root_record['is_dir']

    dir_queue = queue.Queue()

    file_path = root_record['path']
    file_path = os.path.join(parent_dir, file_path)
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    dir_queue.put(root_record)

    while not dir_queue.empty():
        item = dir_queue.get()
        print("Building contents of {}".format(item['path']))
        for child_id in item['children']:
            child = metadata_db.get_file_record_from_id(child_id)
            # check if the child is deleted in the metadata
            if child['is_deleted']:
                # skip the child if it is deleted
                continue
            file_path = child['path']
            file_path = os.path.join(parent_dir, file_path)
            file_path = os.path.abspath(file_path)
            if child['is_dir']:
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
                dir_queue.put(child)
            else:
                print("Rebuilding {}".format(child['path']))
                chunk_hashes = str(child['chunks'][-1]).splitlines()
                build_file_from_chunks(chunk_hashes, file_path)
                
    print("Directory rebuilt successfully from tree!")



def create_file_metadata(file_path):
    # rel_path = os.path.relpath(file_path, config.Config.ROOT_DIR)

    if os.path.isdir(file_path):
        # Create directory record
        create_directory_record(file_path)
    elif os.path.isfile(file_path):
        # Add entry for file
        chunk_and_upload_file(file_path)
    
    # Repopulate the parent directory

    parent_path = os.path.dirname(file_path)
    repopulate_parent_directory(parent_path)
    print("File record created successfully!")


def delete_file_metadata(file_path):
    # Update the given file's metadata

    rel_path = os.path.relpath(file_path, config.Config.ROOT_DIR)
    file_record = metadata_db.get_file_record_from_path(rel_path)

    file_record['is_deleted'] = True

    # add deleted time
    file_record['deleted_time'] = datetime.datetime.now().timestamp()



    # update the metadata db
    metadata_db.update_file_record(file_record)
    print("File deleted from records!")
    

    pass

def update_file_metadata(file_path):

    # Update the given file's metadata

    rel_path = os.path.relpath(file_path, config.Config.ROOT_DIR)
    file_record = metadata_db.get_file_record_from_path(rel_path)

    if os.path.isfile(file_path):
        new_chunks = get_chunks(file_path)
        new_hashes = get_hashes(new_chunks)
        old_hash_set = set(str(file_record['chunks']).splitlines())
        
        # Upload all new chunks
        total_hashes = len(new_chunks)
        current_hash = 1
        for chunk in new_chunks:
            if chunk.hash not in old_hash_set:
                if not store.chunk_exists(chunk.hash):
                    print("\rProcessing New Chunk {} of {}".format(current_hash, total_hashes), end="")
                    chunk_record = {'hash': chunk.hash, 'use_count': 1}
                    # upload new chunk to store
                    store.put_chunk(chunk.hash, chunk.data)
                    # update chunk db
                    metadata_db.put_chunk_record(chunk_record)
                    current_hash += 1
        

        print()

        # Make changes to the metadata file


        file_record['chunks'].append(new_hashes)
        file_record['version'] += 1
        file_record['date_modified'] = datetime.datetime.now().timestamp()

        # update the metadata db
        metadata_db.update_file_record(file_record)
    
    elif os.path.isdir(file_path):
        # if a directory is updated, we need to repopulate the directory children
        repopulate_parent_directory(file_path)

    

    print(f"{file_path} metadata updated successfully!")

    pass


def repopulate_parent_directory(dir_path):
    assert os.path.isdir(dir_path)

    # Update the given directory's children field

    rel_path = os.path.relpath(dir_path, config.Config.ROOT_DIR)

    dir_record = metadata_db.get_file_record_from_path(rel_path)

    # dir_id = dir_record['id']
    # dir_record = file_db[dir_id]

    # dir_record['children'] = []

    real_contents = os.listdir(dir_path)

    # * add new items to the children
    for item in real_contents:
        if item in config.Config.SKIP_FILES:
            continue
        item_path = os.path.join(dir_path, item)
        item_rel_path = os.path.relpath(item_path, config.Config.ROOT_DIR)
        item_id = metadata_db.get_file_record_from_path(item_rel_path)['id']
        # print(dir_record)
        # add only if the item does not already exist
        # check if children exist at all
        if item_id not in dir_record['children']:
            dir_record['children'].append(item_id)

    
    # * remove items not in the directory
    
    items_to_remove = []
    for child_id in dir_record['children']:
        child_record = metadata_db.get_file_record_from_id(child_id)
        child_rel_path = child_record['path']
        child = os.path.basename(child_rel_path)
        if child not in real_contents:
            if not child_record['is_deleted']:
                items_to_remove.append(child_id)
    
    for item in items_to_remove:
        dir_record['children'].remove(item)


    # update modified time
    dir_record['date_modified'] = os.path.getmtime(dir_path)
    # update the metadata db
    metadata_db.update_file_record(dir_record)
    print(f"{dir_path} children field updated successfully!")

    pass
    

def move_file_metadata(src, dst):
    # Update the given file's metadata

    src_rel_path = os.path.relpath(src, config.Config.ROOT_DIR)
    dst_rel_path = os.path.relpath(dst, config.Config.ROOT_DIR)
    src_record = metadata_db.get_file_record_from_path(src_rel_path)

    src_record['path'] = dst_rel_path

    # update the modified time
    src_record['date_modified'] = os.path.getmtime(dst)

    # print(f"src_record: {src_record}")


    # update the metadata db
    metadata_db.update_file_record(src_record)
    print("File metadata moved successfully!")

    pass

def build_file_from_chunks(chunk_hashes, file_path):
    with open(file_path, "ab") as out_ref:
        total_hashes = len(chunk_hashes)
        current_hash = 1
        for hash in chunk_hashes:
            print("\rChunk {} of {}".format(current_hash, total_hashes), end="")
            chunk_data = store.get_chunk(hash)
            out_ref.write(chunk_data)
            current_hash += 1
        print()
            







if __name__ == "__main__":
    
    root_id = ""
    if len(sys.argv) == 3:
        if sys.argv[1] == "1":
            config.Config.ROOT_DIR = "client_one"
        elif sys.argv[1] == "2":
            config.Config.ROOT_DIR = "client_two"
        if sys.argv[2] == "scan":
            config.Config.ROOT_DIR = "../example_sync_dir"
            # remove all internal db
            shutil.rmtree("internal_db")
            os.mkdir("internal_db")
            root_id = build_directory_tree_metadata(config.Config.ROOT_DIR)
        elif sys.argv[2] == "rebuild":
            root_id = '9da31e8d66e649598d4e012c8f4727bd'
            # remove all rebuild dirs
            if sys.argv[1] == "1":
                shutil.rmtree("client_one")
                os.mkdir("client_one")
            elif sys.argv[1] == "2":
                shutil.rmtree("client_two")
                os.mkdir("client_two")
            restore_directory_tree(config.Config.ROOT_DIR, root_id)
        elif sys.argv[2] == "watch":
            watcher.Watcher()

    pass




