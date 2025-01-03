import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp



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

"""
mapping = {'cc': 'cd', 'aa':'ab'}
result = replace_values_in_column(df2, 'index2', mapping=mapping)
newDataFrame = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2': ['ab', 'bb', 'cd', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]})
print(pd.testing.assert_frame_equal(newDataFrame, result))
"""

dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10.3, 22.6, 56.1, 17.9]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

mapping = {'d': 'e'}
result = replace_values_in_column(df2, 'index1', mapping=mapping)
newDataFrame = pd.DataFrame({'index1': ['a', 'b', 'c', 'e'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]})
print(pd.testing.assert_frame_equal(newDataFrame, result))


print(result)
print(newDataFrame)