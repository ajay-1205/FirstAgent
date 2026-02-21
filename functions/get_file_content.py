import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    
    if not valid_target:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_dir, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    return file_content_string

    