import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        elif not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            output.append(f"STDOUT: {result.stdout}")
            output.append(f"STDERR: {result.stderr}")
        
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"



