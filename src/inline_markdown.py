import re
from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        md_images: list[tuple[str]] = extract_markdown_images(node.text)
        current_text = node.text
        for image in md_images:
            image_alt: str = image[0]
            image_link: str = image[1]
            text_as_list: list[str] = current_text.split(f"![{image_alt}]({image_link})", maxsplit=1)
            if text_as_list[0]:
                new_nodes.append(TextNode(text_as_list[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = text_as_list[1]

        if current_text:
            new_nodes.append(
                    TextNode(current_text, TextType.TEXT)
                    )

    return new_nodes

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        md_links: list[tuple[str]] = extract_markdown_links(node.text)
        current_text = node.text
        for link in md_links:
            link_text: str = link[0]
            link_url: str = link[1]
            text_as_list: list[str] = current_text.split(f"[{link_text}]({link_url})", maxsplit=1)
            if text_as_list[0]:
                new_nodes.append(TextNode(text_as_list[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            current_text = text_as_list[1]
        if current_text:
            new_nodes.append(
                    TextNode(current_text, TextType.TEXT)
                    )

    return new_nodes


if __name__ == "__main__":
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) blablabla",
        TextType.TEXT,
    )

    new_nodes = split_nodes_images([node])

    print(new_nodes)
