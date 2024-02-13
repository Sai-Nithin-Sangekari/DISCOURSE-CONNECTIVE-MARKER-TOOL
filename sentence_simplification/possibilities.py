import sys
import re

def extract_inside_outside(sentences):
    inside_parenthesis = []
    outside_parenthesis = []

    for sentence in sentences:
        matches = re.findall(r'\((.*?)\)', sentence)
        
        if matches:
            inside_parenthesis.extend(matches)
            cleaned_sentence = re.sub(r'\(.*?\)', '', sentence).strip()
            outside_parenthesis.append(cleaned_sentence)
        else:
            outside_parenthesis.append(sentence.strip())

    return inside_parenthesis, outside_parenthesis

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]

        with open(input_filename, 'r', encoding='utf-8') as input_file:
            sentences = input_file.readlines()

        # Extract inside and outside parenthesis
        inside, outside = extract_inside_outside(sentences)

        # Write to files
        with open('f1.txt', 'w', encoding='utf-8') as f1:
            f1.write('\n'.join(outside))

        with open('f2.txt', 'w', encoding='utf-8') as f2:
            f2.write('\n'.join(inside))
    else:
        print("Please provide the input file as a command-line argument.")
