import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import requests
import re
import os

from functions import *
from functools import reduce
# this is so I can decide if I want to update the existing data from the source (our world in data) into my repository.
# If update is false, the program will use the existing data.
# If update is true, it will request the data, export it into the repository permanently, and the program will use this data.
update = False

if update:
    pd.read_csv("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-religious-spiritual.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}).to_csv('Datasets/mentalIssuesDealtByReligionSpirituality.csv')
    pd.read_csv("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-friends-family.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}).to_csv('Datasets/mentalIssuesDealtByFriendsFamily.csv')
    pd.read_csv("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-took-prescribed-medication.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}).to_csv('Datasets/mentalIssuesDealtByMedication.csv')
    pd.read_csv("https://ourworldindata.org/grapher/science-helps-a-lot-treating-anxiety-depression-vs-gdp-per-capita.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}).to_csv('Datasets/opinionThatScienceHelpsALotForMentalHealth.csv')
    pd.read_csv("https://ourworldindata.org/grapher/perceived-comfort-speaking-anxiety-depression.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}).to_csv('Datasets/perceivedComfortSpeakingAboutAnxietyDepression.csv')
    pd.read_csv("https://ourworldindata.org/grapher/psychiatrists-working-in-the-mental-health-sector.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}).to_csv('Datasets/amountOfPsychiatristsWorking.csv')


#metadataMentalIssuesDealtByReligionSpirituality = requests.get("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-religious-spiritual.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()
#metadataMentalIssuesDealtByFriendsFamily = requests.get("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-friends-family.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()
#metadataMentalIssuesDealtByMedication = requests.get("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-took-prescribed-medication.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()
#metadataOpinionThatScienceHelpsALotForMentalHealth = requests.get("https://ourworldindata.org/grapher/science-helps-a-lot-treating-anxiety-depression-vs-gdp-per-capita.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()
#metadataPerceivedComfortSpeakingAboutAnxietyDepression = requests.get("https://ourworldindata.org/grapher/perceived-comfort-speaking-anxiety-depression.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()
#metadataAmountOfPsychiatristsWorking = requests.get("https://ourworldindata.org/grapher/psychiatrists-working-in-the-mental-health-sector.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

mentalIssuesDealtByReligionSpirituality = pd.read_csv('Datasets/mentalIssuesDealtByReligionSpirituality.csv')
mentalIssuesDealtByFriendsFamily = pd.read_csv('Datasets/mentalIssuesDealtByFriendsFamily.csv')
mentalIssuesDealtByMedication = pd.read_csv('Datasets/mentalIssuesDealtByMedication.csv')
opinionThatScienceHelpsALotForMentalHealth = pd.read_csv('Datasets/opinionThatScienceHelpsALotForMentalHealth.csv')
perceivedComfortSpeakingAboutAnxietyDepression = pd.read_csv('Datasets/perceivedComfortSpeakingAboutAnxietyDepression.csv')
amountOfPsychiatristsWorking = pd.read_csv('Datasets/amountOfPsychiatristsWorking.csv')
depressionPrevalence = pd.read_csv('Datasets/IHME-GBD_2021_DATA-56bdf511-1.csv')

# fact sheet from 13/11/2024 cited in Zotero
socialMediaFactSheet = pd.read_excel('Datasets/Social media fact sheet.xlsx')

# wikipedia
urbanisation = pd.read_excel('Datasets/Wikipedia Data on Urbanisation.xlsx')

# individualism
individualisticLevels = pd.read_csv('Datasets/individualistic-countries-2024.csv')

"""
NEW SECTION
Data Cleaning
"""
mappingDepressionPrevalenceToOurWorldInDataDatasets = {"Democratic People's Republic of Korea": 'North Korea', 
 "Lao People's Democratic Republic": 'Laos',
 "Viet Nam": 'Vietnam',
 "Taiwan (Province of China)": 'Taiwan',
 "Russian Federation": 'Russia',
 "Republic of Moldova": 'Moldova',
 "Brunei Darussalam": 'Brunei',
 "Republic of Korea": 'South Korea',
 "United States of America": 'United States',
 "United Republic of Tanzania": 'Tanzania',
 "Bolivia (Plurinational State of)": 'Bolivia',
 "Venezuela (Bolivarian Republic of)": 'Venezuela',
 "Iran (Islamic Republic of)": 'Iran',
 'Syrian Arab Republic': 'Syria',
 'Federated States of Micronesia': 'Micronesia',
 'Macedonia': 'North Macedonia',
 }

# conversion of decimal to percentage
depressionPrevalence['val'] = depressionPrevalence['val'] * 100

# change country names to those that match with ourworldindata datasets
depressionPrevalence = replace_values_in_column(depressionPrevalence, 'location_name', mapping=mappingDepressionPrevalenceToOurWorldInDataDatasets)

countriesInIHMENotInOurWorldInData = depressionPrevalence['location_name'][np.invert(depressionPrevalence['location_name'].isin(mentalIssuesDealtByFriendsFamily['Entity']))].unique()

# removed continents (asia and europe), and categories of countries (low-income, lower-middle-income, upper-middle-income 
# and high-income, and north+south america, oceania, kosovo, hong kong, czechia, and world) from ourworldindata datasets 
# to allow comparison of ways of dealing with mental issues and prevalence of depression
continents = ['Asia', 'Africa', 'Europe', 'World']
categoriesOfCountry = ['High-income countries', 'Upper-middle-income countries', 'Lower-middle-income countries', 'Low-income countries']
countries = ['Kosovo', 'Hong Kong', 'Czechia', 'Oceania', 'North America', 'South America']
listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry = continents + categoriesOfCountry + countries

mappingFriendsAndFamily = {'Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all': 'Proportion that talked to friends or family\nwhen anxious/depressed (%)'}
mappingReligiousSpirituality = {'Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all': 'Proportion that engaged in religious/spiritual activities\nwhen anxious/depressed (%)'}
mappingMedication = {'share__question_mh8d__took_prescribed_medication_when_anxious_depressed__answer_yes__gender_all__age_group_all': 'Proportion that took prescribed medication\nwhen anxious/depressed (%)'}

# each of the below's actual labels are someone local at the beginning and someone they know at the end,
# so the proportion is always about a local person's comfort in speaking to someone about anxiety/depression with someone they know
mappingPerceivedComfortSpeakingAboutDepressionAnxiety = {'share__question_mh5__someone_local_comfortable_speaking_about_anxiety_depression_with_someone_they_know__answer_very_comfortable__gender_all__age_group_all': 'Proportion of people very comfortable\nspeaking about anxiety/depression (%)',
'share__question_mh5__someone_local_comfortable_speaking_about_anxiety_depression_with_someone_they_know__answer_somewhat_comfortable__gender_all__age_group_all': 'Proportion of people somewhat comfortable\nspeaking about anxiety/depression (%)',
'share__question_mh5__someone_local_comfortable_speaking_about_anxiety_depression_with_someone_they_know__answer_dont_know_refused__gender_all__age_group_all': 'Proportion of people that don\'t know how comfortable they are\nspeaking about anxiety/depression (%)',
'share__question_mh5__someone_local_comfortable_speaking_about_anxiety_depression_with_someone_they_know__answer_not_at_all_comfortable__gender_all__age_group_all': 'Proportion of people not comfortable\nspeaking about anxiety/depression (%)',
'very_comfortable and somewhat_comfortable': 'Proportion of people very or somewhat comfortable\nspeaking about anxiety/depression (%)'}

mappingIndidividualism = {'IndividualismScore_2023': 'Individualism Score in 2023'}

# removing all countries and terrorities in depression prevalence dataset that are in ourworldindata but not in depression prevalence dataset
depressionPrevalence = remove_rows_from_df(depressionPrevalence, 'metric_name', ['Number', 'Rate'])

# renaming columns in depression dataframe and our world in data dataframes
mentalIssuesDealtByFriendsFamily = mentalIssuesDealtByFriendsFamily.rename(columns=mappingFriendsAndFamily)
mentalIssuesDealtByReligionSpirituality = mentalIssuesDealtByReligionSpirituality.rename(columns=mappingReligiousSpirituality)
mentalIssuesDealtByMedication = mentalIssuesDealtByMedication.rename(columns=mappingMedication)
perceivedComfortSpeakingAboutAnxietyDepression = perceivedComfortSpeakingAboutAnxietyDepression.rename(columns=mappingPerceivedComfortSpeakingAboutDepressionAnxiety)
individualisticLevels = individualisticLevels.rename(columns=mappingIndidividualism)

# removing unnecessary data
mentalIssuesDealtByFriendsFamily = remove_rows_from_ourworldindata_datasets(mentalIssuesDealtByFriendsFamily, listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry)
mentalIssuesDealtByReligionSpirituality = remove_rows_from_ourworldindata_datasets(mentalIssuesDealtByReligionSpirituality, listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry)
mentalIssuesDealtByMedication = remove_rows_from_ourworldindata_datasets(mentalIssuesDealtByMedication, listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry)
perceivedComfortSpeakingAboutAnxietyDepression = remove_rows_from_ourworldindata_datasets(perceivedComfortSpeakingAboutAnxietyDepression, listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry)
amountOfPsychiatristsWorking = remove_rows_from_ourworldindata_datasets(amountOfPsychiatristsWorking, listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry)

depressionPrevalence = depressionPrevalence.rename(columns={'val': 'Proportion of people that are depressed (%)'})

"""
NEW SECTION
Data Exploration
- exploring models and scatter graphs for every 'our world in data' dataset against depression prevalence
"""
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

    return fig, ax, mergedDataset

# negative correlation - good line
explore_data_ourworldindata_ihme(mentalIssuesDealtByFriendsFamily, depressionPrevalence, mappingFriendsAndFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'])

# negative correlation - good line
explore_data_ourworldindata_ihme(mentalIssuesDealtByReligionSpirituality, depressionPrevalence, mappingReligiousSpirituality['Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all'])

# no correlation
explore_data_ourworldindata_ihme(mentalIssuesDealtByMedication, depressionPrevalence, mappingMedication['share__question_mh8d__took_prescribed_medication_when_anxious_depressed__answer_yes__gender_all__age_group_all'])

opinionThatScienceHelpsALotForMentalHealth.drop('Population (historical)', axis=1)
opinionThatScienceHelpsALotForMentalHealth = opinionThatScienceHelpsALotForMentalHealth[opinionThatScienceHelpsALotForMentalHealth['Year'] == 2021]

# good line
fig,ax, mergedDataset = explore_data_ourworldindata_ihme(opinionThatScienceHelpsALotForMentalHealth, depressionPrevalence, 'GDP per capita, PPP (constant 2017 international $)')

ax.set_xlim(0, 35000)

# histograms of how comfortable people are speaking about depression
mergedComfortSpeakingAndDepression = cleanAndMergeMentalIssueAndDepressionData(perceivedComfortSpeakingAboutAnxietyDepression, depressionPrevalence)
for comfortSpeaking in list(mappingPerceivedComfortSpeakingAboutDepressionAnxiety.values()):
    print(comfortSpeaking)
    fig, ax = plt.subplots()
    sns.histplot(mergedComfortSpeakingAndDepression, x=comfortSpeaking, ax=ax)

amountOfPsychiatristsWorking2020 = amountOfPsychiatristsWorking[amountOfPsychiatristsWorking['Year'] == 2020].copy()

# bad line, too many missing values
fig, ax, mergedDataset = explore_data_ourworldindata_ihme(amountOfPsychiatristsWorking2020, depressionPrevalence, 'Total number of psychiatrists per 100,000 population')
ax.set_xlim(-0.5, 20)

# good line
explore_data_ourworldindata_ihme(individualisticLevels, depressionPrevalence, 'Individualism Score in 2023', mentalIssueLocationColumn='country')


# create correlation heatmap for all variables
listOfMentalHealthDatasets = [mentalIssuesDealtByMedication, mentalIssuesDealtByReligionSpirituality, amountOfPsychiatristsWorking2020, perceivedComfortSpeakingAboutAnxietyDepression, opinionThatScienceHelpsALotForMentalHealth]
mentalIssueDealtyByMasterDataset = mentalIssuesDealtByFriendsFamily.copy()
for i in range(len(listOfMentalHealthDatasets)):
    print(f'{i}th: ' + str(len(mentalIssueDealtyByMasterDataset)))
    mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.merge(listOfMentalHealthDatasets[i], on='Entity', how='left', suffixes=(f'_x{i}', f'_y{i}'))
    
fig, ax = plt.subplots()

# removing all duplicate and unnecessary numeric columns
for i in range(0,5):
    try:
        mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.drop(f'Code_x{i}', axis=1)
    except KeyError:
        pass
    try:
        mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.drop(f'Code_y{i}', axis=1)
    except KeyError:
        pass
    try:
        mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.drop(f'Year_x{i}', axis=1)
    except KeyError:
        pass
    try:
        mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.drop(f'Year_y{i}', axis=1)
    except KeyError:
        pass
    try:
        mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.drop(f'Unnamed: 0_x{i}', axis=1)
    except KeyError:
        pass
    try:
        mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.drop(f'Unnamed: 0_y{i}', axis=1)
    except KeyError:
        pass

mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.merge(depressionPrevalence.loc[:, ['location_name', 'Proportion of people that are depressed (%)']], how='inner', left_on='Entity', right_on='location_name')
mentalIssueDealtyByMasterDataset = mentalIssueDealtyByMasterDataset.merge(individualisticLevels, how='inner', left_on='Entity', right_on='country')
mentalIssueDealtyByMasterDataset.to_csv('Datasets/master mental issues.csv')
correlationMatrix = mentalIssueDealtyByMasterDataset.select_dtypes('number').corr()

sns.heatmap(correlationMatrix,annot=True)

GDPColumnName = 'GDP per capita, PPP (constant 2017 international $)'

# good line
fig,ax, mergedDataset = explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=GDPColumnName, depressionDataColumn='Individualism Score in 2023')

ax.set_xlim(0, 60000)

# bad line
fig, ax, mergedDataset = explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=GDPColumnName, depressionDataColumn='Total number of psychiatrists per 100,000 population')

# good line
fig, ax, mergedDataset = explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=GDPColumnName, depressionDataColumn='Proportion that engaged in religious/spiritual activities\nwhen anxious/depressed (%)')

plt.close('all')

"""
NEW SECTION
Final analysis
- final graphs
"""
export = True

title='The higher the gdp per capita, the less religious or spiritual activities are relied upon'
explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=GDPColumnName, depressionDataColumn='Proportion that engaged in religious/spiritual activities\nwhen anxious/depressed (%)', title=title, export=True)
explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=GDPColumnName, depressionDataColumn='Individualism Score in 2023', title='The higher the gdp per capita, the more individualistic countries are', export=export)
explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=GDPColumnName, title='', export=True)
explore_data_ourworldindata_ihme(mentalIssuesDealtByFriendsFamily, depressionPrevalence, mappingFriendsAndFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], title='When people talk about their depression or anxiety to friends or family\nthey are less anxious or depressed', export=export)
explore_data_ourworldindata_ihme(mentalIssuesDealtByReligionSpirituality, depressionPrevalence, mappingReligiousSpirituality['Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], title='When people are more engaged in religious or spiritual activity\nthey are less anxious or depressed', export=export)
explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=mappingReligiousSpirituality['Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], depressionDataColumn=mappingFriendsAndFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], title='Talking to friends and family \nand doing religious or spiritual activity are related', export=export)
explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=mappingReligiousSpirituality['Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], depressionDataColumn='Individualism Score in 2023', title='More religious or spiritual countries are less individualistic\nthan less religious or spiritual countries', export=export)
explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn=mappingFriendsAndFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], depressionDataColumn='Individualism Score in 2023', title='Countries of all levels of individualism talk to friends or family at\nvarying degrees about anxiety or depression', export=export)

explore_data_ourworldindata_ihme(mergedDataset=mentalIssueDealtyByMasterDataset, mentalIssueDataColumn='Individualism Score in 2023', title='Higher rates of individualism correlates with depression prevalence in countries', export=export)

fig,ax=plt.subplots()
sns.histplot(mentalIssueDealtyByMasterDataset, x='Individualism Score in 2023', y=mappingFriendsAndFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'])

fig, ax = plt.subplots()
sns.heatmap(correlationMatrix,annot=True)

"""
NEW SECTION
Final analysis
- statistical analysis
"""

fig, ax= plt.subplots(2)
stats.probplot(mentalIssueDealtyByMasterDataset['Proportion that engaged in religious/spiritual activities\nwhen anxious/depressed (%)'], fit=True, plot=ax[0])
sns.histplot(x=mentalIssueDealtyByMasterDataset['Proportion that engaged in religious/spiritual activities\nwhen anxious/depressed (%)'], ax=ax[1])
fig, ax= plt.subplots()
stats.probplot(mentalIssueDealtyByMasterDataset['Individualism Score in 2023'], fit=True, plot=ax)
fig, ax= plt.subplots(2)
stats.probplot(mentalIssueDealtyByMasterDataset['Proportion of people that are depressed (%)'], fit=True, plot=ax[0])
sns.histplot(mentalIssueDealtyByMasterDataset['Proportion of people that are depressed (%)'], ax=ax[1])


# Individualism Score and Proportion of religious/spiritual activities are non-normal while proportion of people that are depressed is normal
fig, ax=plt.subplots()
# GDP excluded due to its large size
importantVariables = [
    'Proportion of people that are depressed (%)',
    'Proportion that engaged in religious/spiritual activities\nwhen anxious/depressed (%)', 
    'Individualism Score in 2023', 
    mappingFriendsAndFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'], 
    mappingReligiousSpirituality['Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all']
]
sns.boxplot(mentalIssueDealtyByMasterDataset[importantVariables], ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

fig,ax=plt.subplots()
sns.boxplot(mentalIssueDealtyByMasterDataset[GDPColumnName],ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

plt.show()

# correlation coefficient and significance
def statisticalTest(mergedDataset, mentalIssueDataColumn, depressionDataColumn, alternative):
    mergedDataset[mentalIssueDataColumn] = mergedDataset[mentalIssueDataColumn][np.invert(mergedDataset[mentalIssueDataColumn].isna())]
    mergedDataset[depressionDataColumn] = mergedDataset[depressionDataColumn][np.invert(mergedDataset[depressionDataColumn].isna())]
    x, y = mergedDataset[mentalIssueDataColumn], mergedDataset[depressionDataColumn]
    x = x.fillna(x.mean())
    y = y.fillna(y.mean())

    return stats.pearsonr(x,y, alternative=alternative)

importantVariables = importantVariables + [GDPColumnName]

statisticalTestGDPReligiousSpiritual = statisticalTest(mentalIssueDealtyByMasterDataset, GDPColumnName, importantVariables[1], alternative='less')
statisticalTestGDPIndividualism = statisticalTest(mentalIssueDealtyByMasterDataset, GDPColumnName, importantVariables[2], alternative='greater')
statisticalTestGDPDepression = statisticalTest(mentalIssueDealtyByMasterDataset, GDPColumnName, importantVariables[0], alternative='greater')
statisticalTestFriendsFamilyDepression = statisticalTest(mentalIssueDealtyByMasterDataset, importantVariables[3], importantVariables[0], alternative='less')
statisticalTestReligiousSpiritualityDepression = statisticalTest(mentalIssueDealtyByMasterDataset, importantVariables[4], importantVariables[0], alternative='less')

significanceLevel = 0.05
statisticalTests = [statisticalTestGDPReligiousSpiritual, statisticalTestGDPIndividualism, statisticalTestGDPDepression, statisticalTestFriendsFamilyDepression, statisticalTestReligiousSpiritualityDepression]
print("ReligousSpiritualityDepressionTest: " + f"corrcoeff: {statisticalTestGDPReligiousSpiritual.statistic} " + f"p-value: {statisticalTestGDPReligiousSpiritual.pvalue}, pass: " + str(statisticalTestGDPReligiousSpiritual.pvalue < significanceLevel))
print("statisticalTestGDPIndividualism: " + f"corrcoeff: {statisticalTestGDPIndividualism.statistic} " + f"p-value: {statisticalTestGDPIndividualism.pvalue}, pass: " + str(statisticalTestGDPIndividualism.pvalue < significanceLevel))
print("statisticalTestGDPDepression: " + f"corrcoeff: {statisticalTestGDPDepression.statistic} " + f"p-value: {statisticalTestGDPDepression.pvalue}, pass: " + str(statisticalTestGDPDepression.pvalue < significanceLevel))
print("statisticalTestFriendsFamilyDepression: " + f"corrcoeff: {statisticalTestFriendsFamilyDepression.statistic} " + f"p-value: {statisticalTestFriendsFamilyDepression.pvalue}, pass: " + str(statisticalTestFriendsFamilyDepression.pvalue < significanceLevel))
print("statisticalTestReligiousSpiritualityDepression: " + f"corrcoeff: {statisticalTestReligiousSpiritualityDepression.statistic} " + f"p-value: {statisticalTestReligiousSpiritualityDepression.pvalue}, pass: " + str(statisticalTestReligiousSpiritualityDepression.pvalue < significanceLevel))

statisticalTestTable = {"Tests": ["Religous and Spirituality vs Depression", "GDP vs Individualism", "GDP vs Depression", "Talking to Friends and Family vs Depression", "Religious/Spirituality vs Depression"], "Statistic": [], "P-Value": []}
pValue = []
statistics = []
for i in statisticalTests:
    pValue.append(i.pvalue)
    statistics.append(i.statistic)

statisticalTestTable['P-Value'] = pValue
statisticalTestTable['Statistic'] = statistics

statisticalTestTable = pd.DataFrame(statisticalTestTable)
statisticalTestTable.to_csv('Plots/Datasets/statisticalTests')