import unittest

from src.htmlnode import HTMLNode, ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_ValueError(self):
        child_node: LeafNode = LeafNode(
                "a",
                "Click here!",
                {"href": "https://www.google.com"}
                )
        node_without_tag: ParentNode = ParentNode(
                children=[child_node]
                )

        node_without_children: ParentNode = ParentNode(
                tag="div",
                props={"blabla": "_blank"}
                )

        with self.assertRaises(ValueError):
            node_without_tag.to_html()

        with self.assertRaises(ValueError):
            node_without_children.to_html()

    def test_to_html_with_link(self):
        children: list[HTMLNode] = [
                LeafNode("a", "wagwan", {"href": "https://www.ThisIsALink.com"}),
                LeafNode("img", "test image", {"src": "url/of/image.jpg", "alt": "Description of image"})
                ]

        node: ParentNode = ParentNode(
                "p",
                children,
                )

        self.assertEqual(
                node.to_html(),
                '<p><a href="https://www.ThisIsALink.com">wagwan</a><img src="url/of/image.jpg" alt="Description of image" /></p>'
                )

    def test_to_html_with_link_ValueError(self):
        children: list[HTMLNode] = [
                LeafNode("a", "wagwan", {"href": "https://www.ThisIsALink.com"}),
                LeafNode("img", None, {"src": "url/of/image.jpg", "alt": "Description of image"})
                ]

        node: ParentNode = ParentNode(
                "p",
                children,
                )

        with self.assertRaises(ValueError):
            node.to_html()
