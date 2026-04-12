
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node) 

        else:
            matching_delimiters = list(filter(lambda s: s == delimiter,node.text.split()))
            if len(matching_delimiters) % 2 != 0:
                raise Exception("no matching delimiters found")

            node_text: list[str] = node.text.split(delimiter)
            for i in range(len(node_text)):
                if i % 2 == 0:
                    node_text[i]: TextNode = TextNode(node_text[i], TextType.TEXT)
                else:
                    node_text[i]: TextNode = TextNode(node_text[i], text_type)

            new_nodes.extend(node_text)

    return new_nodes
