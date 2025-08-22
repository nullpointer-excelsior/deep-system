import os
import platform
import pytest
import tempfile
from deepsystem.system import get_system_summary, SystemSummary, DirectoryContentRepository


def test_get_system_summary_returns_correct_type():
    summary = get_system_summary()
    assert isinstance(summary, SystemSummary)

def test_get_system_summary_contains_expected_fields():
    summary = get_system_summary()
    assert hasattr(summary, "os")
    assert hasattr(summary, "kernel")
    assert hasattr(summary, "cwd")
    assert hasattr(summary, "home")

def test_get_system_summary_os_value():
    summary = get_system_summary()
    system_name = platform.system()
    expected_os = "MacOS" if system_name == "Darwin" else system_name
    assert summary.os == expected_os

def test_get_system_summary_kernel_value():
    summary = get_system_summary()
    assert summary.kernel == platform.release()

def test_get_system_summary_cwd_value():
    summary = get_system_summary()
    assert summary.cwd == os.getcwd()

def test_get_system_summary_home_value():
    summary = get_system_summary()
    assert summary.home == os.path.expanduser("~")

def test_read_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.txt")
        content = "Hello, World!"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        result = DirectoryContentRepository.read(f"{tmpdir}/test.txt")
        assert result == content


def test_read_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.mkdir(os.path.join(tmpdir, "subdir"))
        open(os.path.join(tmpdir, "file1.txt"), "w").close()
        open(os.path.join(tmpdir, "file2.txt"), "w").close()

        result = DirectoryContentRepository.read(tmpdir)
        assert "subdir" in result
        assert "file1.txt" in result
        assert "file2.txt" in result


def test_path_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError):
            DirectoryContentRepository.read(f"{tmpdir}/nonexistent.txt")


def test_invalid_path_type():
    with tempfile.TemporaryDirectory() as tmpdir:
        fifo_path = os.path.join(tmpdir, "myfifo")
        os.mkfifo(fifo_path)
        try:
            with pytest.raises(ValueError):
                DirectoryContentRepository.read(fifo_path)
        finally:
            os.remove(fifo_path)
