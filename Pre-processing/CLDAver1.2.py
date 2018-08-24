# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 17:10:53 2018

@author: n9648852
"""

import pandas as pd
import numpy as np
import os
import csv
import pickle
import requests
import itertools


import nltk
from nltk import wordpunct_tokenize, WordNetLemmatizer, sent_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
import xml.etree.ElementTree as ET
#from pyspark.mllib.fpm import FPGrowth
#
#import pyspark

# importing some libraries

#from pyspark.sql import SQLContext

# stuff we'll need for text processing




# initialize constants
lemmatizer = WordNetLemmatizer()

#Set the random state number

rand = 11

"""Preparation for the pre-processing"""

#Setting stop words 
def define_sw():
    
#    stop_word_path = "../../R8-Dataset/Dataset/R8/stopwords.txt"

#    with open(stop_word_path, "r") as f:
#        stop_words = f.read().splitlines()
    
    return set(stopwords.words('english'))# + stop_words)

#def create_lda(tf_matrix, params):
#    return LatentDirichletAllocation(n_components=params['lda_topics'], max_iter=params['iterations'],
#                                     learning_method='online', learning_offset=10,
#                                     random_state=0).fit(tf_matrix)


#Defining the lemmatizer
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
                           min_df=0.10, max_df=0.90)

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
        for element in root.iter():
            if(element.text != None):
                result += element.text + ' '
        result = result[:-1]
        
                
        #Initialise 
#        for file in generate_files(path):
            #print("Now reading...")
            #print(open(file, "r").read())

        
        for_test_purpose_data = for_test_purpose_data.append(pd.DataFrame([(os.path.basename((path_string)), result)], 
                                                                            columns=['File', 'Text']))
    
    return for_test_purpose_data


#Create the test vectors 






    

#            yield idx


            


#Retrieve all P(e|c) values
def retrieve_p_e_c(feature_names):
    responses  = {}
    j = 0
    if(not os.path.isfile("../../R8-Dataset/Dataset/ForTest/pec_prob_top.pkl")):
        
        #Retrieve the tenth rankings of the words
        K = 10 #Retrieve as much as it could
        for i in feature_names:
            print('Now processing ' + str(j) + " word...")
            j += 1
            #Replace space to + to tolerate the phrases with space
            req_str = 'https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance=' \
            + i.replace(' ', '+') + '&topK=' + str(K)
            response = requests.get(req_str)
            
            #Retrieve the response from json file
            responses[i] = response.json()  
        with open("../../R8-Dataset/Dataset/ForTest/pec_prob_top.pkl", "wb") as f:
            pickle.dump(responses, f)
        return responses
    else:
        with open("../../R8-Dataset/Dataset/ForTest/pec_prob_top.pkl", "rb") as f:
            return pickle.load(f)
        print('File exist... load the feature...')

#t.phi_set
#t.theta_set        
#    def show_all_the_results(self,feature_names, maxiter=30):
#        
#        for i in:
#            np.argsort()
    

#Now still testing my codes in the
#

def main():
    test_data = read_test_files()
    vect = generate_vector()
    vectorise_data, feature_names = vectorize(vect, test_data)        
    
#    print(feature_names)
    
    
    p_e_c = retrieve_p_e_c(feature_names)
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
   
    #A number of test occurs for generating the good results
    concept_names = sorted(concept_names)
    p_e_c_array= np.zeros(shape=(len(feature_names), len(concept_names)))

    #Make it redundant
    for i in p_e_c.keys():
        for j in p_e_c[i].keys():
            p_e_c_array[feature_names.index(i)][concept_names.index(j)] = p_e_c[i][j]

    #For testing purpos
    concept_array = p_e_c_array
    
    t = CLDA(vectorise_data, p_e_c_array, feature_names, concept_names, 2, 20)
    
    t.run()
    
    t.phi_set[1][1][2]
    
class CLDA(object):
    
    def word_indices(self, vec):
        """
        Turn a document vector of size vocab_size to a sequence
        of word indices. The word indices are between 0 and
        vocab_size-1. The sequence length is equal to the document length.
        """
        for idx in vec.nonzero()[0]:
            for i in range(int(vec[idx])):
                yield idx      
    
    def __init__(self, matrix, concept_array, feature_names, concept_names, n_topics = 3, maxiter = 15, alpha = 0.1, beta = 0.1):
        """
        n_topics: number of topics
        
        """
        #Assign the matrix object
        self.matrix = matrix
        
        #Assign the concept array 
        self.concept_array = concept_array
        
        #Assign feature names
        self.feature_names = feature_names
        
        #Assign concept names
        self.concept_names = concept_names
        
        #The number of topics
        self.n_topics = n_topics
        
        #Alpha value
        self.alpha = alpha
        
        #Beta value
        self.beta = beta
        
        #max iteration value
        self.maxiter = maxiter
        
        
        
    
#    def _initialize(self, matrix, concept_array, feature_names, concept_names, n_topics = 3, alpha = 0.1, beta = 0.1):
    def _initialize(self):  
        self.alpha = 0.1
        self.beta = 0.1
        
        #Take the matrix shapes from 
        
        
        n_docs, vocab_size = self.matrix.shape
        
        n_concepts = self.concept_array.shape[1]
        
        self.matrix = self.matrix.toarray().copy()
        # number of times document m and topic z co-occur
        self.nmz = np.zeros((n_docs, self.n_topics)) #C_D_T Count document topic
        # number of times topic z and word w co-occur
        self.nzc = np.zeros((self.n_topics, n_concepts)) #Topic size * word size
        self.nm = np.zeros(n_docs) # Number of documents
        self.nz = np.zeros(self.n_topics) #Number of topic
        self.topics_and_concepts = {} #Topics and concepts
    
        for m in range(n_docs):
            print(m) #Print the document progress
            # i is a number between 0 and doc_length-1
            # w is a number between 0 and vocab_size-1
            #Count the 
            for i, w in enumerate(self. word_indices(self.matrix[m, :])):
                #Randomly put 
                # choose an arbitrary topic as first topic for word i
                if np.count_nonzero(self.concept_array[w,:]) != 0:
                    z = np.random.randint(self.n_topics) #Randomise the topics
                    c = np.random.randint(n_concepts) #Randomly distribute the concepts ver topics 
                    self.nmz[m,z] += 1 #Distribute the count of topic doucment
                    self.nm[m] += 1 #Count the number of occurrences
                    self.nzc[z,c] += 1 #Counts the number of topic concept distribution
                    self.nz[z] += 1 #Distribute the counts of the number of topics
                    self.topics_and_concepts[(m,i)] = (z,c) # P(zd_i, c_d_i) where d is the document location and i is the instance location in the document
                else:
                    z = np.random.randint(self.n_topics) #Randomise the topics
                    c = self.concept_names.index(self.feature_names[w]) #Randomly distribute the concepts ver topics 
                    self.nmz[m,z] += 1 #Distribute the count of topic doucment
                    self.nm[m] += 1 #Count the number of occurrences
                    self.nzc[z,c] += 1 #Counts the number of topic concept distribution
                    self.nz[z] += 1 #Distribute the counts of the number of topics
                    self.topics_and_concepts[(m,i)] = (z,c) # P(zd_i, c_d_i) where d is the document location and i is the instance location in the document
                #Memorise the correspondence between topics and the entities
                                 #Should be put j in somewhere else...
        
    
    def _sample_index(self, p_z, nzc):
        """
        Sample from the Multinomial distribution and return the sample index.
        """
        
        choice = np.random.multinomial(1,p_z).argmax() #Making the choice throught the 2-dimensional probability array
        concept = int(choice/nzc.shape[0]) #Extract concept array
        topic = choice % nzc.shape[0] #Extract topic index 
        
        #Return topic and concet index
        return topic, concept
    
#     np.array(([2,3,4],[7,6,5]))/np.sum(np.array(([2,3,4],[7,6,5])))
#    np.reshape(, (6, ))
#    np.array(([2,3,4],[7,6,5])).T.reshape((6,))
#    np.array(([2,3,4],[7,6,5])).T.reshape((6,))    
    def _conditional_distribution(self, m, w): #Maybe the computation valuables
        """
        Conditional distribution (vector of size n_topics).
        """
        concept_size = self.nzc.shape[1]
        n_topics = self.nzc.shape[0]
        p_z_stack = np.zeros((self.nzc.shape[1], self.nzc.shape[0]))
        #Count non-zero value in the 
        if np.count_nonzero(self.concept_array[w,:]) != 0:
            #Calculate only the 
            for c in range(self.nzc.shape[1]):
                left = (self.nzc[:,c] + self.beta) / (self.nz + self.beta * concept_size)  #Corresponding to the left hand side of the equation 
                right = (self.nmz[m,:] + self.alpha) / (self.nm[m] + self.alpha * n_topics)
                p_z_stack[c] = left * right * self.concept_array[w][c]
            
            
            return (p_z_stack/np.sum(p_z_stack)).reshape((self.nzc.shape[0] * self.nzc.shape[1],))
        #Calculate the atomic topic distribution calculaiton
        #if there are no positive number in the concept array
        #Calculate the 
        else:
            #Retrieve the atomic index from the documents 
            atomic_index = self.concept_names.index(self.feature_names[w])
            left = (self.nzc[:,atomic_index] + self.beta) / (self.nz + self.beta * concept_size)
            right = (self.nmz[m,:] + self.alpha) / (self.nm[m] + self.alpha * n_topics)
            p_z_stack[atomic_index] = left * right
            #Normalise p_z value
            
            return (p_z_stack/np.sum(p_z_stack)).reshape((self.nzc.shape[0] * self.nzc.shape[1],))
#        #We might need to have the section "Word_Concept: like"
#        # p_e_c = some expression
#        p_z = left * right #* P(e|c)
#        # normalize to obtain probabilities
#        p_z /= np.sum(p_z)
#        return p_z
    
    
    #np.array(([1,2], [3,4],[5,6])).T.T 
    #z_c shape is something like this: (topic_num, concept_num)
    def run(self, alpha =0.1, beta = 0.1):
        """
        Run the Gibbs sampler.
        """
        
        self.alpha = alpha
        self.beta = beta
#        self.maxiter = maxiter
        #Gibbs sampling program
        self.phi_set = [] #Storing all results Initialisation of all different models
        self.theta_set = [] #Storing all document_topic relation results & initalisation of all other models
        n_docs, vocab_size = self.matrix.shape
        
        #Initalise the values
        self._initialize()
#        matrix = matrix.toarray().copy()
        for it in range(self.maxiter):
            print(it)
            for m in range(n_docs):
                for i, w in enumerate(self.word_indices(self.matrix[m, :])):
                    
                    z,c = self.topics_and_concepts[(m,i)] #Extract the topics and concepts from the doucment 
                    self.nmz[m,z] -= 1#Removing the indices 
                    self.nm[m] -= 1 #Removign the indices
                    self.nzc[z,c] -= 1 #Removing the indices
                    self.nz[z] -= 1 #Removing the indices
                    
                    #Calculate the probabilities of both topic and concepts
                    p_z = self._conditional_distribution(m, w) #Put the categorical probability on it
                    #If there are topics, then it returns the random topics based on the 
                    #calculated probabilities, otherwise it returns the atomic bomb
                    z,c = self._sample_index(p_z, self.nzc) #Re-distribute concept and topic 

                    self.nmz[m,z] += 1 #Randomly adding the indices based on the calculated probabilities
                    self.nm[m] += 1 #Adding the entity based on the percentage
                    self.nzc[z,c] += 1 #Addign the entity for 
                    self.nz[z] += 1 #Count the number of the topic occurrences
                    self.topics_and_concepts[(m,i)] = z,c #Re-assign the concepts and topics
            print("Iteration: {}".format(it))
            print("Phi: {}".format(self.phi()))
            print("Theta: {}".format(self.theta()))
            
            self.phi_set.append(self.phi())
            self.theta_set.append(self.theta())
        
    
    def phi(self):
        """
        Compute phi = p(w|z).
        """
        #Not necessary values for the calculation
        #V = nzw.shape[1]
        num = self.nzc + self.beta #Calculate the counts of the number, the beta is the adjust ment value for the calcluation
        num /= np.sum(num, axis=1)[:, np.newaxis] #Summation of all value and then, but weight should be calculated in this case....
        return num
    
    def theta(self):
        
#        T = nmz.shape[0]
        num = self.nmz + self.alpha #Cal
        num /= np.sum(num, axis=1)[:, np.newaxis]
        
        return num
    
    def set_the_rankings(self):
        
        self.concept_ranking = []
        self.doc_ranking = []
        
#        if(not (self.phi_set in locals() or self.phi.set in globals())):
#            print("The calculation of phi or theta is not done yet!")
        
        #Calcualte the topic_word distribution
        temp = np.argsort(self.phi_set[self.maxiter -1])
        #Calculate the topic_document distribuiton
        temp2 = np.argsort(self.theta_set[self.maxiter -1].T)
        
        #Create the leaderships 
        self.concept_ranking = [[[topic, ranking, self.concept_names[idx], temp[topic][idx]] for ranking, idx in enumerate(concept_idx)]
                                for topic, concept_idx in enumerate(temp)]
        
        self.doc_ranking = [[[topic, ranking, doc_idx, temp2[topic][doc_idx]] for ranking, doc_idx in enumerate(docs_idx)]
                    for topic, docs_idx in enumerate(temp2)]
    
    def show_doc_topic_ranking(self, rank=10):
#        if(not (self.doc_ranking in locals() or self.doc_ranking in globals())):
#            print("The calculation of phi or theta is not done yet!")
        for i in range(self.nzc.shape[0]):
            print("#############################")
            print("Topic {} ranking: ".format(i))
            for j in range(rank):
                 print("Rank: {}, Doc_idx: {}, Phi value: {}".format(self.doc_ranking[i][j][1], self.doc_ranking[i][j][2]))
        
        
    def show_word_topic_ranking(self, rank=10):
#        if(not (self.word_ranking in locals() or self.word_ranking in globals())):
#            print("The calculation of phi or theta is not done yet!")
        
        for i in range(self.nzc.shape[0]):
            print("#############################")
            print("Topic {} ranking: ".format(i))
            for j in range(rank):
                print("Rank: {}, Word: {}".format(self.concept_ranking[i][j][1], self.concept_ranking[i][j][2]))
        
    #p_e_c_array[0])
    
    
    
    
    
    
    #Retrieve all possible concepts from the string
    
    #ce_responces = retrieve_p_c_e(R8_training_tf_feature_names)
    #len(concept_sets)
    #
    #concept_sets[3]
    #
    #
    #
    #
    #p_e_c['0']['1-digit activity code']
    
    #Insert the numbers corresponding to the arrays
    
    
    #for topic, word_idx in enumerate(np.argsort(t.phi_set[0])):
    #    print(topic)
    #    print(word_idx)
        
#    t = LDA(2)
#    
#    #t._initialize(R8_training_tf_matrix)
#    #R8_training_tf_feature_names[-5:-1]
#    
#    t.run(vectorise_data, 30)            
#               # np.argsor
#    t.set_the_rankings(feature_names)
#    
#    #t.word_ranking
#    #t.word_ranking
#    t.show_doc_topic_ranking()
#    t.show_word_topic_ranking()


main()


#
#def read_R8_files(path):
#    
#    #Setting the training path for reading xml files
#    RCV1_training_path = path
#    path = RCV1_training_path
#    #RCV1_training_path = "../../R8-Dataset/Dataset/R8/Training"
#    #RCV1_training_path = "../../R8-Dataset/Dataset/R8/Testing"
#    #RCV1_test_path = "../../R8-Dataset/Dataset/R8/Testing"
#    #os.path.dirname(RCV1_training_path)
#    
#    training_path = []
#    
#    for dirpath, dirs, files in os.walk(RCV1_training_path):
#        training_path.append(dirpath)
#    
#    
#    #Remove the directory itself so that there are no troubles
#    training_path.remove(RCV1_training_path)
#    
#    training_text_data = pd.DataFrame([], columns=['Topic', 'File', 'IsTopic', 'Text'])
#    
#    #Extract only last directory name
##    training_text_data = {}
##    training_data_list = []
#    for path_to_file in training_path:
#        path_string = os.path.basename(os.path.normpath(path_to_file))        
#        #training_data_list.append(path_string)
#        #Initialise the list of the strings
#        #training_text_data[path_string] = {}
#        print("Now reading...")
#        print(path_string)
#        #Initialise 
##        for file in generate_files(path):
#            #print("Now reading...")
#            #print(open(file, "r").read())
#        df = pd.read_csv("../../R8-Dataset/Dataset/R8/Topic/" + path_string + ".txt", 
#                              sep = '\s+',  names = ['Topic', 'File', 'IsTopic'])
#        df['Text'] = None
#        df = df[df.IsTopic == 1]
#        df['Text'] = df.File.apply(lambda row: return_text(path, path_string, row))
#        training_text_data.info()
#        training_text_data = training_text_data.append(df)
#        len(training_text_data)
#
#    training_text_data.to_csv("../../R8-Dataset/" +
#                              os.path.basename(os.path.normpath(RCV1_training_path))+ ".csv",
#                              index=False, encoding='utf-8',
#                              quoting=csv.QUOTE_ALL)
#
#    
#    return training_text_data



"""
Currently, testing the CLDA python implementation
in here.
"""