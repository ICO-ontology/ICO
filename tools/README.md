# Tools
This directory contains a number of tools that can be used to work with local `.owl` files and directories for organizing temporary intermediate release artifacts. **Note:** each tool has dependencies. Please look under the each header for more details.

## Release Process
The root directory is structured loosely based on the [Ontology Development Kit](https://github.com/INCATools/ontology-development-kit) (ODK). However, full testing and continuous integration have not been set up to release ICO per ODK (as this is not needed at the time of this writing). The reason this process is labeled temporary is that a simple shell script performs the necessary tasks using ROBOT, the OBO Foundry tool set. **This process assumes that the current release of [ROBOT](http://robot.obolibrary.org/) is installed on the machine that is releasing ICO**. Please visit [http://robot.obolibrary.org/](http://robot.obolibrary.org/) for more information.

### Running the Release Script
The script can be invoked as follows:

```
./release_process.sh
```

The script performs the following actions:

1. Merge `ico-edit.owl` in the `src/ontology/` directory.
1. Create version IRI using the current date.
1. Reason (lightweight), include inferred axioms.
1. Generate reporting.

### Intermediate OWL artifacts
This directory contains intermediate owl files produced by the release process. The products can be removed during the


## Mass Update Tools
This is a set of command line tools designed to extract terms and definitions from an `.owl` file into a `.csv` using Python. The `.csv` file can be imported into a common application such as MS Excel in order to make changes to the content. Once changes have been made the OWL file can be updated for all terms that were changed. This is helpful for teams that want to make significant content changes to terms and definitions at once. The primary reason for including these is that they were used to revise content in `ico.owl` during the summer of 2018.

### `extract_classes.py`
This tool takes one `.owl` file command line argument. It produces a `.csv` file with terms and definitions in the following format:

```
PURL,Term Label,Definition
```

### `insert_new_definitions.py`
This tool takes one `.owl` file and one `.csv` command line argument. It is expected that the `.csv` file is in **exactly** the same format as the output from `extract_classes.py`. It compares the 'PURLS' in the `.csv` to the existing content in the `.owl` file and creates an updated `.owl` file and and revisions file to compare and document the changes.
