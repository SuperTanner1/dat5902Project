import unittest
import pandas as pd
import numpy as np
from functions import *

# mock datasets similar in structure and properties to the original datasets that have been imported
dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10.3, 22.6, 56.1, 17.9]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

class TestSuite(unittest.TestCase):
    def test_merge_datasets(self):
        result = merge_datasets(df1, df2, 'index1')
        # datasets need to have correct data types for each column
        # corrected the datasets' data types here as I cannot find correct data types automatically in general
        result['value_x'] = result['value_x'].astype(float)
        result['value_y'] = result['value_y'].astype(float)
        mergedDataset = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2_x': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10.3, 22.6, 56.1, 17.9], 'value_y': [15.6, 30.1, 74.0, 23.7]})
        self.assertTrue(result.equals(mergedDataset), 'result does not equal to merged dataset')
    def test_create_model(self):
        mr, cr = create_model(df1['value_x'], df2['value_y'], 1)
        m, c = np.polyfit(df1['value_x'], df2['value_y'], 1)
        self.assertTrue(m == mr and c == cr)
    def test_calculate_correlation_columns(self):
        correlation = calculate_correlation_columns(df1['value_x'], df2['value_y'])
        correlationTest = np.corrcoef(df1['value_x'], df2['value_y'])
        self.assertEqual(correlation, correlationTest)
    def test_remove_row_from_df(self):
        result = remove_rows_from_df(df1, 'index1', 'c')
        newDataFrame = df1.drop(2)
        self.assertTrue(newDataFrame.equals(result))
    def test_remove_rows_from_df(self):
        result = remove_rows_from_df(df1, 'index2', ['aa', 'bb'])
        newDataFrame = df1.drop([0, 1])
        print(pd.testing.assert_frame_equal(newDataFrame, result))
        self.assertTrue(newDataFrame.equals(result))
    def test_replace_values_in_column(self):
        result = replace_values_in_column(df2, 'index2', 'cc', 'cd')
        newDataFrame = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cd', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]})
        print(pd.testing.assert_frame_equal(newDataFrame, result))
        self.assertTrue(newDataFrame.equals(result))
    def test_replace_values_in_column_mapping_multiple(self):
        mapping = {'cc': 'cd', 'aa':'ab'}
        # otherwise somehow the next test affectsz the df2 of this one
        df2 = pd.DataFrame(dataset2)
        result = replace_values_in_column(df2, 'index2', mapping=mapping)
        newDataFrame = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2': ['ab', 'bb', 'cd', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]})
        print(pd.testing.assert_frame_equal(newDataFrame, result))
        self.assertTrue(newDataFrame.equals(result))
    def test_replace_values_in_column_mapping(self):
        mapping = {'d': 'e'}
        # otherwise somehow the previous test affect the df2 of this one
        df2 = pd.DataFrame(dataset2)
        result = replace_values_in_column(df2, 'index1', mapping=mapping)
        newDataFrame = pd.DataFrame({'index1': ['a', 'b', 'c', 'e'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [15.6, 30.1, 74.0, 23.7]})
        self.assertTrue(newDataFrame.equals(result))