import os
import shutil
import sys
from src.page_generator import generate_pages_recursive
from src.copy_files import copy_files_recursive

static_dir = "./static"
public_dir = "./docs"
content_dir = "content"

def main():
    try:
        basepath: str = sys.argv[1]
    except IndexError:
        basepath: str = "/"

    if os.path.exists(public_dir):
        print("Deleting public directory...")
        shutil.rmtree(public_dir)

    print("Copying static files to public directory...")
    copy_files_recursive(source_dir="static", destination_dir="docs")
    generate_pages_recursive(
            from_dir="content",
            template_file="template.html",
            dest_dir="docs",
            basepath=basepath
            )

if __name__ == "__main__":
    main()
