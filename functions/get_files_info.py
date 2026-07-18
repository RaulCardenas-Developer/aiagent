import os 

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    
    # Will be True or False
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'


    try:    
        file_info = []
        for item in os.listdir(target_dir):
            path_file = os.path.join(target_dir, item)
            file_size= os.path.getsize(path_file)
            is_dir = os.path.isdir(path_file)
            file_info.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
            
        print(f"Result for {target_dir} directory:")
        return "\n".join(file_info)

    except Exception as e:
        return (f"Error: Cannot list '{target_dir}' as it is outside the permitted working directory")

    schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
    }
    
    
    return f'Success: "{directory}" is within the working directory'
    