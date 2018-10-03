# Command Line Tools for Mass OWL Updates
This is a set of command line tools designed to extract terms and definitions from an OWL file into a `.csv`. The `.csv` file can be imported into a common application such as MS Excel in order to make changes to the content. Once changes have been made the OWL file can be updated for all terms that were changed. This is helpful for teams that want to make significant content changes to terms and definitions at once. The primary reason for including these is that they were used to revise content in `ico.owl` during the summer of 2018.

## Note on robot
These tools are not as robust or system-independent as [robot](http://robot.obolibrary.org/). It is recommended that future work of this nature be conducted using [robot extract](http://robot.obolibrary.org/extract) and [robot template](http://robot.obolibrary.org/template)

## `extract_onto.py`
This tool takes one `.owl` file command line argument. It produces a `.csv` file with terms and definitions in the following format:

    PURL,Term Label,Definition

## ` revise_onto.py`
This tool takes one `.owl` file and one `.csv` command line argument. It is expected that the `.csv` file is in **exactly** the same format as the output from `extract_onto.py`. It compares the 'PURLS' in the `.csv` to the existing content in the `.owl` file and creates an updated `.owl` file and and revisions file to compare and document the changes.
