import os
from config import MAX_CHARS
from google.genai import types


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

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read contents in a specified file relative to the working directory, return the text in that file with the Maximum of 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory",
            ),
        },
        required = ["file_path"],
    ),
)

    