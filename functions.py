### define Player, Team, Game, Stadium and Round functions, build fixture and season

# collect individual game characteristics from each game played:
def build_fixture(df):
    global fixture
    unique_games = []
    for val in df.index.unique():
        unique_games.append(val)

    unique_games = pd.DataFrame(unique_games).drop(columns=[7,8])
    unique_games[4] = unique_games[4].astype(np.datetime64)
    # unique_games[4] = unique_games[4].datetime.date()
    unique_games.rename(columns={0: 'round_num', 1: 'home_team', 2: 'away_team', 3: 'weekday', 4: 'date', 5: 'start_time', 6: 'stadium'}, inplace=True)
    unique_games.set_index('date', drop=True, inplace=True)

    fixture = unique_games.sort_index().drop_duplicates(subset=['round_num', 'weekday', 'stadium', 'start_time'], keep='first').reset_index().drop(columns='stadium')

# assign dfs containing monthly weather information for each Stadium object: 
def assign_stadium_weather(weather_urls): 
    for city,url in weather_urls.items():
        for ven in Stadium.instances:
            if ven.location == city:
                ven._weather = pd.read_html(url, parse_dates=True, skiprows=1, index_col=0, header=0)[0]\
                                 .rename(weather_mapper, axis=1)\
                                 .reindex(columns=['Ann',1,2,3,4,5,6,7,8,9,10,11,12])

# build players using the Player_class:
def gen_Players(df):    
    for row in df.values:
        Player(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27])

# build teams using the Team_class:
def gen_Teams(df):    
    for team in df.Team.unique():
        Team(team)

# define how to construct a Stadium object:
def gen_Stadiums(df):
    for stadium in df.values:
        Stadium(stadium[0], stadium[1], stadium[2], stadium[3])
    assign_stadium_weather(weather_urls)

# read in games from fixture as Game objects:
def gen_Games(df):    
    for game in df.values:
        HomeAwayGame(game[0], game[1], game[2], game[3], game[4], game[5])
    Final._set_finals()

# build all conditions for season:
def _build_season():    
    gen_Players(teams)
    gen_Teams(teams)
    Team._gen_Rosters()
    gen_Stadiums(stadiums)
    build_fixture(pivotafl)
    gen_Games(fixture)