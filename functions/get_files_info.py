import os
import subprocess
import sys
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(abs_working_path, str(directory)))
        target_within_boundaries = abs_target_path.startswith(abs_working_path + os.sep) or abs_target_path == abs_working_path
        if not target_within_boundaries:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_target_path):
            return f'Error: "{directory}" is not a directory'
        
        #built string representing contents of directory
        if abs_target_path == abs_working_path:
            first_line = f"Result for current directory:"
        else:
            first_line = f"Result for '{directory}' directory:"
        return_string = [first_line]
        content_list = os.listdir(abs_target_path)
        for item in content_list:
            item_path = os.path.join(abs_target_path, item)
            return_string.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        
        return "\n".join(return_string)

    except Exception as e:
        return f"Error: {e}"


def get_file_content(working_directory, file_path):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(abs_working_path, file_path))
        target_within_boundaries = abs_target_path.startswith(abs_working_path + os.sep) or abs_target_path == abs_working_path
        if not target_within_boundaries:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(abs_target_path, "r") as file:
            file_content_string = file.read(MAX_CHARS + 1)

        if len(file_content_string) > MAX_CHARS:
            return file_content_string[:-1] + f'[...File "{file_path}" truncated at 10000 characters]'
        else:
            return file_content_string

    except Exception as e:
        return f'Error: {e}'


def write_files(working_directory, file_path, content):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(abs_working_path, file_path))
        target_within_boundaries = abs_target_path.startswith(abs_working_path + os.sep) or abs_target_path == abs_working_path
        if not target_within_boundaries:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(os.path.dirname(abs_target_path)):
            os.makedirs(os.path.dirname(abs_target_path))
        
        with open(abs_target_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(abs_working_path, file_path))
        target_within_boundaries = abs_target_path.startswith(abs_working_path + os.sep) or abs_target_path == abs_working_path
        if not target_within_boundaries:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_target_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            cmd = [sys.executable, abs_target_path, *args]
            completed_process = subprocess.run(cmd, cwd = abs_working_path, timeout = 30, capture_output = True, text = True)
            if completed_process.returncode != 0:
                return f'STDOUT: {completed_process.stdout}STDERR: {completed_process.stderr} Process exited with code {completed_process.returncode}'
            if completed_process.stdout == "":
                return f"No output produced."
            return f'STDOUT: {completed_process.stdout}STDERR: {completed_process.stderr}'

        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f'Error: {e}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns content of specified file restricted to the first 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to return content from, relative to the working directory."
            )
        }
    )
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified file with the specified args, returning stdout and stderr and if it is not 0 also the exit code, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of strings to pass as arguments when running the file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single CLI argument."
                )
            )
        },
        required=["file_path"]
    )
)

schema_write_files = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite the specified existing file with the content or create it if not existent and write the content to it, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to overwrite with content or create and write content to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_files
    ]
)
    