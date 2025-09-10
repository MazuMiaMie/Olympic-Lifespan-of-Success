# import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor,halper


main = preprocessor.preprocess()

st.sidebar.title('Olympics analysis')
user_manu = st.sidebar.radio(
    'Select an option',
    ('Madel tally','overal analysis','Country wise analysis','Athelets wise analysis')
)

# st.dataframe(main)

if user_manu == 'Madel tally':
    st.sidebar.header('Medal tally')
    year,country = halper.country_year_list(main)
    select_year = st.sidebar.selectbox('Selected_Year',year)
    select_country = st.sidebar.selectbox('Selected_country',country)
    medal_tally = halper.fatch_data(main,select_year,select_country)
    if select_year == 'overall' and select_country =='overall':
        st.title('Overall')
    if select_year == 'overall' and select_country != 'overall':
        st.title('Overall of' +' '+ select_country)

    if select_year != 'overall' and select_country == 'overall':
        st.title('Overall in'+' '+ str(select_year))
    
    if select_year != 'overall' and select_country != 'overall':
        st.title(select_country +' '+ 'in' +' '+ str(select_year))

    st.table(medal_tally)

if user_manu == 'overal analysis':
    Editions = main['Year'].unique().shape[0]-1 # No of editions
    cities = main['City'].unique().shape[0] #No of olympics held in cities 
    events = main['Event'].unique().shape[0] #No of events/sport
    athelets = main['Name'].unique().shape[0] #No of athelets
    sports = main['Sport'].unique().shape[0]
    nations = main['region'].unique().shape[0] #participating nations

    st.title('Top Statistics')

    col1,col2,col3 = st.columns(3)
    with col1:
      st.header('Editions')
      st.title(Editions)
    with col2:
      st.header('Cities')
      st.title(cities)
    with col3:
      st.header('sports')
      st.title(sports)
    
    col1,col2,col3= st.columns(3)
    with col1:
      st.header('Name')
      st.title(athelets)
    with col2:
      st.header('Region')
      st.title(nations)
    with col3:
       st.header('Events')
       st.title(events)
    st.title('participating nation over time')
    nation_over_time = halper.data_over_time(main,'region')
    fig = px.line(nation_over_time, x="Year", y="region")
    st.plotly_chart(fig)

    st.title('Events over time')
    event_over_time = halper.data_over_time(main,'Event')
    fig = px.line(event_over_time, x="Year", y="Event")
    st.plotly_chart(fig)

    st.title('participating athelets over time')
    nation_over_time = halper.data_over_time(main,'Name')
    fig = px.line(nation_over_time, x="Year", y="Name")
    st.plotly_chart(fig)

    st.title('No. of Events over the time(All sports)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = main.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successfull Athelets')
    sport_list = main['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')

    select_list = st.selectbox('select a sport',sport_list)

    most_successful = halper.most_successful(main,select_list)
    st.table(most_successful)

if user_manu == 'Country wise analysis':
   country_list = main['region'].dropna().unique().tolist()
   country_list.sort()

   country_select = st.sidebar.selectbox('select country',country_list)
   st.title('Counrty wise analysis' +' '+'of'+' '+country_select)
   country = halper.year_wise_analysis(main,country_select)
   fig = px.line(country, x="Year", y="Medal")
   st.plotly_chart(fig)

   st.title('excless on the following sports' +' '+'of'+' '+country_select)
   pt = halper.yearly_event_wise_analysis(main,country_select)
   fig,ax = plt.subplots(figsize=(20,20))
   if not pt.empty:
    ax = sns.heatmap(pt, annot=True)
   else:
    st.write("Pivot table is empty. Cannot generate heatmap.")
  #  ax = sns.heatmap(pt,annot=True)
   st.pyplot(fig)

   st.title('Top 10 most famous athelets from' + ' '+ country_select)
   top10_athelets = halper.most_successful_country_wise(main,country_select)
   if not top10_athelets.empty:
      st.table(top10_athelets)
   else:
      st.title('No one yet achive medals')

if user_manu == 'Athelets wise analysis':
   st.title('Age distibution')
   athelets_data = main.drop_duplicates(['Name','region'])

   x1 = athelets_data['Age'].dropna()
   x2 = athelets_data[athelets_data['Medal']=='Gold']['Age'].dropna()
   x3 = athelets_data[athelets_data['Medal']=='Silver']['Age'].dropna()
   x4 = athelets_data[athelets_data['Medal']=='Bronze']['Age'].dropna()

   fig = ff.create_distplot([x1,x2,x3,x4],['overall Age','Gold madelest','Silver madelets','Bronze madelest'],show_hist=False,show_rug=False)

   st.plotly_chart(fig)

   st.title('Age distibution with respect to Gold')

   athelets_sport = [
       'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
       'Cricket', 'Ice Hockey', 'Racquets', 'Motorboating', 'Croquet',
       'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
       'Alpinism', 'Aeronautics'
    ]
   x = []
   name = []

   for sport in athelets_sport:
       temp_df = athelets_data[athelets_data['Sport'] == sport]
       ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
       if len(ages) > 1 and ages.nunique() > 1:   # must have >1 unique values
          x.append(ages)
          name.append(sport)

   fig2 = ff.create_distplot(x,name,show_hist=False,show_rug=False)
   st.plotly_chart(fig2)

   st.title('athelets data with respest to weight and height')
   sport_list = main['Sport'].dropna().unique().tolist()
   sport_list.sort()
   sport_list.insert(0,'overall')

   sport_select = st.selectbox('select country',sport_list)

   temp_df = halper.weight_height_analysis(main,sport_select)
   fig,ax =  plt.subplots()
   ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=70)
   st.pyplot(fig)
