"""
Test class for converter.py functions
"""

import unittest

from converter import text_node_to_html
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


if __name__ == "__main__":
    unittest.main()
