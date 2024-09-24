import os

def create_directory_with_permissions(path):
    # Check if the directory exists
    if not os.path.exists(path):
        # Create the directory
        os.makedirs(path)
        # Set the permissions to 777
        os.chmod(path, 0o777)
        print(f"Directory '{path}' created with 777 permissions.")
    else:
        print(f"Directory '{path}' already exists.")
