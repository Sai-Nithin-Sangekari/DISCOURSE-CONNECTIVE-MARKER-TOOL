import os
import sys
import CONSTANTS
from isc_parser import Parser
parser = Parser(lang='hin')
from wxconv import WXC

verb_lst = ['bol', 'kah', 'pUC']
we_lst = ['wA', 'wI', 'we']
hue_lst = ['huA', 'huI', 'hue']
def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'[{logtype}] : {mssg}')
    if logtype == 'ERROR':
        sys.exit()

def get_dependency_by_index(output, index):
    dep = ''
    for row in output:
        if len(row) == 10 and row[0] == index :
            dep =  row[7]
            break
    return dep

def get_term_by_index(output, index):
    term = ''
    for row in output:
        if len(row) == 10 and row[0] == index:
            term = row[1]
            break
    return term

def check_term_ending_with(term, end_term):
    for ele in end_term:
        if term.endswith(ele):
            return True
    return False

def get_tag_by_index(output, index):
    tag = ''
    for row in output:
        if len(row) == 10 and row[0] == index:
            tag = row[3]
            break
    return tag

def get_pointing_index(output, index):
    ptr_index = -1
    for row in output:
        if len(row) == 10 and row[0] == index:
            ptr_index = row[6]
            break
    return ptr_index


def is_followed_by(output, index, term):
    match_words = term.strip().split(' ')
    count = len(match_words)
    itr = 0
    curr_index = index
    for word in match_words:
        next_word = get_term_by_index(output, curr_index+1)
        pointing_index = get_pointing_index(output, curr_index+1)
        next_word_dep = get_dependency_by_index(output, index+1)

        if next_word == word and index == pointing_index and next_word_dep == 'lwg__psp':
            curr_index = curr_index + 1
            itr = itr + 1
            if count == itr:
                return True

    return False

def fetch_VM_info(output, VM_1_index, VM_2_index):
    VM_1_term = output[VM_1_index - 1]
    VM_2_term = output[VM_2_index - 1]
    head_VM = []
    child_VM = []
    for row in output:
        if row[3] == 'CC':
            CC_index = row[0]
            CC_term = output[CC_index - 1]
            CC_term_head = CC_term[6]

            if CC_term_head == VM_1_index:
                head_VM = VM_1_term
                child_VM = VM_2_term
            elif CC_term_head == VM_2_index:
                head_VM = VM_2_term
                child_VM = VM_1_term

            if len(head_VM) and len(child_VM):
                break

    return head_VM, child_VM

def fetch_CC_info(output, CC_index):
# return CC_info other than that on CC_index
    for row in output:
        if row[0] != CC_index and row[3] == 'CC':
            return row

    return []

