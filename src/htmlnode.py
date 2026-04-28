
class HTMLNode:
    def __init__(self, tag: str | None = None, value: str| None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_htlm method not implemented yet")

    def props_to_html(self):
        if self.props is None:
            return ""

        output: str = ""
        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'

        return output

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict[str, str] | None = None):
        super().__init__(tag = tag, value = value, props= props)

    def props_to_html(self):
        return super().props_to_html()

    def to_html(self) -> str:
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
    def __init__(self, tag: str | None = None, children: list[HTMLNode] | None = None, props: dict[str,str] | None = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
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

