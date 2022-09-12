import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
from plotly.offline import plot
from PIL import Image
image=Image.open(r"./bundesliga_logo.png")
st.set_page_config(
     page_title="Bundesliga dashboard",
     page_icon=image,
     layout="wide",
     initial_sidebar_state="expanded",
      )
st.set_option('deprecation.showPyplotGlobalUse', False)
#def add_bg_from_url():    st.markdown(         f"""         <style>         .stApp {{             background-image: url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");             background-attachment: fixed;             background-size: cover         }}         </style>         """,         unsafe_allow_html=True     )
#add_bg_from_url()





#save cleaned dataframe as df
df=pd.read_csv(r"./proj_5_v0.csv")
#drop column Unnamed
df.drop(['Unnamed: 0'],axis=1,inplace=True)
st.title('### Welcome to the Bundesliga dashboard ⚽ ') # set title of dashboard 
st.image(image,width=500) 
 
st.title('### Description')
st.write("The bundesliga is germany's top division of football")
st.write("Since its inception in 1962, Bayern Munich has been the most succesful club,lifting the trophy 31 times ")
st.write("With data from all bundesliga matches between 2017 and 2022, we present the user with this interactive dashbaord to gain insiaghts into the bundesliga")






team=df['home'].unique().tolist()  # get all teams in dataframe across all seasons


df.loc[df['home goals']>df['away goals'],'home win']=1  #create 3 new columns: home win, away win and draw to 
df.loc[df['home goals']<df['away goals'],'home win']=0  #to get number of matches won and tied per team
df.loc[df['home goals']==df['away goals'],'home win']=0
df.loc[df['away goals']>df['home goals'],'away win']=1
df.loc[df['away goals']<df['home goals'],'away win']=0
df.loc[df['away goals']==df['home goals'],'away win']=0
df.loc[df['away goals']>df['home goals'],'draw']=0
df.loc[df['away goals']<df['home goals'],'draw']=0
df.loc[df['away goals']==df['home goals'],'draw']=1
df['home win'] = df['home win'].astype(int)
df['away win'] = df['away win'].astype(int)
df['draw'] = df['draw'].astype(int)

df.loc[df['home goals']>df['away goals'],'home points']=3 # create 2 new columns to store points won at home and away
df.loc[df['home goals']<df['away goals'],'home points']=0
df.loc[df['home goals']==df['away goals'],'home points']=1
df.loc[df['away goals']>df['home goals'],'away points']=3
df.loc[df['away goals']<df['home goals'],'away points']=0
df.loc[df['away goals']==df['home goals'],'away points']=1

df['home points'] = df['home points'].astype(int)
df['away points'] = df['away points'].astype(int)

df['date'] = pd.to_datetime(df['date']) # convert date column into date type for easier manipulation of dates
df.loc[(df['date']>='2017-07')&(df['date']<'2018-07'),'season']='2017-2018'  # get season of each match depending on match date
df.loc[(df['date']>='2018-07')&(df['date']<'2019-07'),'season']='2018-2019'
df.loc[(df['date']>='2019-07')&(df['date']<'2020-07'),'season']='2019-2020'
df.loc[(df['date']>='2020-07')&(df['date']<'2021-07'),'season']='2020-2021'
df.loc[(df['date']>='2021-07')&(df['date']<'2022-07'),'season']='2021-2022'



#Ask user to choose seaon, display winner  and table of selected season using the following commands:
st.header('1- Lets look at the champion and standing during the season of your choice')
st.sidebar.subheader('### 1-Champion and standing')
season = st.sidebar.selectbox(
     'Select season',
     ('2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022'))
st.sidebar.write("  ")
temp=df[df['season']==season]
teams_season=temp['home'].unique().tolist()

st_df=pd.DataFrame(index=teams_season)  #create new dataframe with the index set as the teams that played 
                                        # during the selected season

