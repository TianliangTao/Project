# -*- coding: utf-8 -*-
"""data_clean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gk3AbWwY1hX3SibQCMjh4r6pcVQexVWD
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

def clean_number(data):
  """
  Input data contains dollar sign and comma in str format
  Ouput the data in int format without nan, the dollar sign and comma
  """
  df = data.copy()
  # Remove comma
  df = df.str.replace(',', '',regex=True)
  # Remove dollar sign
  df = df.str.replace('$', '',regex=True)
  # Convert to int type
  df = df.astype(int)
  return df

def change_runningtime(data):
  """
  Input data contains running time information in str format
  Output the running time in minitues and in int format
  """
  df = data.copy()
  
  # Add '00 min' to the data so the index will not be out of range for the data does not contain miniutes inforamtion
  df = df + ' 00 min'
  df = df.str.split(' ').apply(lambda x: int(x[0]) * 60 + int(x[2]))

  return df

def prepare_data(data):
  """
  
  """
  # Take a copy first
  df = data.copy()

  # Fix typo
  df = df.rename(columns = {'Worldwild':'Worldwide', 'Runing_Time':'Running_Time'})

  # Put 0 in the international feature of movies do not have the international box office information
  df['International'] = df['International'].replace(np.nan, '0')

  # Delete the movies with missing information
  df = df.dropna()

  # Delete the dollar sign and the comma, and convert the number in to int format
  df['Domestic'] = clean_number(df['Domestic'])
  df['International'] = clean_number(df['International'])
  df['Worldwide'] = clean_number(df['Worldwide'])
  df['Opening'] = clean_number(df['Opening'])
  df['Budget'] = clean_number(df['Budget'])

  # Convert the format of running_time to minutes
  df['Running_Time'] = change_runningtime(df['Running_Time'])

  # Extract the year and month information from release_date
  df['Release_Date'] = pd.to_datetime(df['Release_Date'])
  df['Release_Year'] = df['Release_Date'].dt.year
  df['Release_Month'] = df['Release_Date'].dt.month

  # Clean the space and \n in Genres feature and create lists contain genre information
  df['Genres'] = df['Genres'].str.replace(' ','')
  df['Genres'] = df['Genres'].str.split('\n\n')

  # Covert Distributor, MPAA, Release_Year, Release_Month and Genres features to dummy variables
  dist_dum = pd.get_dummies(df.Distributor, prefix='Distributor')
  mpaa_dum = pd.get_dummies(df.MPAA, prefix="MPAA")
  year_dum = pd.get_dummies(df.Release_Year, prefix="Release_Year")
  month_dum = pd.get_dummies(df.Release_Month, prefix="Release_Month")
  genre_dum = pd.get_dummies(df['Genres'].apply(pd.Series).stack(), prefix="Genre").groupby(level=0).sum()

  df = pd.concat([df, dist_dum, mpaa_dum, year_dum, month_dum, genre_dum], axis=1)
  df.drop(columns=['Movies', 'Distributor', 'MPAA', 'Release_Date', 'Release_Year', 'Release_Month', 'Genres'], inplace=True)

  # Normalize the data
  columns_to_normalize = ['Domestic', 'International', 'Worldwide', 'Opening', 'Budget', 'Running_Time']
  mean_scaler = preprocessing.StandardScaler()

  df[columns_to_normalize] = mean_scaler.fit_transform(df[columns_to_normalize])
  df['Worldwide'] = df['Worldwide'].to_numpy(dtype = np.float32).reshape((-1, 1))

  return df