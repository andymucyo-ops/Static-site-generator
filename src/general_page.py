
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
    print(extract_title(md))

