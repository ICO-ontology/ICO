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

    # for quick testing - TO REMOVE
    # g = g.parse(file)

    # gather results from rdflib query
    qresults = g.query(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX obo: <http://purl.obolibrary.org/obo/>

        SELECT DISTINCT ?entity ?label ?parent ?parentLabel ?equivalenceAxiom ?subclassAxiom
        WHERE {

            ?entity rdfs:subClassOf ?parent .
            ?parent rdfs:label ?parentLabel .
    		?class rdfs:subClassOf ?parent .
    		?class rdfs:label ?label .

            OPTIONAL { ?class owl:equivalentClass ?equivalenceAxiom }
            OPTIONAL { ?class rdfs:subClassOf ?subclassAxiom }

            FILTER (!regex(str(?label), "^obsolete"))

                }
        ORDER BY DESC(?entity)
        """
        )

    # print all classes with import closure
    for row in qresults:

        # gather different ontologies for separate files
        shortIRI = str(row[0]).rsplit('/', 1)[-1]
        output = str('FOL_output/' + shortIRI.rsplit('_', 1)[0] + '_output.txt')

        # print all closure
        print("%  " + str(row[0]), file=open(output, "a"))
        print("%  source ontology: " + shortIRI.rsplit('_', 1)[0], file=open(output, "a"))
        print("%  entity: " + str(row[0]), file=open(output, "a"))
        print("%  label: " + str(row[1]), file=open(output, "a"))
        print("%  parent: " + str(row[2]), file=open(output, "a"))
        print("%  parentLabel: " + str(row[3]), file=open(output, "a"))
        print("%  EquivalenceAxiom: " + str(row[4]), file=open(output, "a"))
        print("%  SubclassAxiom: " + str(row[4]) + '\n', file=open(output, "a"))
        print("all x (" + str(row[1]).replace(" ", "_") + "(x) -> " + str(row[3]).replace(" ", "_") + "(x)). \n", file=open(output, "a"))

    print("Files printed to FOL_output/ directory.")

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
