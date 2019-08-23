#!/usr/bin/env python
# coding: utf-8

# In[9]:


import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn import svm
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import os


def vectorize_train_data(data_list,mindf=2,maxdf=0.85):

    #from nltk.corpus import stopwords
    stopword_list = stopwords.words('english')
    
    #*************Now  Convert a collection of raw documents to a matrix of TF-IDF features***********#
    #**************We will therefore use TfidfVectorizer ---> ngram = 2***************************#
    vectorizer = TfidfVectorizer(min_df=mindf,max_df=maxdf,sublinear_tf=True,use_idf=True,stop_words=stopword_list)
    #ngram_range=(2,2),
    #****************************normalization******************************************************#
    #***************norm : ‘l1’, ‘l2’ or None, optional (default=’l2’)*******************************#
    #*****************************For without normalization , type 'norm = None'***********************#
    #**********************use_idf=True ==== Enable inverse-document-frequency reweighting************#
    

    data_vector = vectorizer.fit_transform(data_list) # with normalization
    #print(vectorizer)
    #print(data_vector) #it contains the tweet text array where array has word count words ngrams combo and gives tf-idf calculations of that combo
    #print(data_vector.toarray()) # Normalized value to array
    #print(data_vector.shape) # (151, 8) 
    #data_vector = np.reshape(data_vector,(data_vector.shape[0],-1))
    return data_vector,vectorizer
    
    '''
    *********print(vectorizer) *******
    **********************************
    TfidfVectorizer(analyzer='word', binary=False, decode_error='strict',
        dtype=<class 'numpy.float64'>, encoding='utf-8', input='content',
        lowercase=True, max_df=0.8, max_features=None, min_df=4,
        ngram_range=(2, 2), norm='l2', preprocessor=None, smooth_idf=True,
        stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',... 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"],
        strip_accents=None, sublinear_tf=True,
        token_pattern='(?u)\\b\\w\\w+\\b', tokenizer=None, use_idf=True,
        vocabulary=None)
    ************************************ max_features
    '''
def vectorize_test_data(test_data_list,training_model_features,mindf=2,maxdf=0.85):
    
    stopword_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(min_df=mindf,max_df=maxdf,sublinear_tf=True,
                                 max_features=training_model_features,use_idf=True,stop_words=stopword_list)
    data_vector = vectorizer.fit_transform(test_data_list)
    #print("Test set shape")
    #print(data_vector.shape)
    return data_vector
def classify(test_vector,train_vector,train_labels,strategy="linear"):
    '''
    sklearn.svm.LinearSVC  :   Linear Support Vector Classification
    classifier.fit : Fit the model according to the given training data.
     
    ***********************************
    
    #train_vector = np.reshape(train_vector, 1)
    print(train_vector)
    print('********************************')
    print(type(train_vector))
    print(train_vector.shape)
    print(test_vector.shape)
    #row = test_vector[]
    #test_vector = csr_matrix((test_vector.data, test_vector.indices, test_vector.indptr), shape=(test_vector.shape[0],train_vector.shape[1] ))
    #test_vector._shape = (test_vector.shape[0],train_vector.shape[1])
    test_vector = np.reshape(test_vector, (test_vector.shape[0],train_vector.shape[1])) 
    '''
    classifier_l = svm.SVC(kernel=strategy,gamma=2)
    classifier_l.fit(train_vector, train_labels)  #above : ,train_vector.shape[1]
    predictions = classifier_l.predict(test_vector)   ##^&^%
    mean_accuracy_report = classifier_l.score(test_vector, predictions, sample_weight=None)
    
    return predictions, mean_accuracy_report
    # score(X, y, sample_weight=None)[source] : Returns the mean accuracy on the given test data and labels.
    
def accuracy_report(test_acc_labels,predicted_acc_labels):
    """
    """
    res_class_report = classification_report(test_acc_labels,predicted_acc_labels)
    #print(result)
    
    conf_matrix = confusion_matrix(test_acc_labels, predicted_acc_labels)
    
    accuracy = accuracy_score(test_acc_labels, predicted_acc_labels)
    
    return res_class_report, conf_matrix, accuracy

def mean_accuracy_report(X,y):
    res = score(X, y, sample_weight=None)
    print(res)
    
    
def read_data(filename,flag):
    #print(filename)
    #check
    data =[]
    label = []
    with open(filename,'r') as fp:
        csv_reader = csv.reader(fp)
        next(csv_reader)
        for row in csv_reader:
            #data.append(row[0])
            #label.append(row[1])
            # row_terms = row.split(",")
            if flag: # will work for train set data
                data.append(row[0])
                label.append(row[1])
            else: # will work for test set data
                data.append(row[0]) # this is tweet text     
    fp.close()
    if flag: #******will return the data and label of train set.
        return data,label
    else: #*********will return data of test set which will help to predict the label.
        return data
