"""
This module implement LeafNode child class from HTMLNode parent class
"""

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    LeafNode class can have no children member
    and must have tag and value. props is optional
    """

    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("a leaf node *must* have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
