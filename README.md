# Code-Prompt-Forge

**Code-Prompt-Forge** is a Python tool that merges the contents of multiple code (or text) files into one consolidated prompt. This prompt can then be used by Large Language Models (LLMs) to assist in tasks like bug fixing, code improvements, and other automated coding workflows.

---

## Table of Contents
1. [Overview](#overview)  
2. [Installation](#installation)  
3. [Usage](#usage)  
   - [Command Line](#command-line-usage)  
   - [Python API](#python-api-usage)  
4. [Command Line Arguments](#command-line-arguments)  
5. [Examples](#examples)  
   - [Basic Usage](#basic-usage)  
   - [Changing the Base Directory](#changing-the-base-directory)  
   - [Including a Directory Tree](#including-a-directory-tree)  
   - [Dry Run](#dry-run)  
6. [Code Structure](#code-structure)  
7. [Contributing](#contributing)  
8. [License](#license)

---

## Overview

**Code-Prompt-Forge** comes in two parts:
1. A **command-line interface (CLI)** that quickly and easily merges files based on specified extensions.
2. A **Python class** (`PromptForge`) providing programmatic control to locate files, optionally include a directory tree, and write them into a single output file.

### Key Features

- **Search by Extensions**: Recursively scans a base directory for files matching given extensions (e.g., `.py`, `.txt`, `.md`).  
- **Single Output**: Consolidates matched file contents into a single text file, streamlining code reviews or preparing context for an LLM.  
- **Customizable Output Paths**: Specify where the merged file should be placed.  
- **Optional Directory Tree**: Include a text-based directory tree at the top of your output for extra context.  
- **Simple, Lightweight**: Minimal dependencies and straightforward usage.

---

## Installation

1. **Clone or Download** this repository.  
2. Navigate to the root directory (containing the `setup.py` file) in your terminal.  
3. **Install the package**:
   ```bash
   pip install .
   ```
4. After installation, you can run Code-Prompt-Forge directly from the command line if you configure your `setup.py` to expose a script (for example, `code-prompt-forge`). Alternatively, you can import and use the `PromptForge` class in Python scripts.

---

## Usage

### Command Line Usage

Assuming you have configured your `setup.py` to create a console script named `code-prompt-forge`:

```bash
code-prompt-forge <extensions> [OPTIONS]
```

For example:

```bash
code-prompt-forge py txt --base-dir="./codebase" --output-file="./prompts/merged_prompt.txt"
```

This looks for `.py` and `.txt` files in `./codebase`, then writes them into `./prompts/merged_prompt.txt`.

### Python API Usage

You can also invoke **Code-Prompt-Forge**’s functionality programmatically:

```python
from promptforge.main import PromptForge  # or "from code_prompt_forge.main import PromptForge" if you rename your folder

def combine_files():
    forge = PromptForge(
        base_dir="./codebase",
        output_file="./prompts/merged_prompt.txt",
        dry_run=False,
        force=False,
        include_tree=True
    )
    forge.run(["py", "txt"])
    print("Files have been merged successfully!")

if __name__ == "__main__":
    combine_files()
```

When you call `forge.run(["py", "txt"])`, it searches for `.py` and `.txt` files under `./codebase` and merges them into `./prompts/merged_prompt.txt`. If `include_tree=True`, it also prepends a directory tree structure to the beginning of the output file.

---

## Command Line Arguments

| Argument         | Required? | Default                        | Description                                                                                         |
|------------------|----------|--------------------------------|-----------------------------------------------------------------------------------------------------|
| `extensions`     | Yes       | None                           | File extensions to search for, without dots. Multiple can be specified (e.g., `py txt md`).         |
| `--base-dir`     | No        | `./codebase`                   | Base directory to search in.                                                                        |
| `--output-file`  | No        | `./prompts/merged_prompt.txt`  | File where the merged content is written.                                                           |
| `--dry-run`      | No        | `False`                        | Lists the files that would be merged without writing to the output file.                            |
| `--force`        | No        | `False`                        | Overwrites an existing output file without prompting if set.                                        |
| `--include-tree` | No        | `False`                        | Includes a directory tree listing at the top of your output file when set.                          |

---

## Examples

### Basic Usage

```bash
code-prompt-forge py
```
- Searches `./codebase` (by default) for `.py` files, merging them into `./prompts/merged_prompt.txt`.

### Changing the Base Directory

```bash
code-prompt-forge md --base-dir="./docs" --output-file="./prompts/combined_docs.txt"
```
- Locates all `.md` files in `./docs`, writing them into `./prompts/combined_docs.txt`.

### Including a Directory Tree

```bash
code-prompt-forge py txt --include-tree
```
- Merges `.py` and `.txt` files from `./codebase` into `./prompts/merged_prompt.txt` and prepends a directory tree view at the top of the output.

### Dry Run

```bash
code-prompt-forge py --dry-run
```
- Lists all `.py` files in `./codebase` without creating or overwriting the output file.

---

## Code Structure

```
code_prompt_forge/
├── __init__.py   # Package initializer
├── cli.py        # Command-line interface
├── main.py       # Core logic, including PromptForge class
tests/
├── test_code_prompt_forge.py  # Unit tests (requires pytest or similar)
```

- **`__init__.py`**: Makes `code_prompt_forge` a Python package.  
- **`cli.py`**: Defines the CLI entry point using Python’s `argparse`.  
- **`main.py`**: Contains the `PromptForge` class to find and merge files.  
- **`tests/`**: Holds tests verifying functionality of the package.

---

## Contributing

Contributions of any kind are welcome! Submit issues or pull requests to enhance features or fix bugs. Before opening a PR:

1. Adhere to Python’s [PEP 8](https://peps.python.org/pep-0008/) style guidelines.  
2. Write or update tests to confirm correct behavior.  
3. Update the documentation (including this README) if your changes affect usage.

---

## License

This project is distributed under the [MIT License](https://opensource.org/licenses/MIT). You’re free to use, modify, and distribute **Code-Prompt-Forge** under these terms. If you find it helpful, consider giving a shout-out or contributing back to the repository.

Enjoy **Code-Prompt-Forge** and happy coding!