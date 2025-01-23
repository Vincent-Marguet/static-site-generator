"""
This module hold all functions dedicated to
the pipeline text to textnodes
"""

import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    """
    Creates the TextNode objects list by calling each split function
    """
    nodes = [TextNode(text, {TextType.NORMAL})]
    return split_nodes_delimiter(split_nodes_link(split_nodes_image(nodes)))


def split_nodes_delimiter(old_nodes):
    """
    Take a list of old_nodes and split them based on first delimiter found
    """
    # Validation checks via helper function
    validate_textnodes(old_nodes)
    result_nodes = []

    def split_text(text, current_styles):
        """
        Split text based on first delimiter found (*, **, *** or `),
        create TextNodes with appropriate combined styles
        """
        # Base case
        if not text:
            return []

        first_single, first_double, first_triple, first_backtick = (
            find_delimiters_first_position(text)
        )
        # No delimiters found
        if (
            first_single == -1
            and first_double == -1
            and first_triple == -1
            and first_backtick == -1
        ):
            return [TextNode(text, current_styles or {TextType.NORMAL})]

        first_pos = -1
        delimiter = None
        new_style = None
        # Determine which delimiter comes first and what style to apply.
        # If delimiter is "`" or "***", we do not want to apply a new_style because
        # we want {TextType.CODE} to be only code and render the rest of the string
        # unchanged and {TextType.BOLD, TextType.ITALIC} is already a combined style.
        # These styles are applied by the apply_style helper function.
        # So we really want to call extend on the between_text if and only if between_style
        # is either {TextType.ITALIC} or {TextType.BOLD} in case they are nested in one another.
        if (
            first_backtick != -1
            and (first_backtick < first_single or first_single == -1)
            and (first_backtick < first_double or first_double == -1)
        ):
            first_pos = first_backtick
            delimiter = "`"

        elif (
            first_triple != -1
            and (first_triple < first_single or first_single == -1)
            and (first_triple < first_double or first_double == -1)
        ):
            first_pos = first_triple
            delimiter = "***"

        elif first_double != -1 and (first_double < first_single or first_single == -1):
            first_pos = first_double
            delimiter = "**"
            new_style = TextType.BOLD
        else:
            first_pos = first_single
            delimiter = "*"
            new_style = TextType.ITALIC

        second_pos = find_matching_delimiter(text, delimiter, first_pos)
        nodes = []
        # Text before delimiter
        if first_pos > 0:
            nodes.append(
                TextNode(text[:first_pos], current_styles or {TextType.NORMAL})
            )
        # We calculate between_text
        between_text = text[first_pos + len(delimiter): second_pos]
        # We calculate remaining text
        remaining_text = text[second_pos + len(delimiter):]
        # We get between_styles
        between_styles = apply_style(delimiter, current_styles, new_style)

        if between_styles in ({TextType.CODE}, {TextType.BOLD, TextType.ITALIC}):
            # We add the node and go directly to extend on the remaining_text
            nodes.append(TextNode(between_text, between_styles))
        else:
            # Process the text between delimiters with combined styles
            nodes.extend(split_text(between_text, between_styles))
        # Process remaining text after second delimiter
        nodes.extend(split_text(remaining_text, current_styles))

        return nodes

    # Process each node
    for node in old_nodes:
        if node.styles != {TextType.NORMAL}:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.content, set()))

    return result_nodes


def split_nodes_image(old_nodes):
    """
    Takes a list of old_nodes and split them based on image delimiter
    """

    validate_textnodes(old_nodes)

    if len(old_nodes) == 1 and old_nodes[0].styles != {TextType.NORMAL}:
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
            return [TextNode(text, {TextType.NORMAL})]

        # Unpack the tuple returned by the regex
        alt_text_image, url_image = parsed_text_for_image[0]
        # Find first delimiter image
        delimiter = f"![{alt_text_image}]({url_image})"
        # ['text before', 'text after']
        sections = text.split(delimiter, 1)

        if sections[0]:
            image_nodes.append(TextNode(sections[0], {TextType.NORMAL}))

        image_nodes.append(
            TextNode(alt_text_image, {TextType.IMAGE}, url_image))
        # Launch recursive call
        if len(sections) > 1 and sections[1]:
            image_nodes.extend(split_text(sections[1]))

        return image_nodes

    # Process each node
    for node in old_nodes:
        if node.styles != {TextType.NORMAL}:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.content))

    return result_nodes


