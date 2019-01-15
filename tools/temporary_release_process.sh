#!/usr/bin/env bash

# Requires robot to be installed
command -v robot 1> /dev/null 2>&1 || \
  { echo >&2 "robot required but it's not installed.  Aborting."; exit 1; }

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

# Get path, set variables
SCRIPT_DIR=$(dirname "${THIS_SCRIPT}")
ICO="${SCRIPT_DIR}/../src/ontology/ico-edit.owl"
LOG="${SCRIPT_DIR}/release_notes/`date '+%Y-%m-%d'`.txt"

MERGED="${SCRIPT_DIR}/intermediate_owl_artifacts/ICO-MERGED-`date '+%Y-%m-%d'`.owl"
VERSIONED="${SCRIPT_DIR}/intermediate_owl_artifacts/ICO-VERSIONED-`date '+%Y-%m-%d'`.owl"
RELEASE="ICO-RELEASE-`date '+%Y-%m-%d'`.owl"

# merge
robot merge \
  --input ${ICO} \
  --include-annotations true \
  --output ${MERGED}

echo "MERGE DONE."
echo ""

# add date to IRI version
robot annotate \
  --input ${MERGED} \
  --ontology-iri "http://purl.obolibrary.org/obo/ICO.owl" \
  --version-iri "http://purl.obolibrary.org/obo/`date '+%Y-%m-%d'`/ico.owl" \
  --output ${VERSIONED}

echo "VERSIONING DONE."
echo ""

# include reasoned triples
robot reason \
	--input ${VERSIONED} \
  --reasoner ELK \
  --annotate-inferred-axioms true \
  --output ${RELEASE} >> ${LOG}

echo "REASONING DONE."
echo ""

# run robot report, topsheet to stdout and details to file
robot report --input ${RELEASE} --output ${LOG} | head -n 5

echo ""
echo "REPORTING DONE."
echo "Release notes can be found here: ${LOG}"

echo ""

# clean up
while true; do
    read -p "Would you like to remove intermediate artifacts (y/n)?" yn
    case $yn in
        [Yy]* ) rm ${MERGED}; rm ${VERSIONED} break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes (y) or no (n).";;
    esac
done

echo "RELEASE DONE."
