from __future__ import print_function # for 2.7 users
import rdflib
import argparse
import os
import subprocess

def makeFOL(file):
    # used to identify the file queried for the output dataset name
    source_file = os.path.basename(file)
    base = os.path.splitext(source_file)[0]

    file_in = str(file)
    file_out = str(base) + '_merged.owl'

    # merge the ontology to get all subclass axioms
    robotMerge = 'robot merge --input ' + file_in + ' --output ' + file_out
    process = subprocess.Popen(robotMerge.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # rdflib naming conventions to query set-up
    g = rdflib.Graph()
    g = g.parse(file_out)

    # gather results from rdflib query
    qresults = g.query(
        """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX obo: <http://purl.obolibrary.org/obo/>

            SELECT ?superClass ?label ?entity ?elabel
            WHERE {
              ?entity rdfs:subClassOf ?superClass .
              ?superClass rdfs:label ?label .
              ?entity rdfs:label ?elabel .
            }
        """
        )

    # print all classes (no import closure) in FOL format: all x (Continuant(x) -> Entity(x)).
    for row in qresults:
        print(str(row[2]).rsplit('/', 1)[-1] + ": all x (" + str(row[3]) + "(x) -> " + str(row[1]) + "(x)). \n", file=open("output_FOL.txt", "a"))

    print("File output printed to: output_FOL.txt in current directory")

    # clean up the dir
    remove_merged = "rm " + file_out
    process = subprocess.Popen(remove_merged.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='Extract terms from local .OWL file')
    parser.add_argument("file", help="File to query")
    args = parser.parse_args()

    # run puppy, run
    makeFOL(args.file)
