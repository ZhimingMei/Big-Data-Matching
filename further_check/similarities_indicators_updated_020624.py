import os
import numpy as np
import pandas as pd
import polars as pl
import multiprocessing as mp
import re
import ast
import datetime as dt
import time as tm
import gc

from string_grouper import compute_pairwise_similarities

gc.enable()

import zipfile
import glob
import collections

from difflib import SequenceMatcher
from cleanco import basename

# compare naics for revelio data
def check_match(orbis_codes, linkedin_codes, digits=None):
    for orbis_code in orbis_codes:
        for linkedin_code in linkedin_codes:
            # Slice codes to the first 2 digits if needed
            orbis_sub = orbis_code[:digits] if digits else orbis_code
            linkedin_sub = linkedin_code[:digits] if digits else linkedin_code
            if orbis_sub == linkedin_sub:
                return 1
    return 0
def compare_naics_6_and_2_rev(row):
    # Extract and clean the NAICS codes from both sources
    orbis_naics = [naics.strip() for naics in str(row['primarynaics_orbis_orbis']).replace(',', '|').split('|') if
                     naics.strip().lower() != 'nan']
    # Safely handle 'naics_code_rev' to ensure it's correctly interpreted as a list
    rev_naics = []
    if isinstance(row['naics_code_rev'], str) and row['naics_code_rev'].strip() not in ['nan', '[]', '']:
        try:
            # Safely evaluate to list if possible
            rev_naics = eval(row['naics_code_rev'])
            if not isinstance(rev_naics, list):
                rev_naics = [rev_naics]  # Ensure it's a list even if single value
        except:
            rev_naics = [row['naics_code_rev']]  # Treat as single-item list if eval fails
    rev_naics = [str(naics) for naics in rev_naics if str(naics).lower() != 'nan']



    # Handle cases where either list is empty after cleaning
    if 'nan' in orbis_naics or not rev_naics:
        return -1, -1  # Return -1 for both 6-digit and 2-digit checks

    # Check for 6-digit codes
    six_digit_match = check_match(orbis_naics, rev_naics)

    # Check for 2-digit codes
    two_digit_match = check_match(orbis_naics, rev_naics, digits=2)

    return six_digit_match, two_digit_match
def compare_naics_2_digit_bgoro(row):
    # Extract and clean the NAICS codes from Orbis
    orbis_naics = str(row['primarynaics_orbis_orbis']).split(',')
    # Extract and clean the NAICS codes from bgoro
    bgoro_naics = str(row['ind_naics2_bgoro']).split(',')

    # Handle cases where either list is empty after cleaning
    if 'nan' in orbis_naics or 'nan' in bgoro_naics:
        return -1  # Return -1 if either is 'nan'

    # Extract the first 2 digits of each NAICS code from Orbis
    orbis_naics_2_digit = [code[:2] for code in orbis_naics if code != 'nan']

    # Check for matches in the 2-digit codes
    match_found = 0  # Default to no match
    for orbis_code in orbis_naics_2_digit:
        if orbis_code in bgoro_naics:
            match_found = 1  # Set to 1 if a match is found
            break  # Exit loop early if a match is found

    return match_found


# compare postcode
def compare_postcodes_bgoro(row):
    # Check for None or 'nan' values
    if pd.isna(row['postcode_orbis']) or row['postcode_orbis'] == 'nan' or pd.isna(row['zipcode_list_bgoro']):
        return -1  # Case 1: Either value is invalid

    # Ensure the zipcode list is properly formatted and cleaned
    try:
        zipcode_list = eval(row['zipcode_list_bgoro'])
        if not isinstance(zipcode_list, list):
            zipcode_list = [zipcode_list]  # Convert to list if not already
    except:
        zipcode_list = []  # Handle cases where eval fails

    # Remove 'nan' strings from the list
    zipcode_list = [str(z) for z in zipcode_list if z != 'nan']

    # Check for valid values and compare
    postcode = str(row['postcode_orbis'])
    match_found = 0  # Default to no match

    for zipcode in zipcode_list:
        if postcode in zipcode or zipcode in postcode:
            match_found = 1  # Set to 1 if a match is found
            break  # Exit loop early if a match is found

    return match_found


# compare state
def compare_states_bgoro(row):
    # Convert to lowercase and split by '|'
    orbis_states = [state.strip() for state in str(row['region_in_country_orbis']).replace(',', '|').split('|') if
                     state.strip().lower() != 'nan']
    bgoro_state = str(row['state_bgoro']).lower()

    # Check for 'nan' or invalid values
    if 'nan' in orbis_states or bgoro_state == 'nan':
        return -1  # Case: Invalid value

    match_found = 0  # Default to no match
    for orbis_state in orbis_states:
        if orbis_state in bgoro_state or bgoro_state in orbis_state:
            match_found = 1  # Set to 1 if a match is found
            break  # Exit loop early if a match is found

    return match_found


