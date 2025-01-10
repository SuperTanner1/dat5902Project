import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os
import semopy as sm



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
def remove_rows_from_ourworldindata_datasets(df, list):
    return remove_rows_from_df(df, 'Entity', list)
def remove_rows_unshared_between_datasets(df, columnName, df1, columnName1):
    unsharedValues = df[columnName][np.invert(df[columnName].isin(df1[columnName1]))].unique()
    return remove_rows_from_df(df, columnName, list(unsharedValues))

def cleanAndMergeMentalIssueAndDepressionData(mentalIssueData, depressionData, depressionLocationColumn='location_name', mentalIssueLocationColumn='Entity'):
    depressionDataNew = remove_rows_unshared_between_datasets(depressionData, depressionLocationColumn, mentalIssueData, mentalIssueLocationColumn).copy()
    if len(mentalIssueData) != len(depressionDataNew):
        mentalIssueData = remove_rows_unshared_between_datasets(mentalIssueData, mentalIssueLocationColumn, depressionDataNew, depressionLocationColumn)
    
    mergedDataset = pd.merge(mentalIssueData, depressionDataNew, left_on=mentalIssueLocationColumn, right_on=depressionLocationColumn)
    return mergedDataset

def explore_data_ourworldindata_ihme(mentalIssueData=None, depressionData=None, mentalIssueDataColumn=None, title=None, colour=None, depressionLocationColumn='location_name', mentalIssueLocationColumn='Entity', depressionDataColumn='Proportion of people that are depressed (%)', mergedDataset=None, export=False, model=True):
    pathToSaveTo = 'Plots/Custom/'
    fileType = '.png'
    if type(mergedDataset) != pd.DataFrame:
        mergedDataset = cleanAndMergeMentalIssueAndDepressionData(mentalIssueData, depressionData, depressionLocationColumn, mentalIssueLocationColumn)
    
    
    mergedDataset[mentalIssueDataColumn] = mergedDataset[mentalIssueDataColumn][np.invert(mergedDataset[mentalIssueDataColumn].isna())]
    mergedDataset[depressionDataColumn] = mergedDataset[depressionDataColumn][np.invert(mergedDataset[depressionDataColumn].isna())]
    x, y = mergedDataset[mentalIssueDataColumn], mergedDataset[depressionDataColumn]

    x = x.fillna(x.mean())
    y = y.fillna(y.mean())

    fig, ax = plt.subplots()

    if model:
        try:
            m, c = create_model(x, y, 1)
            #print(m,c)
        except np.linalg.LinAlgError:
            try:
                m, c = create_model(x, y, 1)
                #print(m,c)
            except np.linalg.LinAlgError:
                print("Invalid model")
            else:
                yModel = m * x + c
                #print(yModel)
                sns.lineplot(x=x, y=yModel, ax=ax, c='orange')
        else:
            yModel = m * x + c
            sns.lineplot(x=x, y=yModel, ax=ax, c='orange')
            print(f"{title} graph, gradient: {m}, y-intercept: {c}\n")


    if colour != None:
        sns.scatterplot(mentalIssueData, x=x, y=y, ax=ax, hue=colour)
    else:
        sns.scatterplot(x=x, y=y, ax=ax)
    
    ax.set_ylabel(depressionDataColumn)

    if title != None:
        ax.set_title(title)

    if export:
        filePathToEnvironment = os.path.dirname(__file__)
        plotsCustomPath = os.path.join(filePathToEnvironment, pathToSaveTo)
        fig.savefig(plotsCustomPath + title + fileType, bbox_inches='tight')

    return fig, ax, m,c

# correlation coefficient and significance
def statisticalTest(mergedDataset, mentalIssueDataColumn, depressionDataColumn, alternative):
    mergedDataset[mentalIssueDataColumn] = mergedDataset[mentalIssueDataColumn][np.invert(mergedDataset[mentalIssueDataColumn].isna())]
    mergedDataset[depressionDataColumn] = mergedDataset[depressionDataColumn][np.invert(mergedDataset[depressionDataColumn].isna())]
    x, y = mergedDataset[mentalIssueDataColumn], mergedDataset[depressionDataColumn]
    x = x.fillna(x.mean())
    y = y.fillna(y.mean())
 
    return stats.pearsonr(x,y, alternative=alternative), alternative

def createSMAModel(desc, dataset, title, export=False):
    model = sm.Model(desc)
    result = model.fit(dataset)
    test = model.inspect()
    print(f"result:{result}")
    print(f"test:\n{test}")
    print(f"indices for fit:\n{sm.calc_stats(model)}")
    sm.semplot(model, f"Plots/Custom/Models/{title}.png")
    if export:
        test.to_csv(f'Plots/Custom/Models/{title}Test.csv')