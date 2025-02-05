import argparse
import json
import sys
from codepromptforge.main import (
    CodePromptForge, 
    InvalidBaseDirectoryError, 
    NoFilesFoundError, 
    OutputFileAlreadyExistsError
)

def main():
    parser = argparse.ArgumentParser(description="Code management CLI.")
    parser.add_argument(
        "command",
        choices=["tree", "file", "files", "files_recursive", "write", "combine", "clean_result"],
        help="Command to execute"
    )
    parser.add_argument("--folder", help="Folder path")
    parser.add_argument("--file", help="File path")
    parser.add_argument("--content", help="Content for writing")
    parser.add_argument("--base-dir", default=".", help="Base directory")
    parser.add_argument("--extensions", nargs="*", default=[], help="File extensions for combining")
    parser.add_argument("--output-file", help="Output file for combination")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing output file")
    parser.add_argument("--exclude", nargs="*", default=[], help="List of files to exclude from concatenation")
    parser.add_argument("--exclude-clean", nargs="*", default=[], help="Files to remove from .result folder")

    args = parser.parse_args()

    forge = CodePromptForge(
        base_dir=args.base_dir,
        output_file=args.output_file,
        force=args.force,
        excluded=args.exclude
    )

    try:
        if args.command == "tree":
            if not args.folder:
                print("Error: The --folder argument is required for 'tree' command.", file=sys.stderr)
                sys.exit(1)
            print(forge.get_directory_tree(args.folder))

        elif args.command == "file":
            if not args.file:
                print("Error: The --file argument is required for 'file' command.", file=sys.stderr)
                sys.exit(1)
            print(forge.get_file_content(args.file))

        elif args.command == "files":
            if not args.folder:
                raise ValueError("The --folder argument is required for 'files' command.")
            print(json.dumps(forge.get_files_in_folder(args.folder), indent=2))

        elif args.command == "files_recursive":
            if not args.folder:
                raise ValueError("The --folder argument is required for 'files_recursive' command.")
            print(json.dumps(forge.get_files_recursively(args.folder), indent=2))

        elif args.command == "write":
            if not args.file or not args.content:
                raise ValueError("Both --file and --content arguments are required for 'write' command.")
            print(forge.write_file(args.file, args.content))

        elif args.command == "combine":
            if not args.extensions or not args.output_file:
                raise ValueError("--extensions and --output-file are required for 'combine'.")
            forge.forge_prompt(args.extensions)

        elif args.command == "clean_result":
            if not args.exclude_clean:
                raise ValueError("--exclude-clean argument is required for 'clean_result'.")
            forge.clean_result_folder(args.exclude_clean)

    except (InvalidBaseDirectoryError, NoFilesFoundError, OutputFileAlreadyExistsError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()