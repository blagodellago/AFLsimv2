
##### To Do
## Create fixture for future seasons
# determine which data I can reuse and only pull that
## Have players randomly retire after 30
## Draft random new players to fill list vacancies


# determine which data I can reuse and only pull that
# - teams df, same stadium/weather logic
# - reuse 2019 fixture using same match
rounds = list(range(1,24))



# pass it dataframe from 'matches' dictionary
def create_future_season(dict_of_df):

    timeslots = {
    'Thursday' : ['7:25pm'],
    'Friday' : ['7:50pm'],
    'Saturday' : ['1:45pm','4:05pm','7:25pm','7:45pm'],
    'Sunday' : ['1:10pm','3:20pm','5:10pm']
    }

    tmstmp = pd.Timestamp(f'{year}-04-01')

    counter=1
    while counter <= 24:
        df = dict_of_df[counter] 
        while tmstmp.strftime('%A') != 'Thursday':
            tmstmp += pd.Timedelta(1, 'day')


        for day,times in timeslots.items():
            if day == 'Thursday':
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[0], df.away_team[0], tmstmp.strftime('%A'), times)
                tmstmp += pd.Timedelta(1, 'day')
            if day == 'Friday':
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[1], df.away_team[1], tmstmp.strftime('%A'), times)
                tmstmp += pd.Timedelta(1, 'day')
            if day == 'Saturday':
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[2], df.away_team[2], tmstmp.strftime('%A'), times[0])
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[3], df.away_team[3], tmstmp.strftime('%A'), times[1])
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[4], df.away_team[4], tmstmp.strftime('%A'), times[2])
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[5], df.away_team[5], tmstmp.strftime('%A'), times[3])
                tmstmp += pd.Timedelta(1, 'day')
            elif day == 'Sunday':
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[6], df.away_team[6], tmstmp.strftime('%A'), times[0])
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[7], df.away_team[7], tmstmp.strftime('%A'), times[1])
                HomeAwayGame(tmstmp, df.round_num[0], df.home_team[8], df.away_team[8], tmstmp.strftime('%A'), times[2])

        tmstmp += pd.Timedelta(1, 'day')
        counter += 1    
        



Season.afl.loc[Season.afl.Year == 2019].loc[Season.afl.Round != 'EF'].loc[Season.afl.Round != 'PF'].loc[Season.afl.Round != 'SF'].loc[Season.afl.Round != 'QF'].loc[Season.afl.Round != 'GF']
Season._format_df(self._data)
Season._first_last_names(self._data)

fixturedf = self._data.loc[self._data.Year == self.year].pivot(index=['Round', 'Team', 'Player'], columns='Opposition')\
            .stack().reset_index()\
            .set_index(['Round', 'Team', 'Opposition', 'Day', 'Date', 'Start_Time', 'Venue', 'Attendance', 'Rainfall'])

def _build_known_fixture(df):
    # build fixture for in class dataset
    global fixture
    unique_games = []
    for val in df.index.unique():
        unique_games.append(val)
    unique_games = pd.DataFrame(unique_games).drop(columns=[7,8])
    unique_games[4] = unique_games[4].astype(np.datetime64)
    unique_games.rename(columns={0: 'round_num', 1: 'home_team', 2: 'away_team', 3: 'weekday', 4: 'date', 5: 'start_time', 6: 'stadium'}, inplace=True)
    unique_games.set_index('date', drop=True, inplace=True)
    fixture = unique_games.sort_index().drop_duplicates(subset=['round_num', 'weekday', 'stadium', 'start_time'], keep='first').reset_index()
    fixture = fixture.drop(columns=['date','weekday','start_time'])

_build_known_fixture(fixturedf)

rounds = list(range(1,24))
matches = {}
for round_num in rounds:
    matches[round_num] = fixture.loc[fixture.round_num == round_num]

