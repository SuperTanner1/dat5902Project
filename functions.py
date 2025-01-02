import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [5, 30, 74, 23]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

mergedDataset = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2_x': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17], 'value_y': [5, 30, 74, 23]})
def merge_datasets(df, df1, relatedColumn):
    mergedDataset = pd.merge(df, df1, how='inner', on=relatedColumn)
    cleanedDataset = mergedDataset.transpose().drop_duplicates().transpose()
    cleanedDataset['value_x'] = cleanedDataset['value_x'].astype(int)
    cleanedDataset['value_y'] = cleanedDataset['value_y'].astype(int)
    return cleanedDataset
def create_model(df):
    pass
def calculate_mean_average(df):
    pass
def calculate_sum_column(df):
    pass
def calculate_correlation_columns(df):
    pass
def remove_values_from_column(df):
    pass
def replace_values_in_column(df):
    pass

print(mergedDataset)
mergedDatasets = merge_datasets(df1, df2, 'index1')
print(mergedDatasets)

print(mergedDatasets.equals(mergedDataset))