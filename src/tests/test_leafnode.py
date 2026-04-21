import unittest

from src.htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node: LeafNode = LeafNode(
                tag= "p",
                value= "Test paragraph"
                )
        self.assertEqual(node.to_html(), "<p>Test paragraph</p>")

    def test_leaf_to_html_a(self):
        node: LeafNode = LeafNode(
                tag= "a",
                value= "click here",
                props= {"href": "https://www.google.com"} 
                )
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">click here</a>')

    def test_leaf_to_html_img(self):
        node: LeafNode = LeafNode(
                tag= "img",
                value= "image",
                props= {"src": "image.jpg", "alt":"description"} 
                )
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="description" />' )

    def test_leaf_repr(self):
        node: LeafNode = LeafNode(
                tag= "a",
                value= "click here",
                props= {"href":"https://www.google.com"} 
                )
        self.assertEqual(repr(node), "LeafNode(a, click here, {'href': 'https://www.google.com'})")

    def test_leaf_value_error(self):
        node: LeafNode = LeafNode(tag= "p")

        with self.assertRaises(ValueError):
            node.to_html()


