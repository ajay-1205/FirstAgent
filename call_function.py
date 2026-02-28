import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

FILE_CACHE = {}
DIR_CACHE = {}

available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_files_content, schema_write_file, schema_run_python_file])

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role = "tool",
            parts = [
                types.Part.from_function_response(
                    name = function_name,
                    response = {"error": f"Unknown function: {function_name}"}
                )
            ]
        )
    else:
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = os.path.abspath("Site_Generator")

        # 🔥 DIRECTORY CACHE
        if function_name == "get_files_info":
            directory = args.get("directory", ".")
            if directory in DIR_CACHE:
                function_result = DIR_CACHE[directory]
            else:
                function_result = function_map[function_name](**args)
                DIR_CACHE[directory] = function_result

        # 🔥 FILE CACHE
        elif function_name == "get_file_content":
            file_path = args.get("file_path")
            if file_path in FILE_CACHE:
                function_result = FILE_CACHE[file_path]
            else:
                function_result = function_map[function_name](**args)
                FILE_CACHE[file_path] = function_result

        # 🔥 WRITE INVALIDATES CACHE
        elif function_name == "write_file":
            function_result = function_map[function_name](**args)

            # If file modified → remove from cache
            file_path = args.get("file_path")
            if file_path in FILE_CACHE:
                del FILE_CACHE[file_path]

        else:
            function_result = function_map[function_name](**args)

        # 🔥 TRUNCATE LARGE RESPONSES
        MAX_CHARS = 4000
        if isinstance(function_result, str) and len(function_result) > MAX_CHARS:
            function_result = function_result[:MAX_CHARS] + "\n\n... (truncated)"

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": str(function_result)},
                )
            ],
        )

    