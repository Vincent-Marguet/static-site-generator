"""
Test class for converter.py functions
"""

import unittest

from converter import split_nodes_delimiter, text_node_to_html
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
        node = TextNode("Hello, world!", TextType.NORMAL)
        expected = LeafNode(None, "Hello, world!")
        self.assertEqual(text_node_to_html(node), expected)

    def test_empty_text(self):
        """
        Check against empty text
        """
        node = TextNode("", TextType.NORMAL)
        expected = LeafNode(None, "")
        self.assertEqual(text_node_to_html(node), expected)

    def test_bold_text(self):
        """
        Check against bold text
        """
        node = TextNode("Bold text", TextType.BOLD)
        expected = LeafNode("b", "Bold text")
        self.assertEqual(text_node_to_html(node), expected)

    def test_link_with_url(self):
        """
        Check against link with url
        """
        node = TextNode("click me", TextType.LINK, "https://boot.dev")
        expected = LeafNode("a", "click me", {"href": "https://boot.dev"})
        self.assertEqual(text_node_to_html(node), expected)

    def test_link_without_url(self):
        """
        Check against link without url
        """
        node = TextNode("broken link", TextType.LINK)
        expected = LeafNode("a", "broken link", {"href": None})
        self.assertEqual(text_node_to_html(node), expected)

    def test_image_with_url_and_text(self):
        """
        Check against image with url and text
        """
        node = TextNode("alt text", TextType.IMAGE,
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
        node = TextNode("alt text", TextType.IMAGE)
        expected = LeafNode("img", "", {"src": None, "alt": "alt text"})
        self.assertEqual(text_node_to_html(node), expected)


class TestSplitNodesDelimiter(unittest.TestCase):
    """
    Class test for split_nodes_delimiter function
    """

    def test_basic_code_block(self):
        """
        Check against a simple case
        """
        node = TextNode("hello `code` world", TextType.NORMAL)
        expected = [
            TextNode("hello ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.NORMAL),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        # Note: You'll need to implement __eq__ in TextNode for this to work
        self.assertEqual(result, expected)

    def test_multiple_bold_blocks(self):
        """
        Check against a single TextType other than NORMAL
        """
        node = TextNode("this **is** some **bold** text", TextType.NORMAL)
        expected = [
            TextNode("this ", TextType.NORMAL),
            TextNode("is", TextType.BOLD),
            TextNode(" some ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_non_text_node_preserved(self):
        """
        Check against CODE in a NORMAL TextNode
        """
        nodes = [
            TextNode("some ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and `code`", TextType.NORMAL),
        ]
        expected = [
            TextNode("some ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_missing_delimiter_raises_error(self):
        """
        Check against missing delimiter
        """
        # Method 1: Using context manager (recommended)
        node = TextNode("text with unclosed `code", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

        # Method 2: Using assertRaises as a method
        node = TextNode("text with unclosed *italic", TextType.NORMAL)
        self.assertRaises(
            ValueError, split_nodes_delimiter, [node], "*", TextType.ITALIC
        )

    def test_empty_nodes_raises_error(self):
        """
        Check against empty nodes
        """
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([], "`", TextType.CODE)
        # Optionally check the error message
        self.assertTrue("nodes list cannot be empty" in str(context.exception))

    def test_invalid_node_type_raises_error(self):
        """
        Check against invalid node
        """
        nodes = [
            TextNode("valid", TextType.NORMAL),
            "not a text node",  # This should cause an error
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_complex_mixed_nodes(self):
        """
        check against a complex structure of nodes
        """
        # Create a complex input with multiple nodes and mixed cases
        nodes = [
            TextNode("Start ", TextType.NORMAL),
            TextNode("existing_bold", TextType.BOLD),
            TextNode(" then `some code` followed by ", TextType.NORMAL),
            TextNode("more_bold", TextType.BOLD),
            TextNode(" and `another code` and `third code` and text",
                     TextType.NORMAL),
            TextNode(" final_italic ", TextType.ITALIC),
            TextNode("and `last code`!", TextType.NORMAL),
        ]

        expected = [
            TextNode("Start ", TextType.NORMAL),
            TextNode("existing_bold", TextType.BOLD),
            TextNode(" then ", TextType.NORMAL),
            TextNode("some code", TextType.CODE),
            TextNode(" followed by ", TextType.NORMAL),
            TextNode("more_bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("another code", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("third code", TextType.CODE),
            TextNode(" and text", TextType.NORMAL),
            TextNode(" final_italic ", TextType.ITALIC),
            TextNode("and ", TextType.NORMAL),
            TextNode("last code", TextType.CODE),
            TextNode("!", TextType.NORMAL),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
