"""
Test module for converter.py functions
"""

import unittest

from converter import block_to_block_type, markdown_to_blocks, text_node_to_html
from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNodeToHTML(unittest.TestCase):
    """
    This class test text_node_to_html()
    """

    def test_normal_text(self):
        """
        Check against normal text
        """
        node = TextNode("Hello, world!", {TextType.NORMAL})
        expected = LeafNode(None, "Hello, world!")
        self.assertEqual(text_node_to_html(node), expected)

    def test_empty_text(self):
        """
        Check against empty text
        """
        node = TextNode("", {TextType.NORMAL})
        expected = LeafNode(None, "")
        self.assertEqual(text_node_to_html(node), expected)

    def test_bold_text(self):
        """
        Check against bold text
        """
        node = TextNode("Bold text", {TextType.BOLD})
        expected = LeafNode("b", "Bold text")
        self.assertEqual(text_node_to_html(node), expected)

    def test_link_with_url(self):
        """
        Check against link with url
        """
        node = TextNode("click me", {TextType.LINK}, "https://boot.dev")
        expected = LeafNode("a", "click me", {"href": "https://boot.dev"})
        self.assertEqual(text_node_to_html(node), expected)

    def test_link_without_url(self):
        """
        Check against link without url
        """
        node = TextNode("broken link", {TextType.LINK})
        expected = LeafNode("a", "broken link", {"href": None})
        self.assertEqual(text_node_to_html(node), expected)

    def test_image_with_url_and_text(self):
        """
        Check against image with url and text
        """
        node = TextNode("alt text", {TextType.IMAGE},
                        "https://example.com/img.png")
        expected = LeafNode(
            "img", "", {"src": "https://example.com/img.png",
                        "alt": "alt text"}
        )
        self.assertEqual(text_node_to_html(node), expected)

    def test_image_without_url(self):
        """
        Check against image without url
        """
        node = TextNode("alt text", {TextType.IMAGE})
        expected = LeafNode("img", "", {"src": None, "alt": "alt text"})
        self.assertEqual(text_node_to_html(node), expected)


class TestMarkdownToBlocks(unittest.TestCase):
    """
    Test class for markdown_to_blocks function
    """

    def test_normal_blocks(self):
        """
        Check against a simple case
        """
        markdown = "# Heading\n\nThis is a paragraph.\n\n* Item 1\n* Item 2\n"
        expected = ["# Heading", "This is a paragraph.", "* Item 1\n* Item 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_excessive_blank_lines(self):
        """
        Check against excessive blank lines
        """
        markdown = (
            "\n\n# Heading\n\n\nThis is a paragraph.\n\n\n\n* Item 1\n* Item 2\n\n"
        )
        expected = ["# Heading", "This is a paragraph.", "* Item 1\n* Item 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace_only_blocks(self):
        """
        Check against whitespace only blocks
        """
        markdown = "   \n\n# Title\n\n   \n\nContent\n\n   "
        expected = ["# Title", "Content"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block(self):
        """
        Check against a single block
        """
        markdown = "# Only Heading"
        expected = ["# Only Heading"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_input(self):
        """
        Check against empty input
        """
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_complex_markdown(self):
        """
        Check against a complex markdown blocks structure.
        """
        complex_markdown = """
           \n\n# Heading 1

        This is a paragraph with **bold text**.
        It spans multiple lines.

           * Item 1
           * Item 2

        # Heading 2

           Another paragraph with *italic text*.

        \n\n
        """
        expected_output = [
            "# Heading 1",
            "This is a paragraph with **bold text**.\n        It spans multiple lines.",
            "* Item 1\n           * Item 2",
            "# Heading 2",
            "Another paragraph with *italic text*.",
        ]
        self.assertEqual(markdown_to_blocks(complex_markdown), expected_output)

    def test_trailing_whitespace(self):
        """
        Check against leading and trailing whitespaces
        """
        markdown = "      Header\n\n     Next     \n\n"
        expected = ["Header", "Next"]

        self.assertEqual((markdown_to_blocks(markdown)), expected)


class TestBlockToBlockType(unittest.TestCase):
    """
    Test class for block_to_block-type function
    """

    def test_heading(self):
        """
        Checking against simple header
        """
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code_block(self):
        """
        Checking against simple code block
        """
        block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_quote(self):
        """
        Checking against simple quote block
        """
        block = "> First line\n> Second line\n> Third line"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_unordered_list(self):
        """
        Checking against simple unordered_list
        """
        block = "* First item\n* Second item\n* Third item"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list(self):
        """
        Checking against simple ordered_list
        """
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_heading_blocks(self):
        """
        Check against different header blocks
        """
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("###### H6"), "heading")
        self.assertEqual(block_to_block_type("#not_a_heading"), "paragraph")

    def test_code_blocks(self):
        """
        Check against different code blocks
        """
        self.assertEqual(
            block_to_block_type(
                "```\n`inline code`\n* not a list\n```"), "code"
        )
        self.assertEqual(block_to_block_type("```\nsome code\n```"), "code")

    def test_quote_blocks(self):
        """
        Check against different quote blocks
        """
        self.assertEqual(block_to_block_type(
            ">first line\n>second line"), "quote")
        self.assertEqual(
            block_to_block_type(">### Not a heading\n>* Not a list"), "quote"
        )

    def test_unordered_list_blocks(self):
        """
        Check against different unordered_list blocks
        """
        self.assertEqual(block_to_block_type(
            "* first\n* second"), "unordered_list")
        self.assertEqual(block_to_block_type(
            "- first\n- second"), "unordered_list")
        self.assertEqual(
            block_to_block_type(
                "* `code` in list\n* #not heading"), "unordered_list"
        )

    def test_ordered_list_blocks(self):
        """
        Check against different ordered_list blocks
        """
        self.assertEqual(block_to_block_type(
            "1. First\n2. Second"), "ordered_list")
        self.assertEqual(
            block_to_block_type(
                "1. First (note)\n2. Second [link]"), "ordered_list"
        )
        self.assertEqual(block_to_block_type(
            "1. First\n3. Third"), "paragraph")

    def test_paragraph_blocks(self):
        """
        Check against different paragraph blocks
        """
        self.assertEqual(block_to_block_type(
            "just a normal paragraph"), "paragraph")
        self.assertEqual(
            block_to_block_type(
                "1. not a list because no second item"), "paragraph"
        )


if __name__ == "__main__":
    unittest.main()
