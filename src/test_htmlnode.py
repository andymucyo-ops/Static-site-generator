import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_node_repr(self):
        link: HTMLNode = HTMLNode(
                tag = "a", 
                value = "link to something",
                props = {"href":"https://www.google.com"}
                )
        paragraph: HTMLNode = HTMLNode(
                tag = "p",
                value = "This is a paragraph",
                children= [link]
                )
        self.assertEqual(repr(paragraph), "HTMLNode(p, This is a paragraph, [HTMLNode(a, link to something, None, {'href': 'https://www.google.com'})], None)")

    def test_props_to_html(self):
        node: HTMLNode = HTMLNode(
                tag = "a",
                value = "click here",
                props = {"href":"https://www.google.com"}
                )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_is_none(self):
        node: HTMLNode = HTMLNode(
                value = "This is raw text" 
                )

        self.assertEqual(node.props_to_html(), "") 

    def test_values(self):
        node: HTMLNode = HTMLNode(
                tag = "div",
                value = "This is a test"
                )

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "This is a test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)



