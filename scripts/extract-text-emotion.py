#!/usr/bin/env python
# coding: utf-8

import os
import sys
import nltk


import pandas as pd

from tqdm import tqdm

from transformers import BertTokenizer
from model import BertForMultiLabelClassification
from multilabel_pipeline import MultiLabelPipeline
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt

import multiprocessing
from scipy.io import savemat

tokenizer = BertTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-ekman")
model = BertForMultiLabelClassification.from_pretrained("monologg/bert-base-cased-goemotions-ekman")

goemotions = MultiLabelPipeline(
    model=model,
    tokenizer=tokenizer,
    threshold=0.3
)

allfiles = os.listdir(sys.argv[1])

def process(file_name):
    print(file_name)
    chapNum = file_name.split('-')[0]
    lines = open(f"{sys.argv[1]}/{file_name}", "r").read().splitlines()
    
    joined_lines = "!".join(lines)
    sent_text = nltk.sent_tokenize(joined_lines) # this gives us a list of sentences
    sent_text = list(map(lambda x: x.strip("!"), sent_text))
    
    sent_text = lines
    
    sentences = []
    emotions = []

    for i, line in tqdm(enumerate(sent_text)):
        if len(line) == 0:
            continue

    #     sentence = '.'.join(sent_text[i:i+1])
        sentence = sent_text[i]
        sentences.append(sentence)

        emotion = goemotions(sentence)
        emotions.append(emotion[0])
        
    data = {
        'paragraph': sentences,
        'ekman': emotions
    }

    if not os.path.exists(f"{sys.argv[2]}"):
        os.makedirs(f"{sys.argv[2]}", exist_ok=True)
    
    df = pd.DataFrame(data)
    out = df.to_csv(f"{sys.argv[2]}/{chapNum}_emotion_ekman.csv")
    return out


pool = multiprocessing.Pool(1)
pool.map(process, allfiles)