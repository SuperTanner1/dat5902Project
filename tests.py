import unittest
import pandas as pd
import numpy as np
from functions import *

dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd'], 'value_y': [5, 30, 74, 23]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

class TestSuite(unittest.TestCase):
    def test_merge_datasets(self):
        result = merge_datasets(df1, df2, 'index1')
        mergedDataset = pd.DataFrame({'index1': ['a', 'b', 'c', 'd'], 'index2_x': ['aa', 'bb', 'cc', 'dd'], 'value_x': [10, 22, 56, 17], 'value_y': [5, 30, 74, 23]})
        self.assertTrue(result.equals(mergedDataset))
    def test_create_model(self):
        pass
    def test_calculate_mean_average(self):
        pass
    def test_calculate_sum_column(self):
        pass
    def test_calculate_correlation_columns(self):
        pass
    def test_remove_values_from_column(self):
        pass
    def test_replace_values_in_column(self):
        pass