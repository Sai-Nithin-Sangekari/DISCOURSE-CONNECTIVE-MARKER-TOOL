import re
import sys
from googletrans import Translator 
def extract_foreign_word(output_lines):
    result = []
    hin_w=[]
    replace_words=[]
    for line in output_lines:
        match = re.search(r'([^(\s]+)\s*\(([^)]+)\)', line)
        if match:
            index_word = match.group(1)
            english_word = match.group(2)
            translator = Translator()
            translation = translator.translate(english_word, src='en', dest='hi')
            result.append(f"{index_word} \t {english_word} \t It is a foreign word.")
            hin_w.append(translation.text+"\tTranslated FW to hindi word.")
            new_line=line.replace(english_word,translation.text)

            matches = re.finditer(r'(\b\w+\b)\s*\((\b\w+\b)\)', new_line)
            for match in matches:
                word_before = match.group(1)
                word_after = match.group(2)

                if word_before == word_after:
                    new_line = new_line.replace(f"{word_before} ({word_after})", word_before)
            new_line=new_line.replace('(', '').replace(')', '')
            replace_words.append(new_line)
           

    return [result,hin_w,replace_words]

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
                results.extend("\n")
                results.extend(extract_foreign_word(output_lines)[2])
                with open("result.tsv", 'w') as output_tsv:
                    for result in results:
                        output_tsv.write(result + '\n')

            sys.exit(1)  