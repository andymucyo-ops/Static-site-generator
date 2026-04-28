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


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_unordered_list_simple(self):
        md = "- item1\n- item2\n- item3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item1</li><li>item2</li><li>item3</li></ul></div>"
        )

    def test_ordered_list_simple(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )

    def test_heading_all_levels(self):
        md = "# H1\n\n## H2\n\n### H3\n\n#### H4\n\n##### H5\n\n###### H6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3><h4>H4</h4><h5>H5</h5><h6>H6</h6></div>"
        )

    def test_blockquote_simple(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_unordered_list_with_formatting(self):
        md = "- **bold** item\n- _italic_ item\n- `code` item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li><li><code>code</code> item</li></ul></div>"
        )

    def test_ordered_list_with_formatting(self):
        md = "1. **first** with bold\n2. _second_ with italic\n3. [link](https://example.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>first</b> with bold</li><li><i>second</i> with italic</li><li><a href=\"https://example.com\">link</a></li></ol></div>"
        )

    def test_blockquote_with_formatting(self):
        md = "> A quote with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A quote with <b>bold</b> and <i>italic</i></blockquote></div>"
        )

    def test_complex_mixed_blocks(self):
        md = """# Heading

Paragraph with **formatting**.

- List item
- Another item

> A quote here

```
code block
```

1. Ordered item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<pre>", html)
        self.assertIn("<ol>", html)

    def test_empty_input(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

if __name__ == "__main__":
    unittest.main()
