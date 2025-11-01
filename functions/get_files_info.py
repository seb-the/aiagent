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
