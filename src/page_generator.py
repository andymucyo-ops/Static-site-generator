
import os
import textwrap
from src.block_markdown import markdown_to_html_node
from src.htmlnode import HTMLNode


def extract_title(markdown: str) -> str:
    html: HTMLNode = markdown_to_html_node(markdown)
    for node in html.children:
       if node.tag == "h1":
           title_content: list[str] = [s.value for s in node.children]
           return "".join(title_content).strip()
    raise Exception("no Title found")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_path = os.path.abspath(from_path)
    with open(from_path, "r") as f:
        src_file_content: str = f.read()

    template_path = os.path.abspath(template_path)
    with open(template_path, "r") as f:
        template_content: str = f.read()

    src_as_html: str=  markdown_to_html_node(src_file_content).to_html()
    title: str = extract_title(src_file_content)
    
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", src_as_html)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    # print(template_content)
    dest_dir_path = os.path.dirname(os.path.abspath(dest_path))
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(from_dir: str = "content", template_file: str = "template.html", dest_dir: str = "public", basepath: str = "/") -> None:
    content_path: str = os.path.abspath(from_dir)
    dest_path: str = os.path.abspath(dest_dir)
    
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for item in os.listdir(content_path):
        item_path: str = os.path.join(content_path, item)
        if os.path.isfile(item_path):
            new_file: str = item.replace(".md", ".html")
            generate_page(
                from_path=os.path.join(from_dir, item),
                template_path=template_file,
                dest_path=os.path.join(dest_dir, new_file),
                basepath=basepath
                    )
        else:
            generate_pages_recursive(
                    from_dir=os.path.join(from_dir, item),
                    template_file=template_file,
                    dest_dir=os.path.join(dest_dir, item),
                    basepath=basepath
                    )



if __name__ == "__main__":
    md = textwrap.dedent("""
        # Title

        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items

        ```
        #followed by some code
        print('hello world')
        ```

        1. and
        2. an ordered
        3. list

        > and a quote
        """)
    # print(markdown_to_blocks(md))
    #
    # for block in markdown_to_blocks(md):
    #     print(block_to_block_type(block))
    # print(md)
    # print(markdown_to_html_node(md).to_html())
    
    # print(extract_title(md))
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive()
