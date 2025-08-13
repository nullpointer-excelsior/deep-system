import os
import platform
import pytest
from deepsystem.system import get_system_summary, SystemSummary


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
