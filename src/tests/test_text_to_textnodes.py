import unittest

from src.textnode import TextNode, TextType
from src.inline_markdown import text_to_textnodes


class TestTextToTextnodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("This is plain text", TextType.TEXT)])

    def test_bold_only(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_code_only(self):
        text = "Run `code` here"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ]
        )

    def test_all_formats(self):
        text = "**bold** and _italic_ and `code` and ![image](https://example.com/img.png) and [link](https://example.com)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ]
        )

    def test_italic_only(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )


if __name__ == "__main__":
    unittest.main()
