import unittest

from textnode import TextType, TextNode
from split_delimiter import split_nodes_delimiter

class TestSplitDelimiter(unittest.TestCase):
    def test_single_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
                new_nodes,
                [ 
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                    ]
                )

    def test_multiple_nodes(self):
        nodes: list[TextNode] = [
                TextNode("Title", TextType.BOLD),
                TextNode("warning **this code** is dangerous", TextType.TEXT),
                TextNode("sudo rm -rf /", TextType.CODE)
                ]
        new_nodes: list[TextNode] = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("Title", TextType.BOLD),
                    TextNode("warning ", TextType.TEXT),
                    TextNode("this code", TextType.BOLD),
                    TextNode(" is dangerous", TextType.TEXT),
                    TextNode("sudo rm -rf /", TextType.CODE)
                    ]
                )