def process_relation(output):
    dependency_mapper = {
        "r6-k1": "k1",
        "r6-k2": "k2",
        "r6v": "rhh",
        "k1inv": "rvks",
        "k2inv": "rbks",
        "adv": "krvn",
        "rs": "re",
        "jjmod": "intf",
        "jjmod__intf": "intf",
        "nmod__k1inv": "rvks",
        "nmod__k2inv": "rbks",
        "nmod":"mod"
    }

    #to fetch necessary rule info in first iteration
    words = []
    verbs = []
    k2exists = False
    k2gexists = False
    k4exists = False
    k5exists = False
    CC_exists = False
    head_verb_exists = False
    VM_1_exists = False
    VM_2_exists = False
    CC_count = 0

    for row in output:
        if len(row) > 0:
            if row[7] == 'k2':
                k2exists = True
                k2_head_verb_index = row[6]
                k2_index = row[0]
            elif row[7] == 'k2g':
                k2gexists = True
                k2g_head_verb_index = row[6]
                k2g_index = row[0]
            elif row[7] == 'main':
                head_verb_exists = True
                head_verb_index = row[0]
            elif row[7] == 'k4':
                k4exists = True
                k4_index = row[0]
            elif row[7] == 'k5':
                k5exists = True
                k5_index = row[0]
            if row[3] == 'CC':
                CC_count = CC_count + 1
            if not CC_exists and row[3] == 'CC':
                CC_exists = True
                CC_index = row[0]
            elif row[3] == 'VM' and not VM_1_exists:
                VM_1_exists = True
                VM_1_index = row[0]
            elif row[3] == 'VM' and VM_1_exists and not VM_2_exists:
                VM_2_exists = True
                VM_2_index = row[0]

    #For CC and 2 VM processing
    if CC_exists and VM_1_exists and VM_2_exists:
        CC_info = output[CC_index - 1]
        while CC_count and len(CC_info):
            CC_index = CC_info[0]
            CC_term = CC_info[1]
            CC_dep = CC_info[7]
            if CC_term == 'ki' and (CC_dep == 'k2' or CC_dep == 'rs'):
                head_VM, child_VM = fetch_VM_info(output, VM_1_index, VM_2_index)
                if len(head_VM) and len(child_VM):
                    head_VM_index = head_VM[0]
                    child_VM[6] = head_VM_index
                    up_dep = 'vk2'
                    child_VM[7] = up_dep
                    break
            else:
                CC_count = CC_count - 1
                CC_info = fetch_CC_info(output, CC_index)

    #Swap k2 and k2g if both point to same head verb
    if k2exists and k2gexists:
        if k2_head_verb_index == k2g_head_verb_index and k2_head_verb_index == head_verb_index:
            up_dep = 'k2g'
            output[k2_index-1][7] = up_dep
            up_dep = 'k2'
            output[k2g_index-1][7] = up_dep

    #Change k4, k5 to k2g when the list of verbs- bola, kaha, puCa
    if head_verb_exists:
        main_verb = output[head_verb_index-1][1]
        for verb in verb_lst:
            if verb in main_verb:
                up_dep = 'k2g'
                if k4exists:
                    output[k4_index-1][7] = up_dep
                if k5exists:
                    output[k5_index - 1][7] = up_dep

    #For direct dependency mapping
    for row in output:
        if len(row) > 0:
            dep_reln = row[7]
            index = row[0]
            term = row[1]
            POS_tag = row[3]

            if dep_reln == 'nmod__adj':
                if POS_tag == 'JJ' or POS_tag == 'NN':
                    up_dep = 'mod'
                    row[7] = up_dep
                elif POS_tag == 'QC':
                    up_dep = 'card'
                    row[7] = up_dep
                elif POS_tag == 'DEM':
                    up_dep = 'dem'
                    row[7] = up_dep
                elif POS_tag == 'QF':
                    up_dep = 'quant'
                    row[7] = up_dep
            elif dep_reln == 'mod' and POS_tag == 'JJ':
                up_dep = 'mod'
                row[7] = up_dep
            elif dep_reln == 'lwg__neg' and POS_tag == 'NEG':
                up_dep = 'neg'
                row[7] = up_dep
            elif dep_reln in dependency_mapper:
                up_dep = dependency_mapper[dep_reln]
                row[7] = up_dep
            elif dep_reln.startswith('k') and dep_reln.endswith('u'):
                next_word = get_term_by_index(output, index+1)
                if next_word in ('jEsA', 'jEse', 'jEsI'):
                    up_dep = 'ru'
                    row[7] = up_dep
                else:
                    up_dep = 'rv'
                    row[7] = up_dep
            elif POS_tag == 'NNP' and dep_reln == 'k7p':
                if is_followed_by(output, index, 'ke pAsa'):
                    up_dep = 'rsm'
                    row[7] = up_dep
            elif POS_tag == 'NN' and dep_reln == 'k7':
                if is_followed_by(output, index, 'ke pAsa'):
                    up_dep = 'rsm'
                    row[7] = up_dep
            elif POS_tag == 'PRP' and dep_reln == 'k7':
                if is_followed_by(output, index, 'pAsa'):
                    up_dep = 'rsm'
                    row[7] = up_dep

    #For vmod processing
    for row in output:
        if len(row) > 0:
            index = row[0]
            if row[3] == 'VM':
                dependency = get_dependency_by_index(output, index)
                next_term_index = index + 1
                next_term_tag = get_tag_by_index(output, next_term_index)
                next_term = get_term_by_index(output, next_term_index)
                next_term_pointing_index = get_pointing_index(output, next_term_index)
                if dependency == 'vmod':
                    term = get_term_by_index(output, index)
                    if term.endswith('kara'):
                        up_dep = 'rpk'
                        row[7] = up_dep
                    elif check_term_ending_with(term, we_lst):
                        if next_term_tag == 'VAUX' and next_term_pointing_index == index:
                            if check_term_ending_with(next_term, hue_lst):
                                up_dep = 'rsk'
                                row[7] = up_dep
                    elif next_term_tag == 'VAUX' and next_term_pointing_index == index:
                        if next_term.endswith('kara'):
                            up_dep = 'rpk'
                            row[7] = up_dep
                elif dependency == 'k7':
                    term = get_term_by_index(output, index)
                    if term.endswith('ne'):
                        if next_term_tag == 'PSP' and next_term_pointing_index == index:
                            if next_term.endswith('para'):
                                up_dep = 'rblsk'
                                row[7] = up_dep
                elif dependency == 'k7t':
                    if is_followed_by(output, index, 'se pahale'):
                        up_dep = 'rblak'
                        row[7] = up_dep
                    elif is_followed_by(output, index, 'ke bAxa'):
                        up_dep = 'rblpk'
                        row[7] = up_dep

    #For CC and ccof processing
    if CC_exists:
        CC_dep = output[CC_index - 1][7]
        CC_ptr_index = output[CC_index - 1][6]
        for row in output:
            row_ptr_index = row[6]
            row_dep = row[7]
            if row_ptr_index == CC_index and row_dep in ('ccof', 'CCOF'):
                up_dep = CC_dep
                up_ptr_index = CC_ptr_index
                row[7] = up_dep
                row[6] = up_ptr_index

    return output