# compare city
def compare_city_bgoro(row):
    # Convert to lowercase and split by '|'
    orbis_cities = [city.strip() for city in str(row['city_internat_orbis']).replace(',', '|').split('|') if
                     city.strip().lower() != 'nan']
    bgoro_cities = str(row['city_bgoro']).lower()

    # Check for 'nan' or invalid values
    if set(orbis_cities) == {'nan'} or bgoro_cities == 'nan':
        return -1  # Case: Invalid value

    match_found = 0  # Default to no match
    for orbis_city in orbis_cities:
        if orbis_city in bgoro_cities or bgoro_cities in orbis_city:
            match_found = 1  # Set to 1 if a match is found
            break  # Exit loop early if a match is found

    return match_found


# compare ticker
def compare_tickers_rev(row):
    # Correctly split and clean 'ticker_orbis'
    orbis_tickers = [ticker.strip() for ticker in str(row['ticker_orbis']).replace(',', '|').split('|') if
                     ticker.strip().lower() != 'nan']

    # Safely handle 'company_ticker_rev' to ensure it's correctly interpreted as a list
    rev_tickers = []
    if isinstance(row['company_ticker_rev'], str) and row['company_ticker_rev'].strip() not in ['nan', '[]', '']:
        try:
            # Safely evaluate to list if possible
            rev_tickers = eval(row['company_ticker_rev'])
            if not isinstance(rev_tickers, list):
                rev_tickers = [rev_tickers]  # Ensure it's a list even if single value
        except:
            rev_tickers = [row['company_ticker_rev']]  # Treat as single-item list if eval fails
    rev_tickers = [str(ticker) for ticker in rev_tickers if str(ticker).lower() != 'nan']

    # Check for empty or invalid data
    if not orbis_tickers or not rev_tickers:
        return -1  # Invalid or empty inputs

    # Check for match according to the one-in-another rule
    for orbis_ticker in orbis_tickers:
        for rev_ticker in rev_tickers:
            if orbis_ticker in rev_ticker or rev_ticker in orbis_ticker:
                return 1  # Match found

    return 0  # Valid inputs but no match found


# compare sld
def compare_sld_bgoro(row):
    if row['website_std_orbis'] is None or row['SLD'] == 'nan' or row['SLD'] is None:
        return -1

    if row['website_std_orbis'] == row['SLD']:
        return 1

    return 0


# transfer to list column
def cast_string_to_list(s):
    if pd.isna(s) or s == "[]":
        return []  # Return an empty list for NaN or empty list representations
    else:
        # Strip the square brackets and split the string on ", "
        items = s.strip("[]").split(", ")
        # Remove extra quotes from each item if present
        items = [item.strip("'") for item in items]
        return items


## gram distance
def gramdist(a, b, n=10):
    try:
        alist = a.split()  # split name
        if len(alist) > n:  # only get first n parts
            alist = alist[:n]  # only look at the first n strings
        r1 = len([v for v in alist if v in b]) / len(alist)

        blist = b.split()  # only look at the first n strings
        if len(blist) > n:
            blist = blist[:n]
        r2 = len([v for v in blist if v in a]) / len(blist)

        return [r1, r2]

    except:
        return [None] * 2


## levenshtein ratio
def levenshtein_ratio(str1, str2):
    '''

    :param str1: first company name
    :param str2: second company name
    :return: the levenshtein ratio between two strings
    '''
    if not isinstance(str1, str) or not isinstance(str2, str):
        return None

    return SequenceMatcher(None, str1, str2).ratio()


def compute_similarities(filename):
    os.chdir(input_path)

    data_pl = pl.read_parquet(filename)
    # drop the observations with no matched information (linkedin and bgoro)
    data_pl = data_pl.drop_nulls(subset='nob_rev')

    # transfer to pandas dataframe
    data = data_pl.to_pandas()

    # compare naics code
    data[['same_naics_6_rev', 'same_naics_2_rev']] = data.apply(lambda row: compare_naics_6_and_2_rev(row), axis=1,
                                                        result_type='expand')
    data['same_naics_2_bgoro'] = data.apply(compare_naics_2_digit_bgoro, axis=1)

    # compare postcode
    data['same_zipcode_bgoro'] = data.apply(compare_postcodes_bgoro, axis=1)

    # compare state
    data['same_state_bgoro'] = data.apply(compare_states_bgoro, axis=1)

    # compare city
    data['same_city_bgoro'] = data.apply(compare_city_bgoro, axis=1)

    # compare ticker
    data['same_ticker_rev'] = data.apply(compare_tickers_rev, axis=1)

    # compare sld
    pattern = re.compile(r'(?:www\.)?([^\.]+)(?:\.com)?')
    data['website_std_orbis'] = data['website_orbis'].apply(
        lambda cell: pattern.search(cell).group(1) if isinstance(cell, str) and pattern.search(cell) else cell
    )

    data['same_sld_bgoro'] = data.apply(compare_sld_bgoro, axis=1)

    # cosine similarities


    data = data.drop_duplicates(subset=['bvdid', 'company_id', 'company_cleaned_rev', 'name_internat_orbis'])
if __name__ == '__main__':
    input_path = '/Users/ryan/Documents/GitHub/Big-Data-Matching/further_check/sample_data'
    output_path = '/Users/ryan/Documents/GitHub/Big-Data-Matching/further_check/sample_output'

    input_files = os.listdir(input_path)
    output_files = os.listdir(output_path)

    todo = [x for x in input_files if x not in output_files]