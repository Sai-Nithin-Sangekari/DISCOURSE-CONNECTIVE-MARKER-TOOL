import os
from wxconv import WXC


class USR:
   """
       This class contains various methods which facilitate in discourse prediction
      
       Due to the nature of implementation of this file, it is expected to store
       the USRs in a 3-level heirarchy, while passing the path of the root folder
       e.g.  : root -> sub_folder_1 -> usr_file.txt
   """
   def __init__(self) -> None:
           self.set_marker_info()
           #module to convert from devnagri to wx
           self.convert_to_wx = WXC(order='utf2wx')
           self.res_folder_path = ""
           self.root_folder_path = ""
           self.na_kevala_found = False
  
   def set_marker_info(self):
       #set of single word markers
           self.markers = {"Ora","evaM", "waWA", "yaxi", "wo", "kyoMki",
               "isIlie","isalie","jabaki","yaxyapi","waWApi","Pira BI",
               "lekina","kiMwu","paraMwu","jaba","waba","yA","aWavA", 'viparIwa',"hAlAzki"}
          
           #set of multi words marker
           self.multi_word_markers = {"nahIM wo","isake pariNAmasvarUpa", 'isake viparIwa',
                             "isake alAvA", 'isake awirikwa', 'isake sAWa-sAWa','isake sAWa sAWa','isa kAraNa','isake bAvajZUxa'
                               }
          
           #maps all the markers to respective discourse relations
           self.discourse_relation = {
                   "Ora" : "samuccaya",
                #    "ki" : "vAkya-karma",
                   "evaM" : "samuccaya",
                   "waWA" : "samuccaya",
                #    "agara" : "AvaSyakawA-pariNAma",
                   "yaxi" : "AvaSyakawA-pariNAma",
                   "wo" : "AvaSyakawA-pariNAma",
                   "nahIM wo": "AvaSyakawA-pariNAma",
                   "kyoMki" : "kArya-kAraNa",
                   "isIlie" : "pariNAma",
                   "isalie" : "pariNAma",
                   "jabaki" : "viroXI_xyowaka",
                   "yaxyapi" : "vyABicAra",
                   "waWApi" : "vyABicAra",
                   "hAlAzki" : "vyABicAra",
                   "Pira BI" : "vyABicAra",
                   "lekina" : "viroXI",
                   "kiMwu" : "viroXI",
                   "paraMwu" : "viroXI",
                   "jaba" : "samAnakAla",
                   "waba": "samAnakAla",
                   "yA": "anyawra",
                   "aWavA": "anyawra",
                   'isake pariNAmasvarUpa' : "pariNAma",
                   'isake viparIwa' : "viroXI",
                   "viparIwa" : 'viroXI',
                   "isake alAvA" : 'samuccaya x' ,
                   'isake awirikwa' : 'samuccaya x',
                   'isake sAWa-sAWa' : 'samuccaya x',
                   'isake sAWa sAWa' : 'samuccaya x',
                   'isa kAraNa' : 'pariNAma',
                   'isake kAraNa':'kArya-kAraNa',
                   'isake bAvajZUxa' : 'vavicAra',
                   'nA kevala': 'samuccaya'
                   
           }
          
           #maps whether the discourse relation is to be
           #concatenated to current USR or previous USR
           #0  means discourse relation to be added to prev_usr
           #1  means discourse relation to be added to curr_usr
           #x  means discourse relation to be added to curr_usr and 'x' to be added in the 8th row
           self.discourse_pos = {
               "samuccaya" : "1",
            #    "vAkya-karma" : "1",
               "anyawra": "1",
               "samAnakAla":"0",
               "viroXI": "1",
               "vyABicAra":"0",
               "kArya-kAraNa": "1",
               "AvaSyakawA-pariNAma": "0",
               "samuccaya x" : 'x',
               "viroXI_xyowaka" : '1',
               "vavicAra" : 'x',
               "pariNAma" : "1",
           }
           # self.new_relation={
           #   "nA kevala":"samuccaya BI_1",
           #   "isake alAvA":"samuccaya BI_1",
           # }
  
   def get_marker_info(self):
       """
           returns markers, multi-word-markers, discourse relations, discourse_pos
       """
       return self.markers, self.multi_word_markers, self.discourse_relation, self.discourse_pos
  
   def set_res_folder_path(self, res_path):
       """
           sets the path where the processing results
           will be stored
       """
       self.res_folder_path = res_path
      
   def get_res_folder_path(self):
       """
           returns the path to results folder
       """
       return self.res_folder_path


   def set_root_folder_path(self, root_path):
       """
           sets the path where the USRs are stored
       """
       self.root_folder_path = root_path
  
   def get_root_folder_path(self):
       """
           returns the path to root folder
       """
       return self.root_folder_path
  
   def set_input_mode(self, input_mode):
       self.input_mode = input_mode
  
   def get_input_mode(self):
       return self.input_mode
  
   def create_res_folder(self, path):
       """
           in case a result folder is not yet created at the
           specified path, it creates such a folder
       """
       try:
           os.makedirs(path)
       except FileExistsError:
           print("Folder already exists!")
       return path    
  
   def convert_to_usr(self, file_path):
       """
           it opens the file content (USR) & converts it
           from a single string to a list of rows
          
           - file\\_path: path to USR file
       """
       with open(file_path, 'r') as file:
               content = file.read()
               USR_list = content.split("\n")
               for i in range(len(USR_list)):
                   if i == 0:
                       # USR_list[i] = USR_list[i].split(" ")
                       continue
                   USR_list[i] = USR_list[i].split(',')
               return USR_list
  
   def save_usr_to_txt(self, usr, filename,  sub_folder_path):
       """
           it converts the updated USR from list to string
           and writes it in a .txt file
          
           - usr : previous USR (list) object \n
           - filename : name of the file \n
           - sub\\_folder\\_path : path where the file was stored in root structure \n
       """
       with open(sub_folder_path + '/' + filename + '.txt', 'w') as file:
           for row_number in range(len(usr)):
               output_string = ""
               if(row_number == 0):
                   output_string = usr[row_number]
               else:
                   for element in usr[row_number]:
                       if element == None:
                           element = ""
                       output_string += element + ','
                   output_string = output_string[:-1]
               file.write(output_string + '\n')
       file.close()


   def get_main_str(self, usr):
       """
           returns position of the "0:main" string in the current element
           - usr : takes the USR list as input
       """
       if usr and len(usr) > 5 and usr[5]:
           for position in range(len(usr[5])):
            word = usr[5][position]
            if word == "0:main":
                return position
			# Return a default value if "0:main" is not found
       return -1
           
   def get_discourse_from_word(self, sentence):
       """
           get discourse relation from the first word\n
           - sentence : list of first 5 words in the wx converted sentence
       """
       sent = sentence[0]
      
       for i in range(len(sentence)-1):
           print(sent)
           if sent in self.markers or sent in self.multi_word_markers:
               return self.discourse_relation[sent]
           sent += " " + sentence[i+1]
       return "-1"
  
   def process_usr(self,prev_filename, prev_usr, curr_filename, curr_usr):
        """
            process USR
            
                -	prev\\_filename : filename of the previous USR file
                - prev\\_usr : previous USR list
                - curr\\_filename : filename of the current USR file
                - curr\\_usr : current USR list
        """

        sentence_without_hash = curr_usr[0][1:]	#removing '#' symbol
        sentence_without_hash = self.convert_to_wx.convert(sentence_without_hash) #converting to wx notation
        
        #taking the first 5 words from the beginning 
        #of the sentence and arranges them in a list
        sentence_without_hash = sentence_without_hash.split(" ")[:5]	
        if sentence_without_hash[0] == "nA" and sentence_without_hash[1] == "kevala":
               self.na_kevala_found = True
        else:
            if self.na_kevala_found:
                discourse_relation_from_sentence = "samuccaya"
            # add "samuccaya" to 7th row
                usr_id = prev_filename
                pos_main_curr_usr = self.get_main_str(curr_usr) #find position of 0:main in current usr list
                final_string_to_append = usr_id + '.' + str(pos_main_curr_usr + 1) + ':' + discourse_relation_from_sentence
            # add "BI_1" to 8th row
                if prev_usr[6][pos_main_curr_usr]=='':
                    prev_usr[6][pos_main_curr_usr] += final_string_to_append + ' '
                curr_usr[7][pos_main_curr_usr] = 'BI_1'
                self.na_kevala_found = False

        discourse_relation_from_sentence = self.get_discourse_from_word(sentence_without_hash)	#gets the discourse relation from the word list 
        
        if(discourse_relation_from_sentence == "-1"):	#if no discourse relation found, return the USR lists as it is
            return prev_usr, curr_usr
        
        select_usr_to_append = self.discourse_pos[discourse_relation_from_sentence]	#get the USR list where the discourse relation is to be appended.
                                                                                    #select_usr_to_append == 0  means discourse relation to be added to prev_usr
                                                                                    #select_usr_to_append == 1  means discourse relation to be added to curr_usr

        pos_main_prev_usr = self.get_main_str(prev_usr)	#find position of 0:main in previous usr list
        pos_main_curr_usr = self.get_main_str(curr_usr)	#find position of 0:main in current usr list
        print("val: ",sentence_without_hash, discourse_relation_from_sentence, pos_main_curr_usr, pos_main_prev_usr, select_usr_to_append)
        if select_usr_to_append == "1" or select_usr_to_append == 'x':
            """
                if the USR to be updated is the current USR list,
                d 
                e.g. :
                
                    merI pehlI gADZI coTI WI  lekina xUsarI gAdZI Limousine ke AkAra kI hE
                    2a
                    merI pehlI gADZI coTI WI
                    speaker,pehlA_1,gADZI_1,CoTI_1,hE_1-pres
                    1,2,3,4,5
                    anim,,,,
                    [m sg m],,[- sg a],,
                    2:r6,3:ord,5:k1,5:k1s,0:main
                    ,,,,
                    ,,,,
                    ,,,,
                    affirmative

                    2b
                    lekina xUsarI gAdZI Limousine ke AkAra kI hE
                    xUsarA_1,gAdZI_1,limousine, AkAra_1, hE_1-pres
                    1,2,3,4,5
                    ,,ne,,
                    [- sg a],[-  sg a],[- sg a],
                    2:ord,5:k1,5:r6,? 0:main
                    ,,,,2a.5:viroXI
                    ,,,,
                    ,,,,
                    affirmative
            """
            # print(" add ", curr_usr[6], pos_main_curr_usr)
            # usr_id = prev_filename	
            # final_string_to_append = usr_id + '.' + str(pos_main_prev_usr + 1) + ':' + discourse_relation_from_sentence
            # curr_usr[6][pos_main_curr_usr] += final_string_to_append + ' '

            if sentence_without_hash[0] == "isake" and sentence_without_hash[1] == "alAvA":
                discourse_relation_from_sentence='samuccaya'
                final_string_to_append = usr_id + '.' + str(pos_main_prev_usr + 1) + ':' + discourse_relation_from_sentence
                if curr_usr[6][pos_main_curr_usr]=='':
                    curr_usr[6][pos_main_curr_usr] += final_string_to_append + ' '
                curr_usr[7][pos_main_curr_usr] = 'BI_1'
                   
            elif sentence_without_hash[0] == "isake" and sentence_without_hash[1] == "viparIwa":
                discourse_relation_from_sentence='viroXI'
                final_string_to_append = usr_id + '.' + str(pos_main_prev_usr + 1) + ':' + discourse_relation_from_sentence
                if curr_usr[6][pos_main_curr_usr]=='':
                    curr_usr[6][pos_main_curr_usr] += final_string_to_append + ' '
                curr_usr[7][pos_main_curr_usr] = 'viparIwa'
                
            else:
                print(" add ", curr_usr[6], pos_main_curr_usr)
                print(" add ", prev_usr[6], pos_main_curr_usr)
                usr_id = prev_filename	
                final_string_to_append = usr_id + '.' + str(pos_main_prev_usr + 1) + ':' + discourse_relation_from_sentence
                if curr_usr[6][pos_main_curr_usr]=='':
                    curr_usr[6][pos_main_curr_usr] += final_string_to_append + ' '
                if select_usr_to_append == 'x':
                    curr_usr[7][pos_main_curr_usr]  = 'X'
        else:
            """
                if the usr to be updated is previous USR list,
                then we need to append the USR ID of the current file
                
                e.g.:
                    1a
                    #Apa cAhawe hEM
                    addressee,cAha_1-wA_hE_1
                    1,2
                    anim,
                    [m sg u],
                    2:k1,0:main
                    ,1b.4:AvaSaykwA-parinAma
                    ,
                    affirmative
                    

                    1b
                    #wo meM Apake Gara AuzgA
                    speaker,addressee,Gara_1,A_1-gA_1
                    1,2,3,4
                    anim,,,
                    [- sg u],,[- sg a],
                    4:k1,3:r6,4:k2p,0:main
                    ,,,
                    ,respect,,
                    ,,,
                    affirmative
            """
            # print(prev_usr[6], pos_main_prev_usr)
            # usr_id = curr_filename
            # final_string_to_append = usr_id + '.' + str(pos_main_curr_usr + 1) + ':' + discourse_relation_from_sentence
            # prev_usr[6][pos_main_prev_usr] += final_string_to_append + ' '

            if sentence_without_hash[0] == "nahIM" and sentence_without_hash[1] == "wo":
                print(prev_usr[6], pos_main_prev_usr)
                usr_id = curr_filename
                final_string_to_append = usr_id + '.' + str(pos_main_curr_usr + 1) + ':' + discourse_relation_from_sentence
                if prev_usr[6][pos_main_prev_usr]=='':
                    prev_usr[6][pos_main_prev_usr] += final_string_to_append + ' '
                prev_usr[7][pos_main_prev_usr] = 'nahIM_1'
            else:
                print(prev_usr[6], pos_main_prev_usr)
                usr_id = curr_filename
                final_string_to_append = usr_id + '.' + str(pos_main_curr_usr + 1) + ':' + discourse_relation_from_sentence
                if prev_usr[6][pos_main_prev_usr]=='':
                    prev_usr[6][pos_main_prev_usr] += final_string_to_append + ' '
            # try:
            # except IndexError:
            # 	print("error : ", prev_usr[6], pos_main_prev_usr, final_string_to_append)
                
        return prev_usr, curr_usr
  
   def run(self):
       """
           traverses root folder & calls crucial methods required to implement
           rule-based discourse prediction in all existing USRs inside the folder.
      
           Due to the nature of implementation of this file, it is expected to store
           the USRs in a 3-level heirarchy, while passing the path of the root folder
           e.g.  : root -> sub_folder_1 -> usr_file.txt
       """
      
       #create the res folder or print if the folder already exists
       self.create_res_folder(self.res_folder_path)
      
       if self.input_mode == 0:
           #traverse the files inside the folder:
           for _, _, filenames in os.walk(self.root_folder_path):
               filenames = sorted(filenames)
               prev_usr = []
               curr_usr = []
               prev_filename = "0"
              
               #for each file, try rule-based discourse prediction
               for filename in filenames:
                   file_path   = self.root_folder_path + "/" + filename
                  
                   with open(file_path, "r") as file:
                           content = file.read()
                          
                           if content.find("\n") != -1:    #content not empty
                               curr_usr = self.convert_to_usr(file_path) #converts the file content into a list object. This creates a USR list.
                               prev_usr, curr_usr = self.process_usr(prev_filename, prev_usr, filename, curr_usr)
                               self.save_usr_to_txt(prev_usr, prev_filename, self.res_folder_path)
                               self.save_usr_to_txt(curr_usr, filename, self.res_folder_path)
                               prev_filename = filename
                               prev_usr = curr_usr  #current usr becomes the PREVIOUS USR for future file
                              
               #removes the dummy file thus created
               os.remove(self.res_folder_path + "/" + "0.txt")
               break
  
       else:
           #traverse to the subfolders inside root folder
           for _, sub_folder, filenames in os.walk(self.root_folder_path):
               if sub_folder.__sizeof__ != 0:
                  
                   for sub_folder_name in sub_folder:
                       sub_folder_path = self.root_folder_path +  "/" + sub_folder_name
                       path = self.res_folder_path + "/" + sub_folder_name
                       self.create_res_folder(path)
                      
                       #traverse all the files inside the subfolder
                       for _, _, filenames in os.walk(sub_folder_path):
                           filenames = sorted(filenames)
                           prev_usr = []
                           curr_usr = []
                           prev_filename = "0"
                          
                           #for each file, try rule-based discourse prediction
                           for filename in filenames:
                               file_path   = sub_folder_path + "/" + filename
                              
                               with open(file_path, "r") as file:
                                       content = file.read()
                                      
                                       if content.find("\n") != -1:    #content not empty
                                           curr_usr = self.convert_to_usr(file_path) #converts the file content into a list object. This creates a USR list.
                                           prev_usr, curr_usr = self.process_usr(prev_filename, prev_usr, filename, curr_usr)
                                           self.save_usr_to_txt(prev_usr, prev_filename, path)
                                           self.save_usr_to_txt(curr_usr, filename, path)
                                           prev_filename = filename
                                           prev_usr = curr_usr  #current usr becomes the PREVIOUS USR for future file
                                          
                           #removes the dummy file thus created
                           os.remove(self.res_folder_path + "/" + sub_folder_name + "/" + "0.txt")
                           break
              


