import rdflib
import pandas as pd
import argparse
import os


# full-query extract function
def full_extract(file):
    # to store results and output to .csv
    ontoframe = pd.DataFrame()

    # used to identify the file queried in the output dataset
    source_file = os.path.basename(file)
    base = os.path.splitext(source_file)[0]

    # rdflib naming converntions
    g = rdflib.Graph()
    g = g.parse(file)

    # gather results from rdflib query
    qresults = g.query(
        """
        SELECT ?entity ?elabel ?definition
        WHERE {
          ?entity rdfs:label ?elabel .
          OPTIONAL { ?entity obo:IAO_0000115 ?definition }
        }
        GROUP BY ?entity ?elabel ?definition
        """
    )

    lengthCheck = g.query(
        """
        SELECT ?entity
        WHERE {
          ?entity rdfs:label ?elabel .
        }
        """
    )

    print("Results Returned by Query: " + str(len(qresults)))
    print("Results Returned by Check: " + str(len(lengthCheck)))
    if len(qresults) != len(lengthCheck):
        print("WARNING: The results do not match.")
        print("Please take a close look at the IAO_0000115 annotation property in the original OWL file.")
    else:
        print("Results match. Extracting.....")

    # count to maintain dynamic indexing of dataframe
    count = 1

    # iterate through query result and place in dataframe
    for row in qresults:
        ontoframe.loc[count, 'PURL'] = str(row[0]).rsplit('/', 1)[-1]
        ontoframe.loc[count, 'Term Label'] = row[1]
        ontoframe.loc[count, 'Definiton'] = str(row[2])
        count = count + 1

    # output dataframe to .csv
    ontoframe.to_csv(str(base) + "_extractresults.csv")
    print('EXTRACT FILE: ' + str(base) + "_extractresults.csv")
    return ontoframe


if __name__ == "__main__":

    # parse command-line args
    parser = argparse.ArgumentParser(description='Extract terms from local .OWL file')
    parser.add_argument("file", help="File to query")
    args = parser.parse_args()

    full_extract(args.file)
