import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
import requests

# Fetch the data.
mentalIssuesDealtByReligionSpirituality = pd.read_csv("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-religious-spiritual.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadataMentalIssuesDealtByReligionSpirituality = requests.get("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-religious-spiritual.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

# Fetch the data.
mentalIssuesDealtByFriendsFamily = pd.read_csv("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-friends-family.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadataMentalIssuesDealtByFriendsFamily = requests.get("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-friends-family.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

# Fetch the data.
mentalIssuesDealtByMedication = pd.read_csv("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-took-prescribed-medication.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadataMentalIssuesDealtByMedication = requests.get("https://ourworldindata.org/grapher/dealt-with-anxiety-depression-took-prescribed-medication.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

# Fetch the data.
opinionThatScienceHelpsALotForMentalHealth = pd.read_csv("https://ourworldindata.org/grapher/science-helps-a-lot-treating-anxiety-depression-vs-gdp-per-capita.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadataOpinionThatScienceHelpsALotForMentalHealth = requests.get("https://ourworldindata.org/grapher/science-helps-a-lot-treating-anxiety-depression-vs-gdp-per-capita.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

# Fetch the data.
perceivedComfortSpeakingAboutAnxietyDepression = pd.read_csv("https://ourworldindata.org/grapher/perceived-comfort-speaking-anxiety-depression.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadataPerceivedComfortSpeakingAboutAnxietyDepression = requests.get("https://ourworldindata.org/grapher/perceived-comfort-speaking-anxiety-depression.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

# Fetch the data.
amountOfPsychiatristsWorking = pd.read_csv("https://ourworldindata.org/grapher/psychiatrists-working-in-the-mental-health-sector.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadataAmountOfPsychiatristsWorking = requests.get("https://ourworldindata.org/grapher/psychiatrists-working-in-the-mental-health-sector.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

print(mentalIssuesDealtByFriendsFamily)
print(opinionThatScienceHelpsALotForMentalHealth)
print(amountOfPsychiatristsWorking)
print(perceivedComfortSpeakingAboutAnxietyDepression)