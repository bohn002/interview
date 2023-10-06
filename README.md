# Chopper

> Tweaked content from a interview code example, so decided to showcase the work

![OnePiece Chopper](img/onePiece_Chopper.png)

Chopper will give you the top 100, 3 word phrases in a single or multiple text files.

Chopper will read all the text, flatten it, organize it, remove all punctuation and then tokenize the text to look for the phrases.

Currently only supporting `*.txt` files.

Supports Linux and OSX.


- [Chopper](#chopper)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Single \*.txt File](#single-txt-file)
    - [Multiple \*.txt Files](#multiple-txt-files)
  - [Results](#results)
    - [Origin of Species](#origin-of-species)
  - [Alice's Adventures in Wonderland \& Romeo and Juliet](#alices-adventures-in-wonderland--romeo-and-juliet)
  - [Moby Dick from STDIN](#moby-dick-from-stdin)
  - [Tests](#tests)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
    - [Coverage](#coverage)
  - [Credits](#credits)


## Requirements

 - Python 3.11.X
 - [Poetry](https://python-poetry.org/docs/#installation)

Install dependencies via Poetry.
  
```bash
$ poetry install
```

To use the created Virtual Python Environment via poetry, append the Usage instructions by prepending `poetry run` to the beginning of the commands:

```
$ poetry run python chopper file1.txt
```

alternatively you can just run it all through the `poetry shell`

```
$ poetry shell
> python chopper.py file1.txt
```

otherwise, if you manage your own environment, you can skip prepending `poetry`


## Usage

```
❯ python chopper.py -h
usage: chopper.py [-h] [-n NUM] [-w WORDS] [filename ...]

Get up to the top X (default 100) most popular Y (Default 3) word phrases in a single or multiple text files. You can also pipe or redirect text into this script.

positional arguments:
  filename                a file or files to be processed

options:
  -h, --help              show this help message and exit
  -n NUM, --num NUM       the number of phrases to return (default: 100)
  -w WORDS, --words WORDS the number of words in each phrase (default: 3)
```

### Single *.txt File

You can point Chopper at a single file:

`python chopper.py file1.txt`

Or you can point stdin at Chopper:

`cat file1.txt | python chopper.py`

### Multiple *.txt Files

`python chopper.py file1.txt file2.txt file3.txt`

## Results

### Origin of Species
Using Chopper against *The Origin of Species by Means of Natural Selection* from Project Gutenberg

```bash
❯ time python chopper.py ./files/oos.txt
320 - of the same
125 - conditions of life
125 - the same species
116 - in the same
110 - of natural selection
103 - from each other
97 - species of the
...
35 - the power of
35 - reason to believe
34 - the project gutenberg
34 - in relation to
33 - at the present
33 - and this is
python chopper.py ./files/oos.txt  0.49s user 0.04s system 99% cpu 0.535 total
```

## Alice's Adventures in Wonderland & Romeo and Juliet

```bash
❯ time python chopper.py ./files/alice.txt ./files/raj.txt
66 - the project gutenberg
51 - the mock turtle
36 - project gutenberg electronic
30 - the march hare
29 - said the king
28 - the united states
26 - the terms of
...
7 - and looked at
7 - was going to
7 - the top of
7 - i must be
7 - it would be
7 - back to the
7 - the poor little
python chopper.py ./files/alice.txt ./files/raj.txt  0.21s user 0.04s system 82% cpu 0.296 total
```

## Moby Dick from STDIN

```bash
❯ time cat ./files/moby.txt | python chopper.py
83 - the sperm whale
76 - of the whale
71 - the white whale
64 - one of the
57 - of the sea
57 - out of the
...
15 - him in the
15 - in the same
15 - of his head
15 - some of the
15 - of the leviathan
14 - the terms of
14 - with all the
cat ./files/moby.txt  0.00s user 0.00s system 1% cpu 0.192 total
python chopper.py  0.47s user 0.05s system 87% cpu 0.589 total
```

## Tests

### Unit Tests
```bash
❯ python -m pytest tests/unit
===================== test session starts ======================
platform darwin -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/nathanbohn/code/
plugins: cov-4.1.0
collected 7 items

tests/unit/test_chopper.py .......              [100%]

====================== 7 passed in 0.12s =======================
```


### Integration Tests

```bash
❯ python -m pytest tests/integration
===================== test session starts ======================
platform darwin -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/nathanbohn/code/
plugins: cov-4.1.0
collected 2 items 

tests/integration/test_chopper. py ..           [100%]

====================== 2 passed in 0.22s =======================

```

### Coverage

```
❯ python -m pytest --cov --cov-branch
===================== test session starts ======================
platform darwin -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/nathanbohn/code/
plugins: cov-4.1.0
collected 9 items

tests/integration/test_chopper.py ..                        [ 22%]
tests/unit/test_chopper.py .......                          [100%]

---------- coverage: platform darwin, python 3.11.4-final-0 ----------
Name                                Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------------
chopper.py                             46      2     14      1    95%
tests/__init__.py                       0      0      0      0   100%
tests/integration/__init__.py           0      0      0      0   100%
tests/integration/test_chopper.py      26      0     14      0   100%
tests/unit/__init__.py                  0      0      0      0   100%
tests/unit/test_chopper.py             52      8     28      0    90%
---------------------------------------------------------------------
TOTAL                                 124     10     56      1    94%

====================== 9 passed in 0.33s =======================
```

## Credits

- [Chopper Image - bodskih@DeviantArt](https://www.deviantart.com/bodskih/art/Tony-Tony-Chopper-942338478)
- [NLTK - Python Natural Language Toolkit](https://www.nltk.org/)
- [Project Guttenberg](https://www.gutenberg.org/)