# List of to-dos for ICO and RUBRIC

## Term Additions:
1. We have 'specimen' from OBI_0100051, but if we could get 'DNA specimen' or 'biological specimen' that'd be great
1. We have 'repository of documents' (ICO_0000118) but if we could get 'biorepository' either from an OntoBee search or we create it that'd be great
1. I see a bunch of terms under "Needs review," but I think we will want to spell out some more directives (these are all used on my slides, but I think we should combine them), as I believe they belong in either ICO or RUBRIC's ontology (prolly ICO?):
1. Genetic testing directive
1. Directive regarding specimen
1. Directive regarding biological specimen
1. Directive regarding DNA specimen
1. Directive regarding research on specimen
1. We don't have 'medical procedure', and I think we should be able to get it in (OntoBee?) just as we have OBI terms 'investigation' and 'human research investigation'
1. Terms from OMRSE:
1. 'age measurement datum' OMRSE_00000088
1. 'ethnic identity datum' OMRSE_00000100
1. 'gender identity datum' OMRSE_00000133
1. 'female gender identity datum' OMRSE_00000138 (optional)
1. 'male gender identity datum' OMRSE_00000141 (optional)
1. 'racial identity datum' OMRSE_00000098
1. I see you have 'health information entity' (ICO_0000101) and 'medical record' (OMIABIS_0001026), but I don't see 'electronic health record'
1. http://purl.obolibrary.org/obo/OBI_0500028
1. http://purl.obolibrary.org/obo/OBI_0001755

## Future Goals:
1. SEE OBI DICEs
1. Accreditation?
1. 'act of exemption'
1. 'vunerable individual role' and 'vunerabilty' need annotation properties explaining usage
1. ICO or RUBRIC needs to have 'material transfer agreements' and perhaps processes of material transfer
1. RUBRIC: 'Answer directive' label to 'user-input'
1. RUBRIC: Every conditional will have a trigger condition description ('if') and a consequent directive ('then').
1. Medical procedure should be 'research procedure' and 'clinical procedure'
1. Planned and Actual study duration measurements are different
1. Different states for informed consent forms
1. pre-approval vs approved vs filled out (where does each class fall?)
1. Informing does not have to be human-human. I can learn from a book. New class?
1. RUBRIC: specimen use/data use
1. Are these social acts?
1. 'canceling a permission'
1. 'declining to provide consent'
1. 'consenter' and 'agent' not the same superclass (per JV's email)?
1. short form consent?
1. add [principal investigator role](http://purl.obolibrary.org/obo/OBI_0000103) from OBI
1. due we need different levels between PI and institution?
1. directive regarding research of biospecimens
1. genetic testing directive
1. genetic testing procedure?
1. excess material?
1. datetime of consent?

## Development Items
1. Import RO temporal relations
1. add RO to imports
1. RUBRIC: For all CCO terms, add the license info in an annotation property
1. robot testing process
1. Add tooling to spell check all annotations
1. Add tooling to detect definitions have 'genus - differentia' form
1. Robot reasoner to check axiomatic consistency
1. Tooling tooling Resolve synonyms:
1. Known issues: permissions/permitee, subject/person/agent/patient
1. FOL is consistent
1. new PURLS resolve in OBO
1. 'research study' should be replaced by OBI: investigation
1. create ontology publishing process
