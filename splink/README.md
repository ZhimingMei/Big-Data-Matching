# Explore Splink

Splink provides a very comprehensive and digestible document. Here's the link [document](https://moj-analytical-services.github.io/splink/index.html)

In our task, we use splink to conduct the efficient big-data fuzzy matching. Since we can split the dataset by blocking rules (highlight of splink package), in each matching process, we do not go through all the dataset.

## Tutorials and Examples
- Linking two tables of persons by Splink [splink example](https://moj-analytical-services.github.io/splink/demos/example_link_only.html) 
- A trial based on our own dataset (dataset omitted) [explore splink](https://github.com/ZhimingMei/Big-Data-Matching/blob/main/splink/explore_splink.ipynb)

## Further Notes
### Custom comparison level--date in a range: 
Splink does not provide any comparison level that can detect whether a date is in a date range (e.g., I would like to test whether 2023-06-06 falls in between 2023-01-01 and 2023-07-01).

Here's the code for date_in_range comparison level, see [custom_cl_date_in_range.py](https://github.com/ZhimingMei/Big-Data-Matching/blob/main/splink/custom_cl_date_in_range.py).

And we can write the settings as below:
```python
comparison_date = {
    "output_column_name": "date_in_range",
    "comparison_levels": [
        cl.null_level("test_date"),
        DateInRangeLevelBase("test_date", "startdate", "enddate"),
        cl.else_level()
    ],
    "comparison_description": "date in range comparison",
}
```



### Efficiency Test

#### Test 1: Input scale

Since we have very large scale input data, we need to figure out the most efficient dividing scales.

The original data scale is: 

- Left dataframe: 1,000,000*15
- Right dataframe: 20,000,000*15


First trial: we match left dataframe with a sample of 5,000,000 in right dataframe. And the total running time is about 30min. We repeat the process for four times.

Second trial: we match left dataframe with right dataframe. The total running time is about 170min.



**Summary**: Dividing the dataset, and running with for loop is somehow efficient than just directly matching with whole datasets.



#### Test 2: Blocking rules

We set different blocking rules to check the model efficiency.

Our data has several columns: name1, name2, name3. And the idea of blocking rule should be, there should be at least one name from the left, matched with one name from the right.

- First blocking rule: l.name1=r.name1 or l.name1=r.name2, or l.name1=r.name3 (and repeat for l.name2 and l.name3)
- Second blocking rule: we just reshape the data based on name, and there's only one name column (the length should be multiplied by 3). We set the blocking rule as: l.name=r.name, directly.



**Summary**: the second blocking rule is much faster than the first one, in the prediction process. And the data processing time is quite close, (6min and 7min correspondingly).
