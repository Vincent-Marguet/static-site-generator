import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_basic_parent_with_single_child(self):
        node = ParentNode("div", [LeafNode("span", "hello")])
        self.assertEqual(node.to_html(), "<div><span>hello</span></div>")

    def test_parent_with_multiple_children(self):
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
        node = ParentNode("div", [ParentNode("p", [LeafNode("span", "nested")])])
        self.assertEqual(node.to_html(), "<div><p><span>nested</span></p></div>")

    def test_parent_with_props(self):
        node = ParentNode("div", [LeafNode("span", "hello")], {"class": "greeting"})
        self.assertEqual(
            node.to_html(), '<div class="greeting"><span>hello</span></div>'
        )

    def test_no_tag_raises_error(self):
        node = ParentNode(None, [LeafNode("span", "hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
