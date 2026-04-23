from src.textnode import TextNode
from src.textnode import TextType

def main():
    text_node: TextNode = TextNode("dummy text", TextType.LINK, "https://www.boot.dev" )
    print(text_node)

if __name__ == "__main__":
    main()
