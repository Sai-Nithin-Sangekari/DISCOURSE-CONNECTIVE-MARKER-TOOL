import string
import CONSTANTS
import sys
import re
import os
from wxconv import WXC

def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'[{logtype}] : {mssg}')
    #if logtype == 'ERROR':

def read_input(file_path):
    '''Returns dict with key - sentence_id and value - sentence for data given in file'''

    log(f'File ~ {file_path}')
    try:
        with open(file_path, 'r') as file:
            input_data = {}
            lines = file.readlines()
            for i in range(len(lines)):
                lineContent = lines[i].strip()
                if lineContent == '':
                    break
                else:
                    # sentence_info = lineContent.split('\t')
                    sentence_info = lineContent.split(' ', 1)
                    key = sentence_info[0]
                    value = sentence_info[1].strip()
                    input_data[key] = value
            log('File data read.')
    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return input_data


def clean(word, inplace=''):
    """
    Clean concept words by removing numbers and special characters from it using regex.
    >>> clean("kara_1-yA_1")
    'karayA'
    >>> clean("kara_1")
    'kara'
    >>> clean("padZa_1")
    'pada'
    >>> clean("caDZa_1")
    'caDa'

    """
    newWord = word
    if 'dZ' in word:  # handling words with dZ/jZ -Kirti - 15/12
        newWord = word.replace('dZ', 'd')
    elif 'jZ' in word:
        newWord = word.replace('jZ', 'j')
    elif 'DZ' in word:
        newWord = word.replace('DZ', 'D')

    #clword = re.sub(r'[^a-zA-Z]+', inplace, newWord)
    return newWord

def validate_sentence(sentence):
    #sentence not empty - return True
    #Regular expression pattern to match any non-digit character
    pattern = r'\D'
    if not len(sentence) or not re.search(pattern, sentence):
        return False

    return True

def sanitize_input(sentence):

    wx_format = WXC(order="utf2wx", lang="hin")
    generate_wx_text = wx_format.convert(sentence)
    clean_wx_text = ""
    tokens = generate_wx_text.strip().split()
    for word in tokens:
        clean_wx_text = clean_wx_text + clean(word) + " "

    clean_wx_text.strip()
    hindi_format = WXC(order="wx2utf", lang="hin")
    clean_hindi_text = hindi_format.convert(clean_wx_text)

    return clean_hindi_text

def write_output(dictionary, file_path):
    with open(file_path, 'w') as file:
        for key, value in dictionary.items():
            index = 'a'
            line = f"{key}: "
            for i in range(len(value)):
                item = value[i]
                letter = string.ascii_lowercase[i]
                if len(item) > 0 :
                    line = line + "(" + item + ":" + key + letter + ")" + " "
            line += '\n'
            file.write(line)
    log("Output file written successfully")

def is_prev_word_verb(parser_output, index):
    try:
        with open(parser_output, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if i == index:
                    lineContent = lines[i].strip().split()
                    if len(lineContent) > 0 and (lineContent[1] == 'VM' or lineContent[1] == 'VAUX'):
                        return True

    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return False

def get_word_index(words, value):
    index = -1
    for i in range(len(words)):
        if words[i] == value:
            index = i
            break
    return index

def breakPairConnective(sentence):
    # This function return list of sentences if a paired connective is found else returns an empty list
    simpler_sentences = []
    BREAK_SENTENCE = False
    # Tokenize the sentence by splitting it into words
    tokens = sentence.split()
    # Iterate through the tokens to find connectives and split the sentence
    for i in range(len(tokens)):
        token = tokens[i]
        # Check if the token is a paired-connective
        if token in CONSTANTS.COMPLEX_CONNECTIVES:
            pair_value_lst = CONSTANTS.COMPLEX_CONNECTIVES[token]
            for pair_value in pair_value_lst:
                if pair_value in sentence:
                    pair_value = pair_value.strip().split()[0]
                    index_of_pair_value = get_word_index(tokens, pair_value)
                    if not (index_of_pair_value == -1):
                        get_parser_output(sentence)
                        if is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, index_of_pair_value - 1):
                            tokens.pop(i)
                            index_of_pair_value = index_of_pair_value - 1
                            sent1 = tokens[:index_of_pair_value]
                            sent2 = tokens[index_of_pair_value:]
                            simpler_sentences.append(" ".join(sent1))
                            simpler_sentences.append(" ".join(sent2))
                            BREAK_SENTENCE = True
                            break
            if BREAK_SENTENCE:
                break
    return simpler_sentences


def breakSimpleConnective(sentence):
    # This function return list of sentences if a simple connective is found else returns an empty list
    simpler_sentences = []
    # Tokenize the sentence by splitting it into words
    tokens = sentence.split()
    for i in range(len(tokens)):
        token = tokens[i]
        # 'नहीं तो' is simple connective
        if token == 'नहीं':
            following_index = get_word_index(tokens, 'तो')
            if following_index == i+1:
                token = 'नहीं तो'

        # Check if the token is a connective
        if token in CONSTANTS.SIMPLE_CONNECTIVES:
            get_parser_output(sentence)
            if is_prev_word_verb(CONSTANTS.PARSER_OUTPUT, i - 1):
                sent1 = tokens[:i]
                sent2 = tokens[i:]
                simpler_sentences.append(" ".join(sent1))
                simpler_sentences.append(" ".join(sent2))
                break

    return simpler_sentences

def write_input_in_parser_input(file_path, sentence):
    with open(file_path, 'w') as file:
        file.truncate()
        file.write(sentence)
        file.close()

def get_parser_output(sentence):
    parser_input_file = CONSTANTS.PARSER_INPUT
    write_input_in_parser_input(parser_input_file, sentence)
    with open(CONSTANTS.PARSER_OUTPUT, 'w') as file:
        file.truncate()
    os.system("isc-tagger -i p_parser_input.txt -o p_parser_output.txt")

def breakAllPairedConnective(sentence, allPairedConnectiveList):
    simpler_sentences = breakPairConnective(sentence)
    if len(simpler_sentences) == 0:
        allPairedConnectiveList.append(sentence)
        return

    for s in simpler_sentences:
        breakAllPairedConnective(s, allPairedConnectiveList)

    return

def breakAllSimpleConnective(sentence, allSimpleConnectiveList):
    simpler_sentences = breakSimpleConnective(sentence)
    if len(simpler_sentences) == 0:
        allSimpleConnectiveList.append(sentence)
        return

    for s in simpler_sentences:
        breakAllSimpleConnective(s, allSimpleConnectiveList)

    return

if __name__ == '__main__':
    input_data = read_input(CONSTANTS.INPUT_FILE)
    output_data = {}

    for key, value in input_data.items():
        if validate_sentence(value):
            value = sanitize_input(value)
            # First break the sentence by pair connectives
            allPairedConnectiveList = []
            breakAllPairedConnective(value, allPairedConnectiveList)
            allSimpleConnectiveList = []
            for s in allPairedConnectiveList:
                breakAllSimpleConnective(s, allSimpleConnectiveList)
        else:
            allSimpleConnectiveList = ['Error']

        output_data[key] = allSimpleConnectiveList
    write_output(output_data, CONSTANTS.OUTPUT_FILE)

