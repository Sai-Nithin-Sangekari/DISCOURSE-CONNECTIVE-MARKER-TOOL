import re
import sys
from googletrans import Translator 


def same_id_check(output_lines):
    result = []
    ids_by_sentence = {}
    sentences_by_id = {}

    for line in output_lines:
        parts = line.split()

        sentence_id = parts[0]
        sentence = ' '.join(parts[3:-1])

        if sentence not in ids_by_sentence:
            ids_by_sentence[sentence] = [sentence_id]
        else:
            ids_by_sentence[sentence].append(sentence_id)
        if sentence_id not in sentences_by_id:
            sentences_by_id[sentence_id] = [sentence]
        else:
            sentences_by_id[sentence_id].append(sentence)

    for sentence_id, sentences in sentences_by_id.items():
        if len(set(sentences)) > 1:
            result.append(sentence_id + "\tSame ID is present.")

    return result

def space_check(output_lines):
    result = []

    for line in output_lines:
        pattern = re.compile(r'\b\d+[a-zA-Z](?!\s{2,})')

        matches = pattern.findall(line)

        for match in matches:
            result.append(f"{match} \tdoes not have at least 2 spaces after the identifier.")

    return result

def end_marker(output_lines):
    result = []

    for line in output_lines:
        s_id = line.split(" ")[0]
        stripped_line = line.rstrip()
        if stripped_line[-1] in ["।","?","!"]:
            continue
        else:
            result.append(s_id + "\tNot ending with marker")

    return result

def only_one(output_lines):
    result = []

    for line in output_lines:
        s_id = line.split(" ")[0]
        end_markers = ['?', '!', '।']
        count = sum(line.count(marker) for marker in end_markers)
        if count > 1:
            result.append(s_id + "\tError: More than one end marker found at the end of the sentence.")

    return result

def extract_foreign_word(output_lines):
    result = []
    hin_w = []

    for line in output_lines:
        match = re.search(r'([^(\s]+)\s*\(([^)]+)\)', line)
        if match:
            index_word = match.group(1)
            english_word = match.group(2)
            translator = Translator()
            translation = translator.translate(english_word, src='en', dest='hi')
            result.append(f"{index_word}\t{english_word}\tIt is a foreign word.")
            hin_w.append(f"{translation.text}\tTranslated FW to Hindi word")

    return [result, hin_w]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]

        with open(input_filename, 'r') as output_file:
            output_lines = output_file.readlines()
            results = []

            results.extend(same_id_check(output_lines))
            results.extend(space_check(output_lines))
            results.extend(end_marker(output_lines))
            results.extend(only_one(output_lines))
            results.sort(key=lambda x: (int(re.search(r'\d+', x).group()), x))
            results.extend(extract_foreign_word(output_lines)[0])
            results.extend(extract_foreign_word(output_lines)[1])

            with open("output_store.tsv", 'w') as output_tsv:
                # Adding header
                output_tsv.write("Index\tEnglish Word\tResult\n")
                for result in results:
                    output_tsv.write(result + '\n')

        sys.exit(1)
