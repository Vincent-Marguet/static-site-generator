"""
This module hold test cases for split_nodes module
functions
"""

import unittest

from src.markdownnode import MarkdownNodes
from src.textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    """
    Test class for text_to_textnodes function
    """

    def test_plain_text(self):
        """
        Check against plain text
        """
        input_text = "This is plain text."
        expected_output = [TextNode("This is plain text.", {TextType.NORMAL})]
        self.assertEqual(MarkdownNodes.text_to_textnodes(
            input_text), expected_output)

    def test_bold_text(self):
        """
        Check against bold text
        """
        input_text = "This is **bold** text."
        expected_output = [
            TextNode("This is ", {TextType.NORMAL}),
            TextNode("bold", {TextType.BOLD}),
            TextNode(" text.", {TextType.NORMAL}),
        ]
        self.assertEqual(MarkdownNodes.text_to_textnodes(
            input_text), expected_output)

    def test_italic_text(self):
        """
        Check against italic text
        """
        input_text = "Text with *italic* style."
        expected_output = [
            TextNode("Text with ", {TextType.NORMAL}),
            TextNode("italic", {TextType.ITALIC}),
            TextNode(" style.", {TextType.NORMAL}),
        ]
        self.assertEqual(MarkdownNodes.text_to_textnodes(
            input_text), expected_output)

    def test_combined_styles(self):
        """
        Check against bold and italic text
        """
        input_text = "Mix of **bold** and *italic* styles."
        expected_output = [
            TextNode("Mix of ", {TextType.NORMAL}),
            TextNode("bold", {TextType.BOLD}),
            TextNode(" and ", {TextType.NORMAL}),
            TextNode("italic", {TextType.ITALIC}),
            TextNode(" styles.", {TextType.NORMAL}),
        ]
        self.assertEqual(MarkdownNodes.text_to_textnodes(
            input_text), expected_output)

    def test_multiple_inline_and_complex_markdown(self):
        """
        Check against complex MD
        """
        input_text = (
            "Here is a [link](https://example.com) with *italics*, "
            "**bold**, and ![an image](https://image.com)."
        )
        expected_output = [
            TextNode("Here is a ", {TextType.NORMAL}),
            TextNode("link", {TextType.LINK}, "https://example.com"),
            TextNode(" with ", {TextType.NORMAL}),
            TextNode("italics", {TextType.ITALIC}),
            TextNode(", ", {TextType.NORMAL}),
            TextNode("bold", {TextType.BOLD}),
            TextNode(", and ", {TextType.NORMAL}),
            TextNode("an image", {TextType.IMAGE}, "https://image.com"),
            TextNode(".", {TextType.NORMAL}),
        ]
        result = MarkdownNodes.text_to_textnodes(input_text)
        self.assertEqual(result, expected_output)

    def test_nested_formats(self):
        """
        Check against text with both bold and italic
        """
        input_text = "This is ***both bold and italic*** text"
        output = MarkdownNodes.text_to_textnodes(input_text)
        expected = [
            TextNode("This is ", {TextType.NORMAL}),
            TextNode("both bold and italic", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" text", {TextType.NORMAL}),
        ]
        self.assertEqual(output, expected)

    def test_complex_format(self):
        """
        Check against text with italic inside bold
        """
        input_text = (
            "***bold and italic*** something *italic* something ** bold** something"
        )
        expected = [
            TextNode("bold and italic", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" something ", {TextType.NORMAL}),
            TextNode("italic", {TextType.ITALIC}),
            TextNode(" something ", {TextType.NORMAL}),
            TextNode(" bold", {TextType.BOLD}),
            TextNode(" something", {TextType.NORMAL}),
        ]
        output = MarkdownNodes.text_to_textnodes(input_text)
        self.assertEqual(output, expected)

    def test_nested_bold_in_italic(self):
        """
        Check against nested bold in italics
        """
        input_text = "*italic something **bold** something italic* something ***bold and italic***"
        expected = [
            TextNode("italic something ", {TextType.ITALIC}),
            TextNode("bold", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" something italic", {TextType.ITALIC}),
            TextNode(" something ", {TextType.NORMAL}),
            TextNode("bold and italic", {TextType.BOLD, TextType.ITALIC}),
        ]
        output = MarkdownNodes.text_to_textnodes(input_text)
        self.assertEqual(output, expected)

    def test_nested_italic_in_bold(self):
        """
        Check against nested bold in italics
        """
        input_text = (
            "**bold something *italic* something bold** something ***bold and italic***"
        )
        expected = [
            TextNode("bold something ", {TextType.BOLD}),
            TextNode("italic", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" something bold", {TextType.BOLD}),
            TextNode(" something ", {TextType.NORMAL}),
            TextNode("bold and italic", {TextType.BOLD, TextType.ITALIC}),
        ]
        output = MarkdownNodes.text_to_textnodes(input_text)
        self.assertEqual(output, expected)

    def test_simple_nest(self):
        """
        Check against italic nested in bold
        """
        input_text = "**bold *italic-bold* bold**"
        expected = [
            TextNode("bold ", {TextType.BOLD}),
            TextNode("italic-bold", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" bold", {TextType.BOLD}),
        ]
        self.assertEqual(expected, MarkdownNodes.text_to_textnodes(input_text))

    def test_intermediate_nest(self):
        """
        Check against nested code and nested bold in italic
        """
        input_text = "*italic with `code` **bold-italic** and italic*"
        expected = [
            TextNode("italic with ", {TextType.ITALIC}),
            TextNode("code", {TextType.CODE}),
            TextNode(" ", {TextType.ITALIC}),
            TextNode("bold-italic", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" and italic", {TextType.ITALIC}),
        ]
        self.assertEqual(expected, MarkdownNodes.text_to_textnodes(input_text))

    def test_nested_in_code(self):
        """
        Check against nested italic and bold in code
        """
        input_text = "`this is code *all along* **no matter** ***what***`"
        expected = [
            TextNode(
                "this is code *all along* **no matter** ***what***", {
                    TextType.CODE}
            ),
        ]
        self.assertEqual(expected, MarkdownNodes.text_to_textnodes(input_text))

    def test_complex(self):
        """
        Check against a very complex scenario
        """
        input_text = (
            "A very **tricky** string *indeed* [link](https://example.com) "
            "***insane*** **indeed *insane* indeed**"
            " *but it **could** get **even more** insane like this* `or` ** this ** or * this* "
            "or * even * ![alt1](src1) **this ** [link](https://example.com)"
        )
        expected = [
            TextNode("A very ", {TextType.NORMAL}),
            TextNode("tricky", {TextType.BOLD}),
            TextNode(" string ", {TextType.NORMAL}),
            TextNode("indeed", {TextType.ITALIC}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("link", {TextType.LINK}, "https://example.com"),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("insane", {TextType.ITALIC, TextType.BOLD}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("indeed ", {TextType.BOLD}),
            TextNode("insane", {TextType.BOLD, TextType.ITALIC}),
            TextNode(" indeed", {TextType.BOLD}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("but it ", {TextType.ITALIC}),
            TextNode("could", {TextType.ITALIC, TextType.BOLD}),
            TextNode(" get ", {TextType.ITALIC}),
            TextNode("even more", {TextType.ITALIC, TextType.BOLD}),
            TextNode(" insane like this", {TextType.ITALIC}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("or", {TextType.CODE}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode(" this ", {TextType.BOLD}),
            TextNode(" or ", {TextType.NORMAL}),
            TextNode(" this", {TextType.ITALIC}),
            TextNode(" or ", {TextType.NORMAL}),
            TextNode(" even ", {TextType.ITALIC}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("alt1", {TextType.IMAGE}, "src1"),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("this ", {TextType.BOLD}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("link", {TextType.LINK}, "https://example.com"),
        ]
        self.assertEqual(expected, MarkdownNodes.text_to_textnodes(input_text))

    def test_more_complex_for_fun(self):
        """
        Check against asterisks and underscores in the same string
        """
        input_text = "**Tricky _string_ to** __test__"
        expected = [
            TextNode("Tricky ", {TextType.BOLD}),
            TextNode("string", {TextType.ITALIC, TextType.BOLD}),
            TextNode(" to", {TextType.BOLD}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("test", {TextType.BOLD}),
        ]
        self.assertEqual(expected, MarkdownNodes.text_to_textnodes(input_text))

    def test_even_more_complex_for_fun(self):
        """
        Check against asterisks and underscores in the same string
        """
        input_text = "*Tricky __string__ to* _test_"
        expected = [
            TextNode("Tricky ", {TextType.ITALIC}),
            TextNode("string", {TextType.ITALIC, TextType.BOLD}),
            TextNode(" to", {TextType.ITALIC}),
            TextNode(" ", {TextType.NORMAL}),
            TextNode("test", {TextType.ITALIC}),
        ]
        self.assertEqual(expected, MarkdownNodes.text_to_textnodes(input_text))


class TestSplitNodesDelimiter(unittest.TestCase):
    """
    Class test for split_nodes_delimiter function
    """

    def test_basic_code_block(self):
        """
        Check against a simple case
        """
        node = [TextNode("hello *italic* world", {TextType.NORMAL})]
        expected = [
            TextNode("hello ", {TextType.NORMAL}),
            TextNode("italic", TextType.ITALIC),
            TextNode(" world", {TextType.NORMAL}),
        ]
        result = MarkdownNodes.split_nodes_delimiter(node)
        # Note: You'll need to implement __eq__ in TextNode for this to work
        self.assertEqual(result, expected)

    def test_multiple_bold_blocks(self):
        """
        Check against a single TextType other than NORMAL
        """
        node = [TextNode("this **is** some **bold** text", {TextType.NORMAL})]
        expected = [
            TextNode("this ", {TextType.NORMAL}),
            TextNode("is", {TextType.BOLD}),
            TextNode(" some ", {TextType.NORMAL}),
            TextNode("bold", {TextType.BOLD}),
            TextNode(" text", {TextType.NORMAL}),
        ]
        result = MarkdownNodes.split_nodes_delimiter(node)
        self.assertEqual(result, expected)

    def test_non_text_node_preserved(self):
        """
        Check against bold in a normal TextNode
        """
        nodes = [
            TextNode("some ", {TextType.NORMAL}),
            TextNode("**bold**", {TextType.NORMAL}),
            TextNode(" and `code`", {TextType.NORMAL}),
        ]
        expected = [
            TextNode("some ", {TextType.NORMAL}),
            TextNode("bold", {TextType.BOLD}),
            TextNode(" and ", {TextType.NORMAL}),
            TextNode("code", {TextType.CODE}),
        ]
        result = MarkdownNodes.split_nodes_delimiter(nodes)
        self.assertEqual(result, expected)

    def test_missing_delimiter_raises_error(self):
        """
        Check against missing delimiter
        """
        # Method 1: Using context manager (recommended)
        node = [TextNode("text with unclosed *code", {TextType.NORMAL})]
        with self.assertRaises(ValueError):
            MarkdownNodes.split_nodes_delimiter(node)

    def test_invalid_node_type_raises_error(self):
        """
        Check against invalid node
        """
        nodes = [
            TextNode("valid", {TextType.NORMAL}),
            "not a text node",  # This should cause an error
        ]
        with self.assertRaises(TypeError):
            MarkdownNodes.split_nodes_delimiter(nodes)

    def test_complex_mixed_nodes(self):
        """
        Check against a complex structure of nodes
        """
        # Create a complex input with multiple nodes and mixed cases
        nodes = [
            TextNode("Start ", {TextType.NORMAL}),
            TextNode("existing_bold", {TextType.BOLD}),
            TextNode(" then *some italic* followed by ", {TextType.NORMAL}),
            TextNode("more_bold", {TextType.BOLD}),
            TextNode(
                " and *another italic* and *third italic* and text", {
                    TextType.NORMAL}
            ),
            TextNode(" final_italic ", {TextType.ITALIC}),
            TextNode("and **last bold**!", {TextType.NORMAL}),
        ]

        expected = [
            TextNode("Start ", {TextType.NORMAL}),
            TextNode("existing_bold", {TextType.BOLD}),
            TextNode(" then ", {TextType.NORMAL}),
            TextNode("some italic", TextType.ITALIC),
            TextNode(" followed by ", {TextType.NORMAL}),
            TextNode("more_bold", {TextType.BOLD}),
            TextNode(" and ", {TextType.NORMAL}),
            TextNode("another italic", TextType.ITALIC),
            TextNode(" and ", {TextType.NORMAL}),
            TextNode("third italic", TextType.ITALIC),
            TextNode(" and text", {TextType.NORMAL}),
            TextNode(" final_italic ", {TextType.ITALIC}),
            TextNode("and ", {TextType.NORMAL}),
            TextNode("last bold", TextType.BOLD),
            TextNode("!", {TextType.NORMAL}),
        ]

        result = MarkdownNodes.split_nodes_delimiter(nodes)
        self.assertEqual(result, expected)

    def test_adjacent_and_mixed_formatting(self):
        """
        Check against mixed formatting
        """
        input_text = "**bold** followed by **rebold** and then *italic*."
        expected_output = [
            TextNode("bold", {TextType.BOLD}),
            TextNode(" followed by ", {TextType.NORMAL}),
            TextNode("rebold", {TextType.BOLD}),
            TextNode(" and then ", {TextType.NORMAL}),
            TextNode("italic", {TextType.ITALIC}),
            TextNode(".", {TextType.NORMAL}),
        ]
        result = MarkdownNodes.text_to_textnodes(input_text)
        self.assertEqual(result, expected_output)

    def test_edge_markdown_without_plain_text(self):
        """
        Check against MD without plain text
        """
        input_text = "**only bolded text**"
        expected_output = [
            TextNode("only bolded text", {TextType.BOLD}),
        ]
        result = MarkdownNodes.text_to_textnodes(input_text)
        self.assertEqual(result, expected_output)


class TestExtractMarkdownImages(unittest.TestCase):
    """
    Test class for extract_markdown_images function
    """

    def test_single_basic_image(self):
        """
        Check against a single image
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_images(
                "![cat](https://cats.com/cat.jpg)"),
            [("cat", "https://cats.com/cat.jpg")],
        )

    def test_multiple_images(self):
        """
        Check against multiple images
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_images(
                "![dog](dog.jpg) some text ![cat](cat.jpg)"
            ),
            [("dog", "dog.jpg"), ("cat", "cat.jpg")],
        )

    def test_empty_string(self):
        """
        Check against empty strings for image
        """
        self.assertEqual(MarkdownNodes.extract_markdown_images(""), [])

    def test_image_with_spaces_in_alt_text(self):
        """
        Check against space in alt_text
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_images(
                "![cute fluffy cat](https://cats.com/fluffy.jpg)"
            ),
            [("cute fluffy cat", "https://cats.com/fluffy.jpg")],
        )

    def test_complex_url_with_special_characters(self):
        """
        Check against a complex url and special characters
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_images(
                "![test](https://example.com/path?id=123&type=.jpg)"
            ),
            [("test", "https://example.com/path?id=123&type=.jpg")],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    """
    Test class for extract_markdown_link function
    """

    def test_single_basic_link(self):
        """
        Check against a simple link
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_links(
                "[Boot.dev](https://boot.dev)"),
            [("Boot.dev", "https://boot.dev")],
        )

    def test_multiple_links(self):
        """
        Check against multiple links
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_links(
                "Check out [Python](https://python.org) and [Go](https://go.dev)"
            ),
            [("Python", "https://python.org"), ("Go", "https://go.dev")],
        )

    def test_link_with_image_nearby(self):
        """
        Check against image link combination
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_links(
                "![img](img.jpg) [link](url.com)"),
            [("link", "url.com")],
        )

    def test_link_with_special_characters(self):
        """
        Check against link including special characters
        """
        self.assertEqual(
            MarkdownNodes.extract_markdown_links(
                "[query](https://api.com/data?id=123&type=json)"
            ),
            [("query", "https://api.com/data?id=123&type=json")],
        )

    def test_empty_string(self):
        """
        Check against empty string
        """
        self.assertEqual(MarkdownNodes.extract_markdown_links(""), [])

    def test_complex_mix_links_images(self):
        """
        Check against a complex mix of links and images
        """
        string = (
            r"[first](https://first.com) ![img](image.jpg)"
            r"[second](https://second.com) ![another](pic.png)"
            r"[third](https://third.com)"
        )
        self.assertEqual(
            MarkdownNodes.extract_markdown_links(string),
            [
                ("first", "https://first.com"),
                ("second", "https://second.com"),
                ("third", "https://third.com"),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    """
    Test class for split_nodes_image function
    """

    def test_split_nodes_image_basic(self):
        """
        Check against simple image
        """
        node = TextNode("Hello ![alt](src) World", {TextType.NORMAL})
        nodes = MarkdownNodes.split_nodes_image([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].content, "Hello ", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "alt", {TextType.NORMAL})
        self.assertEqual(nodes[1].styles, {TextType.IMAGE})
        self.assertEqual(nodes[2].content, " World", {TextType.NORMAL})

    def test_split_nodes_image_multiple_images(self):
        """
        Check against multiple images
        """
        node = TextNode(
            "Start ![alt1](src1) middle ![alt2](src2) end", {TextType.NORMAL}
        )
        nodes = MarkdownNodes.split_nodes_image([node])
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].content, "Start ", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "alt1", {TextType.NORMAL})
        self.assertEqual(nodes[1].styles, {TextType.IMAGE})
        self.assertEqual(nodes[2].content, " middle ", {TextType.NORMAL})
        self.assertEqual(nodes[3].content, "alt2", {TextType.NORMAL})
        self.assertEqual(nodes[3].styles, {TextType.IMAGE})
        self.assertEqual(nodes[4].content, " end", {TextType.NORMAL})

    def test_split_nodes_image_no_images(self):
        """
        Check against no image
        """
        node = TextNode("Just plain text without images", {TextType.NORMAL})
        nodes = MarkdownNodes.split_nodes_image([node])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(
            nodes[0].content, "Just plain text without images", {
                TextType.NORMAL}
        )
        self.assertEqual(nodes[0].styles, {TextType.NORMAL})

    def test_split_nodes_image_adjacent_images(self):
        """
        Check against adjacent images
        """
        node = TextNode("![alt1](src1)![alt2](src2)", {TextType.NORMAL})
        nodes = MarkdownNodes.split_nodes_image([node])
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].content, "alt1", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "alt2", {TextType.NORMAL})
        self.assertEqual(nodes[0].styles, {TextType.IMAGE})
        self.assertEqual(nodes[1].styles, {TextType.IMAGE})

    def test_split_nodes_image_with_empty_text(self):
        """
        Check against image with empty text
        """
        node = TextNode("![](src)", {TextType.NORMAL})
        nodes = MarkdownNodes.split_nodes_image([node])
        self.assertEqual(len(nodes), 1)


class TestSplitNodesLink(unittest.TestCase):
    """
    Test class for split_nodes_link function
    """

    def test_split_nodes_link_basic(self):
        """
        Check against simple link
        """
        node = TextNode("Hello [text](url) World", {TextType.NORMAL})
        nodes = MarkdownNodes.split_nodes_link([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].content, "Hello ", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "text", {TextType.NORMAL})
        self.assertEqual(nodes[1].styles, {TextType.LINK})
        self.assertEqual(nodes[2].content, " World", {TextType.NORMAL})

    def test_split_nodes_link_with_special_characters(self):
        """
        Check against link with special characters
        """
        node = TextNode(
            "Check [this link!@#$](https://test.com/!@#$) here", {
                TextType.NORMAL}
        )
        nodes = MarkdownNodes.split_nodes_link([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].content, "Check ", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "this link!@#$", {TextType.NORMAL})
        self.assertEqual(nodes[1].styles, {TextType.LINK})
        self.assertEqual(
            nodes[1].url, "https://test.com/!@#$", {TextType.NORMAL})
        self.assertEqual(nodes[2].content, " here", {TextType.NORMAL})

    def test_split_nodes_link_with_text_formatting(self):
        """
        Check against link with text formatting
        """
        node = TextNode(
            "Check out our [Python Course](https://boot.dev/learn/learn-python) - it's great!",
            {TextType.NORMAL},
        )
        nodes = MarkdownNodes.split_nodes_link([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].content, "Check out our ", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "Python Course", {TextType.NORMAL})
        self.assertEqual(nodes[1].styles, {TextType.LINK})
        self.assertEqual(
            nodes[1].url, "https://boot.dev/learn/learn-python", {
                TextType.NORMAL}
        )
        self.assertEqual(nodes[2].content, " - it's great!", {TextType.NORMAL})

    def test_split_nodes_link_at_start_and_end(self):
        """
        Check against link at start and end of TextNode
        """
        node = TextNode("[start](url1)middle[end](url2)", {TextType.NORMAL})
        nodes = MarkdownNodes.split_nodes_link([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].content, "start", {TextType.NORMAL})
        self.assertEqual(nodes[0].url, "url1", {TextType.NORMAL})
        self.assertEqual(nodes[1].content, "middle", {TextType.NORMAL})
        self.assertEqual(nodes[2].content, "end", {TextType.NORMAL})
        self.assertEqual(nodes[2].url, "url2", {TextType.NORMAL})

    def test_split_nodes_link_with_multiple_nodes_input(self):
        """
        Check against link with multiple nodes in input
        """
        nodes = [
            TextNode("[link1](url1)", {TextType.NORMAL}),
            TextNode("plain text", {TextType.NORMAL}),
            TextNode("[link2](url2)", {TextType.NORMAL}),
        ]
        result = MarkdownNodes.split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].content, "link1", {TextType.NORMAL})
        self.assertEqual(result[0].url, "url1", {TextType.NORMAL})
        self.assertEqual(result[1].content, "plain text", {TextType.NORMAL})
        self.assertEqual(result[2].content, "link2", {TextType.NORMAL})
        self.assertEqual(result[2].url, "url2", {TextType.NORMAL})


class TestValidateTextnodes(unittest.TestCase):
    """
    Test class for validate_textnode
    """

    def test_empty_nodes_raises_error(self):
        """
        Check against empty nodes
        """
        with self.assertRaises(ValueError) as context:
            MarkdownNodes.validate_textnodes([])
        # Optionally check the error message
        self.assertTrue("Nodes list cannot be empty" in str(context.exception))

    def test_nodes_not_a_list_raises_error(self):
        """
        Check against nodes not processed as a list
        """
        node = TextNode("Hello world", TextType.NORMAL)
        with self.assertRaises(ValueError) as context:
            MarkdownNodes.validate_textnodes(node)
        # Optionally check the error message
        self.assertTrue(
            "Nodes must be provided as a list" in str(context.exception))

    def test_invalid_node_raises_error(self):
        """
        Check against invalid nodes
        """
        node = "node"
        with self.assertRaises(TypeError) as context:
            MarkdownNodes.validate_textnodes([node, "A normal string"])
        # Optionally check the error message
        self.assertTrue(
            f"Invalid node detected: {
                node}. Must be a TextNode."
            in str(context.exception)
        )

    def test_type_not_a_valid_textype_raises_error(self):
        """
        Check against invalid TextType
        """
        node = [TextNode("Hello world", styles={"test"})]
        with self.assertRaises(ValueError) as context:
            MarkdownNodes.validate_textnodes(node)
        # Optionally check the error message
        self.assertTrue(
            f"TextNode type {node[0].styles} is not a valid TextType"
            in str(context.exception)
        )

    def test_type_image_requires_a_valid_url_raises_error(self):
        """
        Check against no url in image
        """
        node = [TextNode("Hello world", {TextType.IMAGE})]
        with self.assertRaises(ValueError) as context:
            MarkdownNodes.validate_textnodes(node)
        # Optionally check the error message
        self.assertTrue(
            f"TextNode of type {
                node[0].styles} must have a non-empty 'url' string. Found: {node[0].url}"
            in str(context.exception)
        )


class TestFindDelimitersFirstPosition(unittest.TestCase):
    """
    Test class for find_delimiter_first_position
    """

    def test_simple_asterisk(self):
        """
        Check against simple case
        """
        input_text = "*    **"
        a, b, c, d, e, f = MarkdownNodes.find_delimiters_first_position(
            input_text)
        self.assertEqual(a, -1)
        self.assertEqual(b, -1)
        self.assertEqual(c, 5)
        self.assertEqual(d, -1)
        self.assertEqual(e, 0)
        self.assertEqual(f, -1)

    def test_all_asterisk(self):
        """
        Check against all asterisk case
        """
        input_text = "*   ** ***"
        a, b, c, d, e, f = MarkdownNodes.find_delimiters_first_position(
            input_text)
        self.assertEqual(a, -1)
        self.assertEqual(b, 7)
        self.assertEqual(c, 4)
        self.assertEqual(d, -1)
        self.assertEqual(e, 0)
        self.assertEqual(f, -1)

    def test_all_delimiters(self):
        """
        Check against all existing delimiters
        """
        input_text = "** * _ ` *** __"
        a, b, c, d, e, f = MarkdownNodes.find_delimiters_first_position(
            input_text)
        self.assertEqual(a, 7)
        self.assertEqual(b, 9)
        self.assertEqual(c, 0)
        self.assertEqual(d, 13)
        self.assertEqual(e, 3)
        self.assertEqual(f, 5)


class TestFindMatchingDelimiters(unittest.TestCase):
    """
    Test class for find_delimiter_first_position
    """

    def test_simple_asterisk(self):
        """
        Check against simple case
        """
        input_text = "*    *"
        a = MarkdownNodes.find_matching_delimiter(input_text, "*", 0)
        self.assertEqual(a, 5)

    def test_all_asterisk(self):
        """
        Check against all asterisk case
        """
        input_text = "*   **  ** * *** ***"
        a = MarkdownNodes.find_matching_delimiter(input_text, "*", 0)
        b = MarkdownNodes.find_matching_delimiter(input_text, "**", 4)
        c = MarkdownNodes.find_matching_delimiter(input_text, "***", 13)

        self.assertEqual(a, 11)
        self.assertEqual(b, 8)
        self.assertEqual(c, 17)

    def test_all_delimiters(self):
        """
        Check against all existing delimiters
        """
        input_text = "** *  ` *** *    *** ** `"
        a = MarkdownNodes.find_matching_delimiter(input_text, "*", 3)
        b = MarkdownNodes.find_matching_delimiter(input_text, "**", 0)
        c = MarkdownNodes.find_matching_delimiter(input_text, "***", 8)
        d = MarkdownNodes.find_matching_delimiter(input_text, "`", 6)
        self.assertEqual(a, 12)
        self.assertEqual(b, 21)
        self.assertEqual(c, 17)
        self.assertEqual(d, 24)


if __name__ == "__main__":
    unittest.main()
