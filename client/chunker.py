from fastcdc import fastcdc
import shelve
import hashlib
import difflib
import os


def transmit_update(changes):
    pass

def get_hashes(chunks):
    retval = ""
    for chunk in chunks:
        retval += str(chunk.hash) + "\n"
    return retval

def save_chunks(chunks):
    for chunk in chunks:
        # check if chunk already saved
        with open("chunks/{}.chunk".format(chunk.hash), "wb") as chunk_file:
            chunk_file.write(chunk.data)
        
        pass



result1 = list(fastcdc("sample1.txt", None, 1024, 1024, True, hashlib.sha256))
# result2 = list(fastcdc("sample2.txt", None, 1024, 1024, True, hashlib.sha256))

# print(result1)

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

def stitch_file(metadata_file, out_file):

    with open(metadata_file, "r") as meta_ref:
        for chunk in meta_ref:
            chunk = chunk[:-1]
            with open(out_file, "ab") as out_ref:
                with shelve.open("internal_db/chunk_cache.db") as db:
                    out_ref.write(db[chunk])
        

stitch_file("file1.txt", "new_sample1.txt")


d = shelve.open("hashes.db")

for chunk in result1:
    if chunk.hash not in d.keys():
        d[chunk.hash] = chunk.data
    else:
        print('chunk {} already present in db!'.format(chunk.hash))
