import os
from pathlib import Path
from typing import List, Optional


class InvalidBaseDirectoryError(Exception):
    """Raised when the specified base directory is invalid or does not exist."""
    pass


class NoFilesFoundError(Exception):
    """Raised when no files match the specified extensions."""
    pass


class FileAlreadyExistsError(Exception):
    """Raised when the output file already exists and 'force' is not enabled."""
    pass


class PromptForge:
    """
    A tool to combine code files into a single prompt, making it easy to use
    with large language models (LLMs) for code analysis, bug fixing, and refactoring.

    Attributes:
        base_dir (Path): The root directory to search for files.
        output_file (Path): The file where combined content is written.
        dry_run (bool): If True, only preview which files would be combined without writing output.
        force (bool): If True, allows overwriting existing output files without prompting.
    """

    def __init__(self, base_dir: str, output_file: str,
                 dry_run: bool = False, force: bool = False):
        """
        Initializes the PromptForge instance.

        Args:
            base_dir (str): The base directory to search for files.
            output_file (str): The output file to write combined content to.
            dry_run (bool, optional): If True, only preview changes. Defaults to False.
            force (bool, optional): If True, overwrite existing output. Defaults to False.
        """
        self.base_dir = Path(base_dir)
        self.output_file = Path(output_file)
        self.dry_run = dry_run
        self.force = force

    def find_files(self, extensions: List[str]) -> List[Path]:
        """
        Locates all files within base_dir that match the given extensions.

        Args:
            extensions (List[str]): List of file extensions without the dot.

        Returns:
            List[Path]: A unique, sorted list of matched file paths.

        Raises:
            InvalidBaseDirectoryError: If base_dir is not a directory.
            NoFilesFoundError: If no files match the specified extensions.
        """
        if not self.base_dir.is_dir():
            raise InvalidBaseDirectoryError(
                f"Base directory '{self.base_dir}' does not exist or is not a directory."
            )

        matched_files = []
        for ext in extensions:
            matched_files.extend(self.base_dir.rglob(f"*.{ext}"))

        # Remove duplicates and sort
        matched_files = sorted(set(matched_files))

        if not matched_files:
            raise NoFilesFoundError(
                f"No files found with extensions {extensions} in '{self.base_dir}'."
            )

        return matched_files

    def _validate_output_file(self) -> None:
        """
        Checks if the output file already exists. If it does and 'force' is not enabled,
        raises an exception.
        """
        if self.output_file.exists() and not self.force:
            raise FileAlreadyExistsError(
                f"Output file '{self.output_file}' already exists. Use '--force' to overwrite."
            )

    def _write_file_content(self, source_file: Path, outfile) -> None:
        """
        Writes the content of a single file in chunks to the output file.

        Args:
            source_file (Path): Path to the file whose content will be written.
            outfile: A file-like object to write the content to.
        """
        outfile.write(f"### {source_file} ###\n")
        chunk_size = 8192  # Read in 8KB chunks to handle large files efficiently
        with source_file.open('r', encoding='utf-8', errors='replace') as infile:
            while True:
                chunk = infile.read(chunk_size)
                if not chunk:
                    break
                outfile.write(chunk)
        outfile.write("\n")

    def forge_prompt(self, files: List[Path]) -> None:
        """
        Combines the contents of all specified files into the output file.

        Args:
            files (List[Path]): A list of file paths to combine.
        """
        # Make sure the output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Validate output file (overwrite only if forced)
        self._validate_output_file()

        if self.dry_run:
            print("Dry run: the following files would be combined:")
            for f in files:
                print(f" - {f}")
            return

        with self.output_file.open('w', encoding='utf-8', errors='replace') as outfile:
            for file_path in files:
                self._write_file_content(file_path, outfile)

    def run(self, extensions: List[str]) -> None:
        """
        Main method to find matching files and generate the combined prompt.

        Args:
            extensions (List[str]): List of file extensions (without dots).
        """
        files = self.find_files(extensions)
        self.forge_prompt(files)