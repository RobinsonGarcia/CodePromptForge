import os
from pathlib import Path
from typing import List, Optional

class InvalidBaseDirectoryError(Exception):
    """Raised when the specified base directory is invalid or does not exist."""
    pass

class NoFilesFoundError(Exception):
    """Raised when no files are found matching the specified extensions."""
    pass

class OutputFileAlreadyExistsError(Exception):
    """Raised when the output file already exists and 'force' is not enabled."""
    pass

class CodePromptForge:
    """
    A class to consolidate files from a base directory into a single prompt,
    making it easier to use with large language models (LLMs) for code review,
    bug fixing, refactoring, and more.

    Attributes:
        base_dir (Path): The root directory to search for files.
        output_file (Path): The file where combined content is written.
        dry_run (bool): If True, just list files without writing output.
        force (bool): If True, overwrite existing output files without prompting.
        include_tree (bool): If True, append a directory tree to the combined output.
        excluded (List[Path]): A list of paths to exclude from the search.
    """

    def __init__(
        self,
        base_dir: str,
        output_file: str,
        dry_run: bool = False,
        force: bool = False,
        include_tree: bool = False,
        excluded: Optional[List[str]] = None
    ):
        """
        Initialize a new CodePromptForge instance.

        Args:
            base_dir (str): The directory to search for files.
            output_file (str): The path of the file to write combined content to.
            dry_run (bool, optional): If True, just list files. Defaults to False.
            force (bool, optional): If True, overwrite existing output. Defaults to False.
            include_tree (bool, optional): If True, include directory tree in output. Defaults to False.
            excluded (List[str], optional): List of file or directory patterns to exclude. Defaults to None.
        """
        self.base_dir = Path(base_dir)
        self.output_file = Path(output_file)
        self.dry_run = dry_run
        self.force = force
        self.include_tree = include_tree
        self.excluded = [self.base_dir / Path(x) for x in (excluded or [])]
        print(self.excluded)

    def _validate_base_directory(self) -> None:
        """
        Validate that the base directory is a directory.

        Raises:
            InvalidBaseDirectoryError: If self.base_dir is not a valid directory.
        """
        if not self.base_dir.is_dir():
            raise InvalidBaseDirectoryError(
                f"Base directory '{self.base_dir}' does not exist or is not a directory. "
                "Use --help for more information."
            )

    def _validate_output_file(self) -> None:
        """
        Check if the output file already exists and handle overwrite if 'force' is disabled.

        Raises:
            OutputFileAlreadyExistsError: If the file exists and self.force is False.
        """
        if self.output_file.exists() and not self.force and not self.dry_run:
            raise OutputFileAlreadyExistsError(
                f"Output file '{self.output_file}' already exists. Use --force to overwrite. "
                "For example: codepromptforge py --force"
            )

    def find_files(self, extensions: List[str]) -> List[Path]:
        """
        Locate all files within base_dir that match the given extensions,
        excluding any that match the specified exclusion patterns.

        Args:
            extensions (List[str]): The file extensions to search for (without dots).

        Returns:
            List[Path]: A unique, sorted list of file paths matching the extensions.

        Raises:
            InvalidBaseDirectoryError: If base_dir is not a valid directory.
            NoFilesFoundError: If no matching files are found.
        """
        self._validate_base_directory()

        # Filter out files that are directly in or under any excluded path
        def is_excluded(file_path: Path) -> bool:
            for excluded_path in self.excluded:
                # If file_path is excluded or a child of an excluded directory
                if file_path == excluded_path or excluded_path in file_path.parents:
                    return True
            return False

        matched_files = []
        for ext in extensions:
            for file_path in self.base_dir.rglob(f"*.{ext}"):
                if not is_excluded(file_path):
                    matched_files.append(file_path)

        matched_files = sorted(set(matched_files))
        if not matched_files:
            raise NoFilesFoundError(
                f"No files found for extensions {extensions} in '{self.base_dir}' after applying exclusions. "
                "Try removing --exclude or adjusting your patterns."
            )
        return matched_files

    def generate_directory_tree(self, path: Optional[Path] = None, prefix: str = "") -> str:
        """
        Recursively generate a text-based tree structure of the directories.

        Args:
            path (Optional[Path], optional): The starting path for generating the tree.
                                             Defaults to None, which means self.base_dir.
            prefix (str, optional): The current prefix for tree branches. Defaults to "".

        Returns:
            str: A multiline string representing the directory structure.
        """
        if path is None:
            path = self.base_dir

        tree_lines = []
        sub_dirs = sorted([d for d in path.iterdir() if d.is_dir()])

        for i, sub_dir in enumerate(sub_dirs):
            connector = "└── " if i == len(sub_dirs) - 1 else "├── "
            tree_lines.append(f"{prefix}{connector}{sub_dir.name}")

            # Recurse into subdirectories
            extension = "    " if i == len(sub_dirs) - 1 else "│   "
            tree_lines.extend(self.generate_directory_tree(sub_dir, prefix + extension))

        return "\n".join(tree_lines)

    def forge_prompt(self, files: List[Path]) -> None:
        """
        Combine the contents of the specified files into the output file.
        May also include the directory tree if specified.

        Args:
            files (List[Path]): The list of file paths to merge.
        """
        if self.dry_run:
            # Only list the files, do not write anything
            print("Dry run: The following files would be merged:")
            for f in files:
                print(f" - {f}")
            return

        # Create the parent directory if it doesn't exist
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Validate the output file (handle overwriting if not forced)
        self._validate_output_file()

        with self.output_file.open('w', encoding='utf-8') as outfile:
            # Optionally include the directory tree
            if self.include_tree:
                outfile.write("Directory Tree:\n")
                outfile.write(self.generate_directory_tree())
                outfile.write("\n\n")

            # Write each file's content
            for file in files:
                outfile.write(f"### {file} ###\n")
                with file.open('r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                outfile.write("\n")

    def run(self, extensions: List[str]) -> None:
        """
        Main entry point: find matching files and write them to the output (or perform a dry run).

        Args:
            extensions (List[str]): File extensions to include, without dots.
        """
        files = self.find_files(extensions)
        self.forge_prompt(files)