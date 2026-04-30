from src.general_page import generate_page
from src.static_to_public import static_to_public

def main():
    static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
