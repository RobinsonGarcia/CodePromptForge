import pytest
import json
from pathlib import Path
from codepromptforge.main import (
    CodePromptForge,
    InvalidBaseDirectoryError,
    NoFilesFoundError,
    OutputFileAlreadyExistsError
)


def test_invalid_base_directory():
    with pytest.raises(InvalidBaseDirectoryError):
        forge = CodePromptForge(base_dir="non_existent_dir", output_file="output.txt")
        forge.run(["py"])


def test_no_files_found(tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    forge = CodePromptForge(base_dir=str(empty_dir), output_file=str(tmp_path / "merged.txt"))

    with pytest.raises(NoFilesFoundError):
        forge.run(["py"])


def test_forge_prompt_dry_run(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    (code_dir / "test.py").write_text("# sample python file")

    output_file = tmp_path / "merged.txt"
    forge = CodePromptForge(base_dir=str(code_dir), output_file=str(output_file), dry_run=True)
    forge.run(["py"])

    assert not output_file.exists()


def test_forge_prompt_force_overwrite(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    (code_dir / "test.py").write_text("# sample python file")

    output_file = tmp_path / "merged.txt"
    output_file.write_text("Existing content")

    forge_no_force = CodePromptForge(base_dir=str(code_dir), output_file=str(output_file), force=False)
    with pytest.raises(OutputFileAlreadyExistsError):
        forge_no_force.run(["py"])

    forge_force = CodePromptForge(base_dir=str(code_dir), output_file=str(output_file), force=True)
    forge_force.run(["py"])

    merged_content = output_file.read_text()
    assert "sample python file" in merged_content


def test_include_tree(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    sub_dir = code_dir / "subfolder"
    sub_dir.mkdir()
    (sub_dir / "test.py").write_text("# sample python file in subfolder")
    (code_dir / "main.py").write_text("# main python file")

    output_file = tmp_path / "merged_tree.txt"
    forge = CodePromptForge(base_dir=str(code_dir), output_file=str(output_file), include_tree=True, force=True)
    forge.run(["py"])
    merged_content = output_file.read_text()

    assert "Directory Tree:" in merged_content
    assert "subfolder" in merged_content
    assert "sample python file in subfolder" in merged_content
    assert "main python file" in merged_content


def test_exclude_from_combination(tmp_path):
    """Ensure --exclude prevents files from being combined, but does NOT delete them."""
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    include_file = code_dir / "include.py"
    exclude_file = code_dir / "exclude.py"
    include_file.write_text("print('include')")
    exclude_file.write_text("print('exclude')")

    output_file = tmp_path / "merged.txt"
    forge = CodePromptForge(base_dir=str(code_dir), output_file=str(output_file), excluded=["exclude.py"])
    forge.run(["py"])

    merged_content = output_file.read_text()

    assert "print('include')" in merged_content  # Included file must be present
    assert "print('exclude')" not in merged_content  # Excluded file must NOT be present
    assert exclude_file.exists()  # File should NOT be deleted


def test_get_directory_tree(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    (code_dir / "file.py").write_text("# test file")
    (code_dir / "subdir").mkdir()
    (code_dir / "subdir/test.py").write_text("# test in subdir")

    forge = CodePromptForge(base_dir=str(code_dir))
    tree_output = forge.get_directory_tree(".")

    assert "subdir" in tree_output
    assert "file.py" not in tree_output  # Only directories should appear


def test_get_file_content(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    file_path = code_dir / "test.py"
    file_path.write_text("print('Hello')")

    forge = CodePromptForge(base_dir=str(code_dir))
    content = forge.get_file_content("test.py")

    assert content == "print('Hello')"


def test_get_files_in_folder(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    (code_dir / "test1.py").write_text("print('1')")
    (code_dir / "test2.py").write_text("print('2')")

    forge = CodePromptForge(base_dir=str(code_dir))
    files = forge.get_files_in_folder(".")

    assert len(files) == 2
    assert files["test1.py"] == "print('1')"
    assert files["test2.py"] == "print('2')"


def test_get_files_recursively(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    subdir = code_dir / "subdir"
    subdir.mkdir()
    (code_dir / "main.py").write_text("print('main')")
    (subdir / "nested.py").write_text("print('nested')")

    forge = CodePromptForge(base_dir=str(code_dir))
    files = forge.get_files_recursively(".")

    assert "main.py" in files
    assert "subdir/nested.py" in files
    assert files["main.py"] == "print('main')"
    assert files["subdir/nested.py"] == "print('nested')"


def test_write_file(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()

    forge = CodePromptForge(base_dir=str(code_dir))
    forge.write_file("output.txt", "Hello World")

    result_file = code_dir / ".result/output.txt"
    assert result_file.exists()
    assert result_file.read_text() == "Hello World"


def test_clean_result_folder(tmp_path):
    """Ensure only specified files inside `.result` are removed."""
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    forge = CodePromptForge(base_dir=str(code_dir))

    result_file_1 = code_dir / ".result/file1.txt"
    result_file_2 = code_dir / ".result/file2.txt"
    result_file_1.write_text("content1")
    result_file_2.write_text("content2")

    forge.clean_result_folder(["file1.txt"])

    assert not result_file_1.exists()  # Deleted
    assert result_file_2.exists()  # Still exists


def test_langchain_tools(tmp_path):
    code_dir = tmp_path / "codebase"
    code_dir.mkdir()
    (code_dir / "test.py").write_text("print('Hello')")

    forge = CodePromptForge(base_dir=str(code_dir))
    tools = forge.get_tools()

    assert len(tools) == 9  # Includes `clean_result_folder`

    directory_tree_tool = next(tool for tool in tools if tool.name == "get_directory_tree")
    file_content_tool = next(tool for tool in tools if tool.name == "get_file_content")
    write_file_tool = next(tool for tool in tools if tool.name == "write_file")
    clean_result_tool = next(tool for tool in tools if tool.name == "clean_result_folder")

    assert directory_tree_tool._run(folder_path=".")  # Should return a string
    assert file_content_tool._run(file_path="test.py") == "print('Hello')"
    assert "successfully" in write_file_tool._run(file_path="new_file.txt", content="Test Content")

    result_file = code_dir / ".result/new_file.txt"
    assert result_file.exists()
    assert result_file.read_text() == "Test Content"

    # Test clean_result_folder via tool
    clean_result_tool._run(excluded_files=["new_file.txt"])
    assert not result_file.exists()  # It should be deleted