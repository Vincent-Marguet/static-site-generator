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

    def __init__(self, text, text_type, url=None) -> None:
        self._text = text
        self._text_type = text_type
        self._url = url

    @property
    def text(self):
        """
        Getter for text member
        """
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def text_type(self):
        """
        Getter for text_type member
        """
        return self._text_type

    @text_type.setter
    def text_type(self, text_type):
        self._text_type = text_type

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
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
