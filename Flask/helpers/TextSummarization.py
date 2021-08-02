# imports
from nltk.tokenize import word_tokenize, sent_tokenize
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
# import language_check
import torch
import math
import json 
from fpdf import FPDF 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config



def bertSent_embeding(sentences):

    ## Add sentence head and tail as BERT requested
    marked_sent = ["[CLS] " +item + " [SEP]" for item in sentences]
    
    ## USE Bert tokenizization 
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokenized_sent = [tokenizer.tokenize(item) for item in marked_sent]
    
    ## index to BERT vocabulary
    indexed_tokens = [tokenizer.convert_tokens_to_ids(item) for item in tokenized_sent]
    tokens_tensor = [torch.tensor([item]) for item in indexed_tokens]
    
    ## add segment id as BERT requested
    segments_ids = [[1] * len(item) for ind,item in enumerate(tokenized_sent)]
    segments_tensors = [torch.tensor([item]) for item in segments_ids]
    
    ## load BERT base model and set to evaluation mode
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    bert_model.eval()
    
    ## Output 12 layers of latent vector
    assert len(tokens_tensor) == len(segments_tensors)
    encoded_layers_list = []
    for i in range(len(tokens_tensor)):
        with torch.no_grad():
            encoded_layers, _ = bert_model(tokens_tensor[i], segments_tensors[i])
        encoded_layers_list.append(encoded_layers)
    
    ## Use only the last layer vetcor, other choice available
    token_vecs_list = [layers[11][0] for layers in encoded_layers_list]
    
    ## Pooling word vector to sentence vector, use mean pooling, other choice available
    sentence_embedding_list = [torch.mean(vec, dim=0).numpy() for vec in token_vecs_list]
    
    return sentence_embedding_list



def kmeans_sumIndex(sentence_embedding_list):
    
    n_clusters = np.ceil(len(sentence_embedding_list)**0.5)
    kmeans = KMeans(n_clusters=int(n_clusters))
    kmeans = kmeans.fit(sentence_embedding_list)
    
    sum_index,_ = pairwise_distances_argmin_min(kmeans.cluster_centers_, sentence_embedding_list,metric='euclidean')
    
    sum_index = sorted(sum_index)
    
    return sum_index

def bertSummarize(text):
    
    sentences = sent_tokenize(text)
    #print(sentences)
    sentence_embedding_list = bertSent_embeding(sentences)
    #print(sentence_embedding_list)
    #print("hi")
    sum_index = kmeans_sumIndex(sentence_embedding_list)
    summary = ' '.join([sentences[ind] for ind in sum_index])
    
    return summary


def extractive_summary(text):
    a=bertSummarize(text)
    # # tool = language_check.LanguageTool('en-US')
    # # matches1 = tool.check(a)
    # return language_check.correct(a, matches1)
    return a

def abstractive_summary(text ,minlength = 50, maxlength =100):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')
    preprocess_text = text.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)
    # summmarize 

    summary_ids = model.generate(tokenized_text,num_beams=3,no_repeat_ngram_size=1,min_length=minlength, max_length=maxlength,early_stopping=True)
    # tool = language_check.LanguageTool('en-US')
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    # matches2 = tool.check(output)
    # return language_check.correct(output, matches2)
    return output

def generate_pdf(extractive,abstractive):
    file1 = open("myfile1.txt","w+",encoding="latin-1") 
    l=[]
    b=""
    j=0
    for i in extractive:
        j=j+1
        if j==130:
            b=b+i
            l.append(b)
            l.append("\n")
            b=""
            j=1
        else:
            b=b+i
    l.append(b)
    file1.writelines(l)
    file1.close()
    file2 = open("myfile2.txt","w+",encoding="latin-1") 
    l=[]
    b=""
    j=0
    for i in abstractive:
        j=j+1
        if j==130:
            b=b+i
            l.append(b)
            l.append("\n")
            b=""
            j=1
        else:
            b=b+i
    l.append(b)
    file2.writelines(l)
    file2.close()
    # Python program to convert 
    # text file to pdf file 
    # save FPDF() class into 
    # a variable pdf 
    pdf = FPDF() 
    # Add a page 
    pdf.add_page() 
    # set style and size of font 
    # that you want in the pdf 
    f = open("myfile1.txt", "r",encoding="latin-1") 
    pdf.set_font("Arial","U", size = 20) 
    # open the text file in read mode 
    pdf.set_text_color(255,0,0) 
    pdf.cell(200, 10, txt = "Smart Meet", ln = 1, align = 'C') 
    pdf.set_text_color(0,0,0) 
    pdf.set_font("Times", size = 10)
    pdf.cell(200, 10, txt = "----------------------------------------------------------------------------------------------------------", ln = 3, align = 'C') 
    pdf.set_font("Arial","B", size = 15)
    pdf.cell(200, 10, txt = "Short Summary of your meet !!!", ln = 5, align = 'C') 

    # insert the texts in pdf 
    pdf.set_font("Times", size = 10)
    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 7, align = 'J') 
    # save the pdf with name .pdf

    pdf.set_font("Times", size = 10)
    pdf.cell(200, 10, txt = "-----------------------------------------------------", ln = 9, align = 'C') 
    pdf.set_font("Arial","B", size = 15)
    pdf.add_page()
    pdf.cell(200, 10, txt = "AI based minutes of your meet !!!", ln = 11, align = 'C') 
    pdf.set_font("Times", size = 10)

    f = open("myfile2.txt", "r",encoding="latin-1") 
    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 13, align = 'J')

    pdf.cell(200, 10, txt = "-----------------------------------------------------", ln = 15, align = 'C') 
    pdf.output("./static/notes.pdf")