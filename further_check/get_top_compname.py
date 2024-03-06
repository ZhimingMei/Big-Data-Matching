import pandas as pd
import os
import ast

data_path = '/Users/ryan/Documents/GitHub/Big-Data-Matching/further_check/sample_data'

os.chdir(data_path)

data = pd.read_csv('random_sample_position_compname_data.csv')

# Define a function to extract the company with the highest nob
def get_top_company(company_list, nob_list):
    try:
        if not company_list or not nob_list:
            return None
        # Convert PandasArray to list if not already
        company_list = list(company_list)
        nob_list = list(nob_list)
        # Find the index of the highest nob value
        max_nob_index = nob_list.index(max(nob_list))
        # Return the company name at this index
        return company_list[max_nob_index]
    except: return None

# Apply the function to each row
data['company_cleaned_top_nob'] = data.apply(lambda row: get_top_company(row['linkedin_company_cleaned'], row['compname_nob']), axis=1)
