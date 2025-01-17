#!/usr/bin/env -S python3 -i

from textnode import TextNode, TextType


def main():
    new_text_node = TextNode(
        text="it is a test",
        text_type=TextType.ITALIC,
    )
    print(new_text_node)


if __name__ == "__main__":
    main()
