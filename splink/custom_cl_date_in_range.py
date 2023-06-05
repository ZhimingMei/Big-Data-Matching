from splink.comparison_level import ComparisonLevel
from splink.input_column import InputColumn

import splink.duckdb.duckdb_comparison_level_library as cl

class DateInRangeLevelBase(ComparisonLevel):
    def __init__(
            self,
            col_name: str,
            start_date_col_name: str,
            end_date_col_name: str,
            m_probability=None,
    ) -> ComparisonLevel:
        """Compares whether a date falls within a start and end date range

        Arguments:
            col_name (str): Input column name in df_l
            start_date_col_name (str): Start date column name in df_r
            end_date_col_name (str): End date column name in df_r
            m_probability (float, optional): Starting value for m probability.
                Defaults to None.

        Returns:
            ComparisonLevel: A comparison level that evaluates if a date falls within a range
        """
        col = InputColumn(col_name)
        start_date_col = InputColumn(start_date_col_name)
        end_date_col = InputColumn(end_date_col_name)

        col_l = col.name_l()
        col_r_start = start_date_col.name_r()
        col_r_end = end_date_col.name_r()

        sql_exp = (
            f"({col_l} >= {col_r_start} AND {col_l} <= {col_r_end})"
        )
        level_dict = {
            "sql_condition": sql_exp,
            "label_for_charts": f"Date {col_name} is within range of start and end dates",
        }

        if m_probability:
            level_dict["m_probability"] = m_probability

        super().__init__(level_dict)


comparison_date = {
    "output_column_name": "date_in_range",
    "comparison_levels": [
        cl.null_level("patent_date"),
        DateInRangeLevelBase("patent_date", "startdate", "enddate"),
        cl.else_level()
    ],
    "comparison_description": "date in range comparison",
}