class discourseMarkerParser(USR):
   """
       returns discourse relation between two sentence by traversing
       first three words of both sentences.
       Child class of USR
   """
   def __init__(self, sent1:str, sent2:str):
       super().__init__()
       sent1 = sent1.split(' ', 1)
       sent2 = sent2.split(' ', 1)
       sent1_wx = self.convert_to_wx.convert(sent1[1])
       sent2_wx = self.convert_to_wx.convert(sent2[1])
       self.run_process(sent1[0], sent1_wx, sent2[0], sent2_wx)
      
   def run_process(self, sent1_id:str, sent1:str, sent2_id:str, sent2:str):
       self.id1 = sent1_id
       self.s1 = sent1
       self.id2 = sent2_id
       self.s2 = sent2
       self.res_s1, self.res_disc, self.res_s2 = self.set_result()


      
   def get_discourse_from_word(self, sentence:str):
      
       sent = sentence.split()
       s = sent[0]

       for i in range(len(sent) - 1):
           if s in self.markers or s in self.multi_word_markers:
               return self.discourse_relation[s]
           else:
               s += ' ' + sent[i+1]
       return "-1"
       # sent = sentence.split()
       # s = sent[0]
       # print(s)
       # for i in range(len(sent) - 1):
       #   if s == ('isake' or 'isa' or 'Pira'):
       #       if sent[1] == 'pariNAma':
       #           s = s + " " + sent[1] + " " + sent[2]
                  
       #           if s in self.markers or s in self.multi_word_markers:
       #               return self.discourse_relation[s]
       #           s += ' ' + sent[i + 3]


       #       else:
       #           s = s + " " + sent[1]
                  
       #           if s in self.markers or s in self.multi_word_markers:
                      
       #               return self.discourse_relation[s]
       #           s += ' ' + sent[i + 2]
       #   elif s == 'ki':
       #       return 'ki'
       #   elif s in self.markers or s in self.multi_word_markers:
       #       return self.discourse_relation[s]
       #   s += ' ' + sent[i+1]
       # return "-1"
  
   def set_result(self):
       s = ""
       disc_relation = self.get_discourse_from_word(self.s1)
              
       if disc_relation == "-1":
           disc_relation = self.get_discourse_from_word(self.s2)
          
           if disc_relation == "-1":
               return self.s1.rstrip('.'), "NaN", self.s2.rstrip('.')
           else:
              
               disc_pos = self.discourse_pos.get(disc_relation)
               s_w = self.s2.split()
               s = s_w[0]
          
               for i in range(len(s_w) - 1):
                   if s in self.markers or s in self.multi_word_markers:
                       self.s2 = self.s2.replace(s,'')
                      
                   else:
                       s += ' ' + s_w[i+1]
          
           return self.s1.rstrip('.').strip(' '), disc_relation, self.s2.strip('.')
                                  
       else:
           s_w = self.s1.split()
           s_1 = s_w[0]
          
           for i in range(len(s_w) - 1):
               if s_1 in self.markers or s_1 in self.multi_word_markers:
                  
                   self.s1 = self.s1.replace(s_1,'')
               else:
                   s_1 += ' ' + s_w[i+1]

           disc_relation = self.get_discourse_from_word(self.s2)

           if disc_relation == "-1":

               self.s1 = s_1 +" "+ self.s1
              
               return self.s1.rstrip('.'), "NaN", self.s2.rstrip('.')
           else:
               disc_pos = self.discourse_pos.get(disc_relation)
              
               s_w2 = self.s2.split()
               s = s_w2[0]
              
               for i in range(len(s_w2) - 1):
                   if s in self.markers or s in self.multi_word_markers:
                      
                       self.s2 = self.s2.replace(s,'')
                   else:
                       s += ' ' + s_w2[i+1]


               if disc_pos == "0":

                   self.s2 = s_1+" "+self.s2
                  
                   return self.s1.rstrip('.').strip(' '), disc_relation, self.s2.strip('.')

               else:
                   # self.s2 = self.s2.lstrip(' ')
                   # first_space_sent2 = self.s2.find(' ')
                   # if first_space_sent2 != -1:
                   #   self.s2 = self.s2[first_space_sent2 + 1:]
                   self.s1 = s_1+" "+self.s1


                   return self.s1.rstrip('.').strip(' '), disc_relation, self.s2.rstrip('.').strip()
              
   def get_results(self):
       # self.res_s1+= " ।"
       # self.res_s2+= " ।"
       return self.res_s1, self.res_disc, self.res_s2