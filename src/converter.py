"""
This module hold converting between format functions
and some associated helper functions
Regexes in place are documented in their respective
implementation
"""

import re

from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html(text_node: TextNode):
    """
    Convert a TextNode in HTMLNode
    """
    # Get style_type from the set
    style = next(iter(text_node.styles))

    match style:
        case TextType.NORMAL:
            return LeafNode(None, text_node.content)
        case TextType.BOLD:
            return LeafNode("b", text_node.content)
        case TextType.ITALIC:
            return LeafNode("i", text_node.content)
        case TextType.CODE:
            return LeafNode("code", text_node.content)
        case TextType.LINK:
            return LeafNode("a", text_node.content, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.content})
        case _:
            raise ValueError(
                f"styles member of {text_node}"
                "not present in TextType enum in textnode.py"
            )


def markdown_to_blocks(markdown_text):
    """
    Create MarkDown blocks from a MarkDown text, return a list of blocks
    """
    # Base case
    if not markdown_text:
        return []

    split = markdown_text.split("\n\n")

    # Filter out empty or whitespace-only blocks
    split_filtered = list(filter(lambda x: x.strip(), split))

    # After filtering, we use recursive call
    ret = split_filtered[0].strip()
    remaining = "\n\n".join(split_filtered[1:])

    return [ret] + markdown_to_blocks(remaining)


def block_to_block_type(block):
    """
    Take a block and return a string block type.
    - heading starts with 1 to 6 "#" and a space
    - code start with "```" and end with "```"
    - quote has > at each start of line in the block
    - unordered lists starts with "*" or "-" followed by a space
    - ordered_list must start at "1." and increment with same format
    """

    lines = block.split("\n")

    if re.findall(r"^#{1,6}\s", block):
        return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    if all(line.startswith(">") for line in lines):
        return "quote"

    if all(line.startswith(("*", "-")) and line[1:2] == " " for line in lines):
        return "unordered_list"

    if len(lines) > 1 and all(
        line[0].isdigit() and line.startswith(f"{i+1}. ")
        for i, line in enumerate(lines)
    ):
        return "ordered_list"

    return "paragraph"
