# codepromptforge/cli.py

import argparse
from codepromptforge.main import (
    CodePromptForge,
    InvalidBaseDirectoryError,
    NoFilesFoundError,
    OutputFileAlreadyExistsError,
)


def main():
    """
    Entry point for the command-line interface of Code Prompt Forge.
    Parses arguments and executes the file-combining functionality.
    """
    parser = argparse.ArgumentParser(
        description="Combine code files into a single prompt for use with LLMs."
    )
    parser.add_argument(
        "extensions",
        nargs="+",
        help="File extensions to search for (e.g., py txt md), without dots."
    )
    parser.add_argument(
        "--base-dir",
        default="./codebase",
        help="Base directory to search in (default: './codebase')."
    )
    parser.add_argument(
        "--output-file",
        default="./prompts/merged_prompt.txt",
        help="Path to the output file (default: './prompts/merged_prompt.txt')."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the files that would be combined without writing to the output."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the existing output file without prompting."
    )
    parser.add_argument(
        "--include-tree",
        action="store_true",
        help="Include a directory tree listing in the combined output."
    )

    args = parser.parse_args()

    forge = CodePromptForge(
        base_dir=args.base_dir,
        output_file=args.output_file,
        dry_run=args.dry_run,
        force=args.force,
        include_tree=args.include_tree
    )

    try:
        forge.run(args.extensions)
        if args.dry_run:
            print("Dry run complete. No files were written.")
        else:
            print(f"Prompt created at {args.output_file}")
    except InvalidBaseDirectoryError as e:
        print(f"Error: {e}")
    except NoFilesFoundError as e:
        print(f"Error: {e}")
    except OutputFileAlreadyExistsError as e:
        print(f"Error: {e}")
    except ValueError as e:
        # Fallback for any other ValueError not covered above
        print(f"An unexpected error occurred: {e}")