for team in teams_season:  #loop through each team  to get the follwing:
    home_wins=temp[temp['home']==team]['home win'].sum()     #Calculate total number of home wins
    home_goals=temp[temp['home']==team]['home goals'].sum()   #Calculate total number of home goals scored
    home_goals_c=temp[temp['home']==team]['away goals'].sum()  #Calculate total number of home goals conceded
    away_wins=temp[temp['away']==team]['away win'].sum()       #Calculate total number of away wins
    away_goals=temp[temp['away']==team]['away goals'].sum()    #Calculate total number of away goals scored
    away_goals_c=temp[temp['away']==team]['home goals'].sum()   #Calculate total number of away goals conceded
    draws=temp[(temp['home']==team)|(temp['away']==team)]['draw'].sum()  #calculate total number of draws
    tot_wins=home_wins+away_wins                                          #get total wins
    goals_c=home_goals_c+away_goals                                     #get total goals conceded
    losses=34-tot_wins-draws                                           # get total matches lost
    st_df.loc[team,'W']=tot_wins                                       #create new column to store total wins
    st_df.loc[team,'D']=draws                                          #create new column to store total draws
    st_df.loc[team,'L']=losses                                         #create new column to store total losses
    st_df.loc[team,'GF']=home_goals+away_goals                         #create new column to store total goals scored
    st_df.loc[team,'GA']= goals_c                                      #create new column to store total goals conceded

st_df['Points']=st_df['W']*3+st_df['D']*1                              #store total points in new column Points
st_df['GD']=st_df['GF']-st_df['GA']                                     #store goal difference in new column called GD
st_df['W']=st_df['W'].astype(int)
st_df['L']=st_df['L'].astype(int)
st_df['D']=st_df['D'].astype(int)
st_df['Points']=st_df['Points'].astype(int)
st_df['GF']=st_df['GF'].astype(int)
st_df['GA']=st_df['GA'].astype(int)
st_df['GD']=st_df['GD'].astype(int)
st_df["Ranking"] = st_df[["Points","GD"]].apply(tuple,axis=1).rank(method='dense',ascending=False).astype(int)
ranked_table=st_df.sort_values(by='Ranking')         #rank each team based on Points first, and in case of a draw on goal differnce using the rank function
champion=ranked_table.loc[ranked_table['Ranking']==1]
champion=champion.index[0]                              #return the champion of selected season

st.write('The champion was: ',champion)   #display champion of selected season
st.write(ranked_table) #display table of selected season




#In this section, I look at how attendance has changed throughout each season for teams selected
#by the user


st.header("2- Now, lets check how the attendance changed over each season")

# get all teams in dataframe across all seasons
all_teams=df['home'].unique()
attendance_temp=df #create copy of dataframe to manipulate without altering the original cleaned dataframe
t=attendance_temp.groupby(['season','home']).agg({'attendance':np.mean})   #group dataframe by season and home team, agg attendance by the average
t=t.reset_index()   

st.sidebar.subheader("### 2-Attendance")
team_sel = st.sidebar.multiselect(
     'Choose team',             #prompt user to select any team/s he/she wants
     all_teams
     )
st.sidebar.write("  ")
fig,ax=plt.subplots(1,1,figsize=(20,10))
sns.set_style("dark")         #initialize figure and set style to dark
for team in team_sel:          #loop over teams selected by the user
    m=t.loc[t['home']==team]      #get rows that include all season and home team as the iterate teams
    ax=sns.lineplot(x='season',y='attendance',data=m,linewidth = 8)  #plot average attendance vs season 
    plt.legend(labels=team_sel,prop={'size': 14})
    plt.xlabel('Season',fontsize=28,fontweight='bold',color='gold')
    plt.ylabel('Attendance',fontsize=28,fontweight='bold',color='gold')
    plt.xticks(['2017-2018','2018-2019','2019-2020','2020-2021','2021-2022'],fontsize=14,fontweight='bold')
    plt.yticks(fontsize=14,fontweight='bold')
    plt.title('Attendance variance by season',fontweight='bold',color='gold',fontsize=34)
    
    
st.pyplot() #disply plot on streamlit


#In this section, we look at how the ranking of a selected team changes during each matchday of selected season

st.header("3- Aren't you curious to see how each team's ranking changed after each matchday? Lets check together!")
st.sidebar.subheader("### 3-Ranking ")
sel_season= st.sidebar.selectbox(
     'Select season ',
     (('2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022')))
teams_in_season=df[df['season']==sel_season]['home'].unique().tolist()
sel_team= st.sidebar.selectbox(
     'Select Team',                 #prompt user to select season and team
     (teams_in_season))

st.sidebar.write("  ")

#Ranking of team throughout season

