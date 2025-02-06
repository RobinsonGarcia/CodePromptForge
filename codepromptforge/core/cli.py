import argparse
import json
import sys
from .main import CodePromptForge

##############################
# Core Commands Registration #
##############################
def register_core_commands(subparsers):
    # tree command
    parser_tree = subparsers.add_parser("tree", help="Display the directory tree")
    parser_tree.add_argument("--folder", required=True, help="Folder path")
    parser_tree.add_argument("--base-dir", required=True, help="Base directory")
    parser_tree.set_defaults(func=handle_tree)

    # file command
    parser_file = subparsers.add_parser("file", help="Display the content of a file")
    parser_file.add_argument("--file", required=True, help="File path")
    parser_file.add_argument("--base-dir", required=True, help="Base directory")
    parser_file.set_defaults(func=handle_file)

    # files command
    parser_files = subparsers.add_parser("files", help="List files in a folder")
    parser_files.add_argument("--folder", required=True, help="Folder path")
    parser_files.add_argument("--base-dir", required=True, help="Base directory")
    parser_files.set_defaults(func=handle_files)

    # files_recursive command
    parser_files_recursive = subparsers.add_parser("files_recursive", help="Recursively list files")
    parser_files_recursive.add_argument("--folder", required=True, help="Folder path")
    parser_files_recursive.add_argument("--base-dir", required=True, help="Base directory")
    parser_files_recursive.set_defaults(func=handle_files_recursive)

    # write command
    parser_write = subparsers.add_parser("write", help="Write content to a file")
    parser_write.add_argument("--file", required=True, help="File path")
    parser_write.add_argument("--content", required=True, help="Content to write")
    parser_write.add_argument("--base-dir", required=True, help="Base directory")
    parser_write.set_defaults(func=handle_write)

    # combine command
    parser_combine = subparsers.add_parser("combine", help="Combine files into an output file")
    parser_combine.add_argument("--extensions", nargs="+", required=True, help="List of file extensions")
    parser_combine.add_argument("--output-file", required=True, help="Output file for the combination")
    parser_combine.add_argument("--base-dir", required=True, help="Base directory")
    parser_combine.add_argument("--force", action="store_true", help="Force overwrite existing output file")
    parser_combine.add_argument("--exclude", nargs="*", default=[], help="Files to exclude from concatenation")
    parser_combine.set_defaults(func=handle_combine)

    # clean_result command
    parser_clean = subparsers.add_parser("clean_result", help="Clean the .result folder")
    parser_clean.add_argument("--exclude-clean", nargs="+", required=True, help="Files to remove from .result folder")
    parser_clean.add_argument("--base-dir", required=True, help="Base directory")
    parser_clean.set_defaults(func=handle_clean_result)

###########################
# Core Commands Handlers  #
###########################
def handle_tree(args):
    forge = CodePromptForge(base_dir=args.base_dir)
    try:
        tree = forge.get_directory_tree(args.folder)
        print("\n".join(tree))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_file(args):
    forge = CodePromptForge(base_dir=args.base_dir)
    try:
        content = forge.get_file_content(args.file)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_files(args):
    forge = CodePromptForge(base_dir=args.base_dir)
    try:
        files = forge.get_files_in_folder(args.folder)
        print(json.dumps(files, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_files_recursive(args):
    forge = CodePromptForge(base_dir=args.base_dir)
    try:
        files = forge.get_files_recursively(args.folder)
        print(json.dumps(files, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_write(args):
    forge = CodePromptForge(base_dir=args.base_dir)
    try:
        result = forge.write_file(args.file, args.content)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_combine(args):
    forge = CodePromptForge(
        base_dir=args.base_dir,
        output_file=args.output_file,
        force=args.force,
        excluded=args.exclude
    )
    try:
        forge.forge_prompt(args.extensions)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def handle_clean_result(args):
    forge = CodePromptForge(base_dir=args.base_dir)
    try:
        forge.clean_result_folder(args.exclude_clean)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

#######################
# Main CLI Entry Point#
#######################
def main():
    parser = argparse.ArgumentParser(description="Code management CLI for CodePromptForge.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register core commands
    register_core_commands(subparsers)

    # Optionally register assistant commands if the assistant module is installed.
    try:
        from ..assistant import cli as assistant_cli
        assistant_cli.register_commands(subparsers)
    except ImportError:
        # Assistant module is not installed; ignore extra commands.
        raise

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No valid command selected.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()