import re
import sys
from googletrans import Translator
from indic_transliteration import sanscript

def convert_to_hindi(word):
    hindi_word = sanscript.transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI)
    return hindi_word

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
            hindi_translation = convert_to_hindi(english_word)
            result.append(f"{index_word} \t {english_word} \t It is a foreign word.")
            
            hin_w.append(f"{index_word} \t {hindi_translation} \t Translated FW to Hindi.")
   
    return [result, hin_w]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]

        with open(input_filename, 'r') as output_file:
            output_lines = output_file.readlines()
            results = []

            results.sort(key=lambda x: (int(re.search(r'\d+', x).group()), x))
            results.extend(extract_foreign_word(output_lines)[0])
            results.extend("\n")
            results.extend(extract_foreign_word(output_lines)[1])

            with open("store_transword.tsv", 'w') as output_tsv:
                output_tsv.write("Index\tEnglish Word\tResult\n")
                for result in results:
                    output_tsv.write(result + '\n')

        sys.exit(1)