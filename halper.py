import numpy as np

def fatch_data(main,year,country):
    medal_df = main.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'overall' and country == 'overall':
       temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
       temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Bronze','Silver']].sort_values('Year').reset_index()
    else:
       x = temp_df.groupby('region').sum()[['Gold','Bronze','Silver']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Bronze'] + x['Silver']

    
    return (x)
    

def medal_tally(main):
    # Drop duplicates
    medal_tally = main.drop_duplicates(
        subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal']
    )

    # Create indicator columns
    medal_tally['Gold'] = (medal_tally['Medal'] == 'Gold').astype(int)
    medal_tally['Silver'] = (medal_tally['Medal'] == 'Silver').astype(int)
    medal_tally['Bronze'] = (medal_tally['Medal'] == 'Bronze').astype(int)

    # Group and sum
    medal_tally = (
        medal_tally.groupby('region')[['Gold','Silver','Bronze']]
        .sum()
        .sort_values('Gold',ascending=False)
        .reset_index()
    )

    # Add total
    medal_tally['Total'] = (
        medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    )

    return medal_tally

import streamlit as st
@st.cache_data
def country_year_list(main):
    # Years: sorted integers + 'overall' at the top
    year = sorted(main['Year'].dropna().astype(int).unique().tolist())
    year.insert(0, 'overall')  # lowercase to match fatch_data

    # Countries: sorted unique + 'overall' at the top
    country = sorted(main['region'].dropna().unique().tolist())
    country.insert(0, 'overall')  # lowercase to match fatch_data

    return year, country

def data_over_time(main,col):
    nation_over_time = main.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')

    nation_over_time.rename(columns={'count':col},inplace=True)
    return nation_over_time


def most_successful(main, sport):
    # remove rows without medal
    temp_df = main.dropna(subset=['Medal'])

    # filter by sport if needed
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # count medals per athlete
    top_athletes = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(15)

    )
    top_athletes.columns = ['Name', 'Medal Count']

    # merge back to get region and sport info (use drop_duplicates to avoid duplicates)
    top_athletes = top_athletes.merge(
        main[['Name', 'region', 'Sport']].drop_duplicates(subset=['Name']),
        on='Name',
        how='left'
    )

    x =  top_athletes[['Name', 'region', 'Sport', 'Medal Count']]
    return x

def year_wise_analysis(main, country):
    temp_df = main.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)


    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def yearly_event_wise_analysis(main, country):
    temp_df = main.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return pt


def most_successful_country_wise(main, country):
    # remove rows without medal
    temp_df = main.dropna(subset=['Medal'])

    # filter by sport if needed
    if  country!= 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    # count medals per athlete
    top_athletes = (
        temp_df['Name']
        .value_counts()
        .reset_index()
        .head(10)
    )
    top_athletes.columns = ['Name', 'Medal Count']

    # merge back to get region and sport info (use drop_duplicates to avoid duplicates)
    top_athletes = top_athletes.merge(
        main[['Name', 'region', 'Sport']].drop_duplicates(subset=['Name']),
        on='Name',
        how='left'
    )

    x =  top_athletes[['Name', 'region', 'Sport', 'Medal Count']]
    return x

def weight_height_analysis(main, sport):
    athelets_data = main.drop_duplicates(['Name','region'])
    athelets_data['Medal'].fillna('No Medals',inplace=True)
    if sport != 'overall':
     temp_df = athelets_data[athelets_data['Sport'] ==  sport]
     return temp_df
    else:
       return athelets_data