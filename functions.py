import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [15, 30, 74, 23]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

def merge_datasets(df, df1, relatedColumn):
    mergedDataset = pd.merge(df, df1, how='inner', on=relatedColumn)
    cleanedDataset = mergedDataset.transpose().drop_duplicates().transpose()
    return cleanedDataset
def create_model(x, y, degree):
    return np.polyfit(x, y, degree)
def calculate_correlation_columns(series, series1):
    pass
def remove_rows_from_df(df, column, values):
    if type(values) != list:
        return df1[np.invert(df1[column] == values)]
    else:
        return df1[np.invert(df1[column].isin(values))]
def replace_values_in_column(df, column, original, replace, mapping):
    if mapping == None:
        df1[column] = df1[column].replace(original, replace)
    else:
        df1[column] = df1[column].replace(mapping)