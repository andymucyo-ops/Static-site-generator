import os
import shutil

def static_to_public(source: str = "static", destination: str = "public", is_root: bool = True) :
    destination_path: str = os.path.abspath(destination)
    source_path: str = os.path.abspath(source)

    if os.path.exists(destination_path) and os.path.isdir(destination_path):
        if is_root: 
            print(f"Deleting {destination} directory...")
            shutil.rmtree(destination_path)
            os.mkdir(destination)
            print("Copying static files to public directory...")
    else:
        print(f"Creating {destination} directory")
        os.mkdir(destination)
        print("Copying static files to public directory...")
    to_copy: list[str] = os.listdir(source_path)
    for item in to_copy:
        item_path: str = os.path.join(source_path, item)
        if not os.path.isdir(item_path):
            shutil.copy(item_path, destination_path)
        else:
            new_dir = os.path.join(destination, item)
            new_dir_path: str = os.path.join(destination_path, item)
            os.mkdir(new_dir_path)
            static_to_public(source=item_path, destination=new_dir, is_root=False)




if __name__ == "__main__":
    static_to_public()
