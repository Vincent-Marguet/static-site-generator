"""
This module hold converting between format functions
"""

from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html(text_node: TextNode):
    """
    Convert a TextNode in HTMLNode
    """
    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(
                f"text_type member of {text_node}"
                "not present in TextType enum in textnode.py"
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Take a list of old_nodes and split them based on delimiter
    """
    # Validation
    if not old_nodes:
        raise ValueError("nodes list cannot be empty")
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"{node} is not a valid TextNode")

    result_nodes = []

    def split_text(text):
        """
        Split, create two TextNode if necessary (delimiter found)
        and return nodes list
        """
        # Base case
        if not text:
            return []

        # Find first delimiter pair
        first = text.find(delimiter)
        if first == -1:
            return [TextNode(text, TextType.NORMAL)]

        # Find matching delimiter
        second = text.find(delimiter, first + len(delimiter))
        if second == -1:
            raise ValueError(f"No matching delimiter {delimiter}")

        nodes = []
        if first > 0:
            nodes.append(TextNode(text[:first], TextType.NORMAL))
        nodes.append(TextNode(text[first + len(delimiter): second], text_type))
        remaining_text = text[second + len(delimiter):]
        nodes.extend(split_text(remaining_text))
        return nodes

    # Process each node
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.text))

    return result_nodes
