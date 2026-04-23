from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_block(markdown: str) -> list[str]:
    block_list: list[str] = markdown.split("\n\n")
    return list(map(lambda s: s.strip(), block_list))

def block_to_block_type(block: str) -> BlockType:
    patterns: dict = {
            "heading":(r"#{1,6}\s(.*?)", BlockType.HEADING),
            "code":(r"```\n([\s\S]*?)\n\s*```", BlockType.CODE),
            "quotes":(r">\s*(.*?)", BlockType.QUOTE),
            "undordered list":(r"(-\s.*\n)+", BlockType.UNORDERED_LIST),
            "ordered list": (r"(\d+\.\s+.*+\n)+", BlockType.ORDERED_LIST)
            }
    for pattern in patterns:
        p = patterns[pattern][0]
        block_type = patterns[pattern][1]
        if re.match(p,block):
            return block_type

    return BlockType.PARAGRAPH 

if __name__ == "__main__":
    md = """
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
        """
    print(markdown_to_block(md))

    for block in markdown_to_block(md):
        print(block_to_block_type(block))
