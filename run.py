"""Script meant to be called from command line to run the Jack compiler

Command line arguments expected:
    directory with .jack files
    verbosity of output ('full' or 'minimal')

All of the .jack files will be compiled and saved in the same direcotry with
the same names but different extensions.
"""

import sys
import os

from src.glossary import get_verbosity_indicators
from src.translation import run_translation

SOURCE_FOLDER_NAME = "src"
LEXICON_FOLDER_NAME = "LexicalElements"
JACK_EXT = ".jack"

def load_lexicon():
    """Loads the lexical elemets in form of a dictionary"""

    file_dir = os.path.dirname(os.path.realpath(__file__))
    lex_dir = os.path.join(file_dir, SOURCE_FOLDER_NAME, LEXICON_FOLDER_NAME)
    all_files = os.listdir(lex_dir)
    lexicon = {}
    for one_file in all_files:
        if ".txt" not in one_file:
            continue
        one_file_path = os.path.join(lex_dir, one_file)
        with open(one_file_path) as one_file_opened:
            lns = one_file_opened.readlines()
        lns = [el.strip() for el in lns]
        lexicon[one_file.replace(".txt", "")] = lns
    return lexicon

def list_jack_files(jackdir):
    """Creates a list of .jack files to be compiled"""

    jackdir = os.path.realpath(jackdir)

    # Only one .jack file
    if JACK_EXT in jackdir:
        return [jackdir]

    # Get .jack files in the directory
    files = os.listdir(jackdir)
    jack_files = []
    for filename in files:
        if JACK_EXT in filename:
            jack_files.append(os.path.join(jackdir, filename))
    return jack_files

def get_verbosity(args):
    """Returns the verbosity argument. Default is full."""

    verbosity_indicators = get_verbosity_indicators()

    if len(args) >= 3:
        if args[2] not in verbosity_indicators:
            raise Exception(
                "verbosity indicator '" + args[2] + "' unrecognised"
            )
        return args[2]

    return verbosity_indicators[0]

def run_compiler(args):
    """Runs the program"""
    lexicon = load_lexicon()
    jack_files = list_jack_files(args[1])
    verbosity = get_verbosity(args)
    run_translation(lexicon, jack_files, verbosity)

if __name__ == "__main__":
    run_compiler(sys.argv)
