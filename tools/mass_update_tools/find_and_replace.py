#!/usr/bin/env python3
import fileinput
import sys
import os
import argparse
from shutil import copyfile
import pandas as pd


def findAndReplace(ontology_copy, keys):

    keyFile = pd.read_csv(keys, header=None)
    keyFile.columns = ['OldPurl', 'NewPurl']

    # print(keyFile.head())

    for index, row in keyFile.iterrows():
        oldPurl = row['OldPurl']
        newPurl = row['NewPurl']

        with fileinput.FileInput(ontology_copy, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(oldPurl, newPurl), end='')


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--src", help="ontology file")
    parser.add_argument("--key", help="key - value pairs for search/replace (in that order)'")
    parser.add_argument("--dest", help="Name of destination .owl output")
    args = parser.parse_args()

    newFile = copyfile(args.src, args.dest)
    print(args.src, ' copied to ', args.dest)

    # run puppy, run
    findAndReplace(newFile, args.key)
