""" Unit tests for chopper.py """
from io import StringIO
from unittest.mock import patch

import argparse
import pytest

from chopper import (
    build_args,
    clean_content,
    chopper,
    get_phrases,
    process_file_list,
)


@pytest.mark.parametrize(
    "arg_list, piped, expected",
    [
        (
            {"num": 100, "words": 3, "filenames": None, "infile": "-"},
            True,
            {"num": 100, "words": 3, "filenames": None, "infile": "-"},
        ),
        (
            {
                "num": 100,
                "words": 3,
                "filenames": ["one.txt", "two.txt", "three.txt"],
                "infile": "-",
            },
            False,
            {
                "num": 100,
                "words": 3,
                "filenames": ["one.txt", "two.txt", "three.txt"],
                "infile": "-",
            },
        ),
    ],
)
def test_build_args(arg_list, piped, expected):
    """Test build_args"""
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(**arg_list),
    ):
        args = build_args(piped)
        assert args.num == expected["num"]
        assert args.words == expected["words"]
        assert args.filenames == expected["filenames"]
        assert args.infile == expected["infile"]


def test_clean_content():
    """Test clean_content"""
    unclean_text = """This is a test! This is only a test.
    WHAT A TEST!!!!!!@#$%^&*()-+=[]{}|;':",./<>?
    This    is   also a spacing test.
    """
    expected_text = (
        "this is a test this is only a test what "
        "a test this is also a spacing test"
    )
    assert clean_content(StringIO(unclean_text)) == expected_text


def test_process_file_list():
    """Test process_file_list"""
    filenames = [
        "tests/fixtures/one.txt",
        "tests/fixtures/two.txt",
    ]
    with patch(
        "chopper.clean_content",
        side_effect=[
            "im a test document",
            "i am also a test document cant you tell",
        ],
    ):
        assert process_file_list(filenames) == [
            "im a test document",
            "i am also a test document cant you tell",
        ]


@pytest.mark.parametrize(
    "expected, words",
    [
        (
            [
                ("im", "a", "test"),
                ("a", "test", "document"),
                ("i", "am", "also"),
                ("am", "also", "a"),
                ("also", "a", "test"),
                ("a", "test", "document"),
                ("test", "document", "cant"),
                ("document", "cant", "you"),
                ("cant", "you", "tell"),
            ],
            3,
        ),
        (
            [
                ("im", "a", "test", "document"),
                ("i", "am", "also", "a"),
                ("am", "also", "a", "test"),
                ("also", "a", "test", "document"),
                ("a", "test", "document", "cant"),
                ("test", "document", "cant", "you"),
                ("document", "cant", "you", "tell"),
            ],
            4,
        ),
    ],
)
def test_get_phrases(expected, words):
    """Test get_phrases"""
    phrases = [
        "im a test document",
        "i am also a test document cant you tell",
    ]
    assert get_phrases(phrases, words) == expected


@patch("argparse.ArgumentParser.parse_args")
@patch("chopper.get_tty", return_value=False)
@patch("chopper.process_file_list")
@patch("chopper.get_phrases")
def test_chopper(
    mock_get_phrases, mock_process_file_list, mock_get_tty, mock_args
):
    """
    Test chopper. Maybe not needed since we are testing the other functions
    and this is all Mocks, but lets pump up those coverage numbers!
    """
    mock_args.return_value = argparse.Namespace(
        num=100, words=3, filenames=["tests/fixtures/raj.txt"], infile="-"
    )
    mock_process_file_list.return_value = ["this is a test document"]
    mock_get_phrases.return_value = [
        ("this", "is", "a"),
        ("is", "a", "test"),
        ("a", "test", "document"),
    ]
    chopper()
    mock_get_phrases.assert_called_once_with(["this is a test document"], 3)
    mock_process_file_list.assert_called_once_with(["tests/fixtures/raj.txt"])
    mock_get_tty.assert_called_once()
    mock_args.assert_called_once()


@patch("argparse.ArgumentParser.parse_args")
@patch("chopper.get_tty", return_value=True)
@patch("chopper.process_file_list")
@patch("chopper.get_phrases")
def test_chopper_piped(
    mock_get_phrases, mock_process_file_list, mock_get_tty, mock_args
):
    """
    Test chopper. Maybe not needed since we are testing the other functions
    and this is all Mocks, but lets pump up those coverage numbers!
    """
    mock_args.return_value = argparse.Namespace(
        num=100,
        words=3,
        filenames=None,
        infile=StringIO("this is a test document"),
    )
    mock_process_file_list.return_value = ["this is a test document"]
    mock_get_phrases.return_value = [
        ("this", "is", "a"),
        ("is", "a", "test"),
        ("a", "test", "document"),
    ]
    chopper()
    mock_get_phrases.assert_called_once_with(["this is a test document"], 3)
    mock_process_file_list.assert_not_called()
    mock_get_tty.assert_called_once()
    mock_args.assert_called_once()
