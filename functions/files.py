import os

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