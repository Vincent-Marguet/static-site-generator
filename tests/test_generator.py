"""
Test module for generator.py
"""

import os
import shutil
import tempfile
import unittest

from src.generator import generate_pages_recursive


class TestGeneratePagesRecursive(unittest.TestCase):
    """
    This class test generate_pages_recursive()
    """

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create test content directory
        self.content_dir = os.path.join(self.test_dir, "content")
        os.makedirs(self.content_dir)

        # Create test markdown file
        with open(
            os.path.join(self.content_dir, "test.md"), "w", encoding="UTF-8"
        ) as f:
            f.write("# Test Title\n\nTest content")

        # Create template file
        self.template_path = os.path.join(self.test_dir, "template.html")
        with open(self.template_path, "w", encoding="UTF-8") as f:
            f.write(
                "<html><h1>{{ Title }}</h1><div>{{ Content }}</div></html>")

        # Create output directory
        self.output_dir = os.path.join(self.test_dir, "public")
        os.makedirs(self.output_dir)

    def tearDown(self):
        """
        Clean up temporary directory
        """
        shutil.rmtree(self.test_dir)

    def test_basic_generation(self):
        """
        Check against a basic generation
        """
        generate_pages_recursive(
            self.content_dir, self.template_path, self.output_dir)

        # Check if HTML file was created
        output_file = os.path.join(self.output_dir, "test.html")
        self.assertTrue(os.path.exists(output_file))

        # Check content
        with open(output_file, "r", encoding="UTF-8") as f:
            content = f.read()
            self.assertIn("Test Title", content)

    def test_nested_directories(self):
        """
        Check against processing nested directory structure
        """
        # Create nested directory
        blog_dir = os.path.join(self.content_dir, "blog")
        os.makedirs(blog_dir)

        # Create markdown file in subdirectory
        with open(os.path.join(blog_dir, "post.md"), "w", encoding="UTF-8") as f:
            f.write("# Blog Post\n\nThis is a blog post")

        generate_pages_recursive(
            self.content_dir, self.template_path, self.output_dir)

        # Check if nested HTML file was created
        output_file = os.path.join(self.output_dir, "blog", "post.html")
        self.assertTrue(os.path.exists(output_file))

    def test_multiple_files(self):
        """
        Check against processing multiple markdown files
        """
        # Create second markdown file
        with open(
            os.path.join(self.content_dir, "about.md"), "w", encoding="UTF-8"
        ) as f:
            f.write("# About\n\nAbout page content")

        generate_pages_recursive(
            self.content_dir, self.template_path, self.output_dir)

        # Check both files were created
        self.assertTrue(os.path.exists(
            os.path.join(self.output_dir, "test.html")))
        self.assertTrue(os.path.exists(
            os.path.join(self.output_dir, "about.html")))

    def test_empty_directory(self):
        """Test handling of empty content directory"""
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)

        # Should not crash on empty directory
        generate_pages_recursive(
            empty_dir, self.template_path, self.output_dir)

        # Output directory should still exist but be empty
        self.assertTrue(os.path.exists(self.output_dir))
        self.assertEqual(len(os.listdir(self.output_dir)), 0)

    def test_ignores_non_markdown_files(self):
        """Test that non-markdown files are ignored"""
        # Create a non-markdown file
        with open(
            os.path.join(self.content_dir, "readme.txt"), "w", encoding="UTF-8"
        ) as f:
            f.write("This is not markdown")

        generate_pages_recursive(
            self.content_dir, self.template_path, self.output_dir)

        # Should only create HTML for the markdown file
        self.assertTrue(os.path.exists(
            os.path.join(self.output_dir, "test.html")))
        self.assertFalse(os.path.exists(
            os.path.join(self.output_dir, "readme.html")))


if __name__ == "__main__":
    unittest.main()
