import os
from pathlib import Path
from typing import List, Dict, Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
import pathspec  # ✅ Added for .gitignore handling

class InvalidBaseDirectoryError(Exception):
    pass

class NoFilesFoundError(Exception):
    pass

class OutputFileAlreadyExistsError(Exception):
    pass

class CodePromptForge:
    def __init__(
        self,
        base_dir: str = ".",
        output_file: str = None,
        dry_run: bool = False,
        force: bool = False,
        include_tree: bool = False,
        excluded: Optional[List[str]] = None
    ):
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.exists() or not self.base_dir.is_dir():
            raise InvalidBaseDirectoryError(f"Base directory '{self.base_dir}' does not exist or is not a directory.")

        self.output_file = Path(output_file) if output_file else None
        self.dry_run = dry_run
        self.force = force
        self.include_tree = include_tree
        self.result_dir = self.base_dir / ".result"
        self.result_dir.mkdir(parents=True, exist_ok=True)

        # Load .gitignore patterns
        self.gitignore_spec = self._load_gitignore()

        # Convert excluded files into a set for quick lookup
        self.excluded = set(excluded or [])

    def _load_gitignore(self) -> Optional[pathspec.PathSpec]:
        """Loads `.gitignore` and compiles it into a pathspec matcher."""
        gitignore_path = self.base_dir / ".gitignore"
        if not gitignore_path.exists():
            return None  # No .gitignore found

        with gitignore_path.open("r", encoding="utf-8") as f:
            gitignore_patterns = f.readlines()

        return pathspec.PathSpec.from_lines("gitwildmatch", gitignore_patterns)

    def _is_ignored(self, file_path: Path) -> bool:
        """Checks if a file is ignored by .gitignore, explicitly excluded, or in `.git`."""
        relative_path = str(file_path.relative_to(self.base_dir))
        return (
            (self.gitignore_spec and self.gitignore_spec.match_file(relative_path))  # ✅ Checks against .gitignore
            or (relative_path in self.excluded)  # ✅ Explicit exclusions
            or (".git/" in relative_path or relative_path.startswith(".git"))  # ✅ Always ignore `.git`
        )

    def get_directory_tree(self, folder_path: str) -> List[str]:
        """Returns a list of all files in the specified folder, excluding ignored ones."""
        target_path = self.base_dir / folder_path
        if not target_path.is_dir():
            raise InvalidBaseDirectoryError(f"Invalid directory: {target_path}")

        return [
            str(file.relative_to(self.base_dir))
            for file in target_path.rglob("*")
            if file.is_file() and not self._is_ignored(file)
        ]

    def get_file_content(self, file_path: str) -> str:
        target_file = self.base_dir / file_path
        if not target_file.is_file() or self._is_ignored(target_file):
            raise FileNotFoundError(f"File not found or ignored: {target_file}")
        return target_file.read_text(encoding="utf-8")

    def get_files_in_folder(self, folder_path: str) -> Dict[str, str]:
        target_folder = self.base_dir / folder_path
        if not target_folder.is_dir():
            raise InvalidBaseDirectoryError(f"Invalid directory: {target_folder}")

        return {
            file.name: file.read_text(encoding="utf-8")
            for file in target_folder.iterdir()
            if file.is_file() and not self._is_ignored(file)
        }

    def get_files_recursively(self, folder_path: str) -> Dict[str, str]:
        target_folder = self.base_dir / folder_path
        if not target_folder.is_dir():
            raise InvalidBaseDirectoryError(f"Invalid directory: {target_folder}")

        return {
            str(file.relative_to(self.base_dir)): file.read_text(encoding="utf-8")
            for file in target_folder.rglob("*")
            if file.is_file() and not self._is_ignored(file)
        }

    def write_file(self, file_path: str, content: str) -> str:
        """Writes a file inside .result folder and ensures it exists."""
        self.result_dir.mkdir(parents=True, exist_ok=True)
        result_file = self.result_dir / file_path
        result_file.write_text(content, encoding="utf-8")
        return f"File written successfully: {result_file}"

    def find_files(self, extensions: List[str]) -> List[Path]:
        matched_files = [
            file_path
            for ext in extensions
            for file_path in self.base_dir.rglob(f"*.{ext}")
            if not self._is_ignored(file_path)
        ]
        if not matched_files:
            raise NoFilesFoundError(f"No files found for extensions {extensions} in '{self.base_dir}'.")
        return sorted(set(matched_files))

    def _validate_output_file(self) -> None:
        """Ensures output file does not already exist unless force=True."""
        if self.output_file and self.output_file.exists() and not self.force:
            raise OutputFileAlreadyExistsError(
                f"Output file '{self.output_file}' already exists. Use --force to overwrite."
            )

    def forge_prompt(self, extensions: List[str]) -> None:
        self._validate_output_file()
        files = self.find_files(extensions)
        if self.dry_run:
            print("\n".join(str(f) for f in files))
            return
        if not files:
            print("No files found for combination.")
            return
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with self.output_file.open('w', encoding='utf-8') as outfile:
            if self.include_tree:
                outfile.write("Directory Tree:\n")
                outfile.write("\n".join(self.get_directory_tree(".")) + "\n")
            for file in files:
                outfile.write(f"### {file.name} ###\n")
                outfile.write(file.read_text(encoding="utf-8"))
                outfile.write("\n")

    def run(self, extensions: List[str]) -> None:
        self.forge_prompt(extensions)

    def clean_result_folder(self, excluded_files: List[str]) -> None:
        self.result_dir.mkdir(parents=True, exist_ok=True)
        deleted_files = []
        for file_name in excluded_files:
            file_path = self.result_dir / file_name
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                deleted_files.append(file_name)
        print(f"Cleaned .result folder. Removed files: {deleted_files}")

    def get_tools(self) -> List[BaseTool]:
        """Returns LangChain-compatible tools with access to CodePromptForge methods."""

        class GetDirectoryTreeInput(BaseModel):
            folder_path: str = Field(..., description="The directory path to generate a tree from.")

        class GetFileContentInput(BaseModel):
            file_path: str = Field(..., description="Path of the file to read.")

        class WriteFileInput(BaseModel):
            file_path: str = Field(..., description="Path to save the file.")
            content: str = Field(..., description="Content to be written in the file.")

        class CleanResultFolderInput(BaseModel):
            excluded_files: List[str] = Field(..., description="List of filenames to remove inside .result folder.")

        class GetFilesInFolderInput(BaseModel):
            folder_path: str = Field(..., description="Path of the folder to list files from.")

        class GetFilesRecursivelyInput(BaseModel):
            folder_path: str = Field(..., description="Path of the folder to recursively list files.")

        class FindFilesInput(BaseModel):
            extensions: List[str] = Field(..., description="List of file extensions to search for.")

        class ForgePromptInput(BaseModel):
            extensions: List[str] = Field(..., description="List of file extensions to include in the prompt.")

        forge = self

        class GetDirectoryTreeTool(BaseTool):
            name: str = "get_directory_tree"
            description: str = "Returns a list of all files in the specified folder, with paths relative to the base directory."
            args_schema: Type[BaseModel] = GetDirectoryTreeInput

            def _run(self, folder_path: str) -> List[str]:
                return forge.get_directory_tree(folder_path)

        class GetFileContentTool(BaseTool):
            name: str = "get_file_content"
            description: str = "Retrieves the content of a specified file."
            args_schema: Type[BaseModel] = GetFileContentInput

            def _run(self, file_path: str) -> str:
                return forge.get_file_content(file_path)

        class GetFilesInFolderTool(BaseTool):
            name: str = "get_files_in_folder"
            description: str = "Lists all files in the specified folder."
            args_schema: Type[BaseModel] = GetFilesInFolderInput

            def _run(self, folder_path: str) -> Dict[str, str]:
                return forge.get_files_in_folder(folder_path)

        class GetFilesRecursivelyTool(BaseTool):
            name: str = "get_files_recursively"
            description: str = "Lists all files in a folder and its subfolders."
            args_schema: Type[BaseModel] = GetFilesRecursivelyInput

            def _run(self, folder_path: str) -> Dict[str, str]:
                return forge.get_files_recursively(folder_path)

        class FindFilesTool(BaseTool):
            name: str = "find_files"
            description: str = "Finds files with the specified extensions in the base directory."
            args_schema: Type[BaseModel] = FindFilesInput

            def _run(self, extensions: List[str]) -> List[str]:
                return [str(file) for file in forge.find_files(extensions)]

        class WriteFileTool(BaseTool):
            name: str = "write_file"
            description: str = "Writes content to a file inside the .result folder."
            args_schema: Type[BaseModel] = WriteFileInput

            def _run(self, file_path: str, content: str) -> str:
                return forge.write_file(file_path, content)

        class CleanResultFolderTool(BaseTool):
            name: str = "clean_result_folder"
            description: str = "Deletes specific files inside the .result folder."
            args_schema: Type[BaseModel] = CleanResultFolderInput

            def _run(self, excluded_files: List[str]) -> None:
                return forge.clean_result_folder(excluded_files)

        class ForgePromptTool(BaseTool):
            name: str = "forge_prompt"
            description: str = "Combines and processes code files into a single prompt."
            args_schema: Type[BaseModel] = ForgePromptInput

            def _run(self, extensions: List[str]) -> None:
                return forge.forge_prompt(extensions)

        class RunTool(BaseTool):
            name: str = "run"
            description: str = "Runs the forge process on the specified file extensions."
            args_schema: Type[BaseModel] = ForgePromptInput

            def _run(self, extensions: List[str]) -> None:
                return forge.run(extensions)

        return [
            GetDirectoryTreeTool(),
            GetFileContentTool(),
            GetFilesInFolderTool(),
            GetFilesRecursivelyTool(),
            FindFilesTool(),
            WriteFileTool(),
            CleanResultFolderTool(),
            ForgePromptTool(),
            RunTool(),
        ]