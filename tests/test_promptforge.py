# tests/test_CodePromptForge.py

import pytest
import tempfile
import shutil
from pathlib import Path

from codepromptforge.main import (
    CodePromptForge,
    InvalidBaseDirectoryError,
    NoFilesFoundError,
    OutputFileAlreadyExistsError
)

def test_invalid_base_directory():
    """
    Ensure that an InvalidBaseDirectoryError is raised if the base directory does not exist.
    """
    with pytest.raises(InvalidBaseDirectoryError):
        forge = CodePromptForge(base_dir="non_existent_dir", output_file="output.txt")
        forge.run(["py"])

def test_no_files_found(tmp_path):
    """
    Ensure that NoFilesFoundError is raised if no matching files are found.
    """
    # tmp_path is automatically cleaned up by pytest
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    forge = CodePromptForge(base_dir=str(empty_dir), output_file=str(tmp_path / "merged.txt"))

    with pytest.raises(NoFilesFoundError):
        forge.run(["py"])

def test_forge_prompt_dry_run(tmp_path):
    """
    Check that dry_run only lists the files without writing any output.
    """
    # Create a test directory with a dummy .py file
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    py_file = code_dir / "test.py"
    py_file.write_text("# sample python file")

    output_file = tmp_path / "merged.txt"
    forge = CodePromptForge(
        base_dir=str(code_dir),
        output_file=str(output_file),
        dry_run=True
    )
    forge.run(["py"])
    # The output file should not exist because of the dry run
    assert not output_file.exists()

def test_forge_prompt_force_overwrite(tmp_path):
    """
    Check that 'force' allows overwriting existing output files.
    """
    # Create a test directory and a dummy file
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    py_file = code_dir / "test.py"
    py_file.write_text("# sample python file")

    # Create an existing output file
    output_file = tmp_path / "merged.txt"
    output_file.write_text("Existing content")

    # Instantiate CodePromptForge with force=False first to ensure it raises an error
    forge_no_force = CodePromptForge(
        base_dir=str(code_dir),
        output_file=str(output_file),
        force=False
    )
    with pytest.raises(OutputFileAlreadyExistsError):
        forge_no_force.run(["py"])

    # Now run again with force=True; it should overwrite without error
    forge_force = CodePromptForge(
        base_dir=str(code_dir),
        output_file=str(output_file),
        force=True
    )
    forge_force.run(["py"])
    # Confirm the file has new content
    merged_content = output_file.read_text()
    assert "sample python file" in merged_content

def test_include_tree(tmp_path):
    """
    Check that the directory tree is included when --include-tree is set to True.
    """
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()

    # Create some folders/files
    sub_dir = code_dir / "subfolder"
    sub_dir.mkdir()
    (sub_dir / "test.py").write_text("# sample python file in subfolder")
    
    file_main = code_dir / "main.py"
    file_main.write_text("# main python file")

    output_file = tmp_path / "merged_tree.txt"
    forge = CodePromptForge(
        base_dir=str(code_dir),
        output_file=str(output_file),
        include_tree=True,
        force=True
    )
    forge.run(["py"])
    merged_content = output_file.read_text()

    # Check for directory tree notation and file content
    assert "Directory Tree:" in merged_content
    assert "subfolder" in merged_content
    assert "sample python file in subfolder" in merged_content
    assert "main python file" in merged_content


def test_exclude_dirs_and_files(tmp_path):
    """
    Ensure that excluded files and directories are not included in the prompt.
    """
    # Setup a test directory structure
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    include_file = code_dir / "include.py"
    exclude_file = code_dir / "exclude.py"
    exclude_dir = code_dir / "exclude_dir"
    exclude_dir.mkdir()
    exclude_dir_file = exclude_dir / "nested.py"
    include_file.write_text("print('include')")
    exclude_file.write_text("print('exclude')")
    exclude_dir_file.write_text("print('nested')")

    forge = CodePromptForge(
        base_dir=str(code_dir),
        output_file=str(tmp_path / "merged.txt"),
        excluded=[str(exclude_file), str(exclude_dir)]
    )
    files = forge.find_files(["py"])

    # Check that only include.py is listed
    assert len(files) == 1
    assert files[0].name == "include.py"