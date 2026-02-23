import os
from config import MAX_CHARS
from google.genai import types


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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the given contents in the given file path, it will write the given string in the fille.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file where we need to write the given content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The Content text thats need to be written in the file.",
            )
        },
        required = ["file_path", "content"],
    ),
)