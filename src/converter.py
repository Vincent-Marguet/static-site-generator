"""
This module hold converting between format functions
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
    validate_textnodes(old_nodes)

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
        # Launch recursive call
        nodes.extend(split_text(remaining_text))
        return nodes

    # Process each node
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.text))

    return result_nodes


def split_nodes_image(old_nodes):
    """
    Takes a list of old_nodes and split them based on image delimiter
    """

    validate_textnodes(old_nodes)

    if len(old_nodes) == 1 and old_nodes[0].text_type != TextType.NORMAL:
        return old_nodes
    result_nodes = []

    def split_text(text):
        """
        Split, create two TextNode if necessary (image delimiter found)
        and return nodes list
        """
        # Base case
        if not text:
            return []

        image_nodes = []
        parsed_text_for_image = extract_markdown_images(text)
        if len(parsed_text_for_image) == 0:
            return [TextNode(text, TextType.NORMAL)]

        # Unpack the tuple returned by the regex
        alt_text_image, url_image = parsed_text_for_image[0]
        # Find first delimiter image
        delimiter = f"![{alt_text_image}]({url_image})"
        # ['text before', 'text after']
        sections = text.split(delimiter, 1)

        if sections[0]:
            image_nodes.append(TextNode(sections[0], TextType.NORMAL))

        image_nodes.append(TextNode(alt_text_image, TextType.IMAGE, url_image))
        # Launch recursive call
        if len(sections) > 1 and sections[1]:
            image_nodes.extend(split_text(sections[1]))

        return image_nodes

    # Process each node
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.text))

    return result_nodes


def split_nodes_link(old_nodes):
    """
    Takes a list of old_nodes and split them based on link delimiter
    """
    validate_textnodes(old_nodes)
    if len(old_nodes) == 1 and old_nodes[0].text_type != TextType.NORMAL:
        return old_nodes
    result_nodes = []

    def split_text(text):
        """
        Split, create two TextNode if necessary (link delimiter found)
        and return nodes list
        """
        # Base case
        if not text:
            return []

        link_nodes = []

        # Return a list of tuple
        parsed_text_for_link = extract_markdown_links(text)
        # Case where there is no link in the TextNode
        if len(parsed_text_for_link) == 0:
            return [TextNode(text, TextType.NORMAL)]

        # Unpack the first tuple returned by the regex
        link_text, link_url = parsed_text_for_link[0]
        # Find first delimiter link
        delimiter = f"[{link_text}]({link_url})"
        # ['text before', 'text after']
        sections = text.split(delimiter, 1)

        if sections[0]:
            link_nodes.append(TextNode(sections[0], TextType.NORMAL))

        link_nodes.append(TextNode(link_text, TextType.LINK, link_url))
        # Launch recursive call
        if len(sections) > 1 and sections[1]:
            link_nodes.extend(split_text(sections[1]))

        return link_nodes

    # Process each node
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.text))

    return result_nodes


def text_to_textnodes(text):
    """
    Creates the TextNode objects by calling each split function
    """
    nodes = [TextNode(text, TextType.NORMAL)]
    split1 = split_nodes_image(nodes)
    split2 = split_nodes_link(split1)
    split3 = split_nodes_delimiter(split2, "**", TextType.BOLD)
    split4 = split_nodes_delimiter(split3, "*", TextType.ITALIC)
    split5 = split_nodes_delimiter(split4, "`", TextType.CODE)
    return split5


def validate_textnodes(nodes):
    """
    Checks run before processing the nodes in split functons
    """
    if not nodes:
        raise ValueError("nodes list cannot be empty")
    if not isinstance(nodes, list):
        raise ValueError("Nodes must be provided as a list.")

    for node in nodes:
        # Check if the object is an instance of TextNode
        if not isinstance(node, TextNode):
            raise TypeError(
                f"Invalid node detected: {
                    node}. Must be a TextNode."
            )

        # Check that the 'text' field is a string
        if not isinstance(node.text, str):
            raise ValueError(
                f"TextNode 'text' attribute must be a string. Found: {
                    type(node.text)}"
            )

        # Ensure 'type' matches a valid TextType (you'd define these elsewhere)
        if node.text_type not in TextType:
            raise ValueError(
                f"TextNode 'type' is not a valid TextType: {node.text_type}"
            )

        # If the node is of a type that requires a URL, check for its existence/validity
        if node.text_type in [TextType.IMAGE, TextType.LINK]:
            if not isinstance(node.url, str) or not node.url:
                raise ValueError(
                    f"TextNode of type {
                        node.text_type} must have a non-empty 'url' string. Found: {node.url}"
                )

    return True


def extract_markdown_images(text):
    """
    Use a regex ro return a list of tuple ("alt_text", "url")
    """
    #    IMAGE_PATTERN = r"""
    #    !                  # literal exclamation mark
    #    \[                 # literal opening bracket
    #    ([^\[\]]*)         # first capture group (alt text)
    #    \]                 # literal closing bracket
    #    \(                 # literal opening paren
    #    ([^\(\)]*)         # second capture group (url)
    #    \)                 # literal closing paren
    #    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """
    Use a regex to return a list of tuple ("anchor_text", "url")
    """
    #    LINK_PATTERN = r"""
    #    (?<!!)             # negative lookbehind for !
    #    \[                 # literal opening bracket
    #    ([^\[\]]*)         # first capture group (link text)
    #    \]                 # literal closing bracket
    #    \(                 # literal opening paren
    #    ([^\(\)]*)         # second capture group (url)
    #    \)                 # literal closing paren
    #    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