def format_data(row):
    if len(row) == 0:
        return []
    hindi_format = WXC(order="utf2wx", lang="hin")
    index = int(row[0])  if row[0] != '' else log('Value in the index col is missing')
    if row[1] == ' ':
        log('Value in the token col is missing')
    elif row[1] != '|' and row[1] != '।':
        wx_token = hindi_format.convert(row[1])
    else:
        wx_token = row[1]

    token = row[2]
    category = row[3]
    category_1 = row[4]
    col6 = row[5]
    related_to = int(row[6]) if row[6] != '' else log('Value in the related_to col is missing')
    relation = row[7]
    col9 = row[8]
    col10 = row[9]

    formatted_row = [index, wx_token, token, category, category_1, col6, related_to, relation, col9, col10]
    return formatted_row

def generate_parse_data(parser_output_line):
    """
    >>> generate_parse_data("1	यदि	यदि	CC	CC	_	15	vmod	_	_")
    ['1', 'यदि', 'यदि', 'CC', 'CC', '_', '15', 'vmod', '_', '_']
    """
    output = parser_output_line.strip().split()
    return output

def parse_file(parser_output):
    parsed_output = list(map(lambda x: generate_parse_data(x), parser_output))
    format_output = list(map(lambda x: format_data(x), parsed_output))
    return format_output

def clean_input_data(input):
    clean_input = []
    hindi_format = WXC(order="wx2utf", lang="hin")
    for data in input:
        data = hindi_format.convert(data)
        if data[-1] == '।' or data[-1] == '|':
            if data[-2] != ' ':
                data = data[:-1] + ' ' + data[-1]
        elif data[-1] == '.':
            data = data[:-1] + ' ' + '।'
        clean_input.append(data)

    return clean_input

def get_parser_output(input, output):
    os.system("isc-parser -i " + input + " -o " + output)

def read_data(file_path):
    '''Returns list of input sentences'''
    log(f'File ~ {file_path}')
    try:
        with open(file_path, 'r') as file:
            input_data = []
            lines = file.readlines()
            for i in range(len(lines)):
                lineContent = lines[i].strip()
                if lineContent == '':
                    continue
                else:
                    input_data.append(lineContent)
            log('File data read.')
    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return input_data

def write_data(data, file_path, BEGIN_WRITE):
        if isinstance(data[0], list):
            # Write list of lists
            with open(file_path, 'a') as file:
                if BEGIN_WRITE:
                    file.seek(0)
                    file.truncate()

                for sublist in data:
                    line = ' '.join(str(element) for element in sublist)
                    file.write(line + '\n')
                file.write('\n')
            log(f'File ~ {file_path} data written successfully')
        else:
            # Write list of strings or a single string
            if isinstance(data, list):
                # Write list of strings
                with open(file_path, 'a') as file:
                    if BEGIN_WRITE:
                        file.seek(0)
                        file.truncate()

                    for item in data:
                        file.write(str(item) + '\n')
                    file.write('\n')
                log(f'File ~ {file_path} data written successfully')
            else:
                # Write a single string
                with open(file_path, "w") as file:
                    file.write(str(data) + '\n')
                log(f'File ~ {file_path} data written successfully')

if __name__ == "__main__":
    hindi_format = WXC(order="wx2utf", lang="hin")
    input = read_data(CONSTANTS.INPUT_FILE)
    clean_input = clean_input_data(input)
    BEGIN_WRITE = True
    for sentence in clean_input:
        #generate POS - Tagger output for input sentence
        write_data(sentence, CONSTANTS.INTERMEDIATE_PARSER_INPUT, BEGIN_WRITE)
        get_parser_output(CONSTANTS.INTERMEDIATE_PARSER_INPUT, CONSTANTS.INTERMEDIATE_PARSER_OUTPUT)
        data = read_data(CONSTANTS.INTERMEDIATE_PARSER_OUTPUT)

        #write the intetmediate_parser_output in one file
        write_data(data, CONSTANTS.CONSOLIDATED_PARSER_OUTPUT, BEGIN_WRITE)
        format_output = parse_file(data)
        #process parser dependencies
        processed_relation = process_relation(format_output)

        final_output = []
        for inner_list in processed_relation:
            for i in range(len(inner_list)):
                inner_list[i] = str(inner_list[i])
                if i == 1:
                    inner_list[i] = hindi_format.convert(inner_list[i])
            final_output.append('\t'.join(inner_list))
        write_data(final_output, CONSTANTS.PROCESSED_PARSER_OUTPUT_FILE, BEGIN_WRITE)
        BEGIN_WRITE = False




