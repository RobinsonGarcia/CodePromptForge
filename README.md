# CodePromptForge

**CodePromptForge** is a Python tool designed to streamline code reviews and development workflows by merging code files into a single prompt. This consolidated prompt can then be used by Large Language Models (LLMs) for bug fixing, code improvements, and other automated coding tasks.

---

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Command Line Interface (CLI)](#command-line-interface-cli)
   - [Python API](#python-api)
4. [Command Reference](#command-reference)
5. [Examples](#examples)
6. [Code Structure](#code-structure)
7. [Contributing](#contributing)
8. [License](#license)

---

## Overview

### Key Features
- **Find and Merge Files**: Recursively scans a base directory for files matching specified extensions.
- **Single Prompt Output**: Consolidates multiple code files into a single text file.
- **Configurable Output**: Customize output paths and exclusions.
- **Directory Tree Inclusion**: Optionally include a directory structure overview at the top of the output.
- **Lightweight and Easy to Use**: Simple CLI commands and a Python API for seamless integration.

---

## Installation

To install **CodePromptForge**, run:

```bash
pip install codepromptforge
```

To install from source:

```bash
git clone https://github.com/RobinsonGarcia/CodePromptForge.git
cd CodePromptForge
pip install .
```

---

## Usage

### Command Line Interface (CLI)
After installation, the CLI can be accessed using:

```bash
codepromptforge <command> [OPTIONS]
```

#### Example:
```bash
codepromptforge combine --extensions py txt --output-file merged_prompt.txt
```
This merges all `.py` and `.txt` files into `merged_prompt.txt`.

### Python API
You can use **CodePromptForge** programmatically:

```python
from codepromptforge.main import CodePromptForge

forge = CodePromptForge(
    base_dir="./codebase",
    output_file="./merged_prompt.txt",
    include_tree=True
)

forge.run(["py", "txt"])  # Merge .py and .txt files
```

---

## Command Reference

| Command          | Description |
|-----------------|-------------|
| `tree`          | List all files in a directory (excluding ignored ones). |
| `file`          | Print the contents of a specified file. |
| `files`         | List files in a folder with their contents. |
| `files_recursive` | Recursively list files in a directory. |
| `write`         | Write or overwrite a file with given content. |
| `combine`       | Merge specified files into a single output file. |
| `clean_result`  | Remove specified files from the `.result` directory. |

### CLI Options

| Option           | Description |
|-----------------|-------------|
| `--folder`      | Path to the directory (for `tree`, `files`, `files_recursive`). |
| `--file`        | Path to the file (for `file`, `write`). |
| `--content`     | Content to write to a file (for `write`). |
| `--base-dir`    | Base directory for operations (default: `.`). |
| `--extensions`  | List of file extensions to merge (for `combine`). |
| `--output-file` | Path to save the merged output (for `combine`). |
| `--force`       | Overwrite existing output file without confirmation. |
| `--exclude`     | List of files to exclude from merging. |
| `--exclude-clean` | Files to remove from `.result` folder. |

---

## Examples

### List Directory Tree
```bash
codepromptforge tree --folder .
```

### Get File Content
```bash
codepromptforge file --file script.py
```

### Merge `.py` and `.md` Files
```bash
codepromptforge combine --extensions py md --output-file merged_code.txt
```

### Python API Usage
```python
from codepromptforge.main import CodePromptForge

forge = CodePromptForge(
    base_dir=".",
    output_file="merged.txt",
    include_tree=True
)

forge.run(["py", "md"])
```

### Cleaning the `.result` Directory
```bash
codepromptforge clean_result --exclude-clean old_output.txt
```

---

## Code Structure

```
codepromptforge/
├── __init__.py        # Package initializer
├── cli.py             # Command-line interface
├── main.py            # Core logic
tests/
├── test_cli.py        # CLI tests
├── test_main.py       # Main logic tests
```

---

## Contributing

Contributions are welcome! Before submitting a pull request:

1. Follow Python’s [PEP 8](https://peps.python.org/pep-0008/) guidelines.
2. Ensure tests pass.
3. Update documentation if needed.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Use freely and contribute if you find it helpful!

---
Enjoy **CodePromptForge** and happy coding! 🚀