# Informed Consent Ontology (ICO) Makefile
# Jie Zheng
#
# This Makefile is used to build artifacts for the Informed Consent Ontology.
#

### Configuration
#
# prologue:
# <http://clarkgrubb.com/makefile-style-guide#toc2>

MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

### Definitions

SHELL := /bin/bash
OBO   := http://purl.obolibrary.org/obo
ICO    := $(OBO)/ICO_
TODAY := $(shell date +%Y-%m-%d)

### Directories
#
# This is a temporary place to put things.
build:
	mkdir -p $@


### ROBOT
#
# We use the latest official release version of ROBOT
build/robot.jar: | build
	curl -L -o $@ "https://github.com/ontodev/robot/releases/latest/download/robot.jar"

ROBOT := java -jar build/robot.jar

### Imports
#
# Use Ontofox to import terms from external ontologies.

src/ontology/imports/%_OntoFox_import.owl: src/ontology/imports/OntoFox_Inputs/%_OntoFox_import_input.txt | build
	curl -s -F file=@$< -o $@ https://ontofox.hegroup.org/service.php

IMPORT_FILES := $(wildcard src/ontology/imports/*_OntoFox_import.owl)

.PHONY: imports
imports: $(IMPORT_FILES)


### Build
#
# Here we create a standalone OWL file appropriate for release.
# This involves merging, reasoning, annotating,
# and removing any remaining import declarations.

build/ico-merged.owl: src/ontology/ico-edit.owl | build/robot.jar build
	$(ROBOT) merge \
	--input $< \
	annotate \
	--ontology-iri "$(OBO)/ico/ico-merged.owl" \
	--version-iri "$(OBO)/ico/releases/$(TODAY)/ico-merged.owl" \
	--annotation owl:versionInfo "$(TODAY)" \
	--output build/ico-merged.tmp.owl
	sed '/<owl:imports/d' build/ico-merged.tmp.owl > $@
	rm build/ico-merged.tmp.owl

ico.owl: build/ico-merged.owl
	$(ROBOT) reason \
	--input $< \
	--reasoner ELK \
	annotate \
	--ontology-iri "$(OBO)/ico.owl" \
	--version-iri "$(OBO)/ico/releases/$(TODAY)/ico.owl" \
	--annotation owl:versionInfo "$(TODAY)" \
	--output $@

ico-base.owl: ico.owl
	$(ROBOT) remove \
	--input $< \
 	--base-iri http://purl.obolibrary.org/obo/ICO_ \
 	--axioms external \
 	--preserve-structure false \
	--trim false \
 	--output $@

robot_report.tsv: ico-base.owl
	$(ROBOT) report \
	--input $< \
        --fail-on none \
	--output $@

### 
#
# Full build
.PHONY: all
all: ico.owl robot_report.tsv

# Remove generated files
.PHONY: clean
clean:
	rm -rf build



