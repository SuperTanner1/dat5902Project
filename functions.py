import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp



def merge_datasets(df, df1, relatedColumn):
    mergedDataset = pd.merge(df, df1, how='inner', on=relatedColumn)
    cleanedDataset = mergedDataset.T.drop_duplicates().T
    return cleanedDataset
def create_model(x, y, degree):
    return np.polyfit(x, y, degree)
def calculate_correlation_columns(series, series1):
    return np.corrcoef(series, series1)[0, 1]
def remove_rows_from_df(df, column, values):
    if type(values) != list:
        return df[np.invert(df[column] == values)]
    else:
        return df[np.invert(df[column].isin(values))]
def replace_values_in_column(df, column, original=None, replace=None, mapping=None):
    if mapping == None:
        df[column] = df[column].replace(original, replace)
        return df
    else:
        df[column] = df[column].replace(mapping)
        return df