from collections import Counter
import nltk
import re

def replace_common_words_with_identifier(input_string,graph,ones,zeros):

    tokens = nltk.word_tokenize(input_string)
    words=[]

    for i in range(0,len(tokens)):
        if(tokens[i]=="समुच्चय" and i!=len(tokens)-1 and tokens[i+1]=="दोतक"):
            words.append("समुच्चय दोतक")
            i=i+1
        else:
            words.append(tokens[i])

    word_count = Counter(words)
    replaced_words = []
    # print("str",input_string)
    # print(words)
    for word in words:
        if word_count[word] > 1 and (word in ones ):

            replaced_words.append(f'{word}{word_count[word]}')
            graph+="\n"+"\""+f'{word}{word_count[word]}'+"\""+"[label=\""+word+"\"]"

            if(word in ones):
                ones.append(f'{word}{word_count[word]}')
            else:
                zeros.append(f'{word}{word_count[word]}')
            word_count[word] -= 1

        else:
            replaced_words.append(word)

    output_string = ' '.join(replaced_words)

    return [output_string,graph,ones,zeros]

def graph_function(input,final_graph,ones,zeros,graph):
    
    # print("in",input)
    
    prev=0
    word_b=word_b_z=""
    count=0
    temp=temp_z=False
    another_one=False
    sent_list=[]
    pre_graph=""
    first_relation_bool=False
    first_relation=""
    last_relation=""
    check_relation_present=False

    list1=input.split(" ")
    for l in range(0,len(list1)):
        count+=len(list1[l])+1
        if list1[l] in ones:
            last_relation=list1[l]
            check_relation_present=True
            if(first_relation_bool==False):
                first_relation=list1[l]
                first_relation_bool=True
            check_word=list1[l]

            if(list1[l]=="समुच्चय" and list1[l+1].startswith("दोतक")):
                check_word=list1[l]+" "+list1[l+1]
                l=l+1

            if(prev!=0 and temp==True):
                sentence_after=input[prev:count-len(check_word)-2]

                if(sentence_after not in sent_list):
                    sent_list.append(sentence_after)
                    pre_graph+="\n\""+sentence_after+"\"[label=\""+sentence_after+"\"];"

                graph+="\n\""+word_b+"\"->\""+check_word+"\"[label=\"op2\"];"

            
            sentence_before=input[prev:count-len(check_word)-2]

            if(another_one):
                # print(another_one)
                if(sentence_after not in sent_list):
                    sent_list.append(sentence_after)
                    pre_graph+="\n\""+sentence_after+"\"[label=\""+sentence_after+"\"];"
                if(sentence_before not in sent_list):
                    sent_list.append(sentence_before)
                    pre_graph+="\n\""+sentence_before+"\"[label=\""+sentence_before+"\"];"
                
                if(temp_z==False):
                    graph+="\n"+"\""+word_b+"\"->\""+sentence_after+"\"[label=\"op2\"];"
                graph+="\n\""+sentence_after+"\"->\""+sentence_before+"\"[label=\""+word_b_z+"\"];"
                graph+="\n\""+check_word+"\"->\""+sentence_after+"\"[xlabel=\"op1\"];"

            else:
                if(sentence_before not in sent_list):
                    sent_list.append(sentence_before)
                    pre_graph+="\n\""+sentence_before+"\"[label=\""+sentence_before+"\"];"

                graph+="\n\""+check_word+"\"->\""+sentence_before+"\"[xlabel=\"op1\"];"

            temp=True
            temp_z=False
            another_one=False
            prev=count
            word_b=check_word

        elif list1[l] in zeros:
            last_relation=list1[l]
            check_relation_present=True
            if(first_relation_bool==False):
                first_relation=list1[l]
                first_relation_bool=True

            if(prev!=0 and temp_z==True):

                if(sentence_after not in sent_list):
                    sent_list.append(sentence_after)
                    pre_graph+="\n\""+sentence_after+"\"[label=\""+sentence_after+"\"];"
                if(sentence_before not in sent_list):
                    sent_list.append(sentence_before)
                    pre_graph+="\n\""+sentence_before+"\"[label=\""+sentence_before+"\"];"

                graph+="\n"+"\""+word_b+"\"->\""+sentence_before+"\"[label=\"op2\"];"
                graph+="\n\""+sentence_before+"\"->\""+sentence_after+"\"[label=\""+list1[l]+"\"];"

            sentence_before=input[prev:count-len(list1[l])-2]
            if(temp_z==False and prev!=0):
                graph+="\n"+"\""+word_b+"\"->\""+sentence_before+"\"[label=\"op2\"];"

            temp_z=True
            temp=False
            another_one=True
            sentence_after=input[prev:count-len(list1[l])-2]
            prev=count
            word_b_z=list1[l]

    if(temp==True):
        graph+="\n"+"\""+word_b+"\"->\""+input[prev:len(input)]+"\"[label=\"op2\"];"
    if(temp_z==True):
        if(temp_z==False):
            graph+="\n"+"\""+word_b+"\"->\""+sentence_before+"\"[label=\"op2\"];"
        # print(prev)
        # print(len(input))
        # print(input[prev:len(input)])
        # print(sentence_before)
        # print(las_ind)
        graph+="\n"+"\""+sentence_before+"\"->\""+input[prev:len(input)]+"\"[label=\""+word_b_z+"\"];"

 

    final_graph+=pre_graph+graph
    # print("final",final_graph)
    if(check_relation_present==False):
        final_graph=""
        first_relation=""
        return[final_graph,first_relation,last_relation]

    return [final_graph,first_relation,last_relation]

