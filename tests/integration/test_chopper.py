"""Integration tests for chopper.py"""
import argparse

from unittest.mock import patch

from chopper import chopper

arg_list = {
    "num": 100,
    "words": 3,
    "filenames": ["tests/fixtures/raj.txt"],
    "infile": "-",
}

arg_list_tty = {
    "num": 100,
    "words": 3,
    "filenames": None,
    "infile": "-",
}

raj_expected = [
    ("33", "the project gutenberg"),
    ("18", "project gutenberg electronic"),
    ("14", "the united states"),
    ("13", "the terms of"),
    ("13", "project gutenberg literary"),
    ("13", "gutenberg literary archive"),
    ("13", "literary archive foundation"),
    ("12", "in capulets house"),
    ("12", "gutenberg electronic works"),
    ("11", "project gutenberg license"),
    ("10", "in the united"),
    ("10", "of the project"),
    ("10", "friar lawrences cell"),
    ("10", "terms of this"),
    ("10", "of this agreement"),
    ("8", "capulet lady capulet"),
    ("8", "go with me"),
    ("8", "set forth in"),
    ("8", "of project gutenberg"),
    ("7", "i pray thee"),
    ("7", "i can not"),
    ("7", "full project gutenberg"),
    ("7", "to the project"),
    ("6", "romeo and juliet"),
    ("6", "terms of the"),
    ("6", "room in capulets"),
    ("6", "scene iv a"),
    ("6", "hall in capulets"),
    ("6", "what say you"),
    ("6", "lady capulet and"),
    ("6", "enter friar lawrence"),
    ("6", "where is my"),
    ("6", "the full project"),
    ("6", "gutenberg electronic work"),
    ("5", "capulets house scene"),
    ("5", "_exeunt_ scene ii"),
    ("5", "capulets house enter"),
    ("5", "enter lady capulet"),
    ("5", "i am too"),
    ("5", "i know not"),
    ("5", "lawrences cell enter"),
    ("5", "cell enter friar"),
    ("5", "commend me to"),
    ("5", "part of this"),
    ("5", "you do not"),
    ("5", "not protected by"),
    ("5", "project gutenberg trademark"),
    ("5", "work or any"),
    ("5", "a project gutenberg"),
    ("5", "project gutenberg works"),
    ("5", "project gutenberg work"),
    ("4", "the use of"),
    ("4", "if you are"),
    ("4", "the laws of"),
    ("4", "laws of the"),
    ("4", "you are located"),
    ("4", "scene i a"),
    ("4", "i a public"),
    ("4", "a public place"),
    ("4", "scene ii a"),
    ("4", "a street scene"),
    ("4", "iv a street"),
    ("4", "scene iii friar"),
    ("4", "iii friar lawrences"),
    ("4", "lawrences cell scene"),
    ("4", "a room in"),
    ("4", "thou art not"),
    ("4", "of the house"),
    ("4", "if thou art"),
    ("4", "i will be"),
    ("4", "bite my thumb"),
    ("4", "if you do"),
    ("4", "i am not"),
    ("4", "that you love"),
    ("4", "a street enter"),
    ("4", "is but a"),
    ("4", "and i will"),
    ("4", "this is the"),
    ("4", "lady capulet what"),
    ("4", "and i am"),
    ("4", "_exeunt_ scene v"),
    ("4", "we can not"),
    ("4", "it is my"),
    ("4", "you go to"),
    ("4", "not to be"),
    ("4", "i thank you"),
    ("4", "enter romeo romeo"),
    ("4", "by and by"),
    ("4", "i will not"),
    ("4", "friar lawrence o"),
    ("4", "a man to"),
    ("4", "i am the"),
    ("4", "as they say"),
    ("4", "me to thy"),
    ("4", "here comes the"),
    ("4", "friar lawrence hold"),
    ("4", "there art thou"),
    ("4", "give me thy"),
    ("4", "day lady capulet"),
    ("4", "lady capulet o"),
]


def _clean_cap_data(captured):
    cap_data = captured.out.splitlines()
    cap_data_cleaned = []
    for line in cap_data:
        cap_data_cleaned.append(tuple(line.split(" - ")))
    return cap_data_cleaned


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(**arg_list),
)
@patch("chopper.get_tty", return_value=False)
def test_chopper(mock_tty, mock_args, capsys):
    """Test chopper with file input"""
    chopper()  # no return from chopper, only stdout
    cap_data_cleaned = _clean_cap_data(
        capsys.readouterr()
    )  # get stdout and clean it
    assert cap_data_cleaned == raj_expected


@patch("argparse.ArgumentParser.parse_args")
@patch("chopper.get_tty", return_value=True)
def test_chopper_tty(mock_tty, mock_args, capsys):
    """Test chopper with tty"""
    # Load the file into stdin i.e. stream and run chopper
    arg_list_tty["infile"] = open(
        "tests/fixtures/raj.txt", "r", encoding="utf-8"
    )
    mock_args.return_value = argparse.Namespace(**arg_list_tty)
    chopper()  # no return from chopper, only stdout
    cap_data_cleaned = _clean_cap_data(
        capsys.readouterr()
    )  # get stdout and clean it
    assert cap_data_cleaned == raj_expected
