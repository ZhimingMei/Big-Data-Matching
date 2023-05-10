# Big-Data-Matching

## Introduction
Now we have a very large dataset, and we want to figure out our target information using queries that require exact matching, or fuzzy matching.

And we have a lot of existing amazing packages to support this work. In this repository, I will test the time complexity (matching efficiency), and the matching accuracy of some chosen packages.

## Program Structure

```markdown
Program structure is given as follow:
    ├─data: will not uploaded
    ├─paper: some research & empirical papers
    ├─faiss: a package developed by Facebook AI Research
    │  └─tutorial: some code examples
    ├─string_grouper: a super fast string matching package in Python
    │  └─tutorial: some code examples
    ├─splink: help link dataset without unique identifier
    │  └─tutorial: some code examples
    ...
```

## Results

### FAISS

| Input dataset scale\time | SentenceTransformer<br />searching time | Another vectorization (TFIDF)<br />vectorization+training+searching | GPU version |
| ------------------------ | --------------------------------------- | ------------------------------------------------------------ | ----------- |
| (10000*10000)            | 0.4s                                    | 1.4s \| + 0.9s  \| + 1.2s   \| = 3.5s                        |             |
| (50000*50000)            | 9.9s                                    | 8.2s \|+ 4.5s   \| + 48.7s \|= 61.4s                         |             |
| (100000*100000)          | 40.6s                                   | 17s  \|+ 6s      \| + 241.7s\| = 264s                        |             |
| (500000*500000)          | 1043.5s                                 | \|             \|                \|                          |             |

- It's more like an $O(N^2)$ method.
- More details see [README-explore faiss](https://github.com/ZhimingMei/Big-Data-Matching/tree/main/faiss#readme)

### String Grouper

Compared with FAISS

| Input data scale\time | Num_process = int(ncpu\*3/4) | Num_process = 1 | Speed of faiss |
| --------------------- | ---------------------------- | --------------- | -------------- |
| (10000*10000)         | 2.4s                         | 2s              | 3.5s           |
| (50000*50000)         | 10.6s                        | 21s             | 61.4s          |
| (100000*100000)       | 21.1s                        | 65s             | 264s           |
| (500000*500000)       | 127.5s                       | 1272s           |                |

- Also an $O(N^2)$ techique.
- More details see [README-explore string_grouper](https://github.com/ZhimingMei/Big-Data-Matching/tree/main/string_grouper#readme)

## Post and News

- Announcing ScaNN: Efficient Vector Similarity Search [[Blog](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html)]
