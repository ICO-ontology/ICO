import pandas as pd
import argparse
import os
from xml.etree import ElementTree as ET
from tabulate import tabulate

# function call to compare user inputs and
# generate a new ontology file and a changeLog.csv
def revise_ontology(ontology, revisionsFile):

    # used to rename the output into current dir
    ontoFile = os.path.abspath(ontology)
    ontoFileName = os.path.basename(ontology)
    ontoBase = os.path.splitext(ontoFileName)[0]

    # set up xml parser
    tree = ET.parse(ontology)
    root = tree.getroot()

    # define elements needed to make the change
    rdf_class = root.findall('{http://www.w3.org/2002/07/owl#}Class')
    about = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
    rdfs_label = '{http://www.w3.org/2000/01/rdf-schema#}label'
    IAO_definition = '{http://purl.obolibrary.org/obo/}IAO_0000115'

    # dataframe to track changes
    frame = pd.DataFrame()

    # index for data frame
    index = 0

    # expect changes in .csv form
    # need to update the handling to demand a specific format
    try:
        revisionsFrame = pd.read_csv(revisionsFile)
    except:
        print("ERROR: there was an error with the revision file.")

    # iterate through xml tree find matching purls
    for flag in rdf_class:

        for index, row in revisionsFrame.iterrows():

            # only make changes to the purls listed in the file
            if row['PURL'] == str(list(flag.attrib.values())[0]).rsplit('/', 1)[-1]:

                # add the purl to the frame
                frame.loc[index, 'Purl'] = str(list(flag.attrib.values())[0]).rsplit('/', 1)[-1]

                # find rdfs labels and replace with file contents
                for lb in flag.findall(rdfs_label):

                    # record before changes
                    frame.loc[index, 'Old Label'] = str(lb.text)

                    # make changes
                    lb.text = row['Term Label']

                    # record after changes
                    frame.loc[index, 'New Label'] = str(lb.text)

                # find IAO_0000115 defs and replace with file contents
                for df in flag.findall(IAO_definition):

                    # record before changes
                    frame.loc[index, 'Old Definition'] = str(df.text)

                    # make changes
                    df.text = row['Definition']

                    # record after changes
                    frame.loc[index, 'New Definition'] = str(df.text)

                # increment index
                index += 1

    # save changes to file
    print(str(len(frame)) + " changes made and logged in " + str(ontoBase) + '_revision_log.csv')
    frame.to_csv(str(ontoBase) + '_revision_log.csv')

    # save xml object as new file
    print('New ontology save in ' + ontoBase + '_revised.owl')
    tree.write(ontoBase + '_revised.owl')


if __name__ == "__main__":
    print('Starting...')

    # parse command-line args
    parser = argparse.ArgumentParser(description='Extract terms from local .OWL file')
    parser.add_argument("file", help="File to query")
    parser.add_argument('csv', help='Revisions csv file')
    args = parser.parse_args()

    # call
    revise_ontology(args.file, args.csv)
