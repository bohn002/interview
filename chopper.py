""" Take the txt and 'chopper' it up into top X phrases of Y words """
import argparse
import os
import re
import sys

from collections import Counter
from nltk import ngrams
from nltk.tokenize import word_tokenize


def build_args(piped: bool = False):
    """Build the argument parser"""
    parser = argparse.ArgumentParser(
        description="Get up to the top X (default 100) most popular Y "
        "(Default 3) word phrases in a single or multiple text files. "
        "You can also pipe or redirect text into this script."
    )
    if piped:
        parser.add_argument(
            "infile",
            nargs="?",
            type=argparse.FileType("r"),
            default="-",
        )  # Catch stdin
    else:
        parser.add_argument(
            "filenames",
            metavar="filename",
            type=str,
            nargs="*",
            help="a file or files to be processed",
        )

    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=100,
        help="the number of phrases to return (default: 100)",
    )
    # Is the requirement to return up to the top 100 phrases? Yes.
    # In a real-world scenario, would this be likely to change?
    # Yes. Yes it would. So, I'm going to make it a parameter.

    parser.add_argument(
        "-w",
        "--words",
        type=int,
        default=3,
        help="the number of words in each phrase (default: 3)",
    )  # Same as above. I'm going to make this a parameter.
    return parser.parse_args()


def clean_content(unclean_text) -> str:
    """
    Read the file, lowercase it all for better reading split it into lines,
    join it back together with spaces, and send it back

    We are also going to use regex to remove punctuation.
    """
    content = " ".join(unclean_text.read().lower().strip().splitlines())
    content = re.sub(r"\s+", " ", content)  # Remove extra whitespace
    content = re.sub(r"[^\w\s]", "", content)
    # Remove punctuation. The \w is for word characters, and the \s is
    # for whitespace. We would have had to define additional punctuation
    # characters if we used `translate`, and that would have been a pain.
    return content


def process_file_list(filenames: list) -> list:
    """
    Process a list of files and return a list of their contents.

    We will assume that the files are small enough to fit in memory.
    We are going to read the text data, split it into lines, and then
    join it back together with spaces. This will allow us to split on
    spaces and get a list of words by joining them all together.

    If we have multiple files, we will return a list of strings. If we
    have a single file, we will return a list with a single string.
    """
    content = []
    for file in filenames:
        with open(file, "r", encoding="utf-8") as file_handle:
            content.append(clean_content(file_handle))
    return content


def get_phrases(content: list, words: int) -> list:
    """
    Get the top X phrases from the content list. Using nltk because we need
    common phrases of 3 words, not just the text cut up into 3 word phrases.

    This is to make sure we get "the white rabbit" and not "and the white"
    and "white rabbit ran"

    We will be using the magic of n-grams! n-grams can look complicated,
    but they basically show a relationship of proximity in text.
    Read more on the wikipedia page: https://en.wikipedia.org/wiki/N-gram

    """
    chunks = []
    for item in content:
        tokens = word_tokenize(item)
        # Tokenize the text. A token is a single unit of text.
        # In this case, it's a word.
        chunks.extend(ngrams(tokens, words))
        # Get the n-grams. We are using the nltk library to do this.
        # We are going to get the n-grams of the tokens, and we are
        # going to use the number of words specified in the arguments.
        # Pack it all in a big list.
    return chunks


def get_tty():
    """Check if we're being piped to or not"""
    return not os.isatty(sys.stdin.fileno())


def chopper():
    """Main function for chopper.py"""
    # Set up the argument parser. Args get weird if you pipe it
    # vs positional, so let's figure that out and split it up based
    # on if its tty or not.

    piped = get_tty()
    # If there's no terminal, assume we're being piped to. Not bulletproof,
    # but should be good enough for this.

    args = build_args(piped)

    if piped:
        content = [clean_content(args.infile)]
        # Read the file, split it into lines, join it back together
        # with spaces, and append it to the list.
    else:
        content = process_file_list(args.filenames)

    chunks = get_phrases(content, args.words)

    for phrase, count in Counter(chunks).most_common(args.num):
        print(f"{count} - {' '.join(phrase)}")


# Do the needful
if __name__ == "__main__":
    chopper()
