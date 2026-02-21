import os
from config import MAX_CHARS


def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    
    if not valid_target:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    #os.makedirs(target_dir, exist_ok=True)
    with open(target_dir, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'