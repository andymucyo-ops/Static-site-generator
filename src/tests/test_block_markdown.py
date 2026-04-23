import unittest
from src.block_markdown import markdown_to_block


class TestMarkdownToBlock(unittest.TestCase):
    def test_single_block(self):
        md = "single paragraph"
        self.assertEqual(markdown_to_block(md), ["single paragraph"])

    def test_multiple_blocks(self):
        md = "para 1\n\npara 2"
        self.assertEqual(markdown_to_block(md), ["para 1", "para 2"])

    def test_strips_whitespace(self):
        md = "  paragraph with spaces  \n\n  another  "
        self.assertEqual(markdown_to_block(md), ["paragraph with spaces", "another"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_block(""), [""])

    def test_multiline_block(self):
        md = "line1\nline2\n\npara2"
        self.assertEqual(markdown_to_block(md), ["line1\nline2", "para2"])


if __name__ == "__main__":
    unittest.main()
