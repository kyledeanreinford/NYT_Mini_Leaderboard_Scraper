

### INSTALL REQUIREMENTS

## pip install streamlit
## pip install altair
## pip install altair_viewer

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
# alt.renderers.enable('altair_viewer')

### Set some pandas parameters
pd.set_option('precision', 0)
pd.set_option('display.max_columns', None)

### Read Data

### CHANGE TO YOUR PATH HERE
kyle_path="/home/kdr/Desktop/"
david_path="/Users/dszakonyi/Dropbox/GitHub/NYT_Mini_Leaderboard_Scraper/"

### Load CSV
mini=pd.read_csv(kyle_path+"minitimes2.csv",
                 header=None,
                 index_col=False,
                 names=["row_id","solver","score","date"])

### Do some basic data cleaning
mini["score"]=pd.to_numeric(mini['score'], errors='coerce', downcast='integer').round()
mini['solver']=mini['solver'].str.lower()

### Designate the winning score for each day
mini["winner"]=mini.groupby('date')['score'].transform('min')

### Create a label for the plot where we can see the winning score
mini['label'] = np.where(mini['score']==mini["winner"], mini.score, '')
mini['label'] = mini['label'].str.replace(".0","")

### Create a binary variable for the winner
mini["winner_binary"]=np.where(mini['score']==mini["winner"], 1,0)

### See how many 'ties' there are for each day
mini["num_winners"]=mini.groupby('date')['winner_binary'].transform('sum')
mini["winner_relative"]=mini["winner_binary"]/mini["num_winners"]

### Create a binary variable if the player played
mini["played"]=np.where(mini["score"].isna(), 0,1)

#################################
### All-Time Victories        ###
#################################

pd.set_option('precision', 1)

### Aggregate Number of Victories
alltime = mini.groupby(
    ['solver'], as_index=False).agg(
    {'winner_relative':sum}
)

### Clean things up        
alltime = alltime.sort_values('winner_relative',
                                     ascending=False)
alltime.columns=["Solver","Total Wins"]
alltime=alltime.reset_index()
alltime.index += 1 
del alltime["index"]


#################################
### All-Time Average Times        ###
#################################


average = mini.groupby('solver').agg(
    average=pd.NamedAgg(column='score', aggfunc='mean'), 
    games=pd.NamedAgg(column='played', aggfunc='sum')
)

average.columns = average.columns.get_level_values(0)

average=average.reset_index()
average.index += 1 
average = average.sort_values('average',
                                     ascending=True)
average=average.reset_index()
average.index += 1 
del average["index"]
average.columns=["Solver","Mean Time","Days Played"]



### Fastest Times
fastest = mini.sort_values('score',ascending=True).head(5)
fastest = fastest[["solver", "date","score"]]
fastest["score"]=fastest["score"].astype(int)

fastest.columns=["Solver","Date","Score"]
fastest=fastest.reset_index()
fastest.index += 1 
del fastest["index"]


### Long to Wide
# pivoted_mini = mini.pivot(index='date', columns='solver', values='score')

# pivoted_mini=pivoted_mini.replace('--', np.NaN)

####################################
#### Do some Streamlit stuff
####################################

st.set_page_config(layout="wide")
c1, c2, c3 = st.beta_columns([1, 4,1])
# ### Set title information
c1.title('NYT Mini Leaderboard')

#### Plot - for now I'm using all the data, but we may just want to do the most recent seven days
base = alt.Chart(mini).properties(width=1000,height=350)

#### Plot the points
point = base.mark_circle(opacity=0.8,
    size=200).encode(
    x=alt.X('date', axis=alt.Axis(title='Date')),
    y=alt.Y('score', axis=alt.Axis(title='Score')),
    color=alt.Color('solver', legend=alt.Legend(title="Solver"),scale=alt.Scale(scheme='tableau10'))
).properties(
    title="Latest Week's Results"
)

#### Add the text labels     
text = point.mark_text(
    align='left',
    baseline='middle',
    dx=9
).encode(text='label'
)
   
### Put everything together and add the plot to streamlit
point = point + text

point=alt.concat(point,
    title=alt.TitleParams(
        'Winning scores are labelled.',
        color='darkgray',
        baseline='bottom',
        orient='bottom',
        anchor='end'
    )
)

c2.write(point)

#### Add Header
st.header("All-Time Statistics")


#### Create columns for the All-time tables
col1, col2, col3 = st.beta_columns([2, 2, 2])

col1.subheader("Daily Wins")
col1.dataframe(alltime)

col3.subheader("Average Times")
col3.dataframe(average)

col2.subheader("Fastest Times")
col2.dataframe(fastest)