"""
Test case class for HTMLNode class
"""

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    """
    Test cases for HTMLNode class
    """

    def test_props_to_html(self):
        """
        Test the props_to_html method
        """

    # A <p> tag with some text
    paragraph_node = HTMLNode(tag="p", value="This is a test paragraph.")
    assert paragraph_node.props_to_html() == ""  # No properties

    # An <a> tag with a href and target attribute
    link_node = HTMLNode(
        tag="a",
        value="Click here",
        props={"href": "https://example.com", "target": "_blank"},
    )
    assert link_node.props_to_html() == ' href="https://example.com" target="_blank"'

    # A <div> tag with inline styles as nested props
    div_node = HTMLNode(
        tag="div",
        props={"style": {"color": "red", "font-size": "16px"}, "id": "test-div"},
    )
    assert (
        div_node.props_to_html() == ' style="color:red; font-size:16px" id="test-div"'
    )
    # A <ul> tag with nested <li> children
    list_node = HTMLNode(
        tag="ul",
        children=[
            HTMLNode(tag="li", value="First item"),
            HTMLNode(tag="li", value="Second item"),
        ],
    )
    assert isinstance(
        list_node.children, list
    )  # The children should be a list of HTMLNodes


if __name__ == "__main__":
    unittest.main()
