"""
This module hold converting between format functions
and some associated helper functions
Regexes in place are documented in their respective
implementation
"""

import re

from leafnode import LeafNode
from markdownnode import MarkdownNodes
from parentnode import ParentNode
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


def markdown_to_html_node(markdown_text):
    """
    Convert a MD formatted text into HTML Nodes
    """

    blocks = markdown_to_blocks(markdown_text)

    # Base case
    if not blocks:
        return ParentNode(tag="div", children=[])

    block_type = block_to_block_type(blocks[0])
    all_nodes = []

    # Heading case
    if block_type == "heading":
        text_nodes = MarkdownNodes.text_to_textnodes(
            blocks[0].lstrip("#").lstrip())
        html_nodes = [text_node_to_html(node) for node in text_nodes]
        all_nodes.append(
            ParentNode(
                tag=f"h{blocks[0].count('#')}",
                children=html_nodes,
            )
        )

    # Code case
    elif block_type == "code":
        text_nodes = MarkdownNodes.text_to_textnodes(
            blocks[0].lstrip("```").rstrip("```").strip()
        )
        html_nodes = [text_node_to_html(node) for node in text_nodes]
        code_node = ParentNode(tag="code", children=html_nodes)
        all_nodes.append(ParentNode(tag="pre", children=[code_node]))

    # Quote case
    elif block_type == "quote":
        text_nodes = MarkdownNodes.text_to_textnodes(
            blocks[0].lstrip(">").lstrip())
        html_nodes = [text_node_to_html(node) for node in text_nodes]
        all_nodes.append(ParentNode(tag="blockquote", children=html_nodes))

    # Unordered list case
    elif block_type == "unordered_list":
        li_nodes = []
        items = blocks[0].split("\n")
        for item in items:
            text_nodes = MarkdownNodes.text_to_textnodes(
                item.lstrip("- ").lstrip("* "))
            html_nodes = [text_node_to_html(node) for node in text_nodes]
            li_node = ParentNode(tag="li", children=html_nodes)
            li_nodes.append(li_node)
        all_nodes.append(ParentNode(tag="ul", children=li_nodes))

    # Ordered list case
    elif block_type == "ordered_list":
        li_nodes = []
        items = blocks[0].split("\n")
        for item in items:
            text_nodes = MarkdownNodes.text_to_textnodes(
                re.sub(r"^\d\.\s+", "", item))
            html_nodes = [text_node_to_html(node) for node in text_nodes]
            li_node = ParentNode(tag="li", children=html_nodes)
            li_nodes.append(li_node)
        all_nodes.append(ParentNode(tag="ol", children=li_nodes))

    # Paragraph case
    else:
        text_nodes = MarkdownNodes.text_to_textnodes(blocks[0])
        html_nodes = [text_node_to_html(node) for node in text_nodes]
        all_nodes.append(ParentNode(tag="p", children=html_nodes))

    if len(blocks) > 1:
        remaining_blocks = "\n\n".join(blocks[1:])
        next_node = markdown_to_html_node(remaining_blocks)
        all_nodes = all_nodes + next_node.children

    return ParentNode(tag="div", children=all_nodes)
