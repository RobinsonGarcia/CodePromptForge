import subprocess
import json
import pytest
from pathlib import Path


@pytest.fixture
def setup_codebase(tmp_path):
    """Creates a temporary codebase for CLI testing with the correct structure."""
    codebase = tmp_path / "codebase"
    codebase.mkdir()

    # Create test.py
    (codebase / "test.py").write_text("print('Hello')")

    # Create subdir with both script.py and nested.py
    sub_dir = codebase / "subdir"
    sub_dir.mkdir()
    (sub_dir / "script.py").write_text("print('Nested Script')")
    (sub_dir / "nested.py").write_text("print('Nested')")

    # Ensure .result exists for clean_result test
    result_dir = codebase / ".result"
    result_dir.mkdir()
    (result_dir / "old_output.txt").write_text("Old Content")
    (result_dir / "keep.txt").write_text("Keep Me")

    return codebase


import subprocess
import pytest
from pathlib import Path

def run_cli_command(command, cwd, expect_error=False):
    """Runs CLI command using installed package and returns output or error."""
    result = subprocess.run(
        ["python", "-m", "codepromptforge.cli"] + command,  # ✅ Ensure it runs as module
        cwd=cwd,
        text=True,
        capture_output=True
    )

    if expect_error:
        assert result.returncode != 0, f"Expected error but command succeeded: {command}\nOutput: {result.stdout}\nError: {result.stderr}"
        return result.stderr.strip()
    else:
        assert result.returncode == 0, f"Command failed unexpectedly: {command}\nOutput: {result.stdout}\nError: {result.stderr}"
        return result.stdout.strip()



# ✅ Test: Generate Directory Tree
def test_cli_directory_tree(setup_codebase):
    output = run_cli_command(["tree", "--folder", "."], setup_codebase)
    assert "subdir" in output, f"Unexpected output: {output}"


# ✅ Test: Get File Content
def test_cli_get_file_content(setup_codebase):
    output = run_cli_command(["file", "--file", "test.py"], setup_codebase)
    assert "print('Hello')" in output, f"Unexpected output: {output}"


# ✅ Test: List Files in Folder
def test_cli_get_files_in_folder(setup_codebase):
    output = run_cli_command(["files", "--folder", "."], setup_codebase)
    assert output, "Output is empty; expected JSON file list."

    try:
        files = json.loads(output)
        assert "test.py" in files, f"test.py not found in: {files}"
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON output: {output}")


def test_cli_get_files_recursively(setup_codebase):
    output = run_cli_command(["files_recursive", "--folder", "."], setup_codebase)
    assert output, "Output is empty; expected JSON file list."

    try:
        files = json.loads(output)
        assert "test.py" in files, f"test.py not found in: {files}"
        assert "subdir/script.py" in files, f"subdir/script.py not found in: {files}"
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON output: {output}")


def test_cli_write_file(setup_codebase):
    result_dir = setup_codebase / ".result"
    run_cli_command(["write", "--file", "output.txt", "--content", "Test Write"], setup_codebase)

    result_file = result_dir / "output.txt"
    assert result_file.exists(), "File was not created in .result directory."
    assert result_file.read_text() == "Test Write", f"Unexpected file content: {result_file.read_text()}"


def test_cli_combine_files(setup_codebase):
    output_file = setup_codebase / "combined.txt"
    run_cli_command(["combine", "--extensions", "py", "--output-file", "combined.txt"], setup_codebase)

    assert output_file.exists(), "Output file was not created."
    content = output_file.read_text()
    assert "print('Hello')" in content, "Combined file missing 'test.py' content."
    assert "print('Nested Script')" in content, "Combined file missing 'script.py' content."


def test_cli_exclude_from_combination(setup_codebase):
    output_file = setup_codebase / "combined_exclude.txt"
    run_cli_command(["combine", "--extensions", "py", "--output-file", "combined_exclude.txt", "--exclude", "test.py"], setup_codebase)

    assert output_file.exists(), "Output file was not created."
    content = output_file.read_text()
    assert "print('Nested Script')" in content, "Expected 'script.py' in output."
    assert "print('Hello')" not in content, "Excluded 'test.py' should not be in output."


def test_cli_clean_result(setup_codebase):
    result_dir = setup_codebase / ".result"
    run_cli_command(["clean_result", "--exclude-clean", "old_output.txt"], setup_codebase)

    assert not (result_dir / "old_output.txt").exists(), "Excluded file should be deleted."
    assert (result_dir / "keep.txt").exists(), "Non-excluded file should not be deleted."


# ✅ Test: Error Handling - Missing Arguments
def test_cli_missing_arguments(setup_codebase):
    error_output = run_cli_command(["tree"], setup_codebase, expect_error=True)
    assert "The --folder argument is required" in error_output

    error_output = run_cli_command(["file"], setup_codebase, expect_error=True)
    assert "The --file argument is required" in error_output

    error_output = run_cli_command(["combine", "--extensions", "py"], setup_codebase, expect_error=True)
    assert "--output-file are required for 'combine'" in error_output