from fastcdc import fastcdc
import sqlitedict
import hashlib
import difflib
import uuid
import os
import random
import queue
import time
import datetime

random.randrange(0, 1000000000000)

MAX_CHUNK_SIZE = 4096 # Max chunk size in bytes
MIN_CHUNK_SIZE = 256 # Minimum chunk size in bytes
CACHE_SIZE = 1024 # Number of chunks to store in the offline cache
SKIP_FILES = ['.DS_Store', '__pycache__']
ROOT_DIR = os.path.abspath('../example_sync_dir')

# TODO: add chunks database to keep track of the use count of each chunk
# TODO: add the option to restore deleted files
# TODO: consider adding a queue of changes

# * set auto commit to False for performance
# file_db = sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)
# chunk_db = sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=False, outer_stack= False)

def get_file_db():
    return sqlitedict.SqliteDict("internal_db/file.db", autocommit= True)

def get_chunk_db():
    return sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=False, outer_stack= False)

def get_hashes(chunks):
    retval = ""
    for chunk in chunks:
        retval += str(chunk.hash) + "\n"
    return retval

def get_chunks(filename):
    return list(fastcdc(filename, MIN_CHUNK_SIZE, MAX_CHUNK_SIZE, MAX_CHUNK_SIZE, True, hashlib.sha256))


def chunk_and_upload_file(filepath, file_db, chunk_db):

    file = os.path.basename(filepath)
    # Check if file is to be skipped
    if file in SKIP_FILES:
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
        if chunk not in chunk_db.keys():
            chunk_db[chunk.hash] = {'hash': chunk.hash, 'data': chunk.data, 'use_count': 1}
        current_chunk+=1
    print()
    chunk_db.commit()
    print("Chunks Uploaded!")
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    # Add entry for file
    db_data = {
    "id": uuid.uuid4().hex,
    "version": 1,
    "is_dir": False,
    "is_deleted": False,
    "path": rel_path,
    "size": os.path.getsize(filepath),
    "owner": "aniansh@yahoo.com",
    "date_uploaded": datetime.datetime.now().timestamp(),
    "date_created": os.path.getctime(filepath),
    "date_modified": os.path.getmtime(filepath),
    "chunks": [hash_str],
    "editors": [],
    "viewers": []
    }
    
    # Add to internal db
    file_db[db_data['id']] = db_data
    # Reverse map to get id from  path
    file_db[rel_path] = db_data['id']

    return db_data['id']


def create_directory_record(dir_path, file_db, chunk_db):
    dir_path = os.path.abspath(dir_path)
    rel_path = os.path.relpath(dir_path, ROOT_DIR)
    # Add entry for directory
    db_data = {
            "id": uuid.uuid4().hex,
            "version": 1,
            "is_dir": True,
            "is_deleted": False,
            "path": rel_path,
            "size": os.path.getsize(dir_path),
            "owner": "aniansh@yahoo.com",
            "date_uploaded": datetime.datetime.now().timestamp(),
            "date_created": os.path.getctime(dir_path),
            "date_modified": os.path.getmtime(dir_path),
            "children": list(),
            "editors": [],
            "viewers": []
            }
    file_db[db_data['id']] = db_data
    # Reverse map to get id from  path
    file_db[rel_path] = db_data['id']
    # repopulate_parent_directory(dir_path, db_data, file_db)
    return db_data['id']
   

def build_directory_tree_metadata(sync_dir):
    # * open db files
    file_db = get_file_db()
    chunk_db = get_chunk_db()

    abs_path = os.path.abspath(sync_dir)
    assert os.path.isdir(abs_path)
    retval = None
    for (root, dirs, files ) in os.walk(abs_path, topdown=False):
        # Check if the directory is to be skipped
        rel_path = os.path.relpath(root, abs_path)
        if rel_path in SKIP_FILES:
            print("Skipping {}".format(root))
            continue

        print("Root: {}".format(root))
        root_children = []
        for file in files:
            filepath = os.path.join(root, file)
            file_id = chunk_and_upload_file(filepath, file_db, chunk_db)
            root_children.append(file_id)


        # Add root directory to db
        dir_id = create_directory_record(root, file_db, chunk_db)
        repopulate_parent_directory(root, file_db[dir_id],file_db)

        
        # return the id of the root
        if root == abs_path:
            print(root)
            retval = dir_id
        print('------------------------------')
    print("Directory Tree Built Successfully!")
    # * close db files
    file_db.close()
    chunk_db.close()
    return retval


def restore_directory_tree(parent_dir, root_id):
     # * open db files
    file_db = get_file_db()
    chunk_db = get_chunk_db()

    root_record = file_db[root_id]
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
            child = file_db[child_id]
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
                build_file_from_chunks(chunk_hashes, file_path, file_db, chunk_db)
                
    # * close db files
    file_db.close()
    chunk_db.close()
    print("Directory rebuilt successfully from tree!")



