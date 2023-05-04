# Explore FAISS

## Tutorial notes & guidance

- [Medium-How to Use FAISS to Build Your First Similarity Search](https://medium.com/loopio-tech/how-to-use-faiss-to-build-your-first-similarity-search-bf0f708aa772)
- [FAISS-wiki page](http://github.com/facebookresearch/faiss/wiki)
- [DeepNote-Semantic Search](https://deepnote.com/blog/semantic-search-using-faiss-and-mpnet)
- [Pinecone-Tutorial on FAISS](https://www.pinecone.io/learn/faiss/)

## Our data and target
We have the name datasets, and we want to find out the best fuzzy matching pairs between the two name datasets.

~~One thing to note that, the name datasets do not have labels.~~

### ~~Potential solutions~~
- ~~[Extract labels using K-means](https://github.com/facebookresearch/faiss/issues/1236)~~

Actually, we do not need to have labels. We just convert the word to vectors, and this works.



## Implementation Details

- We first convert the word/sentence to vectors, using the package `sentence_transformers`
  -  Also, there are other methods for us to covert the strings, e.g., n-gram
  - Here I give a sample code.

```python
from sentence_transformers import SentenceTransformer
def text2vec(df, col_name):
    text = df[col_name]
    encoder = SentenceTransformer('paraphrase-mpnet-base-v2')
    vectors = encoder.encode(text)
    return vectors
```

- Then, we just follow the tutorial code from FAISS.
- We want to know the time complexity of this algorithm
  - The input size are ( `xb`, the first database, is the database that all vectors are indexed, and we are going to search in. `xq`, the query vectors, for which we need to find the nearest neighbors.)
    - first trial: database (10000, 768), query database (10000, 768)
    - second trial: database (50000, 768), query database (50000, 768)
    - third trial: database (100000, 768), query database (100000, 768)
    - fourth trial: database (500000, 768), query database (500000, 768)
    - we change both the query size and the xb database here, since we want to know whether it is an $O(N^2)$ method
  - The running time
    - first trial: 0.4s
    - second trial: 9.9s
    - third trial: 40.6s
    - fourth trial: 1043.5s

| Input dataset scale\time |         |
| ------------------------ | ------- |
| (10000*10000)            | 0.4s    |
| (50000*50000)            | 9.9s    |
| (100000*100000)          | 40.6s   |
| (500000*500000)          | 1043.5s |

