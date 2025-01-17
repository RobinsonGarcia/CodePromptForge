import argparse
from promptforge.main import PromptForge, NoFilesFoundError, InvalidBaseDirectoryError, FileAlreadyExistsError

def main():
    """
    Entry point for the command-line interface of PromptForge.
    Parses arguments and executes the file-combining functionality.
    """
    parser = argparse.ArgumentParser(description="Combine code files into a single prompt for use with LLMs.")
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
        help="If set, only preview the files that would be combined without writing to the output file."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If set, overwrite existing output files without confirmation."
    )

    args = parser.parse_args()

    forge = PromptForge(
        base_dir=args.base_dir,
        output_file=args.output_file,
        dry_run=args.dry_run,
        force=args.force
    )

    try:
        forge.run(args.extensions)
        if not args.dry_run:
            print(f"Prompt created at {args.output_file}")
        else:
            print("Dry run completed. No files were written.")
    except NoFilesFoundError as e:
        print(e)
    except InvalidBaseDirectoryError as e:
        print(e)
    except FileAlreadyExistsError as e:
        print(e)
    except ValueError as e:
        # Fallback for any other ValueError not covered above
        print(f"An unexpected error occurred: {e}")