def get_files_info(working_directory, directory="."):
    abs_target_path = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_path = os.path.abspath(working_directory)
    target_within_boundaries = abs_target_path.starswith(abs_working_path + os.sep) or abs_target_path == abs_working_path
    if not target_within_boundaries:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
