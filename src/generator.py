"""
This module holds the generator functions for the site and three helper function
to read file safely, list directory safely, and write file safely
"""

import os
import shutil

from config import DOCS_DIR, STATIC_DIR
from converter import extract_title, markdown_to_html_node


def _read_file_safely(file_path, operation_name):
    """
    Helper function to read a file with error handling
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except PermissionError:
        print(f"Permission denied when {operation_name} {file_path}")
        return None
    except OSError as e:
        print(f"Error {operation_name} file {file_path}: {e}")
        return None


def _list_directory_safely(dir_path):
    """
    Helper function to list directory contents with error handling
    """
    try:
        return os.listdir(dir_path)
    except FileNotFoundError:
        print(f"File not found: {dir_path}")
        return None
    except PermissionError:
        print("Failed to read directory : Permission denied")
        return None
    except OSError as e:
        print(f"Error reading directory : {e}")
        return None


def _write_file_safely(file_path, content, operation_name="writing"):
    """
    Helper function to write a file with error handling
    """
    try:
        with open(file_path, "w", encoding="UTF-8") as f:
            f.write(content)
        return True
    except PermissionError:
        print(f"Permission denied when {operation_name} {file_path}")
        return False
    except IsADirectoryError:
        print(f"Cannot write to {file_path}: it's a directory")
        return False
    except UnicodeEncodeError as e:
        print(f"Encoding error when {operation_name} {file_path}: {e}")
        return False
    except OSError as e:
        print(f"Error {operation_name} file {file_path}: {e}")
        return False


def generator():
    """
    Generator function :
    1) remove content in ./docs
    2) copy all static files from ./static to ./docs
    """

    # Remove all directory content AND the directory itself
    try:
        if os.path.exists(DOCS_DIR):
            shutil.rmtree(DOCS_DIR)
    except PermissionError:
        print("Failed to remove public directory: Permission denied")
    except FileNotFoundError:
        print("Public directory does not exist")
    except OSError as e:
        print(f"Operating system error: {e}")

    # Create directory and copy the files

    try:
        shutil.copytree(STATIC_DIR, DOCS_DIR)
    except FileNotFoundError:
        print("Source directory 'static' not found")
    except PermissionError:
        print("Permission denied when copying files")
    except OSError as e:
        print(f"Error copying directory structure: {e}")


def generate_pages_recursive(
    dir_path_content, template_file_path, dest_dir_path, basepath="/"
):
    """
    Generate all HTML pages from MD files
    """
    filesystem_list = _list_directory_safely(dir_path_content)
    if filesystem_list is None:
        return

    template_file = _read_file_safely(template_file_path, "reading")
    if template_file is None:
        return

    for entry in filesystem_list:
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(entry_path) and entry_path.endswith(".md"):
            markdown_content = _read_file_safely(entry_path, "reading")
            if markdown_content is None:
                continue

            html_content = markdown_to_html_node(markdown_content).to_html()

            title = extract_title(markdown_content)

            final_html = template_file.replace("{{ Title }}", title).replace(
                "{{ Content }}", html_content
            )
            final_html = final_html.replace('href="/', f'href="{basepath}')
            final_html = final_html.replace('src="/', f'src="{basepath}')

            item_html = entry.replace(".md", ".html")

            os.makedirs(
                os.path.dirname(os.path.join(dest_dir_path, item_html)), exist_ok=True
            )

            output_path = os.path.join(dest_dir_path, item_html)
            if not _write_file_safely(output_path, final_html):
                return

        elif os.path.isdir(entry_path):
            generate_pages_recursive(
                entry_path,
                template_file_path,
                os.path.join(dest_dir_path, entry),
                basepath,
            )
