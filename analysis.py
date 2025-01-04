import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
import requests

from functions import *

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
urbanisation = pd.read_excel('Datasets/Wikipedia Data on Urbanisation.xlsx')

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
listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry = ['Asia', 'Africa', 'Europe', 'North America', 'South America', 'World', 'High-income countries', 'Upper-middle-income countries', 'Lower-middle-income countries', 'Low-income countries', 'Kosovo', 'Hong Kong', 'Czechia', 'Oceania']

def remove_rows_from_ourworldindata_datasets(df):
    return remove_rows_from_df(df, 'Entity', listOfRemovalOfTerritoriesContinentsAndCategoriesOfCountry)
def remove_rows_unshared_between_datasets(df, columnName, df1, columnName1):
    unsharedValues = df[columnName][np.invert(df[columnName].isin(df1[columnName1]))].unique()
    return remove_rows_from_df(df, columnName, list(unsharedValues))


mentalIssuesDealtByFriendsFamily = remove_rows_from_ourworldindata_datasets(mentalIssuesDealtByFriendsFamily)
mentalIssuesDealtByMedication = remove_rows_from_ourworldindata_datasets(mentalIssuesDealtByMedication)
mentalIssuesDealtByReligionSpirituality = remove_rows_from_ourworldindata_datasets(mentalIssuesDealtByReligionSpirituality)
opinionThatScienceHelpsALotForMentalHealth = remove_rows_from_ourworldindata_datasets(opinionThatScienceHelpsALotForMentalHealth)
perceivedComfortSpeakingAboutAnxietyDepression = remove_rows_from_ourworldindata_datasets(perceivedComfortSpeakingAboutAnxietyDepression)
amountOfPsychiatristsWorking = remove_rows_from_ourworldindata_datasets(amountOfPsychiatristsWorking)

# removing all countries and terrorities in depression prevalence dataset that are in ourworldindata but not in depression prevalence dataset
depressionPrevalence = remove_rows_from_df(depressionPrevalence, 'metric_name', ['Number', 'Rate'])
#depressionPrevalence = remove_rows_from_df(depressionPrevalence, 'location_name', list(countriesInIHMENotInOurWorldInData))
depressionPrevalence = remove_rows_unshared_between_datasets(depressionPrevalence, 'location_name', mentalIssuesDealtByFriendsFamily, 'Entity')

# no correlation, but higher proportion of countries that have 3.5-4.0% depression rates with 85% of talking to friends and family
plt.scatter(depressionPrevalence['val'], mentalIssuesDealtByFriendsFamily['Share - Question: mh8c - Talked to friends or family when anxious/depressed - Answer: Yes - Gender: all - Age group: all'])
plt.show()

print(mentalIssuesDealtByReligionSpirituality['Entity'][mentalIssuesDealtByReligionSpirituality['Entity'].isin(depressionPrevalence['location_name'])])

# no correlation, but higher density of countries between 4.0-4.5%, may investigate into which countries these are
plt.scatter(depressionPrevalence['val'], mentalIssuesDealtByReligionSpirituality['Share - Question: mh8b - Engaged in religious/spiritual activities when anxious/depressed - Answer: Yes - Gender: all - Age group: all'])
plt.show()