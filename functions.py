import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

def merge_datasets(df, df1, relatedColumn):
    mergedDataset = pd.merge(df, df1, how='inner', on=relatedColumn)
    cleanedDataset = mergedDataset.transpose().drop_duplicates().transpose()
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