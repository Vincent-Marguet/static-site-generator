"""
TextNode class has two methods :
--eq-- : compare two TextNode object
--repr-- : represent the TextNode object's member as a string
"""

from enum import Enum


class TextType(Enum):
    """
    Simple Enum to enumerate all type of inline text
    """

    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Class to handle TextNode
    """

    def __init__(self, content, styles, url=None) -> None:
        self._content = content
        self.styles = styles
        self._url = url

    @property
    def content(self):
        """
        Getter for content member
        """
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def styles(self):
        """
        Getter for styles member
        """
        return self._styles

    @styles.setter
    def styles(self, styles):
        if isinstance(styles, set):
            self._styles = styles
        elif styles is None:
            self._styles = set()
        else:
            # If it's a single TextType, create a set with just that type
            self._styles = {styles}

    @property
    def url(self):
        """
        Getter for url member
        """
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def __eq__(self, other):
        return (
            self.content == other.content
            and self.styles == other.styles
            and self.url == other.url
        )

    def __repr__(self):
        # Get style_type from the set
        style = next(iter(self._styles))
        return f"TextNode({self.content}, {style.value}, {self.url})"
