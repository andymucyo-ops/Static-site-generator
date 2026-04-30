import os
import shutil

def copy_files_recursive(source_dir: str = "static", destination_dir: str = "public") :
    destination_path: str = os.path.abspath(destination_dir)
    source_path: str = os.path.abspath(source_dir)

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for item in os.listdir(source_path):
        item_path: str = os.path.join(source_path, item)
        if not os.path.isdir(item_path):
            shutil.copy(item_path, destination_path)
        else:
            new_dir = os.path.join(destination_dir, item)
            new_dir_path: str = os.path.join(destination_path, item)
            os.mkdir(new_dir_path)
            copy_files_recursive(source_dir=item_path, destination_dir=new_dir)




if __name__ == "__main__":
    copy_files_recursive()
