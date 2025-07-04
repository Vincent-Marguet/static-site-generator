"""
This module hold the class MarkDownNodes
Regexes in place are documented in their respective
implementation
"""

import re

from basenode import BaseNodes
from textnode import TextNode, TextType


class MarkdownNodes(BaseNodes):
    """
    Class holding MD specific methods
    """

    @classmethod
    def text_to_textnodes(cls, text):
        """
        Creates the TextNode objects list by calling each split function
        """
        nodes = [TextNode(text, {TextType.NORMAL})]
        return cls.split_nodes_delimiter(
            cls.split_nodes_link(cls.split_nodes_image(nodes))
        )

    @classmethod
    def split_nodes_image(cls, nodes):
        """
        Takes a list of nodes and split them based on image delimiter
        """

        cls.validate_textnodes(nodes)

        if len(nodes) == 1 and nodes[0].styles != {TextType.NORMAL}:
            return nodes
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
            parsed_text_for_image = cls.extract_markdown_images(text)
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
        for node in nodes:
            if node.styles != {TextType.NORMAL}:
                result_nodes.append(node)
            else:
                result_nodes.extend(split_text(node.content))

        return result_nodes

    @classmethod
    def split_nodes_link(cls, nodes):
        """
        Takes a list of old_nodes and split them based on link delimiter
        """
        cls.validate_textnodes(nodes)
        if len(nodes) == 1 and nodes[0].styles != {TextType.NORMAL}:
            return nodes
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
            parsed_text_for_link = cls.extract_markdown_links(text)
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
        for node in nodes:
            if node.styles != {TextType.NORMAL}:
                result_nodes.append(node)
            else:
                result_nodes.extend(split_text(node.content))

        return result_nodes

    @classmethod
    def split_nodes_delimiter(cls, nodes):
        """
        Take a list of nodes and split them based on first delimiter found
        """
        # Validation checks via helper function
        cls.validate_textnodes(nodes)
        result_nodes = []

        def split_text(text, current_styles):
            """
            Split text based on first delimiter found (*, **, ***, _, __, or `),
            create TextNodes with appropriate combined styles
            """
            # Base case
            if not text:
                return []

            # No delimiters found
            positions = cls.find_delimiters_first_position(text)
            if all(pos == -1 for pos in positions):
                return [TextNode(text, current_styles or {TextType.NORMAL})]

            delimiter = None
            new_style = None
            # Determine which delimiter comes first and what style to apply.
            # If delimiter is "`" or "***", we do not want to apply a new_style because
            # we want {TextType.CODE} to be only code and render the rest of the string
            # unchanged and {TextType.BOLD, TextType.ITALIC} is already a combined style.
            # These styles are applied by the apply_style helper function.
            # So we really want to call extend on the between_text if and only if between_style
            # is either {TextType.ITALIC} or {TextType.BOLD} in case they are nested in one another.
            # Here we indicate the tuple positions :
            #     first_backtick = positions[0]
            #     first_triple_asterisk = positions[1]
            #     first_double_asterisk = positions[2]
            #     first_double_underscore = positions[3]
            #     first_single_asterisk = positions[4]
            #     first_single_underscore = positions[5]

            if cls.is_first_position(
                positions[0],
                [
                    positions[1],
                    positions[2],
                    positions[3],
                    positions[4],
                    positions[5],
                ],
            ):
                first_pos = positions[0]
                delimiter = "`"

            elif cls.is_first_position(
                positions[1],
                [
                    positions[0],
                    positions[2],
                    positions[3],
                    positions[4],
                    positions[5],
                ],
            ):
                first_pos = positions[1]
                delimiter = "***"

            elif cls.is_first_position(
                positions[2],
                [
                    positions[0],
                    positions[1],
                    positions[3],
                    positions[4],
                    positions[5],
                ],
            ):
                first_pos = positions[2]
                delimiter = "**"
                new_style = TextType.BOLD

            elif cls.is_first_position(
                positions[3],
                [
                    positions[0],
                    positions[1],
                    positions[2],
                    positions[4],
                    positions[5],
                ],
            ):
                first_pos = positions[3]
                delimiter = "__"
                new_style = TextType.BOLD

            elif cls.is_first_position(
                positions[4],
                [
                    positions[0],
                    positions[1],
                    positions[2],
                    positions[3],
                    positions[5],
                ],
            ):
                first_pos = positions[4]
                delimiter = "*"
                new_style = TextType.ITALIC

            else:
                first_pos = positions[5]
                delimiter = "_"
                new_style = TextType.ITALIC

            if first_pos == -1:
                # No delimiter found, return the text as-is
                return [TextNode(text, current_styles or {TextType.NORMAL})]

            second_pos = cls.find_matching_delimiter(
                text, delimiter, first_pos)
            nodes = []
            # Text before delimiter
            if first_pos > 0:
                nodes.append(
                    TextNode(text[:first_pos],
                             current_styles or {TextType.NORMAL})
                )
            # We calculate between_text
            between_text = text[first_pos + len(delimiter): second_pos]
            # We calculate remaining text
            remaining_text = text[second_pos + len(delimiter):]
            # We get between_styles
            between_styles = cls.apply_style(
                delimiter, current_styles, new_style)

            if between_styles == {TextType.CODE}:
                # We add the node and go directly to extend on the remaining_text
                nodes.append(TextNode(between_text, between_styles))
            else:
                # Process the text between delimiters with combined styles
                nodes.extend(split_text(between_text, between_styles))
            # Process remaining text after second delimiter
            nodes.extend(split_text(remaining_text, current_styles))

            return nodes

        # Process each node
        for node in nodes:
            if node.styles != {TextType.NORMAL}:
                result_nodes.append(node)
            else:
                result_nodes.extend(split_text(node.content, set()))

        return result_nodes

    @classmethod
    def validate_textnodes(cls, nodes):
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

    @classmethod
    def find_delimiters_first_position(cls, text):
        """
        Check if single is really a double/triple
        of if a double is a triple here, before if/elif chain
        in split_nodes_delimiter function
        """
        # Find first occurrence of each delimiter
        first_triple_asterisk = text.find("***")
        first_double_asterisk = text.find("**")
        first_single_asterisk = text.find("*")
        first_backtick = text.find("`")
        first_single_underscore = text.find("_")
        first_double_underscore = text.find("__")

        # Ensure single * or _ is not part of a double/triple
        # and adjust search position accordingly
        if first_single_asterisk == first_double_asterisk:
            first_single_asterisk = text.find("*", first_double_asterisk + 2)
        if first_single_asterisk == first_triple_asterisk:
            first_single_asterisk = text.find("*", first_triple_asterisk + 3)
        if first_single_underscore == first_double_underscore:
            first_single_underscore = text.find(
                "_", first_double_underscore + 2)
        # Ensure double * is not part of triple
        # and adjust search position accordingly
        if first_double_asterisk == first_triple_asterisk:
            first_double_asterisk = text.find("**", first_triple_asterisk + 3)

        return (
            first_backtick,
            first_triple_asterisk,
            first_double_asterisk,
            first_double_underscore,
            first_single_asterisk,
            first_single_underscore,
        )

    @classmethod
    def find_matching_delimiter(cls, text, delimiter, first_pos):
        """
        Find the matching delimiter for first_pos in text
        """
        # Find matching delimiter
        if delimiter == "_":
            second_pos = text.find(delimiter, first_pos + len(delimiter))
            # In case of single _ keeps searching till next valid single
            while second_pos != -1 and not cls.is_valid_single_underscore(
                text, second_pos
            ):
                second_pos = text.find(delimiter, second_pos + 1)

        elif delimiter == "__":
            second_pos = text.find(delimiter, first_pos + len(delimiter))
            while second_pos != -1 and not cls.is_valid_double_underscore(
                text, second_pos
            ):
                second_pos = text.find(delimiter, second_pos + 1)
        elif delimiter == "*":
            second_pos = text.find(delimiter, first_pos + len(delimiter))
            # In case of single * keeps searching till next valid single
            while second_pos != -1 and not cls.is_valid_single_asterisk(
                text, second_pos
            ):
                second_pos = text.find(delimiter, second_pos + 1)

        elif delimiter == "**":
            second_pos = text.find(delimiter, first_pos + len(delimiter))
            while second_pos != -1 and not cls.is_valid_double_asterisk(
                text, second_pos
            ):
                second_pos = text.find(delimiter, second_pos + 1)

        else:
            second_pos = text.find(delimiter, first_pos + len(delimiter))

        if second_pos == -1:
            raise ValueError(f"No matching delimiter {delimiter}")
        return second_pos

    @classmethod
    def is_first_position(cls, pos, other_positions):
        """
        Return True if pos is valid and comes before all other valid positions
        """
        if pos == -1:
            return False
        return all(pos < other_pos or other_pos == -1 for other_pos in other_positions)

    @classmethod
    def is_valid_single_asterisk(cls, text, pos):
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

    @classmethod
    def is_valid_double_asterisk(cls, text, pos):
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

    @classmethod
    def is_valid_single_underscore(cls, text, pos):
        """
        Check if the underscore at position pos is a valid single underscore
        (not part of double or triple).
        """
        # Check backwards
        if pos > 0 and text[pos - 1] == "_":
            return False
        if pos > 1 and text[pos - 2] == "_" and text[pos - 1] == "_":
            return False

        # Check forwards
        if pos < len(text) - 1 and text[pos + 1] == "_":
            return False
        if pos < len(text) - 2 and text[pos + 2] == "_" and text[pos + 1] == "_":
            return False

        return True

    @classmethod
    def is_valid_double_underscore(cls, text, pos):
        """
        Check if the underscore at position pos is a valid double underscore
        (not part of triple).
        """
        # Check backwards
        if pos > 0 and text[pos - 1] == "_":
            return False

        if pos > 1 and text[pos - 2] == "_" and text[pos - 1] == "_":
            return False

        # Check forwards
        if pos < len(text) - 2 and text[pos + 2] == "_" and text[pos + 1] == "_":
            return False

        return True

    @classmethod
    def apply_style(cls, delimiter, current_styles, new_style=None):
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

    @classmethod
    def extract_markdown_images(cls, text):
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

    @classmethod
    def extract_markdown_links(cls, text):
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
