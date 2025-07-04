"""
This module holds the paths for the project
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "..", "content")
TEMPLATE_FILE = os.path.join(BASE_DIR, "..")
DOCS_DIR = os.path.join(BASE_DIR, "..", "docs")
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")

# Specific files
TEMPLATE_FILE = os.path.join(TEMPLATE_FILE, "template.html")
INDEX_MARKDOWN = os.path.join(CONTENT_DIR, "index.md")
INDEX_HTML = os.path.join(DOCS_DIR, "index.html")
