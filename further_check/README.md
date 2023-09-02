# Further Check

We have already generated some fuzzy matching results. And now, we need to identify whether the matched pairs are true pairs or not. In this folder, we will try several methods/algorithms to measure the matching quality.

## Using LLM to do the "manual" check
- explore_claude.py: shows an example of using LLM in testing the matching pairs. 

## Calculate Scores
- Some traditional scoring techniques, like Levenshtein, ngram (Jaccard), phonetic, etc.
- Name-based scoring algorithm