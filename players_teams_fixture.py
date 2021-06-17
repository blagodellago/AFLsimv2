import pandas as pd

#### Stats for every player in every game of AFL since 2012 ####
# format columns:
def format_df(df):
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df.columns = [c.replace('(mm)', '') for c in df.columns]
    df.Player = df.Player.str.replace(', ', '_')
    df.Round = df.Round.str.replace('R', '').astype(int)

# isolate first and last names of each player and assign to respective columns:
def first_last_names(df):    
    pattern = r'^([A-Z][a-z]+)_([A-Z][a-z]+)$'
    names = df.Player.str.split(r'_', expand=True).rename({0: 'Last_Name', 1: 'First_Name'}, axis=1)
    df.insert(df.columns.get_loc('DOB'), 'First_Name', names.First_Name)
    df.insert(df.columns.get_loc('DOB'), 'Last_Name', names.Last_Name)

# read in dataset of AFL player statistics and format:
afl = pd.read_csv(r'data/afl_stats.csv')
afl = afl.loc[afl.Year == 2020].loc[afl.Round != 'EF'].loc[afl.Round != 'PF'].loc[afl.Round != 'SF'].loc[afl.Round != 'QF'].loc[afl.Round != 'GF']
format_df(afl)
first_last_names(afl)

# isolate players from each team:
teams = pd.pivot_table(afl, values=[
                                    
       'Height', 'Weight', 'Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals',
       'Behinds', 'Hit_Outs', 'Tackles', 'Rebounds', 'Inside_50s',
       'Clearances', 'Clangers', 'Frees', 'Frees_Against', 'Brownlow_Votes',
       'Contested_Possessions', 'Uncontested_Possessions', 'Contested_Marks',
       'Marks_Inside_50', 'One_Percenters', 'Bounces', 'Goal_Assists'

       ], index=['Team', 'Player', 'First_Name', 'Last_Name'])\
          .reset_index()\
          .reindex(columns=[
                
       'Player', 'First_Name', 'Last_Name', 'Team', 'Height', 'Weight', 
       'Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals',
       'Behinds', 'Hit_Outs', 'Tackles', 'Rebounds', 'Inside_50s',
       'Clearances', 'Clangers', 'Frees', 'Frees_Against', 'Brownlow_Votes',
       'Contested_Possessions', 'Uncontested_Possessions', 'Contested_Marks',
       'Marks_Inside_50', 'One_Percenters', 'Bounces', 'Goal_Assists'
       
       ]).round(2)

# pivot DF to get access to individual game characteristics:
pivotafl = afl.loc[afl.Year == 2020].pivot(index=['Round', 'Team', 'Player'], columns='Opposition')\
              .stack().reset_index()\
              .set_index(['Round', 'Team', 'Opposition', 'Day', 'Date', 'Start_Time', 'Venue', 'Attendance', 'Rainfall'])