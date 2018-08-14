from __future__ import print_function # for 2.7 users
import rdflib
import argparse
import os


# full-query extract function
def makeFOL(file):
    # used to identify the file queried for the output dataset name
    source_file = os.path.basename(file)
    base = os.path.splitext(source_file)[0]

    # rdflib naming conventions
    g = rdflib.Graph()
    g = g.parse(file)

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

if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='Extract terms from local .OWL file')
    parser.add_argument("file", help="File to query")
    args = parser.parse_args()

    # run puppy, run
    makeFOL(args.file)
