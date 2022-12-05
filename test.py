from fastcdc import fastcdc
import hashlib
import difflib
import os

def get_hashes(chunks):
    retval = ""
    for chunk in chunks:
        retval += chunk.hash + "\n"
    return retval



result1 = list(fastcdc("sample1.txt", None, 1024, 1024, False, hashlib.sha256))
result2 = list(fastcdc("sample2.txt", None, 1024, 1024, False, hashlib.sha256))

hash_str1 = get_hashes(result1)
hash_str2 = get_hashes(result2)

file1 = open("file1.txt", "w")
file2 = open("file2.txt", "w")

file1.write(hash_str1)
file2.write(hash_str2)

file1.close()
file2.close()

os.system("diff -Naur file1.txt file2.txt")