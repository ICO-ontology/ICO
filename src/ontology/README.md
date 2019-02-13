# Developer Read Me
This read me is designed for those intending to make contributions to ICO. The primary purpose of this document is to justify development decisions and provide information regarding the release process and repository structure. For content contributions, please see the [Contributing Guidelines](../../CONTRIBUTING.md).

## Temporary Release Process
Please see the [developer tools](../../tools/) for more details regarding specific development process. At the time of this writing (early 2019) there is not a need for a high development bar for ICO. As ICO moves toward an application space, this will need to change.

### The OWL files
1. The `ICO/src/ontology/ico-edit.owl` file is the file that should be edited.
1. When this file is stable, and all work has been verified, run `ICO/tools/temporary_release_process.sh`
1. Rename and move the resulting merged file to the correct file path.
1. Move previous OWL file to `releases/` as appropriate.   
1. Create a new release via GitHub releases.

##### Download:
* [http://purl.obolibrary.org/obo/ico.owl](http://purl.obolibrary.org/obo/ico.owl)
* This should point to: [https://raw.githubusercontent.com/ICO-ontology/ICO/master/src/ontology/ico_merged.owl](https://raw.githubusercontent.com/ICO-ontology/ICO/master/src/ontology/ico_merged.owl)

##### Relevant ICO websites:
* Home: [https://github.com/ICO-ontology/ICO](https://github.com/ICO-ontology/ICO)
* Tracker: [https://github.com/ICO-ontology/ICO/issues](https://github.com/ICO-ontology/ICO/issues)
* ICO ontology discussion mailing-list: [https://groups.google.com/forum/#!forum/ico-discuss](https://groups.google.com/forum/#!forum/ico-discuss)
* ICO discussion notes: https://docs.google.com/document/d/1j5HHtnm2nZn89O-EM1wsGjFTcoVMS_Ew8s4Z1uhfHsI/edit?usp=sharing

##### Browsing:
* Default browsing in Ontobee: [http://www.ontobee.org/ontology/ico](http://www.ontobee.org/ontology/ico)
* Browsing in NCBO BioPortal: [https://bioportal.bioontology.org/ontologies/ICO](https://bioportal.bioontology.org/ontologies/ICO)
