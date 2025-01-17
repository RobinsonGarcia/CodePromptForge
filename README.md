# PromptForge

PromptForge is a Python package designed to seamlessly combine code files into a single prompt. This consolidated prompt can then be used with Large Language Models (LLMs) to facilitate bug fixing, code improvements, and general code reviews. By gathering multiple files in one place, PromptForge streamlines your workflow for AI-assisted analysis.

---

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Usage](#usage)  
   - [Command Line](#command-line-usage)  
   - [Python API](#python-api-usage)  
4. [Command-Line Arguments](#command-line-arguments)  
5. [Examples](#examples)  
6. [Contributing](#contributing)  
7. [License](#license)

---

## Features

- **Combine multiple files**: Merge the contents of numerous files matching specified extensions into a single prompt.
- **Customizable base directory**: Easily specify which directory to scan for files.
- **Optional dry run**: Preview the files that would be merged, without actually writing any content to the output file.
- **Force overwrite**: Overwrite existing prompt files safely, or choose to abort if the file already exists.
- **Chunk-based reading**: Efficiently handle large files by reading in chunks.
- **Extensible code base**: Written in a highly modular way, making it straightforward to add or modify functionality.

---

## Installation

To install PromptForge, clone or download the repository and navigate to the project’s root directory (the one containing `setup.py`). Then, run the following command:

```bash
pip install .
```

This will install PromptForge and its command-line interface (promptforge) into your Python environment.

## Usage

### Command Line Usage
	1.	Basic command:

    ```bash
    promptforge py txt
    ```
    This command searches the ./codebase directory (default) for .py and .txt files, then merges them into ./prompts/merged_prompt.txt (the default output file).

	2.	Using additional flags:
	•	--dry-run: Lists which files would be merged, without creating or overwriting the output file.
	•	--force: Overwrites the existing output file without raising an error if the file already exists.

    ```bash
    promptforge py txt --dry-run --force
    ``` 
    In this example, PromptForge will preview the files it would merge. If --dry-run is removed, it will overwrite ./prompts/merged_prompt.txt automatically because --force is specified.

## Command Line Arguments

| Argument         | Required? | Default                       | Description                                                                                 |
|------------------|----------|-------------------------------|---------------------------------------------------------------------------------------------|
| `extensions`     | Yes      | None                          | File extensions to search for, without dots. Multiple extensions can be specified.          |
| `--base-dir`     | No       | `./codebase`                  | Base directory to search for files.                                                         |
| `--output-file`  | No       | `./prompts/merged_prompt.txt` | File path where merged content will be written.                                             |
| `--dry-run`      | No       | `False`                       | Lists the files that would be merged without writing anything.                              |
| `--force`        | No       | `False`                       | Overwrites the output file if it already exists.                                            |
    

## Examples

1.	Default invocation:

    ```bash
    promptforge py md
    ```
    
    Searches ./codebase for all .py and .md files, merging them into ./prompts/merged_prompt.txt.

    
2.	Overwriting an existing file:
    
    ```bash
    promptforge md --base-dir="./docs" --output-file="./prompts/docs_merged.txt" --force
    ```
    
    Looks for .md files in ./docs, writes them to ./prompts/docs_merged.txt, overwriting the output file if it already exists.

3.	Dry run:
    ```bash
    promptforge py --dry-run
    ```
    Displays which .py files would be merged without actually creating or overwriting the merged prompt file.

## Python API Usage

You can also use PromptForge as a library in your Python code:

```python
from promptforge.main import PromptForge, NoFilesFoundError, InvalidBaseDirectoryError

def combine_code_files():
    try:
        # Create an instance of PromptForge
        forge = PromptForge(
            base_dir="./codebase",
            output_file="./prompts/merged_prompt.txt",
            dry_run=False,
            force=False
        )

        # Run with desired file extensions
        forge.run(["py", "txt"])
        print("Files combined successfully!")
    except NoFilesFoundError:
        print("No matching files found.")
    except InvalidBaseDirectoryError as e:
        print(f"Invalid directory: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    combine_code_files()
```

By instantiating the PromptForge class and calling run with the list of file extensions you’d like to combine, the merged file is created (unless dry_run=True, in which case the operation only logs which files would be processed).

## Contributing

We welcome contributions of all kinds—bug reports, feature requests, and pull requests. Feel free to open an issue or fork the repository and submit a pull request with any changes you’d like to see.

Before submitting a pull request:
	1.	Ensure your code follows Python’s PEP 8 style guidelines.
	2.	Add tests for any new features or bug fixes.
	3.	Update the documentation (including this README) when adding new functionality.



## License

PromptForge is released under the MIT License. You’re free to use, modify, and distribute this software as permitted by the license.

Enjoy PromptForge, and happy coding!