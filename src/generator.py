"""
This module holds the generator function for the site
"""

import os
import shutil


def generator():
    """
    Generator function : remove content in public
    """
    try:
        if os.path.exists(r"./public"):
            # Remove all directory content AND the directory itself
            shutil.rmtree("./public")
    except PermissionError:
        print("Failed to remove public directory: Permission denied")
    except FileNotFoundError:
        print("Public directory does not exist")
    except OSError as e:
        print(f"Operating system error: {e}")

    # Create directory and copy the files

    try:
        shutil.copytree("./static", "./public")
    except FileNotFoundError:
        print("Source directory 'static' not found")
    except PermissionError:
        print("Permission denied when copying files")
    except OSError as e:
        print(f"Error copying directory structure: {e}")
