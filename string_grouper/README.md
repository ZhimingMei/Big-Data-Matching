# Explore String Grouper

## Implementation details

- This method contains both the vectorization step and fuzzy matching step.
- Hence, we just check the overall time, to test the time complexity.
- Below are the trials and results.



| Input data scale\time | Num_process = int(ncpu\*3/4) | Num_process = 1 | Speed of faiss |
| --------------------- | ---------------------------- | --------------- | -------------- |
| (10000*10000)         | 2.4s                         | 2s              | 3.5s           |
| (50000*50000)         | 10.6s                        | 21s             | 61.4s          |
| (100000*100000)       | 21.1s                        | 65s             | 264s           |
| (500000*500000)       | 127.5s                       | 1272s           |                |

- The input data scale means (the \# rows in xb dataset * \# rows in query vectors)
- From the above results, it seems that this algorithm is $O(N)$.