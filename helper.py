import pandas as pd
import numpy as np

def preprocess(df, region_df):
    # Filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # Merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # Dropping duplicates
    df.drop_duplicates(inplace=True)
    # One hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def data_over_time(df, col):
    # Check if 'Year' and the specified column exist in the DataFrame
    if 'Year' not in df.columns or col not in df.columns:
        raise KeyError(f"Required columns 'Year' or '{col}' are missing from the DataFrame")

    # Get unique counts of years and specified column values
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    
    # Rename columns
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    
    # Debugging: Print the columns to check names
    print("Columns before sorting:", nations_over_time.columns)
    
    # Ensure the 'Edition' column exists
    if 'Edition' not in nations_over_time.columns:
        raise KeyError("'Edition' column is missing from the DataFrame")
    
    # Sort by 'Edition'
    nations_over_time = nations_over_time.sort_values('Edition')
    
    # Debugging: Print the DataFrame to check data
    print("DataFrame after sorting:", nations_over_time.head())
    
    return nations_over_time



def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    # Filter the DataFrame based on the selected country
    temp_df = temp_df[temp_df['region'] == country]

    # Count the number of medals per athlete
    x = temp_df['Name'].value_counts().reset_index()
    
    # Rename columns to ensure they match
    x.columns = ['Name', 'Medals']
    
    # Ensure the 'Name' column exists
    if 'Name' not in x.columns or 'Name' not in df.columns:
        raise KeyError("Column 'Name' is missing from one of the DataFrames")

    # Merge with the original DataFrame to get additional details
    x = x.head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final

