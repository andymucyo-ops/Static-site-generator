import unittest
from src.textnode import TextNode, TextType
from src.inline_markdown import split_nodes_images, split_nodes_links


class TestSplitNodesImages(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("This is text with an ![image](https://example.com/img.png) inside", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" inside", TextType.TEXT),
            ]
        )

    def test_multiple_images(self):
        node = TextNode("Here is ![img1](url1.png) and ![img2](url2.png)", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2.png"),
            ]
        )

    def test_no_images(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [TextNode("This is plain text with no images", TextType.TEXT)])

    def test_image_at_start(self):
        node = TextNode("![first](url.png) is at start", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("first", TextType.IMAGE, "url.png"),
                TextNode(" is at start", TextType.TEXT),
            ]
        )

    def test_image_at_end(self):
        node = TextNode("text ends with ![last](link.png)", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("text ends with ", TextType.TEXT),
                TextNode("last", TextType.IMAGE, "link.png"),
            ]
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("This is text with a [link](https://example.com) inside", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" inside", TextType.TEXT),
            ]
        )

    def test_multiple_links(self):
        node = TextNode("Here is [link1](url1) and [link2](url2)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
            ]
        )

    def test_no_links(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(result, [TextNode("This is plain text with no links", TextType.TEXT)])

    def test_link_at_start(self):
        node = TextNode("[first](url.com) is at start", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("first", TextType.LINK, "url.com"),
                TextNode(" is at start", TextType.TEXT),
            ]
        )

    def test_link_at_end(self):
        node = TextNode("text ends with [last](link.com)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("text ends with ", TextType.TEXT),
                TextNode("last", TextType.LINK, "link.com"),
            ]
        )


if __name__ == "__main__":
    unittest.main()