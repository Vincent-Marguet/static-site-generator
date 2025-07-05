"""
Test case class for TextNode class
"""

import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """
    Test cases for TextNode class
    """

    def test_eq(self):
        """
        Test the eq method
        """
        node1 = TextNode("This is a test text node", TextType.ITALIC)
        node2 = TextNode("This is a test text node", TextType.ITALIC)
        node3 = TextNode("This is a text node", TextType.NORMAL)
        node4 = TextNode("This is a text node", TextType.NORMAL)
        node5 = TextNode("This is a text node", TextType.NORMAL)
        node6 = TextNode(
            "Testing is insanely good", TextType.BOLD, "https://www.babouya.net"
        )
        node7 = TextNode(
            "Testing is insanely good", TextType.BOLD, "https://www.babouya.net"
        )

        self.assertEqual(node1, node2)
        self.assertEqual(node5, node3)
        self.assertEqual(node5, node4)
        self.assertEqual(node4, node3)
        self.assertEqual(node6, node7)

    def test_repr(self):
        """
        Test the repr method
        """
        node = TextNode("This is a test text node", TextType.ITALIC)
        node2 = TextNode("I LOVE testing", TextType.BOLD,
                         "https://www.babouya.net")
        self.assertEqual(
            repr(node), "TextNode(This is a test text node, italic, None)")
        self.assertEqual(
            repr(node2),
            "TextNode(I LOVE testing, bold, https://www.babouya.net)",
        )

    def test_not_eq(self):
        """
        Test if not equal if text is the same but TextType is different
        """
        node1 = TextNode("This is a test text node", TextType.ITALIC)
        node2 = TextNode("I LOVE testing", TextType.BOLD,
                         "https://www.babouya.net")
        node3 = TextNode("This is a text node", TextType.NORMAL)
        node4 = TextNode("This is a text node", TextType.BOLD)
        node5 = TextNode("This is a text node", TextType.NORMAL)
        node6 = TextNode(
            "More testing is always good", TextType.ITALIC, "https://www.babouya.net"
        )
        node7 = TextNode(
            "More testing is always good", TextType.ITALIC, "http://www.babouya.net"
        )

        self.assertNotEqual(node4, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node5, node4)
        self.assertEqual(node5, node3)
        # Last line test case with same text/type but different URL
        self.assertNotEqual(node7, node6)


if __name__ == "__main__":
    unittest.main()
