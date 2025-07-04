#!/usr/bin/env -S python3 -i

"""
Main module for MD-HTML Project
"""

import sys

from config import CONTENT_DIR, DOCS_DIR, TEMPLATE_FILE
from generator import generate_pages_recursive, generator


def main():
    """
    The main function
    """
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generator()
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_FILE, DOCS_DIR, basepath)


if __name__ == "__main__":
    main()
