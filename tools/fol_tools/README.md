# First Order Logic Tools
The `Build_FOL.py` tool is a command line python (3) script used to extract terms and 'is_a' relations from an `.owl` file (including import closure) and format the output for [prover9](https://www.cs.unm.edu/~mccune/mace4/) in order to check consistency.

The output for `ico.owl` and imported ontologies has been moved to `FOL_Output/`.

## Note on Axioms
Ideally this tool would also create first order logic expressions for subclass and equivalence axioms. At this point in time this is not supported. 
