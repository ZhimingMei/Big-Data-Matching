import os
import numpy as np
import pandas as pd
import glob

import phonetics
import Levenshtein
from nltk.util import ngrams

training_path = '/path/to/train_data'
os.chdir(training_path)
df_train = pd.concat(pd.read_excel(file, index_col=[0]) for file in glob.glob('inventor_user_results_w_label_*.xlsx'))

def compute_jaccard_similarity(str1, str2, n=3):
    try:
        # generate n-grams for each string
        ngrams_str1 = set(ngrams(str1, n))
        ngrams_str2 = set(ngrams(str2, n))
        
        # compute the Jaccard similarity
        intersection = ngrams_str1.intersection(ngrams_str2)
        union = ngrams_str1.union(ngrams_str2)
        similarity = len(intersection) / len(union)
        return similarity
    except: return np.nan


def compute_phonetic_match(name1, name2):
    # Generate metaphone for each name
    try:
        meta_name1 = phonetics.metaphone(name1)
        meta_name2 = phonetics.metaphone(name2)

        return Levenshtein.ratio(meta_name1, meta_name2) # ratio phonetic score
    except: return np.nan

def compute_levenshtein_similarity(name1, name2):
    # compute levenshtein similarity 
    try:
        ratio = Levenshtein.ratio(name1, name2)
        return ratio
    except: return np.nan