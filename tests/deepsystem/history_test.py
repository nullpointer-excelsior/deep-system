# test_history.py
import pytest
from unittest.mock import patch, MagicMock
from deepsystem import history


@patch("deepsystem.history.create_checkpointer")
@patch("deepsystem.history.system_summary")
def test_find_message_content(mock_system_summary, mock_create_checkpointer):
    # Mock system_summary.cwd
    mock_system_summary.cwd = "thread-123"

    # Mock checkpointer
    mock_checkpoint_instance = MagicMock()
    mock_checkpoint_instance.get.return_value = {
        "channel_values": {
            "messages": [
                MagicMock(content="Hello"),
                MagicMock(content="World"),
            ]
        }
    }
    mock_create_checkpointer.return_value = mock_checkpoint_instance

    result = history.find_message_content()
    assert result == ["Hello", "World"]

    mock_create_checkpointer.assert_called_once()
    mock_checkpoint_instance.get.assert_called_once_with(
        {"configurable": {"thread_id": "thread-123"}}
    )

@pytest.mark.parametrize(
    "markdown, expected",
    [
        ("```python\nprint('hello')\n```", [{"code": "print('hello')", "ext": "py"}]),
        (
            "```python\nprint('hi')\n```"
            "```javascript\nconsole.log('hi')\n```"
            "```bash\necho hi\n```",
            [
                {"code": "print('hi')", "ext": "py"},
                {"code": "console.log('hi')", "ext": "js"},
                {"code": "echo hi", "ext": "sh"},
            ],
        ),
        ("```brainfuck\n+++++\n```", [{"code": "+++++", "ext": "brainfuck"}]),
        ("This is plain text without code.", []),
    ],
)
def test_extract_code_snippets(markdown, expected):
    result = history.extract_code_snippets(markdown)
    assert result == expected


@pytest.mark.parametrize(
    "contents, expected_exts",
    [
        (["```python\nprint('a')\n```", "```bash\necho b\n```"], ["py", "sh"]),
        ([], []),
    ],
)
def test_get_code_snippets(contents, expected_exts):
    result = history.get_code_snippets(contents)
    assert [item["ext"] for item in result] == expected_exts
