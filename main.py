import os
import shutil
from src.page_generator import generate_page
from src.copy_files import copy_files_recursive

static_dir = "./static"
public_dir = "./public"
content_dir = "content"

def main():
    if os.path.exists(static_dir):
        print("Deleting public directory...")
        shutil.rmtree(public_dir)

    print("Copying static files to public directory...")
    copy_files_recursive("static", "public")
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    generate_page("content/index.md", "template.html", "public/index.html")



if __name__ == "__main__":
    main()
