#!/bin/bash

## This script greps a file for the PURLS and outputs
## them to a new file
echo ""
echo "######################### owl:Class #########################"
echo ""
result=$(grep 'owl:Class rdf:about' ${1} | cut -d '"' -f2)
printf "${result}" 
echo ""

echo ""
echo "######################### owl:ObjectProperty #########################"
echo ""
result=$(grep 'owl:ObjectProperty rdf:about' ${1} | cut -d '"' -f2)
printf "${result}" 
echo ""

echo ""
echo "######################### owl:AnnotationProperty #########################"
echo ""
result=$(grep 'owl:AnnotationProperty rdf:about' ${1} | cut -d '"' -f2)
printf "${result}" 
echo ""
