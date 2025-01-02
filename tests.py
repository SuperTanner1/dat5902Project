import unittest
import pandas as pd
import numpy as np

dataset1 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd', 'ee'], 'value': [10, 22, 56, 17]}
dataset2 = {'index1': ['a', 'b', 'c', 'd'], 'index2': ['aa', 'bb', 'cc', 'dd', 'ee'], 'value': [5, 30, 74, 23]}

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)

class TestSuite(unittest.TestCase):
    def test_merge_datasets(self):
        pass
    def test_model(self):
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