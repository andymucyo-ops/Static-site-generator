

def markdown_to_block(markdown: str) -> list[str]:
    block_list: list[str] = markdown.split("\n\n")
    return list(map(lambda s: s.strip(), block_list))

if __name__ == "__main__":
    md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
    print(markdown_to_block(md))
