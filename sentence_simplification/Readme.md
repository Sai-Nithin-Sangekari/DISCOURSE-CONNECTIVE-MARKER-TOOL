## Assumptions -
- Input file has unique sentence id for each input
- Input file has - sentence_id - space separated - sentence
- Input file can have many sentences
- Input sentences are in hindi language

## Steps of execution -
- Run this script by executing sentence_subparts.py file.
- Prerequisite to run this script is sentence_input.txt file, which should be present in same path with list of input sentences.
- Each input line should have format "sentence_id sentence". Please refer sample input.txt file from this repo.
- Output will be generated as sentence_output.txt file
- The isc parser should be set up in the same project
- Update the file paths in CONSTANTS.py as per your directory

## Notes - 
- script takes some time to run - as for every sentence parser output is fetched

## Next version Todos - 
- Optimize the parser output calls
- For input sentences with a connective but, if the prev term of connective is not a VM or VAUX we flag the sentence for manual evaluation
