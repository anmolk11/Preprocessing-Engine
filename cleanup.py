import os

def cleanup_folder():
    path = 'static/data'
    print("Cleaning up folder:", path)
    
    files_to_delete = os.listdir(path)

    for file_name in files_to_delete:
        file_path = os.path.join(path, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")