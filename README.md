# Static Site Generator

A Python-based static site generator for building fast, secure, and easily updatable websites.

## Features
- Markdown to HTML conversion
- Customizable templates
- GitHub Pages support

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/static-site-generator.git
   cd static-site-generator
   ```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
Usage

Local build:
   ```bash
    python3 src/main.py
   ```
Production build for GitHub Pages:
```bash
./build.sh
```
This will build the site to the docs/ directory with the correct base path for GitHub Pages.

Deploying to GitHub Pages

    Commit and push all contents of the docs/ directory to your main branch.
    In your GitHub repo, go to Settings > Pages and select main branch and docs/ folder as the source.
    Visit https://yourusername.github.io/static-site-generator/ after a minute or two.

Note: The docs/ directory must be tracked by git to deploy via GitHub Pages.
Adding Content

    Add Markdown files to the content/ directory. Organize into subfolders as desired.
    Edit template.html to customize the layout of generated pages.

Development

We use pre-commit to manage code quality.
Install and enable with:

pip install pre-commit
pre-commit install

Now each commit will automatically run formatting, linting, and tests.
License

MIT License—see LICENSE for details.

## Contact

For questions, suggestions, or business inquiries, feel free to reach out:

- Email: [marguet.vincent@gmail.com](mailto:marguet.vincentl@gmail.com)
- GitHub Issues: [Open an issue](https://github.com/yourusername/static-site-generator/issues)

I welcome feedback and collaboration!
