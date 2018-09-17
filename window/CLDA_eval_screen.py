# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 22:07:34 2018

@author: Shotaro Baba
"""
import datetime
import time
#from multiprocessing import Pool
import pickle
import csv
import json
import pandas as pd
from nltk.corpus import wordnet as wn
import sys
sys.path.append("..\/models/")
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from multiprocessing import cpu_count
from multiprocessing import Pool
dataset_dir = "../../CLDA_data_training"
dataset_test = "../../CLDA_data_testing"
score_result_dir = "../../score_result"
score_result_dataframe_suffix = "_score.csv"
score_result_txt_suffix = "_score.txt"
score_result_log_suffix = "_log.txt"
LDA_score_result_dataframe_suffix = "_LDA_score.csv"
LDA_score_result_txt_suffix = "_LDA_score.txt"
LDA_score_result_log_suffix = "_LDA_log.txt"
stop_word_folder = "../stopwords"
concept_prob_suffix_json = "_c_prob.json"
concept_name_suffix_txt = "_c_name.txt"
feature_matrix_suffix_csv = "_f_mat.csv"
feature_name_suffix_txt = "_f_name.txt"
file_name_df_suffix_csv = "_data.csv"
tokenized_dataset_suffix= "_tokenized.csv"
CLDA_suffix_pickle = "_CLDA.pkl"
LDA_suffix_pickle = "_LDA.pkl"
converted_xml_suffix = "_conv.txt"
default_score_threshold = 0.10
asterisk_len = 20

stop_word_folder = "../stopwords"
stop_word_smart_txt = "smart_stopword.txt"
smart_stopwords = []

with open(stop_word_folder + '/' + stop_word_smart_txt , "r") as f:
    for line in f:
    #Remove the \n
        smart_stopwords.append(line.strip('\n'))

# This will be run asynchronously to reduce
# The time to calculate...
        




import tkinter as tk
import gc
import os
import main_window
dataset_training = "../../CLDA_data_training"
dataset_testing = "../../CLDA_data_testing"

from nltk import wordpunct_tokenize, WordNetLemmatizer, sent_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from string import punctuation
# initialize constants
lemmatizer = WordNetLemmatizer()
def define_sw():
    
    # Use default english stopword     
    return set(stopwords.words('english') + smart_stopwords)


## Defining the lemmatizer
#def lemmatize(token, tag):
#    tag = {
#        'N': wordnet.NOUN,
#        'V': wordnet.VERB,
#        'R': wordnet.ADV,
#        'J': wordnet.ADJ
#    }.get(tag[0], wordnet.NOUN)
#
#    return lemmatizer.lemmatize(token, tag)
#
## The tokenizer for the documents
#def cab_tokenizer(document):
#    tokens = []
#    sw = define_sw()
#    punct = set(punctuation)
#
#    # split the document into sentences
#    for sent in sent_tokenize(document):
#        # tokenize each sentence
#        for token, tag in pos_tag(wordpunct_tokenize(sent)):
#            # preprocess and remove unnecessary characters
#            token = token.lower()
#            token = token.strip()
#            token = token.strip('_')
#            token = token.strip('*')
#
#            # If punctuation, ignore token and continue
#            if all(char in punct for char in token):
#                continue
#
#            # If stopword, ignore token and continue
#            if token in sw:
#                continue
#
#            # Lemmatize the token and add back to the token
#            lemma = lemmatize(token, tag)
#
#            # Append lemmatized token to list
#            tokens.append(lemma)
#    return tokens        

##    for training_file_head in training_head:
#def calculate_score_all_async(training_file_head):
##      T_TP = T_TN =  T_FN =  T_FP = 0
#      #Listing the score
#    score_list = []
#    files_test = []
#    
#    for dirpath, dirs, files in os.walk(dataset_test):
#        files_test.extend(files)
#      
#    
#    test_head = [x[:-len(file_name_df_suffix_csv)] for x in files_test if x.endswith(file_name_df_suffix_csv)]
#      
#
#    print(training_file_head)
#    
#    
#    test_concept_prob, test_concept_names = (None, [])
#        
#    with open(dataset_dir + '/' + training_file_head + concept_prob_suffix_json, "r") as f:
#        test_concept_prob = json.load(f)
#        
#    
#    with open(dataset_dir + '/' + training_file_head + concept_name_suffix_txt, "r") as f:
#        for line in f:
#            test_concept_names.append(line.strip('\n'))
#    
#    with open(dataset_dir + '/' + training_file_head + CLDA_suffix_pickle, "rb") as f:
#        test_CLDA = pickle.load(f)
#      
#      
#    doc_topic = test_CLDA.theta_set[0].sum(axis = 0)/test_CLDA.theta_set[0].shape[0]
#    topic_concept = test_CLDA.show_and_construct_normalized_concept_topic_ranking()
#    word_under_concept = test_CLDA.show_words_prob_under_concept(test_concept_prob)
##        test_file_data = pd.read_csv(data_dir + '/' + test_name + file_name_df_suffix_csv, encoding='utf-8', sep=',', 
##                            error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
#   
#    training_head_number = ''.join(filter(str.isdigit, training_file_head))
#    
##      vector_analysis = generate_vector_for_analysis()
#    for testing_file_head in test_head:
#        print(testing_file_head)
#        test_file_data = pd.read_csv(dataset_test + '/' + testing_file_head + file_name_df_suffix_csv,
#                                      encoding='utf-8', sep=',', error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
#        
#        testing_head_number = ''.join(filter(str.isdigit, testing_file_head))
#        for i in range(len(test_file_data)):
#            score = 0
#            test_files_feature_name  = cab_tokenizer(test_file_data.iloc[i]['Text'])
#    #          _, test_files_feature_name   = vectorize_for_analysis(vector_analysis, test_file_data.iloc[i])
#            for topic_num, topic_prob in enumerate(doc_topic):
#                for concept, concept_prob in topic_concept[topic_num]:
#                      for word, word_prob in [(x[0][0], x[1]) for x in word_under_concept.items() if x[0][1] == concept]:
#                          if word in test_files_feature_name:
#    #                          print('topic_num: {}, concept: "{}", word: "{}"'.format(topic_num, concept, word))
#                              score += topic_prob * concept_prob * word_prob
#        
#            print('Score: {}, File name: "{}"'.format(score, test_file_data.iloc[i]['File']))
#            score_list.append((test_file_data.iloc[i]['File'], training_head_number, testing_head_number, score))  
#    
#    return score_list      
    
    
#        with open()





class CLDA_evaluation_screen(object):
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CLDA Evaluation")
        
        
        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label="Quit", command=None)
        self.menubar.add_command(label="Help", command=None)
        
        self.root.config(menu=self.menubar)
        
        self.start_menu()
        
        self.listing_all_model()
        
        self.root.mainloop()
        
    def start_menu(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        
        self.bottom_button_frame = tk.Frame(self.root)
        self.bottom_button_frame.pack()
        
        self.result_and_selection_frame = tk.Frame(self.main_frame)
        self.result_and_selection_frame.pack()
        '''
        ##########################################################
        ####Text-based result
        ##########################################################
        '''
        #Showing the result of the calculation in the text field
        self.result_frame = tk.Frame(self.result_and_selection_frame)
        self.result_frame.pack(side = tk.RIGHT, pady = 10, padx = 5)
        
        self.result_screen_label = tk.Label(self.result_frame, text = "CLDA & LDA Evaluation Result")
        self.result_screen_label.pack()
        
        self.result_screen_text = tk.Text(self.result_frame)
        self.result_screen_text.pack(side = tk.LEFT)
        self.result_screen_text.configure(state='disabled')
        
        self.result_screen_text_scroll = tk.Scrollbar(self.result_frame)
        self.result_screen_text_scroll.pack(side = tk.RIGHT, fill = 'y')
        
        self.result_screen_text['yscrollcommand'] = \
        self.result_screen_text_scroll.set
        self.result_screen_text_scroll['command'] = self.result_screen_text.yview
        
        #Selection menu for generating algorithms
        
        '''
        ##########################################################
        ####CLDA model selection
        ##########################################################
        '''
        self.CLDA_selection_and_preference = tk.Frame(self.result_and_selection_frame, relief = tk.RAISED, borderwidth = 1)
        self.CLDA_selection_and_preference.pack(side = tk.RIGHT, padx = 10)
        
        
        
        self.CLDA_selection_label = tk.Label(self.CLDA_selection_and_preference, text = "CLDA Selection")
        self.CLDA_selection_label.grid(row = 0)
        
        #######################################
        #Scrolling section
        #######################################
        self.CLDA_selection_and_preference_list_scroll = tk.Frame(self.CLDA_selection_and_preference)
        self.CLDA_selection_and_preference_list_scroll.grid(row = 1)
        
        self.CLDA_selection_listbox = tk.Listbox(self.CLDA_selection_and_preference_list_scroll)
        self.CLDA_selection_listbox.pack(side = tk.LEFT)
        
        self.CLDA_selection_listbox_scroll = tk.Scrollbar(self.CLDA_selection_and_preference_list_scroll)
        self.CLDA_selection_listbox_scroll.pack(side = tk.RIGHT, fill = 'y')
        
        #########################################
        ##Button section
        #########################################
        
        self.CLDA_word_ranking_input_frame = tk.Frame(self.CLDA_selection_and_preference)
        self.CLDA_word_ranking_input_frame.grid(row = 2)
        
        self.CLDA_selection_word_ranking_label = tk.Label(self.CLDA_word_ranking_input_frame, text = "Enter Word\nfor Ranking\nfor CLDA:")
        self.CLDA_selection_word_ranking_label.pack(side = tk.LEFT)
        
        self.CLDA_selection_word_ranking_box = tk.Entry(self.CLDA_word_ranking_input_frame)
        self.CLDA_selection_word_ranking_box.pack(side = tk.RIGHT)
        
        
        self.CLDA_selection_word_ranking_button = tk.Button(self.CLDA_selection_and_preference, text = "Word Ranking\nEvaluation")
        self.CLDA_selection_word_ranking_button.grid(row = 3)
        
        self.CLDA_accuracy_calculation_button = tk.Button(self.CLDA_selection_and_preference, text = "Calculate CLDA accuracy")
        self.CLDA_accuracy_calculation_button.grid(row = 4)
        
        self.CLDA_selection_listbox['yscrollcommand'] = \
        self.CLDA_selection_listbox_scroll.set
        self.CLDA_selection_listbox_scroll['command'] = self.CLDA_selection_listbox.yview
        
        '''
        ##########################################################
        ####LDA model selection
        ##########################################################
        '''
        self.LDA_selection_and_preference = tk.Frame(self.result_and_selection_frame, relief = tk.RAISED, borderwidth = 1)
        self.LDA_selection_and_preference.pack(side = tk.RIGHT, padx = 10)
        
        
        
        self.LDA_selection_label = tk.Label(self.LDA_selection_and_preference, text = "LDA selection")
        self.LDA_selection_label.grid(row = 0)
        
        #######################################
        #Scrolling section
        #######################################
        self.LDA_selection_and_preference_list_scroll = tk.Frame(self.LDA_selection_and_preference)
        self.LDA_selection_and_preference_list_scroll.grid(row = 1)
        
        self.LDA_selection_listbox = tk.Listbox(self.LDA_selection_and_preference_list_scroll)
        self.LDA_selection_listbox.pack(side = tk.LEFT)
        
        self.LDA_selection_listbox_scroll = tk.Scrollbar(self.LDA_selection_and_preference_list_scroll)
        self.LDA_selection_listbox_scroll.pack(side = tk.RIGHT, fill = 'y')
        
        #########################################
        ##Button section
        #########################################
        
        self.LDA_word_ranking_input_frame = tk.Frame(self.LDA_selection_and_preference)
        self.LDA_word_ranking_input_frame.grid(row = 2)
        
        self.LDA_selection_word_ranking_label = tk.Label(self.LDA_word_ranking_input_frame, text = "Enter Word\nfor Ranking\nfor LDA:")
        self.LDA_selection_word_ranking_label.pack(side = tk.LEFT)
        
        self.LDA_selection_word_ranking_box = tk.Entry(self.LDA_word_ranking_input_frame)
        self.LDA_selection_word_ranking_box.pack(side = tk.RIGHT)
        
        
        self.LDA_selection_word_ranking_button = tk.Button(self.LDA_selection_and_preference, text = "Word Ranking\nEvaluation")
        self.LDA_selection_word_ranking_button.grid(row = 3)
        
        
        self.LDA_accuracy_calculation_button = tk.Button(self.LDA_selection_and_preference, text = "Calculate LDA Accuracy")
        self.LDA_accuracy_calculation_button.grid(row = 4)
        
        self.LDA_selection_listbox['yscrollcommand'] = \
        self.LDA_selection_listbox_scroll.set
        self.LDA_selection_listbox_scroll['command'] = self.LDA_selection_listbox.yview
        
        
        '''
        ##########################################################
        ####CLDA button
        ##########################################################
        '''
        self.LDA_evaluation_button = tk.Button(self.bottom_button_frame, text = "Eval LDA")
        self.LDA_evaluation_button.pack()
        self.LDA_evaluation_button['command'] = self.asynchronous_LDA_evaluation
        
        self.CLDA_evaluation_button = tk.Button(self.bottom_button_frame, text = "Eval CLDA")
        self.CLDA_evaluation_button.pack()
        self.CLDA_evaluation_button['command'] = self.asynchronous_CLDA_evaluation
        
        self.change_to_model_creation = tk.Button(self.bottom_button_frame, text = "Return to model creation")
        self.change_to_model_creation.pack()
        self.change_to_model_creation['command'] = self.move_to_model_creation
        
        
        '''
        ##########################################################
        ####LDA button
        ##########################################################
        '''
        
    def move_to_model_creation(self):
        
        #Erase all the display in the directory
        self.root.destroy()
        
        #Delete the object to erase its data
        del self
        
        #Conduct the garbage collection for reducing memory
        #Usage
        gc.collect()
        
        
        main_window.main()
    
    def listing_all_model(self):
        files_tmp = []
        
        for dirpath, dirs, files in os.walk(dataset_training):
            files_tmp.extend(files)
        
        self.LDA_list = [x for x in files_tmp if x.endswith("_LDA.pkl")]
        
        for i in self.LDA_list:
            self.LDA_selection_listbox.insert(tk.END, i)

        self.CLDA_list = [x for x in files_tmp if x.endswith("_CLDA.pkl")]
        
        for i in self.CLDA_list:
            self.CLDA_selection_listbox.insert(tk.END, i)
            
    def asynchronous_CLDA_evaluation(self):
        # Initialize file_tmp list
        self.result_screen_text.delete("1.0", tk.END)
        files_training = []
        for dirpath, dirs, files in os.walk(dataset_dir):
                files_training.extend(files)

#        score_list = []
        files_test = []
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_test.extend(files)
        

        #Tokenize all data in test dataset
        def concurrent1():
        #        files_list_for_modelling_CLDA = sorted(list(set([os.path.splitext(x)[0] for x in files if x.endswith('.csv')])))
            
            fm = Asynchronous_CLDA_evaluation_class()
            
            results = fm.asynchronous_tokenization()
            
            return results
        
        testing_dict = concurrent1()
#        for testing_file_head in test_head:
#            testing_dict[testing_file_head] = pd.read_csv(dataset_test + '/' + testing_file_head + file_name_df_suffix_csv,
#                                          encoding='utf-8', sep=',', error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
#            testing_dict[testing_file_head]['Text'] = testing_dict[testing_file_head]['Text'].apply(lambda x: cab_tokenizer(x))
        
        def concurrent2():
        #        files_list_for_modelling_CLDA = sorted(list(set([os.path.splitext(x)[0] for x in files if x.endswith('.csv')])))
            
            fm = Asynchronous_CLDA_evaluation_class()
            
            results = fm.asynchronous_evaluation(testing_dict)
            
            return results
        
        score_result = concurrent2()
            # Return processed result
        score_result_total = []
        for score_i, buffer_str in score_result:
            score_result_total.extend(score_i)
            self.result_screen_text.configure(state='normal')
            self.result_screen_text.insert(tk.END, buffer_str.getvalue())
            self.result_screen_text.configure(state='disabled')
#        print(score_result_total)  
        
        self._generate_score(score_result_total)
#        score_data_frame = pd.DataFrame(score_result_total, columns = ['File_name', 'Training_topic', 'Testing_topic', 'Score'])
#        storing_result_name_data = score_result_dir + '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + feature_matrix_suffix_csv
#        
#        storing_result_name_text = score_result_dir + '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + score_result_txt_suffix
#        score_data_frame_TP_FN = score_data_frame[score_data_frame['Training_topic'] == score_data_frame['Testing_topic']]
#        log_txt_name = score_result_dir + '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + score_result_log_suffix
#        
#        
#        Total_TP_count  = (score_data_frame_TP_FN['Score'] > default_score_threshold).sum()
#        Total_FN_count = (score_data_frame_TP_FN['Score'] < default_score_threshold).sum()
#        
#        score_data_frame_TN_FP = score_data_frame[score_data_frame['Training_topic'] != score_data_frame['Testing_topic']]
#        
#        Total_TN_count = (score_data_frame_TN_FP['Score'] < default_score_threshold).sum()
#        Total_FP_count = (score_data_frame_TN_FP['Score'] > default_score_threshold).sum()
#        
#        precision = Total_TP_count / (Total_TP_count + Total_FP_count)
#        recall = Total_TP_count / (Total_TP_count + Total_FN_count)
#        
#        score_data_frame.to_csv(storing_result_name_data,
#                              index=False, encoding='utf-8',
#                              quoting=csv.QUOTE_ALL)
#        
#        with open(storing_result_name_text, 'w') as f:
#            result_str = "Precision: {}, Recall: {}\n".format(precision, recall) + \
#            "Trup Positive: {}, False Positive: {}\n".format(Total_TP_count, Total_FP_count) + \
#            "Trup Negative: {}, False Negative: {}\n".format(Total_TN_count, Total_FN_count)
#            self.result_screen_text.configure(state='normal')
#            self.result_screen_text.insert(tk.END, "".join(['*' for m in range(asterisk_len)]) + '\n')
#            self.result_screen_text.insert(tk.END, result_str)
#            self.result_screen_text.insert(tk.END, "".join(['*' for m in range(asterisk_len)]))
#            self.result_screen_text.configure(state='disabled')
#            f.write(result_str)
        
#        with open(log_txt_name, 'w') as f:
#            result_screen = self.result_screen_text.get("1.0", tk.END)
#            f.write(result_screen)
    
    def asynchronous_LDA_evaluation(self):
        # Initialize file_tmp list
        self.result_screen_text.delete("1.0", tk.END)
        files_training = []
        for dirpath, dirs, files in os.walk(dataset_dir):
                files_training.extend(files)

#        score_list = []
        files_test = []
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_test.extend(files)
        

        #Tokenize all data in test dataset
        def concurrent1():
        #        files_list_for_modelling_CLDA = sorted(list(set([os.path.splitext(x)[0] for x in files if x.endswith('.csv')])))
            
            fm = Asynchronous_CLDA_evaluation_class()
            
            results = fm.asynchronous_tokenization()
            
            return results
        
        testing_dict = concurrent1()
#        for testing_file_head in test_head:
#            testing_dict[testing_file_head] = pd.read_csv(dataset_test + '/' + testing_file_head + file_name_df_suffix_csv,
#                                          encoding='utf-8', sep=',', error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
#            testing_dict[testing_file_head]['Text'] = testing_dict[testing_file_head]['Text'].apply(lambda x: cab_tokenizer(x))
        
        def concurrent2():
        #        files_list_for_modelling_CLDA = sorted(list(set([os.path.splitext(x)[0] for x in files if x.endswith('.csv')])))
            
            fm = Asynchronous_CLDA_evaluation_class()
            
            results = fm.asynchronous_evaluation_LDA(testing_dict)
            
            return results
        
        score_result = concurrent2()
            # Return processed result
        score_result_total = []
        for score_i, buffer_str in score_result:
            score_result_total.extend(score_i)
            self.result_screen_text.configure(state='normal')
            self.result_screen_text.insert(tk.END, buffer_str.getvalue())
            self.result_screen_text.configure(state='disabled')
#        print(score_result_total)  
        
        self._generate_score(score_result_total, 
                             0.4,
                             LDA_score_result_dataframe_suffix,
                             LDA_score_result_txt_suffix, 
                             LDA_score_result_log_suffix)
        
    # Calculate the score from the
    # obtained result
    def _generate_score(self, score_result_total, 
                        threshold = default_score_threshold, 
                        score_result_dataframe_suffix = score_result_dataframe_suffix, 
                        score_result_txt_suffix = score_result_txt_suffix, 
                        score_result_log_suffix = score_result_log_suffix):
        ts = time.time()   
        score_data_frame = pd.DataFrame(score_result_total, columns = ['File_name', 'Training_topic', 'Testing_topic', 'Score'])
        storing_result_name_data = score_result_dir + '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + score_result_dataframe_suffix
        
        storing_result_name_text = score_result_dir + '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + score_result_txt_suffix
        score_data_frame_TP_FN = score_data_frame[score_data_frame['Training_topic'] == score_data_frame['Testing_topic']]
        log_txt_name = score_result_dir + '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + score_result_log_suffix
        
        
        Total_TP_count  = (score_data_frame_TP_FN['Score'] > threshold).sum()
        Total_FN_count = (score_data_frame_TP_FN['Score'] < threshold).sum()
        
        score_data_frame_TN_FP = score_data_frame[score_data_frame['Training_topic'] != score_data_frame['Testing_topic']]
        
        Total_TN_count = (score_data_frame_TN_FP['Score'] < threshold).sum()
        Total_FP_count = (score_data_frame_TN_FP['Score'] > threshold).sum()
        
        precision = Total_TP_count / (Total_TP_count + Total_FP_count)
        recall = Total_TP_count / (Total_TP_count + Total_FN_count)
        
        score_data_frame.to_csv(storing_result_name_data,
                              index=False, encoding='utf-8',
                              quoting=csv.QUOTE_ALL)
        
        
        local_result_str = ""
        for i in score_data_frame.Training_topic.unique():
            score_data_frame_TP_FN_local = score_data_frame[score_data_frame['Training_topic'] == score_data_frame['Testing_topic']]
            score_data_frame_TP_FN_local = score_data_frame_TP_FN_local[score_data_frame_TP_FN_local['Training_topic'] == i]
            score_data_frame_TN_FP_local = score_data_frame[score_data_frame['Training_topic'] != score_data_frame['Testing_topic']]
            score_data_frame_TN_FP_local = score_data_frame_TN_FP_local[score_data_frame_TN_FP_local['Training_topic'] == i]
        
            local_TP_count = (score_data_frame_TP_FN_local['Score'] > threshold).sum()
            local_FN_count = (score_data_frame_TP_FN_local['Score'] < threshold).sum()
            
            local_TN_count = (score_data_frame_TN_FP_local['Score'] < threshold).sum()
            local_FP_count = (score_data_frame_TN_FP_local['Score'] > threshold).sum()
            
            local_precision = local_TP_count / (local_TP_count + local_FP_count)
            local_recall = local_TP_count / (local_TP_count + local_FN_count)
            local_result_str += "Topic {}: Precision: {}, Recall: {}\n".format(i, local_precision, local_recall) + \
            "Trup Positive: {}, False Positive: {}\n".format(local_TP_count, local_FP_count) + \
            "Trup Negative: {}, False Negative: {}\n\n".format(local_TN_count, local_FN_count)
            
        with open(storing_result_name_text, 'w') as f:
            result_str = "All: Precision: {}, Recall: {}\n".format(precision, recall) + \
            "Trup Positive: {}, False Positive: {}\n".format(Total_TP_count, Total_FP_count) + \
            "Trup Negative: {}, False Negative: {}\n\n".format(Total_TN_count, Total_FN_count) + local_result_str
            self.result_screen_text.configure(state='normal')
            self.result_screen_text.insert(tk.END, "".join(['*' for m in range(asterisk_len)]) + '\n')
            self.result_screen_text.insert(tk.END, result_str)
            self.result_screen_text.insert(tk.END, "".join(['*' for m in range(asterisk_len)]))
            self.result_screen_text.configure(state='disabled')
            f.write(result_str)
        
        with open(log_txt_name, 'w') as f:
            result_screen = self.result_screen_text.get("1.0", tk.END)
            f.write(result_screen)
        
    
            
class Asynchronous_CLDA_evaluation_class():
    
    def __init__(self):
        pass
    
    from nltk import wordpunct_tokenize, WordNetLemmatizer, sent_tokenize, pos_tag
    from nltk.corpus import stopwords, wordnet
    from string import punctuation
    import gc
    
    # initialize constants
    lemmatizer = WordNetLemmatizer()
    def define_sw(self):
        
        # Use default english stopword     
        return set(stopwords.words('english') + smart_stopwords)


    # Defining the lemmatizer
    def lemmatize(self,token, tag):
        tag = {
            'N': wordnet.NOUN,
            'V': wordnet.VERB,
            'R': wordnet.ADV,
            'J': wordnet.ADJ
        }.get(tag[0], wordnet.NOUN)
    
        return lemmatizer.lemmatize(token, tag)
    
    # The tokenizer for the documents
    def cab_tokenizer(self, document):
        tokens = []
        sw = self.define_sw()
        punct = set(punctuation)
    
        # split the document into sentences
        for sent in sent_tokenize(document):
            # tokenize each sentence
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                # preprocess and remove unnecessary characters
                token = token.lower()
                token = token.strip()
                token = token.strip('_')
                token = token.strip('*')
    
                # If punctuation, ignore token and continue
                if all(char in punct for char in token):
                    continue
    
                # If stopword, ignore token and continue
                if token in sw:
                    continue
    
                # Lemmatize the token and add back to the token
                lemma = self.lemmatize(token, tag)
    
                # Append lemmatized token to list
                tokens.append(lemma)
        return tokens        
    
    #    for training_file_head in training_head:
    def calculate_score_all_async(self, training_file_head, testing_dict):
#      T_TP = T_TN =  T_FN =  T_FP = 0
      #Listing the score
        sys.stdout = buffer = StringIO() 
        score_list = []
        files_test = []
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_test.extend(files)
          
        
        test_head = [x[:-len(file_name_df_suffix_csv)] for x in files_test if x.endswith(file_name_df_suffix_csv)]
          
        print("".join(['*' for m in range(asterisk_len)]))
        print("Training_topic: {}".format(training_file_head))
        print("".join(['*' for m in range(asterisk_len)]))
        
        test_concept_prob = None
            
        with open(dataset_dir + '/' + training_file_head + concept_prob_suffix_json, "r") as f:
            test_concept_prob = json.load(f)
            
        
        
        with open(dataset_dir + '/' + training_file_head + CLDA_suffix_pickle, "rb") as f:
            test_CLDA = pickle.load(f)
          
          
        doc_topic = test_CLDA.theta_set[0].sum(axis = 0)/test_CLDA.theta_set[0].shape[0]
        topic_concept = test_CLDA.show_and_construct_normalized_concept_topic_ranking()
        word_under_concept = test_CLDA.construct_word_concept_prob_under_concept(test_concept_prob)
    #        test_file_data = pd.read_csv(data_dir + '/' + test_name + file_name_df_suffix_csv, encoding='utf-8', sep=',', 
    #                            error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
       
        training_head_number = ''.join(filter(str.isdigit, training_file_head))
       
    #      vector_analysis = generate_vector_for_analysis()
        for testing_file_head in test_head:
            print("".join(['*' for m in range(asterisk_len)]))
            print("Test topic: {}".format(testing_file_head))
            print("".join(['*' for m in range(asterisk_len)]))
#            test_file_data = pd.read_csv(dataset_test + '/' + testing_file_head + file_name_df_suffix_csv,
#                                          encoding='utf-8', sep=',', error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
            test_file_data = testing_dict[testing_file_head]
            testing_head_number = ''.join(filter(str.isdigit, testing_file_head))
            for i in range(len(test_file_data)):
                score = 0
                test_files_feature_name  = test_file_data.iloc[i]['Text']
        #          _, test_files_feature_name   = vectorize_for_analysis(vector_analysis, test_file_data.iloc[i])
                for topic_num, topic_prob in enumerate(doc_topic):
                    for concept, concept_prob in topic_concept[topic_num]:
                        for word, word_prob in [(x[0], x[2]) for x in word_under_concept if x[1] == concept]:
                            if word in test_files_feature_name:
#                                  print('topic_num: {}, concept: "{}", word: "{}"'.format(topic_num, concept, word))
                                score += topic_prob * concept_prob * word_prob
            
                print('Score: {}, File name: "{}"'.format(score, test_file_data.iloc[i]['File']))
                score_list.append((test_file_data.iloc[i]['File'], training_head_number, testing_head_number, score))
        print("".join(['*' for m in range(asterisk_len)]))
        print("".join(['*' for m in range(asterisk_len)]))
        sys.stdout = sys.__stdout__
        return (score_list, buffer)
    
    def asynchronous_evaluation(self, testing_dict):
        files_training = []
        for dirpath, dirs, files in os.walk(dataset_dir):
                files_training.extend(files)
        
        # Walk down the files to search for
        # files to geenrate model
        training_head = [x[:-len(file_name_df_suffix_csv)] for x in files_training if x.endswith(file_name_df_suffix_csv)]


        
        # Core use
        # Asynchronically create the LDA object
        with Pool(cpu_count()-1) as p:
            pool_async = p.starmap_async(self.calculate_score_all_async, [[i, testing_dict] for i in training_head])
            gc.collect()
            # Return processed result
            return pool_async.get()
    
    def asynchronous_evaluation_LDA(self, testing_dict):
        files_training = []
        for dirpath, dirs, files in os.walk(dataset_dir):
                files_training.extend(files)
        
        # Walk down the files to search for
        # files to geenrate model
        training_head = [x[:-len(file_name_df_suffix_csv)] for x in files_training if x.endswith(file_name_df_suffix_csv)]


        
        # Core use
        # Asynchronically create the LDA object
        with Pool(cpu_count()-1) as p:
            pool_async = p.starmap_async(self.calculate_score_all_async_LDA, [[i, testing_dict] for i in training_head])
            gc.collect()
            # Return processed result
            return pool_async.get()
        
    
    def calculate_score_all_async_LDA(self, training_file_head, testing_dict):
        sys.stdout = buffer = StringIO() 
        score_list = []
        files_test = []
        for dirpath, dirs, files in os.walk(dataset_test):
            files_test.extend(files)
        test_head = [x[:-len(file_name_df_suffix_csv)] for x in files_test if x.endswith(file_name_df_suffix_csv)]
        
        print("".join(['*' for m in range(asterisk_len)]))
        print("Training_topic: {}".format(training_file_head))
        print("".join(['*' for m in range(asterisk_len)]))
            
        
        with open(dataset_dir + '/' + training_file_head + LDA_suffix_pickle, "rb") as f:
            test_LDA = pickle.load(f)
          
        doc_topic = test_LDA.doc_prob_set[0].sum(axis = 0)/test_LDA.doc_prob_set[0].shape[0]
        # Extract rank  = 10
        word_topic_prob = test_LDA.generate_word_prob()
        
        training_head_number = ''.join(filter(str.isdigit, training_file_head))
        for testing_file_head in test_head:
            test_file_data = pd.read_csv(dataset_test + '/' + testing_file_head + file_name_df_suffix_csv,
                                         encoding='utf-8', sep=',', error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
            test_file_data = testing_dict[testing_file_head]
            testing_head_number = ''.join(filter(str.isdigit, testing_file_head))
            print("".join(['*' for m in range(asterisk_len)]))
            print("Test topic: {}".format(testing_file_head))
            print("".join(['*' for m in range(asterisk_len)]))

            for i in range(len(test_file_data)):
                score = 0
                test_files_feature_name  = test_file_data.iloc[i]['Text']
    #          _, test_files_feature_name   = vectorize_for_analysis(vector_analysis, test_file_data.iloc[i])
                for topic_num, topic_prob in enumerate(doc_topic):
                    for word, word_prob in [(x[1], x[2]) for x in word_topic_prob if x[0] == topic_num]:
                        if word in test_files_feature_name:
                            score += topic_prob * word_prob
                         
                print('Score: {}, File name: "{}"'.format(score, test_file_data.iloc[i]['File']))
                score_list.append((test_file_data.iloc[i]['File'], training_head_number, testing_head_number, score)) 
        print("".join(['*' for m in range(asterisk_len)]))
        print("".join(['*' for m in range(asterisk_len)]))    
        sys.stdout = sys.__stdout__
        
        return (score_list, buffer)
    
    
    def tokenization_test(self, testing_file_head):
        wn.ensure_loaded()
        
        testing_dict = {}
        testing_dict[testing_file_head] = pd.read_csv(dataset_test + '/' + testing_file_head + file_name_df_suffix_csv,
                                          encoding='utf-8', sep=',', error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
        testing_dict[testing_file_head]['Text'] = testing_dict[testing_file_head]['Text'].apply(lambda x: self.cab_tokenizer(x))
        file_name = dataset_test + '/' + testing_file_head + tokenized_dataset_suffix
        testing_dict[testing_file_head].to_csv(file_name,
                              index=False, encoding='utf-8',
                              quoting=csv.QUOTE_ALL)
        return testing_dict
    
    def asynchronous_tokenization(self):
        files_test = []
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_test.extend(files)
        
        
        
        test_head = [x[:-len(file_name_df_suffix_csv)] for x in files_test if x.endswith(file_name_df_suffix_csv)]
        
        tokenized_result = None
        with Pool(cpu_count()-1) as p:
            pool_async = p.starmap_async(self.tokenization_test, [[i] for i in test_head])
           
            
            tokenized_result = pool_async.get()
        final_dict = {}
        
        
        for i in tokenized_result:
            final_dict.update(i)
        gc.collect()    
        return final_dict
        
def main():
    
    CLDA_evaluation_screen()
    
if __name__ == "__main__":
    main()