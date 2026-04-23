from enum import Enum
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
    return list(map(lambda s: s.strip(), block_list))

def block_to_block_type(block: str) -> BlockType:
    lines: list[str] = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
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
    print(markdown_to_blocks(md))

    for block in markdown_to_blocks(md):
        print(block_to_block_type(block))