if __name__=="__main__":
    ones=['समुच्चय', 'कार्य-कारण', 'विरोधि', 'अन्यत्र','समुच्चय दोतक','वाक्य-कर्म','विरोधि.viparIwa','परिणाम','विरोधि_द्योतक','समुच्चय.BI_1','समुच्चय.x' ]
    zeros=['आवश्यकता-परिणाम', 'व्याभिचार','समानकाल']
    final_graph="digraph G{ \n node [fontsize=18];\n rankdir=TB;"
    with open("sentence_output.txt","r") as file:
        input=file.read()

    input=re.sub(r'<.*?>', '', input)

    graph=""
    out_com = replace_common_words_with_identifier(input,graph,ones,zeros)
    # print(ones)
    input=out_com[0]
    # print(input)
    graph=out_com[1]
    ones=out_com[2]
    zeros=out_com[3]

    left_bracket=input.find("[")+1
    right_bracket=input.find("]")
    if left_bracket-1==-1 and right_bracket==-1:
        matches=input[left_bracket:right_bracket]
        brack_relation=matches.strip().split(" ",1)[0]
        brack_text=matches.strip().split(" ",1)[1]
    else:
        brack_text=input
    final_graph=graph_function(brack_text,final_graph,ones,zeros,graph)[0]
    next_relation=graph_function(brack_text,final_graph,ones,zeros,graph)[1]

    if left_bracket-1==-1 and right_bracket==-1:
        before_input=input
    else:
        before_input=input[0:left_bracket]
    if(next_relation in ones):
        ones.remove(next_relation)
    elif(next_relation in zeros):
        zeros.remove(next_relation)
    
    # print(next_relation)
    before_input=before_input.strip()
    if(before_input[-1]=="["):
        before_input=before_input[0:len(before_input)-1]
    
    # final_graph=graph_function(before_input,final_graph,ones,zeros)[0]
    if(len(final_graph)>0):
        brack_text=before_input+" "+brack_relation+" "+next_relation
        final_graph+=graph_function(before_input,final_graph,ones,zeros,graph)[0]
        last_relation=graph_function(before_input,final_graph,ones,zeros,graph)[2]
        if left_bracket-1!=-1 and right_bracket!=-1:
            final_graph+="\n\""+last_relation+"\"->\""+next_relation+"\"[label=\""+brack_relation+"\"];"
    else:
        final_graph="digraph G{ \n node [fontsize=18];\n rankdir=TB;"
        brack_text=before_input+" "+brack_relation+" "+brack_text
        final_graph=graph_function(brack_text,final_graph,ones,zeros,graph)[0]
    # print(brack_text)
    
    
    
    final_graph+="\n}"
    print(final_graph)
    with open("input.dot","w") as file:
        file.write(final_graph)