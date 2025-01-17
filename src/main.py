#!/usr/bin/env -S python3 -i

"""
Main module for MD-HTML Project
"""

from textnode import TextNode, TextType


def main():
    """
    The main function
    """
    new_text_node = TextNode(
        text="it is a test",
        text_type=TextType.ITALIC,
    )
    print(new_text_node)


if __name__ == "__main__":
    main()
