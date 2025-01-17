# PromptForge

PromptForge is a simple Python tool that merges the contents of multiple code (or text) files into one consolidated prompt. This consolidated prompt can then be fed into a Large Language Model (LLM) to assist in tasks like bug fixing, code improvements, and other automated coding workflows.

---

## Table of Contents
1. [Overview](#overview)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Command Line Arguments](#command-line-arguments)  
5. [Example Workflow](#example-workflow)  
6. [Code Structure](#code-structure)  
7. [Contributing](#contributing)  
8. [License](#license)

---

## Overview

PromptForge is built around two main components:
1. A **command-line interface (CLI)** that allows you to quickly specify a base directory, file extensions, and an output file.
2. A **Python class** (`PromptForge`) that encapsulates the logic of finding files and merging their contents.

### Key Features

- **Search by Extensions**: Recursively searches the specified base directory for files matching given extensions (e.g., `.py`, `.txt`, `.md`).  
- **Consolidation into One File**: Appends all matching file contents into a single file, making it easier to review code or feed it to an LLM.  
- **Customizable Output Paths**: Specify where the merged file should be generated.  
- **Simple and Lightweight**: Minimal dependencies, easy to integrate into your existing projects.

---

## Installation

1. **Clone or Download** this repository.  
2. In your terminal, navigate to the project’s root directory (the one containing `setup.py`, if you create one for distribution).
3. **Install the package locally**:
   ```bash
   pip install .
   ```
4. After a successful install, you can run PromptForge directly from the command line using the `promptforge` command. Alternatively, you can import and use the `PromptForge` class in Python scripts.

---

## Usage

### Command Line Usage

```bash
promptforge py txt
```

- This example scans `./codebase` (default) for `.py` and `.txt` files and merges their contents into `./prompts/merged_prompt.txt` by default.

#### Changing the Base Directory and Output File

```bash
promptforge md --base-dir="./docs" --output-file="./prompts/docs_combined.txt"
```

- Here, only `.md` files under `./docs` are merged into `./prompts/docs_combined.txt`.

### Python API Usage

```python
from promptforge.main import PromptForge

def combine_files():
    # Create a PromptForge instance
    forge = PromptForge(
        base_dir="./codebase",
        output_file="./prompts/merged_prompt.txt"
    )

    # Find .py and .txt files and merge them
    forge.run(["py", "txt"])
    print("Files have been merged successfully!")

if __name__ == "__main__":
    combine_files()
```

By invoking `forge.run(["py", "txt"])`, the contents of all `.py` and `.txt` files in `./codebase` will be saved into `./prompts/merged_prompt.txt`.

---

## Command Line Arguments

| Argument         | Required? | Default                        | Description                                                                     |
|------------------|----------|--------------------------------|---------------------------------------------------------------------------------|
| `extensions`     | Yes       | None                           | File extensions to search for, without dots. Multiple can be specified.         |
| `--base-dir`     | No        | `./codebase`                   | Base directory to scan for files.                                               |
| `--output-file`  | No        | `./prompts/merged_prompt.txt`  | Path to the merged output file.                                                 |

**Example:**

```bash
promptforge txt py --base-dir="my_project" --output-file="all_code_prompt.txt"
```

---

## Example Workflow

1. **Add or Update Code**  
   Work on your codebase as you normally do.
2. **Generate Prompt**  
   Run `promptforge` to merge all new or updated files into a single prompt:
   ```bash
   promptforge py md
   ```
3. **Use Prompt in an LLM**  
   Copy the combined file content into your LLM or feed it programmatically to your AI tools for bug detection, code refactoring, or other tasks.
4. **Iterate**  
   Refine your code, generate a new prompt, repeat as needed.

---

## Code Structure

Below is a simplified overview of the project layout:

```
promptforge/
├── __init__.py
├── cli.py
├── main.py
tests/
├── test_promptforge.py
```

- **`__init__.py`**: Makes this directory a Python package.  
- **`cli.py`**: Defines the command-line entry point using Python’s `argparse`.  
- **`main.py`**: Contains the `PromptForge` class with methods to find and consolidate files.  
- **`tests/`**: Contains tests verifying the core functionality (requires `pytest` or similar).

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests. Before creating a PR, make sure you:

1. Use Python’s [PEP 8](https://peps.python.org/pep-0008/) style conventions.  
2. Write or update tests relevant to your changes.  
3. Update documentation (including this README) if your changes add or modify functionality.

---

## License

This project is distributed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute this tool as permitted by the license. If you find this helpful, we’d appreciate a shout-out or a contribution back to the project.

Enjoy PromptForge and happy coding!