chosen_season=df[df['season']==sel_season]          #store the dataframe of selected season in a new variable   
teams_season=chosen_season['home'].unique()         #get teams that participated in selected season
teams_season.sort()                                 #sort teams by name
#teams_season
chosen_season=chosen_season[['home','away','home goals','away goals','home points','away points']] #get the relevant columns from dataframe for ease of use
weeks=np.array_split(chosen_season, 34)  #split dataframe into 34 parts, each representing the matchday week (total 34 weeks in the bundesliga per season)
standing=pd.DataFrame({'Teams':teams_season,'Points':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'Goal difference':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]})
standing.set_index('Teams',inplace=True)  #create a new dataframe with the teams as an index and 2 columns representing the points and goal difference
standing_dict={}                                   #create dictionary to store each team's ranking during each matchday
for team in teams_season:
    standing_dict[team]=[]                      #loop over selected teams to set dict keys as team name
for week in weeks:                              #loop over each matchday week
    x=week
    x_home=x[['home','home points','home goals','away goals']]  #store home components as a new dataframe
    x_home.rename(columns={'home':'Team','home points':'Points','home goals':'gf','away goals':'ga'},inplace=True)
    x_home['Goal diff']=x_home['gf']-x_home['ga']
    x_home.drop(['gf','ga'],axis=1,inplace=True) #Rename columns to match away columns, this is helpful to concat the two columns vertically
    
    x_away=x[['away','away points','away goals','home goals']]
    x_away.rename(columns={'away':'Team','away points':'Points','away goals':'gf','home goals':'ga'},inplace=True)
    x_away['Goal diff']=x_away['gf']-x_away['ga']
    x_away.drop(['gf','ga'],axis=1,inplace=True) #rename columns to match home columns
    
    x_conc=pd.concat([x_home,x_away],axis=0,ignore_index=True) #concat the two dataframe vertically, we now have 18 rows, each representing a team's points and goal difference
    x_conc=x_conc.sort_values(by='Team') #sort the concatenated dataframe by name to match the standings dataframe
    week_points=np.array(x_conc['Points'])  #store the current week's points in an array
    week_gd=np.array(x_conc['Goal diff'])    #store the current week's goal difference in an array
    standing['points_week']=week_points         #add current week's points to a column in the dataframe
    standing['gd_week']=week_gd                #add current week's goal difference to a column in the dataframe
    standing['Points']=standing['Points']+standing['points_week']   #during each week, the points accumulated in the previous week are added to the new points gained during the current week
    standing['Goal difference']=standing['Goal difference']+standing['gd_week'] #same for goal difference
    #now we use the rank function during each week to get the ranking of each team during the current week based on points and GD accumulated upto current week
    standing["Rank"] = standing[["Points","Goal difference"]].apply(tuple,axis=1).rank(method='dense',ascending=False).astype(int)
    for team in standing_dict.keys():
        standing_dict[team].append(standing.loc[team]["Rank"]) #we add the weekly ranking of each team to the dictionary by key of team
game_week=range(1,35)
plt.plot(game_week,standing_dict[sel_team],linewidth=2, markersize=12,marker='o',markerfacecolor='red') # now that we have a dictionary with the keys as the team and values as a list of ranking throught each week
plt.gca().invert_yaxis()                                                                               # we plot the ranking of the team during each week
plt.xlabel('Matchday',fontsize=20,fontweight='bold',color='b')
plt.ylabel('Ranking',fontsize=20,color='b',fontweight='bold')
plt.title(f"{sel_team}'s ranking over the {sel_season} season", fontweight='bold', fontsize=24)
plt.xticks(fontsize=16,fontweight='bold',color='r')
plt.yticks(fontsize=16,fontweight='bold',color='r')
plt.xlim(0,35)
plt.xticks(range(1,35)) 

st.pyplot() #display plot on streamlit app




#in this section,we take a look at the win % of teams when being officiated by a certain referee
#only referees who served at least 5 games were 
#a bar chart will be plotted for visualization
  
st.header("4- We all heard that some teams dont like being officiated by a certain referee,do they have a point?")

st.sidebar.subheader('### 4-Referee influence')
#promt user to select team of interest
team_selected=st.sidebar.selectbox(label='Select team',options=df['home'].unique().tolist())



