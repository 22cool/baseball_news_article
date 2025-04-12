import os
import stat

def get_permission_string(file_path):
    try:
        mode = os.stat(file_path).st_mode
        return stat.filemode(mode)  # e.g. '-rw-r--r--'
    except FileNotFoundError:
        return 'File not found'

print(get_permission_string('testdir/dog1.txt'))
print(get_permission_string('testdir/dog2.txt'))
print(get_permission_string('testdir/test1.txt'))
print(get_permission_string('testdir/test2.txt'))
