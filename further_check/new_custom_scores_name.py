import os
import pandas as pd


### read data
training_path = 'path/todata'
os.chdir(training_path)
df = pd.read_csv('filter_test.csv')

### compute scores
def extract_names_from_fullname(row, name_col):
    # convert the comb_col to list
    initials = eval(row['comb_l'])
    
    # split the fullname
    names_ = row[name_col].split()
    
    # extract name corresponding to initial
    names_1 = [name for name in names_ if name.lower().startswith(initials[0])]
    names_2 = [name for name in names_ if name.lower().startswith(initials[1])]
    
    names_1 = names_1[0] if len(names_1) == 1 else names_1 # return string if there's only one match
    names_2 = names_2[0] if len(names_2) == 1 else names_2
    
    return names_1, names_2

df['name_l_1'], df['name_l_2'] = zip(*df.apply(lambda row: extract_names_from_fullname(row, 'fullname_l'), axis=1))
df['name_r_1'], df['name_r_2'] = zip(*df.apply(lambda row: extract_names_from_fullname(row, 'fullname_r'), axis=1))

def calculate_score_substring(name_l, name_r):
    # convert name to list
    name_l = [name_l] if isinstance(name_l, str) else name_l
    name_r = [name_r] if isinstance(name_r, str) else name_r
    
    # score initialization
    score_direct = 0
    score_reverse = 0
    
    # score=2: identical names
    if name_l == name_r:
        score_direct = 2
        score_reverse = 2
    else:
        # score=1: name_l is a substring of name_r
        if all(sub_name in str(name_r) for sub_name in name_l):
            score_direct = 1
        
        # score=1 (reverse): name_r is a substring of name_l
        if all(sub_name in str(name_l) for sub_name in name_r):
            score_reverse = 1

    return max(score_direct, score_reverse)

### test functions
test_score1 = calculate_score_substring('smith', 'adamsmith')
test_score2 = calculate_score_substring('appletest', 'apple')
test_score3 = calculate_score_substring('apple', 'abble')

df['score_1'] = df.apply(lambda row: calculate_score_substring(row['name_l_1'], row['name_r_1']), axis=1)
df['score_2'] = df.apply(lambda row: calculate_score_substring(row['name_l_2'], row['name_r_2']), axis=1)

### drop data based on levenshtein threshold (based on our own dataset)
df_drop = df.loc[(df['levenshtein_distance_company']<=0.5)&(df['levenshtein_distance_fullname']<=0.6)]
df_drop.to_csv('drop_based_on_levenshtein.csv')

df = df.loc[~((df['levenshtein_distance_company']<=0.5)&(df['levenshtein_distance_fullname']<=0.6))]
df.to_csv('filtered_results_with_scores.csv')