import unittest
from src.general_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_missing_h1_raises(self):
        md = "Just a paragraph\n\nNo h1 here"
        with self.assertRaises(Exception) as ctx:
            extract_title(md)
        self.assertIn("no Title found", str(ctx.exception))

    def test_h1_complex_content(self):
        md = "# Title with **bold** and _italic_"
        self.assertEqual(extract_title(md), "Title with bold and italic")

if __name__ == "__main__":
    unittest.main()