#create a datafrane with only the matches played by selected team, and count number of matches officiated by each referee
count_ref=df[(df['home']==team_selected)|(df['away']==team_selected)]['referee'].value_counts()
count_ref=pd.DataFrame(count_ref)
count_ref.rename(columns={'referee':'num of matches'},inplace=True)
count_ref=count_ref[count_ref['num of matches']>=5] #keep only referees with >=5 games officiated
refs=list(count_ref.index) #store referee names in a list
for ref in refs:  #loop over referee list
    home_wins=df[(df['home']==team_selected) & (df['referee']==ref)]['home win'].sum()
    away_wins=df[(df['away']==team_selected) & (df['referee']==ref)]['away win'].sum()
    total_wins=home_wins+away_wins #get the total home and away wins by team by referee
    count_ref.loc[ref,'num of wins']=int(total_wins) #store num of wins in dataframe
count_ref['num of wins']=count_ref['num of wins'].astype(int)
count_ref['Win %']=(count_ref['num of wins']/count_ref['num of matches']) * 100 #get % of matches won when each referee officiated
count_ref=count_ref.sort_values(by='Win %',ascending=False) #sort by win %
count_ref=count_ref.reset_index()
count_ref.rename(columns={'index':'Referee'},inplace=True)
#plot a barchart

z=px.bar(count_ref,x='Referee',y='Win %',color='Referee', hover_data=['num of matches'],title=f"Influence of referees on {team_selected}'s matches since 2017-2018",width=1000, height=800)
#st.plotly_chart(z,use_container_width=True)
z.update_layout(
font=dict(
        family="Courier New, monospace",
        size=22,
        color="orange"
    )
)
st.write(z) #display plot on streamlit



#In this section, we track the expected goals and actual goals scored by a selected team during a selected season

st.header("5- Analytics have entered the sports world, one of those metrics is expected goals (the estimated number of goals a team will score in a certain game.Is it reliable?")



#prompt user to select season and team
col1, col2 = st.columns(2)
with col1:
    season_sel=st.radio("Choose season",('2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022'))

with col2:
        tg=st.selectbox(label='Select team',options=df[df['season']==season_sel]['home'].unique().tolist())

team=tg
seas=season_sel
df_temp=df[((df['home']==team) | (df['away']==team)) & (df['season']==seas)] #create dataframe with only matched played by selected team during a selected season
c_home=df_temp[df_temp['home']==team][['date','xg_home','home goals']]
c_home.rename(columns={'home goals':'Goals scored','xg_home':'xg'},inplace=True) #store date, expected goals and actual goals at home in a dataframe
c_home['loc']='H'
c_away=df_temp[df_temp['away']==team][['date','xg_away','away goals']]
c_away.rename(columns={'away goals':'Goals scored','xg_away':'xg'},inplace=True) #store date, expected goals and actual goals away in a dataframe
c_away['loc']='A'
combined_df=pd.concat([c_home,c_away],ignore_index=True) #concat the two dataframes
combined_df=combined_df.sort_values(by='date') #sort by date
combined_df=combined_df.set_index('date') # set date as index
sns.lineplot(x=combined_df.index,y=combined_df['xg'],color='r',label='Expected goals',linewidth = 8) #plot xg vs date and actual goals vs date on same plot
sns.lineplot(x=combined_df.index,y=combined_df['Goals scored'],color='g',label='Goals scored',linewidth = 8)
plt.xlabel('Date',fontweight='bold',fontsize=22)
plt.ylabel('Goals',fontweight='bold',fontsize=22)
plt.xticks(rotation='vertical',fontsize=16,fontweight='bold')
plt.yticks(fontsize=16,fontweight='bold',color='orange')
plt.legend(fontsize=15)
plt.title(f"{team}'s expected vs actual goals scored during the {seas} season", fontsize=32,fontweight='bold')
st.pyplot() #diplay plot on steamlit

#for the same team and seaosn, we plot a scatter plot, where we differentiate between home and away 
x=px.scatter(combined_df, x="xg", y="Goals scored", color="loc",width=1000, height=500, trendline="ols",trendline_scope="overall", trendline_color_override="black")
x.update_layout(
    margin=dict(l=0.5, r=0.5, t=0.5, b=0.5)
)
#.plotly_chart(x,use_container_width=True)
x.update_traces(marker=dict(size=20,
                              line=dict(width=4,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
x.update_layout(
    
    
    xaxis_title="Expected goals",
    yaxis_title="Actual goals",
    legend_title="Location",
    font=dict(
        family="Courier New, monospace",
        size=22,
        color="orange"
    )
)
st.write(x) #display plot on streamlit

