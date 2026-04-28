from enum import Enum

from src.htmlnode import LeafNode

class TextType(Enum):
    """Enumeration of inline text formatting types."""
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Represents a text element with formatting type and optional URL.
    
    Used to represent inline markdown elements before conversion to HTML.
    """
    
    def __init__(self, text: str, text_type: TextType, url: str | None = None ):
        """Initialize a text node with content, type, and optional URL for links/images."""
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        """Compare two text nodes for equality based on text, type, and URL."""
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert a TextNode to an HTML LeafNode based on text type."""
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid text node")
