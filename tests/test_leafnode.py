"""
Test case class for LeafNode class
"""

import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    """
    Test cases for LeafNode class
    """

    def test_to_html(self):
        """
        Test the to_html method
        """
        node1 = LeafNode("p", "Hello")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode(None, "Just text")

        self.assertEqual(node1.to_html(), "<p>Hello</p>")
        self.assertEqual(
            node2.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )
        self.assertEqual(node3.to_html(), "Just text")

    def test_leaf_node_nested_props(self):
        """
        Test a nested leaf node
        """
        # Create a div with some nested style properties
        style_props = {"style": {"color": "blue", "font-size": "12px"}}
        node = LeafNode("div", "Styled text", style_props)
        expected = '<div style="color:blue; font-size:12px">Styled text</div>'

        self.assertEqual(node.to_html(), expected)
