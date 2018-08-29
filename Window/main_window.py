# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 21:45:47 2018

@author: Shotaro Baba
"""
#Reading all necessary packages

#Import all necessary packages.
import tkinter as tk
import os
import time
import xml.etree.ElementTree as ET
import pandas as pd 
from tkinter.filedialog import askdirectory
import csv
import pickle
import itertools

import nltk
from nltk import wordpunct_tokenize, WordNetLemmatizer, sent_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer

import asyncio
import concurrent.futures
import requests

lemmatizer = WordNetLemmatizer()
dataset_dir = "../../CLDA_data_training"
dataset_test = "../../CLDA_data_testing"
#Download all necessary nltk download
#components
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
#Create main menu            
#Defining the lemmatizer

def define_sw():
    
    return set(stopwords.words('english'))# + stop_words)

def lemmatize(token, tag):
    tag = {
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV,
        'J': wordnet.ADJ
    }.get(tag[0], wordnet.NOUN)

    return lemmatizer.lemmatize(token, tag)

#The tokenizer for the documents
def cab_tokenizer(document):
    tokens = []
    sw = define_sw()
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
            lemma = lemmatize(token, tag)

            # Append lemmatized token to list
            tokens.append(lemma)
    return tokens



#Create vectorise files
#Define the function here
#Generate vector for creating the data
def generate_vector():
    return CountVectorizer(tokenizer=cab_tokenizer, ngram_range=[1,2],
                           min_df=0.02, max_df=0.98)

#Generate count vectorizer
def vectorize(tf_vectorizer, df):
    #Generate_vector
    #df = df.reindex(columns=['text'])  # reindex on tweet

    tf_matrix = tf_vectorizer.fit_transform(df['Text'])
    tf_feature_names = tf_vectorizer.get_feature_names()

    return tf_matrix, tf_feature_names


#Retrieve the text file from the files
def generate_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield (path + '\\' + file)

#Returns texts in the xml documents 
def return_text(path, path_string, x):
    file = path + '/' + path_string + '/' +str(x) + ".xml"
    tree = ET.parse(file)
    root = tree.getroot()
    result = ''
    for element in root.iter():
        if(element.text != None):
            result += element.text + ' '
    result = result[:-1]
    
    with open(file + ".txt", "w", encoding = 'utf-8') as f:
        f.write(result)
        
    return result

#Read all files in the training dataset


#Read the test files for the test purpose
def read_test_files():
    for_test_purpose_data = pd.DataFrame([], columns=['File', 'Text'])
    training_path = []

    #Creating 
    test_path = "../../R8-Dataset/Dataset/ForTest"
    for dirpath, dirs, files in os.walk(test_path):
        training_path.extend(files)
    
    #Remove the files other than xml files
    training_path = [x for x in training_path if x.endswith('xml')]
    #Remove the path where the 
    #Extract only last directory name
#    for_test_purpose_data = {}
#    training_data_list = []
    for path_to_file in training_path:
        path_string = os.path.basename(os.path.normpath(path_to_file))        
        #training_data_list.append(path_string)
        #Initialise the list of the strings
        #for_test_purpose_data[path_string] = {}
        
        file = test_path + '/' + path_string 
        tree = ET.parse(file)
        
        #Turn the string into
        root = tree.getroot()
        result = ''
        #Retrieving the text from xml files
        for element in root.iter():
            if(element.text != None):
                result += element.text + ' '
        result = result[:-1] #Removing the space
        
                
        #Initialise 
#        for file in generate_files(path):
            #print("Now reading...")
            #print(open(file, "r").read())

        
        for_test_purpose_data = for_test_purpose_data.append(pd.DataFrame([(os.path.basename((path_string)), result)], 
                                                                            columns=['File', 'Text']))
    
    return for_test_purpose_data


#Create the test vectors 


#Root class for the application 
class Application():
    
        
    def __init__(self):
        self.root = tk.Tk()
#        self.pack()
        self.start_menu()
        
        '''
        Training part
        '''
        #The list of the files for the upload
        self.upload_file_list_labelling = []
        self.upload_file_list_classifier = []
        
        self.linked_folders = []
        self.folder_directory = None
        self.document_data = []
        
        '''
        List all LDA and CLDA list to
        the values
        '''
        self.folder_name_list = []
        
        
        self.LDA_model_list = []
        
        #The generation of CLDA model list
        #Later this will be used for generating results
        
        self.CLDA_model_list = []
        self.LDA_model_list = []
        
        #Initialisation of the topic feature concept list by retrieving the data from
        #the documents
        
        '''
        Testing part
        '''
       
        #The list of the files for the upload
        self.upload_file_list_labelling_test = []
        self.upload_file_list_classifier_test = []
        
        self.linked_folders_test = []
        self.folder_directory_test = None
        self.document_data_test = []
        
        '''
        List all LDA and CLDA list to
        the values
        '''
        self.folder_name_list_test = []
        
        
        self.LDA_model_list_test = []
        
        #The generation of CLDA model list
        #Later this will be used for generating results
        
        self.CLDA_model_list_test = []
        self.LDA_model_list_test = []
        
        
        
        
        self.retrieve_topic_feature_concept_list()
        
        self.root.mainloop()
        
        
    def start_menu(self):
        
        #Bring all the frame which include all the Listbox frame together
        '''
        ##############################################################################
        ###Main frame
        ##############################################################################
        '''
        self.main_group = tk.Frame(self.root)
        self.main_group.pack()
        
        self.main_listbox_and_buttons = tk.Frame(self.main_group)
        self.main_listbox_and_buttons.pack(side = tk.LEFT)
        
        self.result_box = tk.Frame(self.main_group)
        self.result_box.pack(side = tk.RIGHT, anchor = tk.N)
        
        self.main_listbox_and_result = tk.Frame(self.main_listbox_and_buttons)
        self.main_listbox_and_result.pack()
        
        '''
        #######################################
        ####Folder selection & feature generation part
        #######################################
        '''
        
        #Main frame of the selection
        self.frame_for_folder_selection = tk.Frame(self.main_listbox_and_result)
        self.frame_for_folder_selection.pack(side = tk.LEFT)
        
        self.user_drop_down_select_folder_label = tk.Label(self.frame_for_folder_selection , text = "Folder (Topic)\nSelection")
        self.user_drop_down_select_folder_label.pack()
        
        self.frame_for_drop_down_menu_folder = tk.Frame(self.frame_for_folder_selection)
        self.frame_for_drop_down_menu_folder.pack()
        
        self.scrollbar_drop_down_menu_file = tk.Scrollbar(self.frame_for_drop_down_menu_folder, orient = "vertical")
        self.scrollbar_drop_down_menu_file.pack(side = tk.RIGHT, fill = 'y')
        
        self.user_drop_down_select_folder_list = tk.Listbox(self.frame_for_drop_down_menu_folder, exportselection=0)
        self.user_drop_down_select_folder_list.pack(side = tk.LEFT, fill = 'y')
        self.user_drop_down_select_folder_list['yscrollcommand'] = \
        self.scrollbar_drop_down_menu_file.set
        self.scrollbar_drop_down_menu_file['command'] = self.user_drop_down_select_folder_list.yview
        
        
        
        
        '''
        #######################################
        ####Folder selection & feature generation part end
        #######################################
        '''
        
        '''
        #######################################
        ####Result screen
        #######################################
        '''
        self.folder_selection_result_frame = tk.Frame(self.result_box)
        self.folder_selection_result_frame.pack(side = tk.LEFT, anchor = tk.N)
        
        self.user_drop_down_file_selection_results_label = tk.Label(self.folder_selection_result_frame,
                                                                    text = "Selection & Processing Result")
        
        self.user_drop_down_file_selection_results_label.pack(side = tk.TOP) 
        
        self.user_drop_down_folder_selection_results_frame = tk.Frame(self.folder_selection_result_frame)
        self.user_drop_down_folder_selection_results_frame.pack()
        
        
        self.user_drop_down_folder_selection_results_scroll_bar = \
        tk.Scrollbar(self.user_drop_down_folder_selection_results_frame, orient = "vertical")
        self.user_drop_down_folder_selection_results_scroll_bar.pack(side = tk.RIGHT, fill = 'y')
        
        self.user_drop_down_folder_selection_results_scroll_list = tk.Text(self.user_drop_down_folder_selection_results_frame)
        self.user_drop_down_folder_selection_results_scroll_list.pack(side = tk.LEFT)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
        self.user_drop_down_folder_selection_results_scroll_list['yscrollcommand'] = \
        self.user_drop_down_folder_selection_results_scroll_bar.set
        
        self.user_drop_down_folder_selection_results_scroll_bar['command'] = \
        self.user_drop_down_folder_selection_results_scroll_list.yview
        '''
        #######################################
        ####Result screen END
        #######################################
        '''
        
        
        '''
        #######################################
        ####Word vector generation part
        ####Already created list part
        #######################################
        '''
        self.word_vector_generation_list_frame = tk.Frame(self.main_listbox_and_result)
        self.word_vector_generation_list_frame.pack(side = tk.LEFT, anchor = tk.N)
        
        self.drop_down_list_word_vector_label = tk.Label(self.word_vector_generation_list_frame,
                                                         text = "Word Vector\nCreated List")
        self.drop_down_list_word_vector_label.pack()
        
        self.drop_down_list_word_vector_frame = tk.Frame(self.word_vector_generation_list_frame)
        self.drop_down_list_word_vector_frame.pack()
        
        self.drop_down_list_word_vector_list = tk.Listbox(self.drop_down_list_word_vector_frame,
                                                          exportselection = 0)
        
        self.drop_down_list_word_vector_list.pack(side = tk.LEFT, fill = 'y')
        
        self.drop_down_list_word_vector_bar = tk.Scrollbar(self.drop_down_list_word_vector_frame, orient = "vertical")
        self.drop_down_list_word_vector_bar.pack(side = tk.RIGHT, fill = 'y')
        
        self.drop_down_list_word_vector_list['yscrollcommand'] = \
        self.drop_down_list_word_vector_bar.set
        
        self.drop_down_list_word_vector_bar['command'] = \
        self.drop_down_list_word_vector_list.yview
        
        '''
        #######################################
        ####Word vector generation part end
        #######################################
        '''
        
        '''
        #######################################
        ####Concept word probabilities creation part
        ####
        #######################################
        '''
        self.concept_prob_generation_list_frame = tk.Frame(self.main_listbox_and_result)
        self.concept_prob_generation_list_frame.pack(side = tk.LEFT, anchor = tk.N)
        
        self.drop_down_concept_prob_vector_label = tk.Label(self.concept_prob_generation_list_frame,
                                                         text = "Concept Prob\nCreated List")
        self.drop_down_concept_prob_vector_label.pack()
        
        self.drop_down_concept_prob_vector_frame = tk.Frame(self.concept_prob_generation_list_frame)
        self.drop_down_concept_prob_vector_frame.pack()
        
        self.drop_down_concept_prob_vector_list = tk.Listbox(self.drop_down_concept_prob_vector_frame,
                                                          exportselection = 0)
        
        self.drop_down_concept_prob_vector_list.pack(side = tk.LEFT, fill = 'y')
        
        self.drop_down_concept_prob_vector_bar = tk.Scrollbar(self.drop_down_concept_prob_vector_frame, orient = "vertical")
        self.drop_down_concept_prob_vector_bar.pack(side = tk.RIGHT, fill = 'y')
        
        self.drop_down_concept_prob_vector_list['yscrollcommand'] = \
        self.drop_down_concept_prob_vector_bar.set
        
        self.drop_down_concept_prob_vector_bar['command'] = \
        self.drop_down_concept_prob_vector_list.yview
        
        '''
        #######################################################################################
        ###Retrieving the test data part 
        #######################################################################################

        '''
        self.main_listbox_and_result_test = tk.Frame(self.main_listbox_and_buttons)
        self.main_listbox_and_result_test.pack()
        
        
       
        '''
        #######################################
        ####Folder selection (test)
        #######################################
        '''
        
        self.frame_for_folder_selection_test = tk.Frame(self.main_listbox_and_result_test )
        self.frame_for_folder_selection_test.pack(side = tk.LEFT)
        
        self.user_drop_down_select_folder_label_test = tk.Label(self.frame_for_folder_selection_test , text = "Folder (Topic)\nSelection")
        self.user_drop_down_select_folder_label_test.pack()
        
        self.frame_for_drop_down_menu_folder_test = tk.Frame(self.frame_for_folder_selection_test)
        self.frame_for_drop_down_menu_folder_test.pack()
        
        self.scrollbar_drop_down_menu_file_test = tk.Scrollbar(self.frame_for_drop_down_menu_folder_test, orient = "vertical")
        self.scrollbar_drop_down_menu_file_test.pack(side = tk.RIGHT, fill = 'y')
        
        self.user_drop_down_select_folder_list_test = tk.Listbox(self.frame_for_drop_down_menu_folder_test, exportselection=0)
        self.user_drop_down_select_folder_list_test.pack(side = tk.LEFT)
        self.user_drop_down_select_folder_list_test['yscrollcommand'] = \
        self.scrollbar_drop_down_menu_file_test.set
        self.scrollbar_drop_down_menu_file_test['command'] = self.user_drop_down_select_folder_list_test.yview
        

        
        '''
        #######################################
        ####Feature vector extraction
        #######################################
        '''
        
        self.word_vector_generation_list_frame_test = tk.Frame(self.main_listbox_and_result_test)
        self.word_vector_generation_list_frame_test.pack(side = tk.LEFT, anchor = tk.N)
        
        self.drop_down_list_word_vector_label_test = tk.Label(self.word_vector_generation_list_frame_test,
                                                         text = "Word Vector\nCreated List (Test)")
        self.drop_down_list_word_vector_label_test.pack()
        
        self.drop_down_list_word_vector_frame_test = tk.Frame(self.word_vector_generation_list_frame_test)
        self.drop_down_list_word_vector_frame_test.pack()
        
        self.drop_down_list_word_vector_list_test = tk.Listbox(self.drop_down_list_word_vector_frame_test,
                                                          exportselection = 0)
        
        self.drop_down_list_word_vector_list_test.pack(side = tk.LEFT, fill = 'y')
        
        self.drop_down_list_word_vector_bar_test = tk.Scrollbar(self.drop_down_list_word_vector_frame_test, orient = "vertical")
        self.drop_down_list_word_vector_bar_test.pack(side = tk.RIGHT, fill = 'y')
        
        self.drop_down_list_word_vector_list_test['yscrollcommand'] = \
        self.drop_down_list_word_vector_bar_test.set
        
        self.drop_down_list_word_vector_bar_test['command'] = \
        self.drop_down_list_word_vector_list_test.yview
    
        
        '''
        #######################################
        ####Concpet-word vector extraction
        #######################################
        '''
        
        self.concept_prob_generation_list_frame_test = tk.Frame(self.main_listbox_and_result_test)
        self.concept_prob_generation_list_frame_test.pack(side = tk.LEFT, anchor = tk.N)
        
        self.drop_down_concept_prob_vector_label_test = tk.Label(self.concept_prob_generation_list_frame_test,
                                                         text = "Concept Prob\nCreated List (Test)")
        self.drop_down_concept_prob_vector_label_test.pack()
        
        self.drop_down_concept_prob_vector_frame_test = tk.Frame(self.concept_prob_generation_list_frame_test)
        self.drop_down_concept_prob_vector_frame_test.pack()
        
        self.drop_down_concept_prob_vector_list_test = tk.Listbox(self.drop_down_concept_prob_vector_frame_test,
                                                          exportselection = 0)
        
        self.drop_down_concept_prob_vector_list_test.pack(side = tk.LEFT, fill = 'y')
        
        self.drop_down_concept_prob_vector_bar_test = tk.Scrollbar(self.drop_down_concept_prob_vector_frame_test, orient = "vertical")
        self.drop_down_concept_prob_vector_bar_test.pack(side = tk.RIGHT, fill = 'y')
        
        self.drop_down_concept_prob_vector_list_test['yscrollcommand'] = \
        self.drop_down_concept_prob_vector_bar_test.set
        
        self.drop_down_concept_prob_vector_bar_test['command'] = \
        self.drop_down_concept_prob_vector_list_test.yview
        
        
        '''
        ################################################################################
        ###End of retrieving the test data part 
        ################################################################################
        '''
        
        #Forming the button group for putting them together
        self.button_groups = tk.Frame(self.main_listbox_and_buttons)
        self.button_groups.pack()
        
        
        '''
        #######################################
        ###Training data generation button
        #######################################
        '''
        
        self.button_for_training = tk.Frame(self.button_groups)
        self.button_for_training.pack(side = tk.LEFT)        
        
        self.user_drop_down_select_folder_buttom = tk.Button(self.button_for_training , text = "Select Folder\n(Training)")
        self.user_drop_down_select_folder_buttom.pack()
        self.user_drop_down_select_folder_buttom['command'] = self.select_folder_and_extract_xml
        
        self.user_drop_down_select_folder_button_create_vector = tk.Button(self.button_for_training ,
                                                                           text = "Create Feature\nVector(s) (Training)")
        self.user_drop_down_select_folder_button_create_vector.pack()
        self.user_drop_down_select_folder_button_create_vector['command'] = self.create_feature_vector
        
        self.user_drop_down_select_folder_button_create_concept_prob = tk.Button(self.button_for_training,
                                                                           text = "Create Concept\nProb(s) (Training)")
        self.user_drop_down_select_folder_button_create_concept_prob.pack()
        self.user_drop_down_select_folder_button_create_concept_prob['command'] = self.create_concept_matrix
        
        self.exit_button = tk.Button(self.root, text = 'quit')
        
        '''
        #######################################
        ###Testing data generation button
        #######################################
        '''
        
        self.button_for_test = tk.Frame(self.button_groups)
        self.button_for_test.pack(side = tk.LEFT)        
        
        self.user_drop_down_select_folder_buttom_test = tk.Button(self.button_for_test , text = "Select Folder\n(Tesing)")
        self.user_drop_down_select_folder_buttom_test.pack()
        self.user_drop_down_select_folder_buttom_test['command'] = self.select_folder_and_extract_xml_test
        
        self.user_drop_down_select_folder_button_create_vector_test = tk.Button(self.button_for_test ,
                                                                           text = "Create Feature\nVector(s) (Tesing)")
        self.user_drop_down_select_folder_button_create_vector_test.pack()
        self.user_drop_down_select_folder_button_create_vector_test['command'] = self.create_feature_vector_test
        
        self.user_drop_down_select_folder_button_create_concept_prob_test = tk.Button(self.button_for_test,
                                                                           text = "Create Concept\nProb(s) (Tesing)")
        self.user_drop_down_select_folder_button_create_concept_prob_test.pack()
        self.user_drop_down_select_folder_button_create_concept_prob_test['command'] = self.create_concept_matrix_test
        
        '''
        ##########################################
        ###Quit button.
        ##########################################
        '''
        
        
        self.exit_button = tk.Button(self.root, text = 'quit')
        
        self.exit_button.pack(side = tk.BOTTOM)
        self.exit_button['command'] = self.root.destroy
        
        self.test_button = tk.Button(self.root, text = 'test')
        
        self.test_button.pack(side = tk.BOTTOM)
        self.test_button['command'] = self.asynchronous_training_topic_concept_retrieval
       
        self.test_button = tk.Button(self.root, text = 'test2')
        
        self.test_button.pack(side = tk.BOTTOM)
        self.test_button['command'] = self.asynchronous_testing_topic_concept_retrieval
        
        
        '''
        #######################################
        ####End the main menu
        #######################################
        '''
        
    def retrieve_topic_feature_concept_list(self):
        files_tmp = []
        files_tmp_test = []
        for dirpath, dirs, files in os.walk(dataset_dir):
            files_tmp.extend(files)
#        print(files_tmp)
            #only retrieve the files_tmp which end with .csv
            #Initialise the topic list
        self.topic_list = [x for x in files_tmp if x.endswith('.csv')]
        for i in self.topic_list:
            self.user_drop_down_select_folder_list.insert(tk.END, i)
        #Initialise the features_list
        #Extract feature files from the file lists
        #No need to sort the values as the files are already sorted by names
        self.feature_list = [x for x in files_tmp if x.endswith('_f.pkl')]
        
        for i in self.feature_list:
            self.drop_down_list_word_vector_list.insert(tk.END, i)
        
        self.concept_list = [x for x in files_tmp if x.endswith('_c.pkl')]
        
        for i in self.concept_list:
            self.drop_down_concept_prob_vector_list.insert(tk.END, i)
            
        
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_tmp_test.extend(files)
#        print(files_tmp_test)
            #only retrieve the files_tmp_test which end with .csv
            #Initialise the topic list
        self.topic_list_test = [x for x in files_tmp_test if x.endswith('.csv')]
        
        for i in self.topic_list_test:
            self.user_drop_down_select_folder_list_test.insert(tk.END, i)
        #Initialise the features_list
        #Extract feature files from the file lists
        #No need to sort the values as the files are already sorted by names
        self.feature_list_test = [x for x in files_tmp_test if x.endswith('_f.pkl')]
        
        for i in self.feature_list_test:
            self.drop_down_list_word_vector_list_test.insert(tk.END, i)
        
        self.concept_list_test = [x for x in files_tmp_test if x.endswith('_c.pkl')]
        
        for i in self.concept_list_test:
            self.drop_down_concept_prob_vector_list_test.insert(tk.END, i)
            
    #Select the folder and extract the information
    def select_folder_and_extract_xml(self, ask_folder = None):
        if(ask_folder == None):
            self.folder_directory = askdirectory()
        else:
            self.folder_directory = ask_folder
        
#        self.folder_name = "C:/Users/n9648852/Desktop/New folder for project/RCV1/Training/Training101"        
        
#        folder_name = os.path.basename("C:/Users/n9648852/Desktop/New folder for project/RCV1/Training/Training101")
        temp_substr = os.path.basename(self.folder_directory)
            
        #If the processed file has already exists, then the process of the
        #topics will stop.
        if any(temp_substr in string for string in self.topic_list):
            self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "Topic already exists") 
            return 
        
        for_test_purpose_data = pd.DataFrame([], columns=['File','Topic', 'Text'])
        self.training_path = []
        
        for dirpath, dirs, files in os.walk(self.folder_directory):
            self.training_path.extend(files)
    
        #Remove the files other than xml files
        self.training_path = [x for x in self.training_path if x.endswith('xml')]
        print(self.training_path)
        topic_name = os.path.basename(self.folder_directory)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        for path_to_file in self.training_path:
            path_string = os.path.basename(os.path.normpath(path_to_file)) 
            
            #Extract xml information from the files
            #then it construct the information
            file = self.folder_directory + '/' + path_string 
            tree = ET.parse(file)
            root = tree.getroot()
            result = ''
            for element in root.iter():
                if(element.text != None):
                    result += element.text + ' '
            #Remove the remained data
            result = result[:-1]
            
            name_of_the_file = (os.path.basename(path_string))
            
            for_test_purpose_data = for_test_purpose_data.append(pd.DataFrame([(name_of_the_file, 
                                                                               topic_name,
                                                                               result)], 
            columns=['File','Topic', 'Text']))
            if not os.path.isdir(dataset_dir):
                os.makedirs(dataset_dir)
            
            self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "{} has been read.\n".format(name_of_the_file))
        for_test_purpose_data.to_csv(dataset_dir + '/' +
                          topic_name + ".csv",
                          index=False, encoding='utf-8',
                          quoting=csv.QUOTE_ALL)
        #print(for_test_purpose_data)
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "File read complete!\n")
        
        #Adding already created data lists
        self.user_drop_down_select_folder_list.insert(tk.END, 
                                                          topic_name + ".csv")
        
        self.document_data.append(for_test_purpose_data)
        
        self.topic_list.append(topic_name + ".csv")
        
        #Sort the data list after appending csv file
        self.topic_list = sorted(self.topic_list)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
    
    def select_folder_and_extract_xml_async(self,ask_folder, topic_list, dataset_dir):
  
        folder_directory = ask_folder
        
#        self.folder_name = "C:/Users/n9648852/Desktop/New folder for project/RCV1/Training/Training101"        
        
#        folder_name = os.path.basename("C:/Users/n9648852/Desktop/New folder for project/RCV1/Training/Training101")
        temp_substr = os.path.basename(folder_directory)
            
        #If the processed file has already exists, then the process of the
        #topics will stop.
        if any(temp_substr in string for string in topic_list):
            print("topic already exist.")
            return 
        
        for_test_purpose_data = pd.DataFrame([], columns=['File','Topic', 'Text'])
        
        training_path = []
        for dirpath, dirs, files in os.walk(folder_directory):
            training_path.extend(files)
    
        #Remove the files other than xml files
        training_path = [x for x in training_path if x.endswith('xml')]
        print(training_path)
        topic_name = os.path.basename(folder_directory)
       
        for path_to_file in training_path:
            path_string = os.path.basename(os.path.normpath(path_to_file)) 
            
            #Extract xml information from the files
            #then it construct the information
            file = folder_directory + '/' + path_string 
            tree = ET.parse(file)
            root = tree.getroot()
            result = ''
            for element in root.iter():
                if(element.text != None):
                    result += element.text + ' '
            #Remove the remained data
            result = result[:-1]
            
            name_of_the_file = (os.path.basename(path_string))
            
            for_test_purpose_data = for_test_purpose_data.append(pd.DataFrame([(name_of_the_file, 
                                                                               topic_name,
                                                                               result)], 
            columns=['File','Topic', 'Text']))
            if not os.path.isdir(dataset_dir):
                os.makedirs(dataset_dir)
        if(len(for_test_purpose_data) != 0):
            for_test_purpose_data.to_csv(dataset_dir + '/' +
                              topic_name + ".csv",
                              index=False, encoding='utf-8',
                              quoting=csv.QUOTE_ALL)
            
            return topic_name + ".csv"
    #Retrieving topic list
    
    #Based on the files_tmp made by the vectors 
    #Depending on what test vector u used 
    #The contents of the vector can be changed 
    def create_feature_vector(self):
        
        files_tmp = []
        
        for dirpath, dirs, files in os.walk(dataset_dir):
            files_tmp.extend(files)
        
        #Extract only the csv files and remove extension!
        files_tmp = [os.path.splitext(x)[0] for x in files_tmp if x.endswith('.csv')]
        
        
        for file_string in files_tmp:
            if any(file_string in substring for substring in self.feature_list):
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
                self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                                "Feature {} already exists.\n".format(file_string +  '_c.pkl'))
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
                print("Feature {} already exists".format(file_string +  '_f.pkl'))
            else:
                #Read csv files 
                datum = pd.read_csv(dataset_dir + '/' +file_string + '.csv', encoding='utf-8', sep=',', 
                            error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
                #Vectorise the document 
                vect = generate_vector()
                vectorized_data, feature_names = vectorize(vect, datum)
                
                with open(dataset_dir + '/' + file_string + '_f.pkl', "wb") as f:
                    pickle.dump([vectorized_data, feature_names], f)
                
                self.drop_down_list_word_vector_list.insert(tk.END, file_string + '_f.pkl')
                self.feature_list.append(file_string + '_f.pkl')
        
        #Sort feature list after appending some elements
        self.feature_list = sorted(self.feature_list)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, "Complete {} feature generation.\n".format(file_string))
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
    
    
    
    #Asynchoronic feature vector retrieval
    def create_feature_vector_async(self, file_string, feature_list, dataset_dir):
        
        file_string = os.path.splitext(os.path.basename(file_string))[0]
        if any(file_string in substring for substring in feature_list):
            print("Feature {} already exists".format(file_string +  '_f.pkl'))
            return None
        else:
            #Read csv files 
            datum = pd.read_csv(dataset_dir + '/' + file_string + '.csv', encoding='utf-8', sep=',', 
                        error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
            
            #Vectorise the document 
            vect = generate_vector()
            vectorized_data, feature_names = vectorize(vect, datum)
            
            with open(dataset_dir + '/' + file_string + '_f.pkl', "wb") as f:
                pickle.dump([vectorized_data, feature_names], f)
            return file_string + '_f.pkl'
            


    def retrieve_data(feature_name, K = 10):
        print('Now processing ' + str(feature_name) + " word...")

        #Replace space to + to tolerate the phrases with space
        req_str = 'https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance=' \
        + feature_name.replace(' ', '+') + '&topK=' + str(K)
        response = requests.get(req_str)
        
        #Retrieve the response from json file
        return response.json()
    
    
    #Data directory and object should be in arguments to 
    #optimise the data
    def create_concept_matrix(self):
        
        files_tmp = []
        
        #Checking entire files in the text
        for dirpath, dirs, files in os.walk(dataset_dir):
            files_tmp.extend(files) 
        rem_len = -len('_f.pkl')
        #Check whether the concept file(s) exist(s)
        files_tmp = [x[:rem_len] for x in files_tmp if x.endswith('_f.pkl')]
#        "ssss"[3:4]
        
        #Define the methods for generating functions
        #Retrieve the concept data asynchonically
        #to retrieve the data simultaneously
        async def retrieve_word_concept_data(feature_names, K = 20):
            with concurrent.futures.ThreadPoolExecutor(max_workers=220) as executor:
                collection_of_results = []
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        requests.get, 
                        'https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance=' +
                        i.replace(' ', '+') + 
                        '&topK=' + str(K)
                    )
                    for i in feature_names
                ]
                for response in await asyncio.gather(*futures):
                    collection_of_results.append(response.json())
                
                return collection_of_results
        
        for file_string in files_tmp:
            #Check whether the test subject exists or no
            if any(file_string in substring for substring in self.concept_list):
                #Feature already exists
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
                self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                                "Concept {} already exists.\n".format(file_string +  '_c.pkl'))
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
                print("Feature {} already exists".format(file_string +  '_c.pkl'))
            else:
                p_e_c  = {}

                feature_names = None                    
                with open(dataset_dir + '/' + file_string + '_f.pkl', "rb") as f:
                     _, feature_names = pickle.load(f)
                
                
                #Sort the feature names just in case...
                feature_names = sorted(feature_names)
                '''
                #Retrieve the tenth rankings of the words
                
                #K needed to be adjustable so that the
                #Researcher can find the characteristics of
                #all values!
                '''
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(retrieve_word_concept_data(feature_names))
                results = loop.run_until_complete(future)
                
                #temporary
                for idx, i  in enumerate(feature_names):
                #    print(i)
                #    print(idx)
                    p_e_c[i] = results[int(idx)]
                
#                print(p_e_c)
#                temp = {}
#                type(temp) == dict
                #List up the concept names
                
                l = [list(i.keys()) for i in list(p_e_c.values())]
                concept_names = sorted(list(set(itertools.chain.from_iterable(l))))
                
                #    concept_sets[len(concept_sets)-1]
                #Put the atom concept if there are no concepts in the words
                
                
                #Adding atomic elements
                for i in feature_names:
                    #if there are no concepts in the words, then...
                    if p_e_c[i] == {}:
                        
                        #Append the words with no related concpets
                        #as the atomic concepts
                        concept_names.append(i)
#                    else:
                        
                #Sorting the concept_names after adding feature names
                concept_names = sorted(concept_names)

                
                with open(dataset_dir + '/' + file_string +  '_c.pkl', "wb") as f:
                    pickle.dump([p_e_c, concept_names], f)
                    
                self.concept_list.append(file_string +  '_c.pkl')
                self.drop_down_concept_prob_vector_list.insert(tk.END, file_string +  '_c.pkl')
        
        #Sort after adding all values
        self.concept_list = sorted(self.concept_list)
#        for i in self.feature_list:
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, "Complete {} concept generation.\n".format(file_string))
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
#   
    def create_concept_matrix_async(self, file_string, concept_list, dataset_dir):

        async def retrieve_word_concept_data(feature_names, K = 20):
            with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
                collection_of_results = []
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        requests.get, 
                        'https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance=' +
                        i.replace(' ', '+') + 
                        '&topK=' + str(K)
                    )
                    for i in feature_names
                ]
                for response in await asyncio.gather(*futures):
                    collection_of_results.append(response.json())
                
                return collection_of_results
        
        file_string = os.path.splitext(os.path.basename(file_string))[0]
        #Check whether the test subject exists or no
        if any(file_string in substring for substring in concept_list):
            #Feature already exists
            print("Feature {} already exists".format(file_string +  '_c.pkl'))
        else:
            p_e_c  = {}

            feature_names = None                    
            with open(dataset_dir + '/' + file_string + '_f.pkl', "rb") as f:
                 _, feature_names = pickle.load(f)
            
            
            #Sort the feature names just in case...
            feature_names = sorted(feature_names)
            '''
            #Retrieve the tenth rankings of the words
            
            #K needed to be adjustable so that the
            #Researcher can find the characteristics of
            #all values!
            '''
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(retrieve_word_concept_data(feature_names))
            results = loop.run_until_complete(future)
            
            #temporary
            for idx, i  in enumerate(feature_names):
            #    print(i)
            #    print(idx)
                p_e_c[i] = results[int(idx)]
            
#                print(p_e_c)
#                temp = {}
#                type(temp) == dict
            #List up the concept names
            
            l = [list(i.keys()) for i in list(p_e_c.values())]
            concept_names = sorted(list(set(itertools.chain.from_iterable(l))))
            
            #    concept_sets[len(concept_sets)-1]
            #Put the atom concept if there are no concepts in the words
            
            
            #Adding atomic elements
            for i in feature_names:
                #if there are no concepts in the words, then...
                if p_e_c[i] == {}:
                    
                    #Append the words with no related concpets
                    #as the atomic concepts
                    concept_names.append(i)
#                    else:
                    
            #Sorting the concept_names after adding feature names
            concept_names = sorted(concept_names)

            
            with open(dataset_dir + '/' + file_string +  '_c.pkl', "wb") as f:
                pickle.dump([p_e_c, concept_names], f)
                
            return file_string +  '_c.pkl'
            
#        for i in self.feature_list:

             
    #Selecting test directory
    def select_folder_and_extract_xml_test(self, ask_folder = None):
        if(ask_folder == None):
            self.folder_directory = askdirectory()
        else:
            self.folder_directory = ask_folder
        self.folder_directory_test = askdirectory()
#        self.folder_name = "C:/Users/n9648852/Desktop/New folder for project/RCV1/Training/Training101"        
        
#        folder_name = os.path.basename("C:/Users/n9648852/Desktop/New folder for project/RCV1/Training/Training101")
        temp_substr = os.path.basename(self.folder_directory_test)
            
        #If the processed file has already exists, then the process of the
        #topics will stop.
        if any(temp_substr in string for string in self.topic_list_test):
            self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "Topic already exists") 
            return 
        
        for_test_purpose_data = pd.DataFrame([], columns=['File','Topic', 'Text'])
        self.testing_path = []
        
        for dirpath, dirs, files in os.walk(self.folder_directory_test):
            self.testing_path.extend(files)
    
        #Remove the files other than xml files
        self.testing_path = [x for x in self.testing_path if x.endswith('xml')]
        print(self.testing_path)
        topic_name = os.path.basename(self.folder_directory_test)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        for path_to_file in self.testing_path:
            path_string = os.path.basename(os.path.normpath(path_to_file)) 
            
            #Extract xml information from the files
            #then it construct the information
            file = self.folder_directory_test + '/' + path_string 
            tree = ET.parse(file)
            root = tree.getroot()
            result = ''
            for element in root.iter():
                if(element.text != None):
                    result += element.text + ' '
            #Remove the remained data
            result = result[:-1]
            
            name_of_the_file = (os.path.basename((path_string)))
            
            for_test_purpose_data = for_test_purpose_data.append(pd.DataFrame([(name_of_the_file, 
                                                                               topic_name,
                                                                               result)], 
            columns=['File','Topic', 'Text']))
            if not os.path.isdir(dataset_test):
                os.makedirs(dataset_test)
        
            self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "{} has been read.\n".format(name_of_the_file))
        for_test_purpose_data.to_csv(dataset_test + '/' +
                          topic_name + ".csv",
                          index=False, encoding='utf-8',
                          quoting=csv.QUOTE_ALL)
        #print(for_test_purpose_data)
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "File read complete!\n")
        
        #Adding already created data lists
        self.user_drop_down_select_folder_list_test.insert(tk.END, 
                                                          topic_name + ".csv")
        
        self.document_data_test.append(for_test_purpose_data)
        
        self.topic_list_test.append(topic_name + ".csv")
        
        #Sort the data list after appending csv file
        self.topic_list_test = sorted(self.topic_list_test)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
    
    def create_feature_vector_test(self):
        
        files_tmp = []
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_tmp.extend(files)
        
        #Extract only the csv files and remove extension!
        files_tmp = [os.path.splitext(x)[0] for x in files_tmp if x.endswith('.csv')]
        
        
        for file_string in files_tmp:
            if any(file_string in substring for substring in self.feature_list_test):
                #Feature already exists
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
                self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                                "Feature {} already exists.\n".format(file_string +  '_c.pkl'))
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
                print("Feature {} already exists".format(file_string +  '_f.pkl'))
            else:
                #Read csv files 
                datum = pd.read_csv(dataset_test + '/' +file_string + '.csv', encoding='utf-8', sep=',', 
                            error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
                #Vectorise the document 
                vect = generate_vector()
                vectorized_data, feature_names = vectorize(vect, datum)
                
                with open(dataset_test + '/' + file_string + '_f.pkl', "wb") as f:
                    pickle.dump([vectorized_data, feature_names], f)
                
                self.drop_down_list_word_vector_list_test.insert(tk.END, file_string + '_f.pkl')
                self.feature_list_test.append(file_string + '_f.pkl')
        
        #Sort feature list after appending some elements
        self.feature_list_test = sorted(self.feature_list_test)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, "Complete {} feature generation.\n".format(file_string))
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
        
    def create_feature_vector_test_async(self, file_string):
        files_tmp = []
        
        for dirpath, dirs, files in os.walk(dataset_test):
            files_tmp.extend(files)
        
        #Extract only the csv files and remove extension!
        files_tmp = [os.path.splitext(x)[0] for x in files_tmp if x.endswith('.csv')]
        
        
        
        if any(file_string in substring for substring in self.feature_list_test):
            #Feature already exists
            self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
            self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                            "Feature {} already exists.\n".format(file_string +  '_c.pkl'))
            self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
            print("Feature {} already exists".format(file_string +  '_f.pkl'))
        else:
            #Read csv files 
            datum = pd.read_csv(dataset_test + '/' +file_string + '.csv', encoding='utf-8', sep=',', 
                        error_bad_lines = False, quotechar="\"",quoting=csv.QUOTE_ALL)
            #Vectorise the document 
            vect = generate_vector()
            vectorized_data, feature_names = vectorize(vect, datum)
            
            with open(dataset_test + '/' + file_string + '_f.pkl', "wb") as f:
                pickle.dump([vectorized_data, feature_names], f)
            
            self.drop_down_list_word_vector_list_test.insert(tk.END, file_string + '_f.pkl')
            self.feature_list_test.append(file_string + '_f.pkl')
        
        #Sort feature list after appending some elements
        self.feature_list_test = sorted(self.feature_list_test)
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, "Complete {} feature generation.\n".format(file_string))
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
    
    
    def create_concept_matrix_test(self):
        
        files_tmp = []
        
        #Checking entire files in the text
        for dirpath, dirs, files in os.walk(dataset_test):
            files_tmp.extend(files) 
        rem_len = -len('_f.pkl')
        #Check whether the concept file(s) exist(s)
        files_tmp = [x[:rem_len] for x in files_tmp if x.endswith('_f.pkl')]
#        "ssss"[3:4]
        
        #Define the methods for generating functions
        #Retrieve the concept data asynchonically
        #to retrieve the data simultaneously
        async def retrieve_word_concept_data(feature_names, K = 20):
            with concurrent.futures.ThreadPoolExecutor(max_workers=220) as executor:
                collection_of_results = []
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        requests.get, 
                        'https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance=' +
                        i.replace(' ', '+') + 
                        '&topK=' + str(K)
                    )
                    for i in feature_names
                ]
                for response in await asyncio.gather(*futures):
                    collection_of_results.append(response.json())
                
                return collection_of_results
        
        for file_string in files_tmp:
            #Check whether the test subject exists or no
            if any(file_string in substring for substring in self.concept_list_test):
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
                self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, 
                                                                                "Concept {} already exists.\n".format(file_string +  '_c.pkl'))
                self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
                print("Concept {} already exists".format(file_string +  '_c.pkl'))
            else:
                p_e_c  = {}
                
                feature_names = None                    
                with open(dataset_test + '/' + file_string + '_f.pkl', "rb") as f:
                     _, feature_names = pickle.load(f)
                
                
                #Sort the feature names just in case...
                feature_names = sorted(feature_names)
                '''
                #Retrieve the tenth rankings of the words
                
                #K needed to be adjustable so that the
                #Researcher can find the characteristics of
                #all values!
                '''
                loop = asyncio.get_event_loop()
                future = asyncio.ensure_future(retrieve_word_concept_data(feature_names))
                results = loop.run_until_complete(future)
                
                #temporary
                for idx, i  in enumerate(feature_names):
                #    print(i)
                #    print(idx)
                    p_e_c[i] = results[int(idx)]
                
#                print(p_e_c)
#                temp = {}
#                type(temp) == dict
                #List up the concept names
                
                l = [list(i.keys()) for i in list(p_e_c.values())]
                concept_names = sorted(list(set(itertools.chain.from_iterable(l))))
                
                #    concept_sets[len(concept_sets)-1]
                #Put the atom concept if there are no concepts in the words
                
                
                #Adding atomic elements
                for i in feature_names:
                    #if there are no concepts in the words, then...
                    if p_e_c[i] == {}:
                        
                        #Append the words with no related concpets
                        #as the atomic concepts
                        concept_names.append(i)
#                    else:
                        
                #Sorting the concept_names after adding feature names
                concept_names = sorted(concept_names)

                with open(dataset_test + '/' + file_string +  '_c.pkl', "wb") as f:
                    pickle.dump([p_e_c, concept_names], f)
                    
                self.concept_list_test.append(file_string +  '_c.pkl')
                self.drop_down_concept_prob_vector_list_test.insert(tk.END, file_string +  '_c.pkl')
        
        #Sort after adding all values
        self.concept_list_test = sorted(self.concept_list_test)
#        for i in self.feature_list:
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='normal')
        self.user_drop_down_folder_selection_results_scroll_list.insert(tk.END, "Complete {} concept generation.\n".format(file_string))
        self.user_drop_down_folder_selection_results_scroll_list.configure(state='disabled')
    '''
    #Retrieve all test and training data asynchrously
    '''
    def asynchronous_training_topic_concept_retrieval(self):
        train_folder_selection = askdirectory()
        #train_folder_selection = "C:/Users/n9648852/Desktop/R8-Dataset/Dataset/R8/Testing"
        
        training_folders_tmp = []
        
        for dirpath, dirs, files in os.walk(train_folder_selection):
            if len([x for x in files if x.endswith('.xml')]) != 0:
                training_folders_tmp.append(dirpath) 
        
        #training_folders_tmp.remove(train_folder_selection)
        
        topic_list = self.topic_list
        
        '''
        Asynchronous training dataset retrieval
        '''
        async def retrieve_file_data(training_folders_tmp, topic_list):
        #Max worker set to 10
           with concurrent.futures.ThreadPoolExecutor() as executor:
            
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        self.select_folder_and_extract_xml_async, 
                        folder_name,
                        topic_list, dataset_dir
                    )
                    for folder_name in training_folders_tmp
                ]
                topics_vec = []
                for i in await asyncio.gather(*futures):
                    topics_vec.append(i)
                    
                return topics_vec 
      
        topic_list = self.topic_list
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(retrieve_file_data(training_folders_tmp, topic_list))
        topics = loop.run_until_complete(future)
        
        print(topics)
        if None in topics:
            topics = list(filter((None).__ne__, topics))
        print(topics)
        if type(topics) == list:
            self.topic_list.extend(topics)
            
        self.topic_list = sorted(self.topic_list)
        
        if type(topics) == list:
            for i in topics:
                self.user_drop_down_select_folder_list.insert(tk.END, i)
        
        
        time.sleep(4)
        
        async def create_feature_vectors(training_folders_tmp, feature_list, dataset_dir):
            
           with concurrent.futures.ThreadPoolExecutor() as executor:
            
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        self.create_feature_vector_async, 
                        folder_name, feature_list, dataset_dir
                    )
                    for folder_name in training_folders_tmp
                ]
                features_vec = []
                
                for i in await asyncio.gather(*futures):
                    features_vec.append(i)
                    
                return features_vec
        
        feature_list = self.feature_list
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(create_feature_vectors(training_folders_tmp, feature_list, dataset_dir))
        features = loop.run_until_complete(future)
        
        
        if None in features:
            features = list(filter((None).__ne__, features))
            
        
        if type(features) == list:    
            self.feature_list.extend(features)
            
        self.feature_list = sorted(self.feature_list)
        
        if type(features) == list:
            for i in topics:
                self.drop_down_list_word_vector_bar.insert(tk.END, i)
        
        print("Feature extraction completed!!")
        
        time.sleep(2)
        concept_list = self.concept_list
        
        #Asyncio is not used for retrieving web data simultaneously
        def create_concept_word_lists(training_folders_tmp, concept_list, dataset_dir):
            concept_vec = []
            for i in training_folders_tmp:
                concept_vec.append(self.create_concept_matrix_async(i, concept_list, dataset_dir))
            time.sleep(2)    
            return concept_vec
    
        concepts = create_concept_word_lists(training_folders_tmp, concept_list, dataset_dir)
        
        if None in concepts:
            concepts = list(filter((None).__ne__, concepts))
            
        if type(concepts) == list:    
            self.concept_list.extend(concepts)
        
        
        self.concept_list = sorted(self.concept_list)
        
        
        if type(concepts) == list:
            for i in topics:
                self.drop_down_concept_prob_vector_list.insert(tk.END, i)
        
        print("Concept graph retrieval completed!!")
        
    def asynchronous_testing_topic_concept_retrieval(self):
        train_folder_selection = askdirectory()
        #train_folder_selection = "C:/Users/n9648852/Desktop/R8-Dataset/Dataset/R8/Testing"
        
        training_folders_tmp = []
        
        for dirpath, dirs, files in os.walk(train_folder_selection):
            if len([x for x in files if x.endswith('.xml')]) != 0:
                training_folders_tmp.append(dirpath) 
        
        
        
        
        topic_list = self.topic_list_test
        
        '''
        Asynchronous training dataset retrieval
        '''
        async def retrieve_file_data(training_folders_tmp, topic_list, dataset_dir):
        #Max worker set to 10
           with concurrent.futures.ThreadPoolExecutor() as executor:
            
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        self.select_folder_and_extract_xml_async, 
                        folder_name,
                        topic_list, dataset_dir
                    )
                    for folder_name in training_folders_tmp
                ]
                topics_vec = []
                for i in await asyncio.gather(*futures):
                    topics_vec.append(i)
                    
                return topics_vec 
      
        topic_list = self.topic_list_test
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(retrieve_file_data(training_folders_tmp, topic_list, dataset_test))
        topics = loop.run_until_complete(future)
        
        print(topics)
        if None in topics:
            topics = list(filter((None).__ne__, topics))
        print(topics)
        if type(topics) == list:
            self.topic_list_test.extend(topics)
            
        self.topic_list_test = sorted(self.topic_list_test)
        
        if type(topics) == list:
            for i in topics:
                self.user_drop_down_select_folder_list_test.insert(tk.END, i)
        
        
        time.sleep(2)
        print(training_folders_tmp)
        async def create_feature_vectors(training_folders_tmp, feature_list, dataset_dir):
            
           with concurrent.futures.ThreadPoolExecutor() as executor:
            
                loop = asyncio.get_event_loop()
                futures = [
                    loop.run_in_executor(
                        executor, 
                        self.create_feature_vector_async, 
                        folder_name, feature_list, dataset_dir
                    )
                    for folder_name in training_folders_tmp
                ]
                features_vec = []
                
                for i in await asyncio.gather(*futures):
                    features_vec.append(i)
                    
                return features_vec
        
        feature_list = self.feature_list_test
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(create_feature_vectors(training_folders_tmp, feature_list, dataset_test))
        features = loop.run_until_complete(future)
        
        
        if None in features:
            features = list(filter((None).__ne__, features))
            
        if type(features) == list:    
            self.feature_list_test.extend(features)
            
        self.feature_list_test = sorted(self.feature_list_test)
        
        if type(features) == list:
            for i in topics:
                self.drop_down_list_word_vector_bar_test.insert(tk.END, i)
        
        print("Feature extraction completed!")
        
        #Just in case of erroneous latency...
        time.sleep(2)
        concept_list = self.concept_list_test
        
        #Asyncio is not used for retrieving web data simultaneously
        def create_concept_word_lists(training_folders_tmp, concept_list, dataset_dir):
            concept_vec = []
            for i in training_folders_tmp:
                concept_vec.append(self.create_concept_matrix_async(i, concept_list, dataset_dir))
                time.sleep(2)
            return concept_vec
    
        concepts = create_concept_word_lists(training_folders_tmp, concept_list, dataset_test)
        
        if None in concepts:
            concepts = list(filter((None).__ne__, concepts))
            
        if type(concepts) == list:    
            self.concept_list_test.extend(concepts)
        
        
        self.concept_list_test = sorted(self.concept_list_test)
        
        
        if type(concepts) == list:
            for i in topics:
                self.drop_down_concept_prob_vector_list_test.insert(tk.END, i)
        
        print("Concept graph retrieval completed!!")
        
        
def main():
    #Run the main application
    Application()


if __name__ == "__main__":
    main()
