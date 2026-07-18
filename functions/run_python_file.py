import os 
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    try:
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        
        if args != None:
            command.extend(args)
        command_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)
        
        if command_process.returncode != 0:
            return f"Process exited with code {command_process.returncode}"
        
        if command_process.stdout == "" and command_process.stderr == "":
            return "No output produced"

        output_list = []
        if command_process.stdout != "":
            output_list.append(f"STDOUT: {command_process.stdout}")
            
        
        if command_process.stderr != "":
            output_list.append(f"STDERR: {command_process.stderr}")
            
        
        result_output = "\n".join(output_list)
        return result_output
    except Exception as e:
        return (f"Error: executing Python file: {e}")

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "executes the file as a program , returns the programs standard output and standard error ",
        "parameters": {
            "type": "object",
            "properties":{
                "file_path": {
                "type": "string",
                "description":"the path to the file",
                },
                "args": {
                    "type": "array",
                    "description":"the argument provided by caller",
                    "items": {
                        "type":"string",
                        "description": "items inside the array of arguments"
                    }
                }
            },
            "required": ["file_path"],
                },
            },
        }