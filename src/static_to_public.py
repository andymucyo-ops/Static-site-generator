import os
import shutil

def static_to_public(source: str = "static", destination: str = "public", root: str = ".") :
    destination_path: str = os.path.abspath(destination)
    source_path: str = os.path.abspath(source)
    root_path: str = os.path.abspath(root)

    if os.path.exists(destination_path) and os.path.isdir(destination_path):
        if destination == "public": 
            shutil.rmtree(os.path.join(root_path, destination))
            os.mkdir(destination)
    else:
        os.mkdir(destination)
    to_copy: list[str] = os.listdir(source_path)
    for item in to_copy:
        item_path: str = os.path.join(source_path, item)
        if not os.path.isdir(item_path):
            shutil.copy(item_path, destination_path)
        else:
            new_dir = os.path.join(destination, item)
            new_dir_path: str = os.path.join(destination_path, item)
            if not os.path.exists(new_dir_path):
                os.mkdir(new_dir_path)
            static_to_public(source=item_path, destination=new_dir, root=source)




if __name__ == "__main__":
    static_to_public()
