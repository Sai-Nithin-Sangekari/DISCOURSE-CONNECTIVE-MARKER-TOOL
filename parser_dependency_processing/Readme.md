## Assumptions -
- Input file can have many sentences
- Input file can have blank lines in between two sentences
- Input sentences can also be in wx convention
- Input sentences might end in fullstop or poornaviram
- Each sentence is separated by a newline character

## File purpose - 
- "input.txt" - Input sentences (one or more sentences)
- "output.txt" - Final output of the program. All the parser outputs (separated by an extra newline character) after processing their dependency relations
- "inter_parser_input.txt" - input file (one sentence at a time) to isc-tagger command
- "inter_parser_output.txt" - output file (parser output) of isc-tagger command
- "consolidated_parser_output.txt" - All the intermediate parser outputs are appended in this file

## Prerequisite - 
- The isc tagger should be set up in the same project
- Update the file paths in CONSTANTS.py as per your directory

## Steps of execution -
- Run this script by executing dependency.py file
