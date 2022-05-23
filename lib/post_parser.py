import pandas as pd
from typing import List, Tuple


def transform_schedule(schedule_list: List[List[str]], parameters: Tuple[str], output_csv: str) -> pd.DataFrame:
    """
    read an input .inc file forming an output PanDas dataframe and writing output .inc and .csv files

    @param schedule_list: prepared to be transformed to the DataFrame list of elements
    @param parameters: list of columns in output .csv file
    @param output_csv: path to output .csv file (optional)

    @return: dataframe with dates and corresponding wells and another keywords parameters
    """

    schedule_df = pd.DataFrame(schedule_list, columns=parameters)
    schedule_df.to_csv(output_csv, sep=';')

    return schedule_df