def create_file_metadata(file_path):
    # * open db files
    file_db = get_file_db()
    chunk_db = get_chunk_db()
    # rel_path = os.path.relpath(file_path, ROOT_DIR)

    if os.path.isdir(file_path):
        # Create directory record
        create_directory_record(file_path, file_db, chunk_db)
    elif os.path.isfile(file_path):
        # Add entry for file
        chunk_and_upload_file(file_path, file_db, chunk_db)
    
    # Repopulate the parent directory

    print(file_path)
    parent_path = os.path.dirname(file_path)
    print(parent_path)
    parent_rel_path = os.path.relpath(parent_path, ROOT_DIR)
    parent_id = file_db[parent_rel_path]
    parent_record = file_db[parent_id]
    repopulate_parent_directory(parent_path, parent_record, file_db)

    # close db files
    file_db.close()
    chunk_db.close()

def delete_file_metadata(file_path):
    # * open db files
    file_db = get_file_db()
    # chunk_db = get_chunk_db()
    # Update the given file's metadata

    rel_path = os.path.relpath(file_path, ROOT_DIR)
    file_id = file_db[rel_path]
    file_record = file_db[file_id]

    file_record['is_deleted'] = True

    # add deleted time
    file_record['deleted_time'] = datetime.datetime.now().timestamp()



    # update the metadata db
    file_db[file_id] = file_record
    

    # * close db files
    file_db.close()
    # chunk_db.close()




    pass

def update_file_metadata(file_path):
     # * open db files
    file_db = get_file_db()
    chunk_db = get_chunk_db()

    # Update the given file's metadata

    rel_path = os.path.relpath(file_path, ROOT_DIR)
    file_id = file_db[rel_path]
    file_record = file_db[file_id]

    if os.path.isfile(file_path):
        new_chunks = get_chunks(file_path)
        new_hashes = get_hashes(new_chunks)
        old_hash_set = set(str(file_record['chunks']).splitlines())
        
        # Upload all new chunks
        total_hashes = len(new_chunks)
        current_hash = 1
        for chunk in new_chunks:
            if chunk.hash not in old_hash_set:
                if chunk.hash not in chunk_db.keys():
                    print("\rProcessing New Chunk {} of {}".format(current_hash, total_hashes), end="")
                    chunk_db[chunk.hash] = {'hash': chunk.hash, 'data': chunk.data, 'use_count': 1}
                    current_hash += 1
        
        # commit changes to chunk db
        chunk_db.commit()

        print()

        # Make changes to the metadata file


        file_record['chunks'].append(new_hashes)
        file_record['version'] += 1
        file_record['date_modified'] = datetime.datetime.now().timestamp()

        # update the metadata db
        file_db[file_id] = file_record
    
    elif os.path.isdir(file_path):
        # if a directory is updated, we need to repopulate the directory children
        repopulate_parent_directory(file_path, file_record, file_db)

    

    # * close db files
    file_db.close()
    chunk_db.close()

    print(f"{file_path} metadata updated successfully!")

    pass


def repopulate_parent_directory(dir_path, dir_record, file_db):
    # * open db files
    assert os.path.isdir(dir_path)
    # file_db = get_file_db()
    # chunk_db = get_chunk_db()

    # Update the given directory's children field

    # rel_path = os.path.relpath(dir_path, ROOT_DIR)
    dir_id = dir_record['id']
    # dir_record = file_db[dir_id]

    # dir_record['children'] = []

    real_contents = os.listdir(dir_path)

    # * add new items to the children
    for item in real_contents:
        if item in SKIP_FILES:
            continue
        item_path = os.path.join(dir_path, item)
        item_rel_path = os.path.relpath(item_path, ROOT_DIR)
        item_id = file_db[item_rel_path]
        print(dir_record)
        # add only if the item does not already exist
        # check if children exist at all
        if item_id not in dir_record['children']:
            dir_record['children'].append(item_id)

    
    # * remove items not in the directory
    
    items_to_remove = []
    for child_id in dir_record['children']:
        child_record = file_db[child_id]
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
    file_db[dir_id] = dir_record

    # * close db files
    # file_db.close()
    # chunk_db.close()

    print(f"{dir_path} children field updated successfully!")

    pass
    

def move_file_metadata(src, dst):
    # * open db files
    file_db = get_file_db()
    # chunk_db = get_chunk_db()

    # Update the given file's metadata

    src_rel_path = os.path.relpath(src, ROOT_DIR)
    dst_rel_path = os.path.relpath(dst, ROOT_DIR)
    src_id = file_db[src_rel_path]
    src_record = file_db[src_id]

    src_record['path'] = dst_rel_path

    # update the modified time
    src_record['date_modified'] = os.path.getmtime(dst)

    # update the metadata db
    file_db[src_id] = src_record
    file_db[dst_rel_path] = src_id

    # * close db files
    file_db.close()
    # chunk_db.close()

    pass

def build_file_from_chunks(chunk_hashes, file_path, file_db, chunk_db):
    with open(file_path, "ab") as out_ref:
        total_hashes = len(chunk_hashes)
        current_hash = 1
        for hash in chunk_hashes:
            print("\rChunk {} of {}".format(current_hash, total_hashes), end="")
            out_ref.write(chunk_db[hash]['data'])
            current_hash += 1
        print()
            







if __name__ == "__main__":

    # root_id = build_directory_tree_metadata("../example_sync_dir")
    root_id = '0dafd49005f14ba493deff20631bd811'
    print(root_id)

    restore_directory_tree("rebuilt_dir", root_id)
    # update_file_metadata('')
    pass




