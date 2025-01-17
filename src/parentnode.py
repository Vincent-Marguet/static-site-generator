"""
This module implement ParentNode child class from HTMLNode parent class
"""

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """
    ParentNode class is a child from HTMLNode class
    """

    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have at least one child")
        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{''.join(map(lambda x: x.to_html(), self.children))
               }</{self.tag}>"
        )
