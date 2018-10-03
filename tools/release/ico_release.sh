#!/usr/bin/bash

# Requires robot to be installed locally
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

# Get path to the scripts directory.
SCRIPT_DIR=$(dirname "${THIS_SCRIPT}")


# variables' set here
# ICO="${SCRIPT_DIR}/../ico.owl"
# LOG="${SCRIPT_DIR}/ico_log.txt"

# add date to IRI version
robot annotate \
  --input ${ICO} \
  --ontology-iri "http://purl.obolibrary.org/obo/ico.owl" \
  --version-iri "http://purl.obolibrary.org/obo/`date '+%Y-%m-%d'`/ico.owl" \
  --output ico-updated.owl

# run robot report, results to stdout and some to file
robot report --input ${ICO} --output ${LOG} | head -n 5

echo "Robot results can be seen here: ${LOG}"

# update dictionary as part of release process
${SCRIPT_DIR}/make-dict.sh

# Final check before release
while true; do
    read -p "Are you ready to release this version? (y/n)" yn
    case $yn in
        [Yy]* ) rm ico.owl; mv ico-updated.owl ico.owl; echo 'RELEASE COMPLETE. You can commit and '; break;;
        [Nn]* ) rm ico-updated.owl; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
