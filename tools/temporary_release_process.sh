#!/usr/bin/env bash

# This release process is a number of shortcuts used to create a
# stable owl representation of ICO.

# Check to see if robot installed
command -v robot 1> /dev/null 2>&1 || \
  { printf >&2 "robot (http://robot.obolibrary.org/) required. Aborting."; exit 1; }

# Start by assuming it was the path invoked.
THIS_SCRIPT="$0"

# Handle resolving symlinks to this script.
# Using ls instead of readlink, because bsd and gnu flavors
# have different behavior.
while [ -h "$THIS_SCRIPT" ] ; do
  ls=`ls -ld "$THIS_SCRIPT"`
  # Drop everything prior to ->
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    THIS_SCRIPT="$link"
  else
    THIS_SCRIPT=`dirname "$THIS_SCRIPT"`/"$link"
  fi
done

# Get path
SCRIPT_DIR=$(dirname "${THIS_SCRIPT}")

# parameters
# TODO: make repository paths more robust
ICO="${SCRIPT_DIR}/../src/ontology/ico-edit.owl"
LOG="${SCRIPT_DIR}/release_notes/`date '+%Y-%m-%d'`.txt"

# ELK is chosen because ICO does not have strict logical
# requirements. Needs to be updated as requirements change.
REASONER='ELK'
MERGED="${SCRIPT_DIR}/intermediate_owl_artifacts/ICO-MERGED-`date '+%Y-%m-%d'`.owl"
VERSIONED="${SCRIPT_DIR}/intermediate_owl_artifacts/ICO-VERSIONED-`date '+%Y-%m-%d'`.owl"
RELEASE="ICO-RELEASE-`date '+%Y-%m-%d'`.owl"

# Gather ontology imports to single file.
robot merge \
  --input ${ICO} \
  --include-annotations true \
  --output ${MERGED} &> ${LOG}

printf "Merging ontologies ... DONE\n"

# add date to IRI version (per OBO best-practices)
robot annotate \
  --input ${MERGED} \
  --ontology-iri "http://purl.obolibrary.org/obo/ICO.owl" \
  --version-iri "http://purl.obolibrary.org/obo/`date '+%Y-%m-%d'`/ico.owl" \
  --output ${VERSIONED} &> ${LOG}

printf "Versioning ... DONE\n"

# include inferred axioms in reasoning check
# TODO: handle errors caused by improperly specificied axioms
robot reason \
	--input ${VERSIONED} \
  --reasoner ${REASONER} \
  --annotate-inferred-axioms true \
  --output ${RELEASE} &> ${LOG}

printf "Reasoning using ${REASONER} ... DONE\n"

# report based on standard robot QA parameters
robot report \
  --input ${RELEASE} \
  --output ${LOG} &> ${LOG} | head -n 5

printf "Reporting ... DONE - Release notes can be found here: ${LOG}\n"
printf "\n***** USER INPUT NEEDED *****\n"

# clean up option, demand user input
while true; do
    read -p "Would you like to remove intermediate artifacts and EXIT the release process (y/n)?" yn
    case $yn in
        [Yy]* ) printf "Intermediate artifacts removed"; rm ${MERGED}; rm ${VERSIONED}; break;;
        [Nn]* ) printf "Intermediate artifacts not removed"; break;;
        * ) printf "Please answer yes (y) or no (n).";;
    esac
done

# ICO's purls resolve to src/ontology/ico_merged.owl, so it is
# necessary to place the updated owl file in this location.
printf "Release .. DONE\n \n***** IMPORTANT NOTE *****"
printf "\nPlease rename and move ${RELEASE} in the root directory to 'src/ontology/ico_merged.owl'\n"
