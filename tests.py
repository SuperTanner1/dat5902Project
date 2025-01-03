import unittest
import pandas as pd
import numpy as np
from functions import *

dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [15, 30, 74, 23]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

class TestSuite(unittest.TestCase):
    def test_merge_datasets(self):
        result = merge_datasets(df1, df2, 'index1')
        # datasets need to have correct data types for each column
        # corrected the datasets' data types here as I cannot find correct data types automatically in general
        result['value_x'] = result['value_x'].astype(int)
        result['value_y'] = result['value_y'].astype(int)
        mergedDataset = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2_x': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17], 'value_y': [15, 30, 74, 23]})
        self.assertTrue(result.equals(mergedDataset), 'result does not equal to merged dataset')
    def test_create_model(self):
        mr, cr = create_model(df1['value_x'], df2['value_y'], 1)
        m, c = np.polyfit(df1['value_x'], df2['value_y'], 1)
        self.assertTrue(m == mr and c == cr)
    def test_calculate_correlation_columns(self):
        pass
    def test_remove_row_from_column(self):
        result = remove_values_from_column(df1, 'index1', 'a')
        newDataFrame = pd.DataFrame({'index1': ['b', 'c', 'd'], 'index2': ['bb', 'cc', 'dd'], 'value_x': [22, 56, 17]})
        self.assertTrue(newDataFrame.equals(result))
    def test_remove_rows_from_column(self):
        pass
        #remove_values_from_column(df1, 'index2', ['aa', 'bb'])
    def test_replace_values_in_column(self):
        pass