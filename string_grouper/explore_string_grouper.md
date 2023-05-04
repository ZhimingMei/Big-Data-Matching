# Explore String Grouper

## Implementation details

- This method contains both the vectorization step and fuzzy matching step.
- Hence, we just check the overall time, to test the time complexity.
- Below are the trials and results.



| Input data scale\time |        |
| --------------------- | ------ |
| (10000*10000)         | 2.4s   |
| (50000*50000)         | 10.6s  |
| (100000*100000)       | 21.1s  |
| (500000*500000)       | 127.5s |

- The input data scale means (the \# rows in xb dataset * \# rows in query vectors)