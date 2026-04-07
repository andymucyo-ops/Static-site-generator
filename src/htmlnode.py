
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
