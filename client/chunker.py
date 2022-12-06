from fastcdc import fastcdc
import sqlitedict
import hashlib
import difflib
import os
import random
import queue
import time

random.randrange(0, 1000000000000)

MAX_CHUNK_SIZE = 4096 # Max chunk size in bytes
MIN_CHUNK_SIZE = 256 # Minimum chunk size in bytes
CACHE_SIZE = 1024 # Number of chunks to store in the offline cache
SKIP_FILES = ['.DS_Store']

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


def build_directory_tree_metadata(sync_dir):
    # * open db files
    file_db = get_file_db()
    chunk_db = get_chunk_db()

    abs_path = os.path.abspath(sync_dir)
    assert os.path.isdir(abs_path)
    retval = None
    dir_map = {}
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
            # Check if file is to be skipped
            if file in SKIP_FILES:
                print("Skipping {}".format(filepath))
                continue
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
                    chunk_db[chunk.hash] = chunk.data
                current_chunk+=1
            print()
            chunk_db.commit()
            print("Chunks Uploaded!")
            rel_path = os.path.relpath(filepath, abs_path)
            # Add entry for file
            db_data = {
            "id": str(random.randrange(0, 1000000000000)),
            "is_dir": False,
            "path": rel_path,
            "size": os.path.getsize(filepath),
            "owner": "aniansh@yahoo.com",
            "chunks": [hash_str],
            }
            root_children.append(db_data['id'])
            # Add to internal db
            file_db[db_data['id']] = db_data

             
        # add dirs to children
        print("Adding children dirs to parent map")
        if root in dir_map.keys():
            for dir_id in dir_map[root]:
                root_children.append(dir_id)

        rel_path = os.path.relpath(root, abs_path)
        # Add entry for root
        db_data = {
            "id": str(random.randrange(0, 1000000000000)),
            "is_dir": True,
            "path": rel_path,
            "size": os.path.getsize(root),
            "owner": "aniansh@yahoo.com",
            "children": root_children,
            }
        file_db[db_data['id']] = db_data

        # make a map of directories and their parent directories
        root_parent = os.path.dirname(root)
        if root_parent not in dir_map.keys():
            file_list = [db_data["id"]]
            dir_map[root_parent] = file_list
        else:
            dir_map[root_parent].append(db_data["id"])

        
        # return the id of the root
        if root == abs_path:
            print(root)
            retval = db_data['id']
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
                    

def update_directory_tree(root_dir, changes):
    pass

def delete_file_metadata(root_id):
    pass

def update_file_metadata(file_path):
     # * open db files
    file_db = get_file_db()
    chunk_db = get_chunk_db()

    # Update the given file's metadata
    conn = file_db.conn
    resp_queue = queue.Queue()
    print(conn.execute("select * from unnamed", res=resp_queue))
    print(resp_queue.get())

    # * close db files
    file_db.close()
    chunk_db.close()

    pass

def move_file_metadata(src, dst):
    pass

def build_file_from_chunks(chunk_hashes, file_path, file_db, chunk_db):
    with open(file_path, "ab") as out_ref:
        total_hashes = len(chunk_hashes)
        current_hash = 1
        for hash in chunk_hashes:
            print("\rChunk {} of {}".format(current_hash, total_hashes), end="")
            out_ref.write(chunk_db[hash])
            current_hash += 1
        print()
            




# def save_chunks(chunks):
#     for chunk in chunks:
#         # check if chunk already saved
#         with open("chunks/{}.chunk".format(chunk.hash), "wb") as chunk_file:
#             chunk_file.write(chunk.data)
        
#         pass



# result1 = list(fastcdc("sample1.txt", None, 1024, 1024, True, hashlib.sha256))
# result2 = list(fastcdc("sample2.txt", None, 1024, 1024, True, hashlib.sha256))

# # print(result1)

# hash_str1 = get_hashes(result1)
# hash_str2 = get_hashes(result2)

# file1 = open("file1.txt", "w")
# file2 = open("file2.txt", "w")

# file1.write(hash_str1)
# file2.write(hash_str2)

# file1.close()
# file2.close()


# save_chunks(result1)
# os.system("diff -Naur file1.txt file2.txt")

# def stitch_file(metadata_file, out_file):

#     with open(metadata_file, "r") as meta_ref:
#         for chunk in meta_ref:
#             chunk = chunk[:-1]
#             with open(out_file, "ab") as out_ref:
#                 out_ref.write(chunk_db[chunk])
        

# stitch_file("file1.txt", "new_sample1.txt")


# d = sqlitedict.SqliteDict("internal_db/chunk_cache.db", autocommit=True)

# for chunk in result1:
#     if chunk.hash not in d.keys():
#         d[chunk.hash] = chunk.data
#     else:
#         print('chunk {} already present in db!'.format(chunk.hash))
# d.close()




if __name__ == "__main__":

    # root_id = build_directory_tree_metadata("../example_sync_dir")
    # # root_id = str(144632294965)
    # print(root_id)

    # restore_directory_tree("rebuilt_dir", root_id)
    update_file_metadata('')
    pass




# file_db.close()
# chunk_db.close()