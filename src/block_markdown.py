from enum import Enum
from src.inline_markdown import text_to_textnodes
from src.htmlnode import LeafNode, ParentNode
from src.textnode import TextNode, TextType
import textwrap


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered list"
    O_LIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    block_list: list[str] = markdown.split("\n\n")
    return [s.strip() for s in block_list]


def block_to_block_type(block: str) -> BlockType:
    lines: list[str] = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Strip lines for code block detection to handle indented blocks
    stripped_lines = [line.strip() for line in lines]
    if len(stripped_lines) > 1 and stripped_lines[0].startswith("```") and stripped_lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        lines = [line for line in lines if line]
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if line and not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.U_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if line and not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.O_LIST
    return BlockType.PARAGRAPH


def leaf_nodes(block: str) -> list[LeafNode]:
    normalized_block: str = block.replace("\n", " ")
    normalized_block: str = " ".join(normalized_block.split())
    text_nodes : list[TextNode] = text_to_textnodes(normalized_block)
    childen_nodes: list[LeafNode] = [] 
    for node in text_nodes:
        match node.text_type:
            case TextType.TEXT:
                childen_nodes.append(LeafNode(None, node.text))
            case TextType.BOLD:
                childen_nodes.append(LeafNode("b", node.text))
            case TextType.ITALIC:
                childen_nodes.append(LeafNode("i", node.text))
            case TextType.CODE:
                childen_nodes.append(LeafNode("code", node.text))
            case TextType.IMAGE:
                childen_nodes.append(
                        LeafNode(
                            "img", node.text, 
                            {
                            "src":node.url,
                            "alt":node.text 
                            } 
                                )
                        )
            case TextType.LINK:
                childen_nodes.append(
                        LeafNode(
                            "a",
                            node.text,
                            {"href":node.url}
                            )
                        )
    return childen_nodes


def heading_block(block: str) -> ParentNode:
    if block.startswith("###### "):
        return ParentNode("h6", leaf_nodes(block))
    elif block.startswith("##### "):
        return ParentNode("h5", leaf_nodes(block))
    elif block.startswith("#### "):
        return ParentNode("h4", leaf_nodes(block))
    elif block.startswith("### "):
        return ParentNode("h3", leaf_nodes(block))
    elif block.startswith("## "):
        return ParentNode("h2", leaf_nodes(block))
    else: 
        return ParentNode("h1", leaf_nodes(block))

def tagged_items_Olist(block: str) -> list:
    items: list[str]= block.split("\n")
    stripped_marked_items: list[str] = [item[3:] for item in items] 
    tagged_items = []
    for item in stripped_marked_items:
        child_nodes: list[LeafNode] = leaf_nodes(item) 
        tagged_items.append(ParentNode("li",child_nodes))

    return tagged_items


def tagged_items_Ulist(block: str) -> list:
    items: list[str]= block.split("\n")
    stripped_marked_items: list[str] = [item[2:] for item in items]
    tagged_items = []
    for item in stripped_marked_items:
        child_nodes: list[LeafNode] = leaf_nodes(item) 
        tagged_items.append(ParentNode("li",child_nodes))

    return tagged_items

def get_raw_code(block: str) -> str:
    raw_code = block.split("```")[1]
    # Remove leading and trailing whitespace, then dedent
    lines = raw_code.split('\n')
    # Strip leading/trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    
    # Dedent: find minimum indentation
    if lines:
        min_indent = float('inf')
        for line in lines:
            if line.strip():  # Only consider non-empty lines
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        # Remove the minimum indentation from all lines
        if min_indent < float('inf'):
            lines = [line[min_indent:] if line.strip() else line for line in lines]
    
    # Join back and add trailing newline
    return '\n'.join(lines) + '\n' 

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    blocks: list[str] = [block for block in blocks if block != ""]
    childrens: list[ParentNode] = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                childrens.append(heading_block(block))
            case BlockType.PARAGRAPH:
                childrens.append(ParentNode(
                        "p", 
                        leaf_nodes(block)
                            )
                                 )
            case BlockType.CODE:
                childrens.append(ParentNode(
                    "pre",
                    [LeafNode("code", get_raw_code(block))]
                    )
                                 ) 
            case BlockType.QUOTE:
                childrens.append(ParentNode(
                        "blockquote",
                        leaf_nodes(block[2:])
                            )
                                 )
            case BlockType.O_LIST:
                tagged_items = tagged_items_Olist(block)
                childrens.append(ParentNode(
                    "ol",
                    tagged_items
                    ))
            case BlockType.U_LIST:
                tagged_items = tagged_items_Ulist(block)
                childrens.append(ParentNode(
                    "ul",
                    tagged_items
                    ))
    return ParentNode("div", childrens)


if __name__ == "__main__":
    md = textwrap.dedent("""
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
    print(md)
    print(markdown_to_html_node(md).to_html())
