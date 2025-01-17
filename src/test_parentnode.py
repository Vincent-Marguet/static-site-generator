"""
Test class for ParentNode class
"""

import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    """
    Test class
    """

    def test_basic_parent_with_single_child(self):
        """
        Test a basic parent with one child
        """
        node = ParentNode("div", [LeafNode("span", "hello")])
        self.assertEqual(node.to_html(), "<div><span>hello</span></div>")

    def test_parent_with_multiple_children(self):
        """
        Test a parent with multiple children
        """
        node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        self.assertEqual(
            node.to_html(), "<p><b>bold text</b>normal text<i>italic text</i></p>"
        )

    def test_nested_parent_nodes(self):
        """
        Test a nested parent
        """
        node = ParentNode(
            "div", [ParentNode("p", [LeafNode("span", "nested")])])
        self.assertEqual(
            node.to_html(), "<div><p><span>nested</span></p></div>")

    def test_parent_with_props(self):
        """
        Test a parent with props
        """
        node = ParentNode("div", [LeafNode("span", "hello")], {
                          "class": "greeting"})
        self.assertEqual(
            node.to_html(), '<div class="greeting"><span>hello</span></div>'
        )

    def test_no_tag_raises_error(self):
        """
        Test that no tag raise Error
        """
        node = ParentNode(None, [LeafNode("span", "hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises_error(self):
        """
        Test that no children for ParentNode raise Error
        """
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_complex_nested_structure(self):
        """
        Test a more complex nested structure
        """
        # This represents a typical article structure with header, content sections and footer
        node = ParentNode(
            "article",
            [
                ParentNode(
                    "header",
                    [
                        ParentNode(
                            "h1", [LeafNode(None, "Welcome to my Blog")]),
                        ParentNode(
                            "nav",
                            [
                                LeafNode("a", "Home", {"href": "/"}),
                                LeafNode(None, " | "),
                                LeafNode("a", "About", {"href": "/about"}),
                            ],
                        ),
                    ],
                ),
                ParentNode(
                    "section",
                    [
                        ParentNode("h2", [LeafNode(None, "Recent Posts")]),
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "First Post:"),
                                LeafNode(
                                    None, " Some interesting content here with "),
                                LeafNode("i", "italic"),
                                LeafNode(None, " and "),
                                LeafNode("b", "bold"),
                                LeafNode(None, " text."),
                            ],
                        ),
                    ],
                ),
                ParentNode(
                    "footer",
                    [
                        LeafNode(None, "Copyright "),
                        LeafNode("span", "2024", {"class": "year"}),
                    ],
                ),
            ],
        )

        expected = (
            "<article><header><h1>Welcome to my Blog</h1><nav>"
            '<a href="/">Home</a> | <a href="/about">About</a></nav></header>'
            "<section><h2>Recent Posts</h2><p><b>First Post:</b> Some interesting "
            "content here with <i>italic</i> and <b>bold</b> text.</p></section>"
            '<footer>Copyright <span class="year">2024</span></footer></article>'
        )

        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