def split_nodes_link(old_nodes):
    """
    Takes a list of old_nodes and split them based on link delimiter
    """
    validate_textnodes(old_nodes)
    if len(old_nodes) == 1 and old_nodes[0].styles != {TextType.NORMAL}:
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
            return [TextNode(text, {TextType.NORMAL})]

        # Unpack the first tuple returned by the regex
        link_text, link_url = parsed_text_for_link[0]
        # Find first delimiter link
        delimiter = f"[{link_text}]({link_url})"
        # ['text before', 'text after']
        sections = text.split(delimiter, 1)

        if sections[0]:
            link_nodes.append(TextNode(sections[0], {TextType.NORMAL}))

        link_nodes.append(TextNode(link_text, {TextType.LINK}, link_url))
        # Launch recursive call
        if len(sections) > 1 and sections[1]:
            link_nodes.extend(split_text(sections[1]))

        return link_nodes

    # Process each node
    for node in old_nodes:
        if node.styles != {TextType.NORMAL}:
            result_nodes.append(node)
        else:
            result_nodes.extend(split_text(node.content))

    return result_nodes


def validate_textnodes(nodes):
    """
    Checks run before processing the nodes in split functions
    """
    if not nodes:
        raise ValueError("Nodes list cannot be empty")
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
        if not isinstance(node.content, str):
            raise ValueError(
                f"TextNode 'text' attribute must be a string. Found: {
                    type(node.content)}"
            )

        # Ensure 'type' matches a valid TextType
        for style in node.styles:
            if style not in TextType:
                raise ValueError(
                    f"TextNode type {
                        node.styles} is not a valid TextType"
                )

        # If the node is of a type that requires a URL, check for its existence/validity
        if node.styles in [{TextType.IMAGE}, {TextType.LINK}]:
            if not isinstance(node.url, str) or not node.url:
                raise ValueError(
                    f"TextNode of type {
                        node.styles} must have a non-empty 'url' string. Found: {node.url}"
                )

    return True


def find_delimiters_first_position(text):
    """
    Check if single is really a double/triple
    of if a double is a triple here, before if/elif chain
    in split_nodes_delimiter function
    """
    # Find first occurrence of each delimiter
    first_triple = text.find("***")
    first_double = text.find("**")
    first_single = text.find("*")
    first_backtick = text.find("`")

    # Ensure single * is not part of a double/triple
    # and adjust search position accordingly
    if first_single == first_double:
        first_single = text.find("*", first_double + 2)
    if first_single == first_triple:
        first_single = text.find("*", first_triple + 3)
    # Ensure double * is not part of triple
    # and adjust search position accordingly
    if first_double == first_triple:
        first_double = text.find("**", first_triple + 3)

    return first_single, first_double, first_triple, first_backtick


def find_matching_delimiter(text, delimiter, first_pos):
    """
    Find the matching delimiter for first_pos in text
    """
    # Find matching delimiter
    if delimiter == "*":
        second_pos = text.find(delimiter, first_pos + len(delimiter))
        # In case of single * keeps searching till next valid single
        while second_pos != -1 and not is_valid_single_asterisk(text, second_pos):
            second_pos = text.find(delimiter, second_pos + 1)
    elif delimiter == "**":
        second_pos = text.find(delimiter, first_pos + len(delimiter))
        while second_pos != -1 and not is_valid_double_asterisk(text, second_pos):
            second_pos = text.find(delimiter, second_pos + 1)
    else:
        second_pos = text.find(delimiter, first_pos + len(delimiter))

    if second_pos == -1:
        raise ValueError(f"No matching delimiter {delimiter}")
    return second_pos


def is_valid_single_asterisk(text, pos):
    """
    Check if the asterisk at position pos is a valid single asterisk
    (not part of double or triple).
    """
    # Check backwards
    if pos > 0 and text[pos - 1] == "*":
        return False
    if pos > 1 and text[pos - 2] == "*" and text[pos - 1] == "*":
        return False

    # Check forwards
    if pos < len(text) - 1 and text[pos + 1] == "*":
        return False
    if pos < len(text) - 2 and text[pos + 2] == "*" and text[pos + 1] == "*":
        return False

    return True


def is_valid_double_asterisk(text, pos):
    """
    Check if the asterisk at position pos is a valid double asterisk
    (not part of triple).
    """
    # Check backwards
    if pos > 0 and text[pos - 1] == "*":
        return False

    if pos > 1 and text[pos - 2] == "*" and text[pos - 1] == "*":
        return False

    # Check forwards
    if pos < len(text) - 2 and text[pos + 2] == "*" and text[pos + 1] == "*":
        return False

    return True


def apply_style(delimiter, current_styles, new_style=None):
    """
    Apply style following conditions
    """
    # Text between delimiters - combine styles
    if delimiter == "`":
        between_styles = {TextType.CODE}
    elif delimiter == "***" and current_styles != {TextType.CODE}:
        between_styles = {TextType.BOLD, TextType.ITALIC}
    else:
        between_styles = current_styles.copy() if current_styles else set()
        if new_style is not None and current_styles != {TextType.CODE}:
            between_styles.add(new_style)
    return between_styles


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
