
class HTMLNode:
    """Base class for representing HTML elements with tag, value, and properties."""
    
    def __init__(self, tag: str | None = None, value: str| None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None ):
        """Initialize an HTML node with optional tag, value, children, and properties."""
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Convert node to HTML string. Must be implemented by subclasses."""
        raise NotImplementedError("to_htlm method not implemented yet")

    def props_to_html(self):
        """Convert node properties dictionary to HTML attribute string."""
        if self.props is None:
            return ""

        output: str = ""
        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'

        return output

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """Represents a leaf node with no children. Outputs a single HTML tag.
    
    For img tags, outputs self-closing tag. For other tags, wraps value
    in opening and closing tags.
    """
    
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict[str, str] | None = None):
        """Initialize a leaf node with tag, value, and optional properties."""
        super().__init__(tag = tag, value = value, props= props)

    def props_to_html(self):
        """Convert properties to HTML attribute string."""
        return super().props_to_html()

    def to_html(self) -> str:
        """Convert leaf node to HTML string.
        
        Returns plain text if tag is None, self-closing tag for img elements,
        and standard open/close tags for other elements.
        """
        if self.value is None:
            raise ValueError("Error: this node has no value")

        if self.tag is None:
            return self.value

        if self.props is not None:
            if self.tag == "img":
                return f"<{self.tag}{self.props_to_html()} />"

            if self.tag == "a":
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """Represents a parent node that renders all children recursively.
    
    Recursively converts all child nodes to HTML and wraps them in the
    parent's opening and closing tags.
    """
    
    def __init__(self, tag: str | None = None, children: list[HTMLNode] | None = None, props: dict[str,str] | None = None):
        """Initialize a parent node with tag, children list, and optional properties."""
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        """Convert parent node to HTML by recursively converting all children.
        
        Raises ValueError if tag or children are missing.
        """
        if self.tag is None:
            raise ValueError("Invalid parent node: missing tag")

        if self.children is None:
            raise ValueError("Invalid parent node: missing children")

        output: str = ""
        for child in self.children:
            output += child.to_html()

        return f"<{self.tag}>{output}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


if __name__=="__main__":
    node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
            )

    print(node.to_html())

