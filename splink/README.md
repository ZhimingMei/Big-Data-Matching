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