def collector_details(mean_accuracy_acc_report,res_classification_report,conf_matrix,accuracy,predicted_labels,test_data):

    positive_label = 0
    negative_label = 0
    positive_string_index = 0
    negative_string_index = 0 

    for i in range(len(predicted_labels)):
        if predicted_labels[i] == str(0):
            negative_string_index = i
            negative_label+=1
        elif predicted_labels[i] == str(1):
            positive_string_index = i
            positive_label+=1
   
    with open("classify_details.txt",'w') as fp:
        #fp.write("No of Users Collected : " + str(No_of_users) +"\n")
        fp.write("Classify.py:\n")
        fp.write("NMean Accuracy report : " + str(mean_accuracy_acc_report)+"\n")
        fp.write("Classification report : " + res_classification_report+"\n")
        fp.write("Confusion Matrix : " + str(conf_matrix)+"\n")
        fp.write("Accuracy of the MODEL : " + str(accuracy)+"\n")
        
        fp.write("Predicted Labels : " + str(predicted_labels)+"\n")
        
        fp.write("Total Predicted Labels : " + str(len(predicted_labels))+"\n")

        fp.write("Positive Number of Instances : " + str(positive_label) + "\n")
        
        fp.write("Negative Number of Instances : " + str(negative_label)+ "\n")
        
        fp.write("Positive Instance Example : " + str(test_data[positive_string_index])+ "\n")
        
        fp.write("Negative Instance Example : " + str(test_data[negative_string_index])+ "\n")
       

        
        
        
    fp.close()   


def plot_bar_x(label_view,predicted_labels):
    


    positive_label = 0
    negative_label = 0

    for i in range(len(predicted_labels)):


        if predicted_labels[i] == str(0):
            negative_label+=1
        elif predicted_labels[i] == str(1):
            positive_label+=1

    count_label = [negative_label,positive_label]
    # this is for plotting purpose
    index = np.arange(len(label_view))
    plt.bar(index, count_label)
    plt.xlabel('Negatives  and  Positives', fontsize=10)
    plt.ylabel('Count', fontsize=8)
    plt.xticks(index, count_label, fontsize=10, rotation=30)
    plt.title('Sentimental analysis of Trump')
    #plt.legend((x,y), ('Positive Tweets', 'Negative Tweets'))
    plt.show()
    
def main():
    """
    """
    train_data,train_label = read_data("Training_Data"+os.path.sep+"trump.csv",True)
    #print(train_data)
    
    test_data = read_data("Collected_Data"+os.path.sep+"trump.csv",False)
    train_vector,vectorizer = vectorize_train_data(data_list=train_data)
    #training_model_features = train_vector.shape[1]
    test_vector = vectorize_test_data(test_data_list=test_data,training_model_features=train_vector.shape[1])
    predicted_labels, mean_accuracy_report = classify(test_vector=test_vector,train_vector=train_vector,train_labels=train_label,strategy="linear")
    #save_classify_details(test_data=test_data,predicted_labels=predicted_labels)
    print(predicted_labels)

    print(len(predicted_labels))
    
    print("\t\033[1m ❂❂❂❂❂❂❂❂❂❂❂❂❂❂ __PRINT ACCURACY & CLASSIFICATION REPORT OF THE SVM MODEL__ ❂❂❂❂❂❂❂❂❂❂❂❂❂❂")
    
    train_acc_data,train_acc_label = read_data("Training_Data"+os.path.sep+"trump.csv",True)
    #print(train_data)
    
    test_acc_data = read_data("Training_Data"+os.path.sep+"Without_label"+os.path.sep+"trump.csv",False)
    train_acc_vector,vectorizer_acc = vectorize_train_data(data_list=train_acc_data)
    #training_model_features = train_vector.shape[1]
    test_acc_vector = vectorize_test_data(test_data_list=test_acc_data,training_model_features=train_acc_vector.shape[1])
    predicted_acc_labels, mean_accuracy_acc_report = classify(test_vector=test_acc_vector,train_vector=train_acc_vector,train_labels=train_acc_label,strategy="linear")
    #save_classify_details(test_data=test_data,predicted_labels=predicted_labels)
    
    res_classification_report, conf_matrix, accuracy = accuracy_report(train_acc_label,predicted_acc_labels)
    
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣ __Mean Accuracy Report__ ✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    print("\t\t\t\t",mean_accuracy_acc_report,"\n")
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣ __Classification Report__ ✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    print(res_classification_report,"\n")
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣ __Confusion MATRIX__ ✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    print(conf_matrix,"\n")
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣ __ACCURACY OF THE MODEL__ ✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    print("\t\t\t\t",accuracy,"\n")
    print("✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣✣","\n")
    
    print('\t❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂ _End_ ❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂')
    

    collector_details(mean_accuracy_acc_report,res_classification_report,conf_matrix,accuracy,predicted_labels,test_data)

    label_view = ['0','1']


    plot_bar_x(label_view,predicted_labels)



if __name__ == main():
    main()


# In[ ]:




