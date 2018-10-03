from __future__ import print_function # for 2.7 users
import rdflib
import argparse
import os
import subprocess
import owlready2 as ow
import re

def makeFOL(file):

    # used to identify the file queried for the output dataset name
    source_file = os.path.basename(file)
    base = os.path.splitext(source_file)[0]

    # load owlready graph object in order to print EquivalenceAxioms
    onto = ow.get_ontology(str("file://" + source_file)).load()

    # OWL file variables
    OWL_file_in = str(file)
    OWL_file_out = str(base) + '_merged.owl'

    # merge the ontology to get all subclass axioms
    robotMerge = 'robot merge --input ' + OWL_file_in + ' --output ' + OWL_file_out
    process = subprocess.Popen(robotMerge.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # rdflib naming conventions to query set-up
    g = rdflib.Graph()
    g = g.parse(OWL_file_out)

    # # for quick testing non-merged OWL file
    # # TO REMOVE
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

        # different ontologies for separate files
        shortIRI = str(row[0]).rsplit('/', 1)[-1]
        output = str('FOL_output/' + shortIRI.rsplit('_', 1)[0] + '_output.txt')
        axiom_output = str('FOL_output/AXIOMS_output.txt')

        # print humand readable comments and PURL in proven9 syntax
        print("%  " + str(row[1]) + " is subclass of " + \
            str(row[3]), file=open(output, "a"))
        print("%  entity: " + str(shortIRI), file=open(output, "a"))

        # print EquivalenceAxiom if they exist
        if row[4] != None:
            print("% Has EquivalenceAxiom! ", file=open(output, "a"))
            print("% Check FOL_output/AXIOMS_output.txt for EquivalenceAxiom", file=open(output, "a"))

        print("all x (" + str(row[1]).title().replace(" ","") + "(x) -> " + \
            str(row[3]).title().replace(" ","") + "(x)). \n", file=open(output, "a"))

        ## WARNING: need to check against empty list []
        ## not sure if checking for bnodes is good enough

        # some entities don't have labels, handle
        try:
            # search for purl to get EquivalenceAxioms
            search = str("*" + str(row[2]) + "*")
            ow_IRI = onto.search_one(iri=search)
            entity_name = str(ow_IRI.label)
            axiom = str(ow_IRI.equivalent_to)

            # remove brackets from axiom to parse individual purls
            axiom = axiom.replace("[", "").replace("]", "")

            # turn into a list
            axiom = axiom.split()

            # only print axioms that exist
            if axiom != []:

                # print entity and axiom
                print('ENTITY: ' + entity_name + ', ' + str(ow_IRI.name), file=open(axiom_output, "a"))
                print("AXIOM: " + str(axiom), file=open(axiom_output, "a"))

                # iterate through the axiom string to find rdfs:labels
                for item in axiom:

                    # search for each component
                    sub_axiom_search = str("*" + str(item) + "*")
                    sub_axiom_search = sub_axiom_search.replace("obo.", "")
                    sub_axiom_IRI = onto.search_one(iri=sub_axiom_search)

                    # get human readable label and purl for components
                    if sub_axiom_IRI != None:
                        sub_axiom_name = str(sub_axiom_IRI.label)
                        print(sub_axiom_IRI.name, sub_axiom_name, file=open(axiom_output, "a"))

                # newline for readablility
                print("\n", file=open(axiom_output, "a"))

        # catch entities without labels
        except AttributeError:
            continue

    # clean up the dir
    remove_merged = "rm " + OWL_file_out
    process = subprocess.Popen(remove_merged.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    print("Files printed to FOL_Output/ directory.")

if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='Extract terms from local OWL file')
    parser.add_argument("file", help="File to query")
    args = parser.parse_args()

    # run puppy, run
    makeFOL(args.file)
