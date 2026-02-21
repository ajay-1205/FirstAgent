import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
    valid_target = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    if not valid_target:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    list_of_files = os.listdir(target_dir)
    file_info = []
    try:
        for file in list_of_files:
            if directory == ".":
                new = os.path.normpath(os.path.join(working_directory_abs, file))
            else:
                new = os.path.join(target_dir, file)
            file_size = os.path.getsize(new)
            is_dir = os.path.isdir(new)
            info = f"   - {file}: file_size={file_size} bytes, is_dir={is_dir}"
            file_info.append(info)
        result = "\n".join(file_info)
        return result
    except Exception as err:
        return f'Error: {err}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
    
    

     
