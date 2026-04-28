import unittest
from src.block_markdown import markdown_to_blocks, block_to_block_type, BlockType,markdown_to_html_node


class TestMarkdownToBlock(unittest.TestCase):
    def test_single_block(self):
        md = "single paragraph"
        self.assertEqual(markdown_to_blocks(md), ["single paragraph"])

    def test_multiple_blocks(self):
        md = "para 1\n\npara 2"
        self.assertEqual(markdown_to_blocks(md), ["para 1", "para 2"])

    def test_strips_whitespace(self):
        md = "  paragraph with spaces  \n\n  another  "
        self.assertEqual(markdown_to_blocks(md), ["paragraph with spaces", "another"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [""])

    def test_multiline_block(self):
        md = "line1\nline2\n\npara2"
        self.assertEqual(markdown_to_blocks(md), ["line1\nline2", "para2"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_single_hash(self):
        block = "# Hello"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_multiple_hashes(self):
        block = "###### Six"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_indent(self):
        block = "```\n  code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> A quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_single(self):
        block = "- item\n"
        self.assertEqual(block_to_block_type(block), BlockType.U_LIST)

    def test_unordered_list_multiple(self):
        block = "- item1\n- item2"
        self.assertEqual(block_to_block_type(block), BlockType.U_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second"
        self.assertEqual(block_to_block_type(block), BlockType.O_LIST)

    def test_paragraph(self):
        block = "Plain text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_no_space_after_hash(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space_after_dot(self):
        block = "1.item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_out_of_order(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
