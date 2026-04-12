import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node) 

        else:
            split_nodes: list[TextNode] = []
            node_text: list[str] = node.text.split(delimiter)

            if len(node_text) % 2 == 0:
                raise Exception("invalid markdown, formatted section not closed")

            for i in range(len(node_text)):
                if node_text[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(node_text[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(node_text[i], text_type))

            new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
