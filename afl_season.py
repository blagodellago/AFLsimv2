import re, os, sys, getopt
import pandas as pd
import numpy as np
from main import InstanceList, Player, Team, Game, HomeAwayGame, Final, Stadium, Round, color
from random import choice
from time import sleep

class Season:
    """Pass a year to initialize a complete season simulation of AFL football,
    based on stats from every player in every game in the 2020 AFL season"""

    # read in dataset of AFL player statistics
    afl = pd.read_csv(r'data/afl_stats.csv')

    instances = InstanceList()

    @classmethod
    def _reset_class_instances(cls):
        Season.afl = pd.read_csv(r'data/afl_stats.csv')
        Team.instances.clear()
        Game.instances.clear()
        HomeAwayGame.games_scheduled.clear()
        HomeAwayGame.games_played.clear()
        HomeAwayGame.instances.clear()
        HomeAwayGame.fixture.clear()
        Stadium.instances.clear()
        Final.instances.clear()
        Player.instances.clear()
        Round.instances.clear()
        Team.ladder = None

    @classmethod
    def _welcome_message(cls,season):

        year_stats = {
            2012 : {'Premier' : 'Sydney Swans', 'Wooden Spoon' : 'Greater Western Sydney', 'Brownlow Medal' : ['Sam Mitchell', 'Trent Cotchin']},
            2013 : {'Premier' : 'Hawthorn', 'Wooden Spoon' : 'Greater Western Sydney', 'Brownlow Medal' : 'Gary Ablett, Jr.'},
            2014 : {'Premier' : 'Hawthorn', 'Wooden Spoon' : 'St. Kilda', 'Brownlow Medal' : 'Matt Priddis'},
            2015 : {'Premier' : 'Hawthorn', 'Wooden Spoon' : 'Carlton', 'Brownlow Medal' : 'Nat Fyfe'},
            2016 : {'Premier' : 'Western Bulldogs', 'Wooden Spoon' : 'Essendon', 'Brownlow Medal' : 'Patrick Dangerfield'},
            2017 : {'Premier' : 'Richmond', 'Wooden Spoon' : 'Brisbane Lions', 'Brownlow Medal' : 'Dusty Martin'},
            2018 : {'Premier' : 'West Coast', 'Wooden Spoon' : 'Carlton', 'Brownlow Medal' : 'Tom Mitchell'},
            2019 : {'Premier' : 'Richmond', 'Wooden Spoon' : 'Gold Coast', 'Brownlow Medal' : 'Nat Fyfe'},
            2020 : {'Premier' : 'Richmond', 'Wooden Spoon' : 'Adelaide', 'Brownlow Medal' : 'Lachie Neale'},
        }

        for year,stats in year_stats.items():
            if season == year:
                message1 = f'Season {season} came and went...'
                message2 = '*' + color.BOLD + f'{stats["Premier"]}' + color.END + ' won the premiership after a stellar season'
                message3 = '*On the other hand, it was a long year for the wooden spooners ' + color.BOLD + f'{stats["Wooden Spoon"]}' + color.END
                message4 = '*There were two clear standouts, along with a drug cheat:'
                message5 = color.BOLD + f'\t\t*{stats["Brownlow Medal"][0]}' + color.END + ' and ' + color.BOLD + f'{stats["Brownlow Medal"][1]}' + color.END +  ' were both outstanding, and joint Brownlow Medal winners'
                message6 = '*Individually, ' + color.BOLD + f'{stats["Brownlow Medal"]}' + color.END + ' was outstanding, winning the Brownlow Medal'
                print(message1)
                print()
                sleep(1)
                print(message2)
                print()
                sleep(1)
                print(message3)
                print()
                sleep(1)
                if type(stats["Brownlow Medal"]) == list:
                    print(message4)
                    print(message5)
                else:
                    print(message6)

        message7 = color.YELLOW + f"...Building season conditions for {season}..." + color.END
        print()
        print(color.CYAN + "-------------------------------------------------------------------------------------------------------------------" + color.END)
        print(f'\t\t\t\t\t{message7}')
        print(color.CYAN + "-------------------------------------------------------------------------------------------------------------------" + color.END)

    @classmethod
    def _format_df(cls, df):
        # format columns to accommodate Player and Team initializers
        df.columns = [c.replace(' ', '_') for c in df.columns]
        df.columns = [c.replace('(mm)', '') for c in df.columns]
        df.Player = df.Player.str.replace(', ', '_')
        df.Round = df.Round.astype(str)
        df.Round = df.Round.str.replace('R', '').astype(int)

    @classmethod 
    def _first_last_names(cls, df):    
        # isolate first and last names of each player
        pattern = r'^([A-Z][a-z]+)_([A-Z][a-z]+)$'
        names = df.Player.str.split(r'_', expand=True).rename({0: 'Last_Name', 1: 'First_Name'}, axis=1)
        while df.columns.size != 44:
            df.insert(df.columns.get_loc('DOB'), 'First_Name', names.First_Name)
            df.insert(df.columns.get_loc('DOB'), 'Last_Name', names.Last_Name)

    def __init__(self, year=None):
        # generate data corresponding to the year passed from the class dataset if requested year falls in range of dataset
        Season._reset_class_instances()

        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        print(color.CYAN + "*******************************************************************************************" + color.END, color.BOLD + "github.com/blagodellago" + color.END)
        print(color.CYAN + "*******************************" + color.END, color.BOLD + "WELCOME TO THE AFL SEASON SIMULATOR" + color.END, color.CYAN + "***********************************************" + color.END)
        print(color.CYAN + "*******************************************************************************************************************" + color.END)
        print(color.BLUE + "###################################################################################################################" + color.END)
        print(color.BLUE + "###################################################################################################################" + color.END)
        print(color.BLUE + "####" + color.END + color.RED + "##########################################################################################################" + color.END + color.BLUE + "#####" + color.END)
        print(color.BLUE + "####" + color.END + color.RED + "##########################################################################################################" + color.END + color.BLUE + "#####" + color.END)
        print(color.BLUE + "####" + color.END + color.BOLD + "##########################################################################################################" + color.END + color.BLUE + "#####" + color.END)
        print(color.BLUE + "####" + color.END + color.BOLD + "##########################################################################################################" + color.END + color.BLUE + "#####" + color.END)
        print(color.BLUE + "###################################################################################################################" + color.END)
        print(color.BLUE + "###################################################################################################################" + color.END)
        print()
        print()

        # if no year specified use a random known year
        if year == None:
            self.year = choice([2012,2013,2014,2015,2016,2017,2018,2019,2020])
        else:
            self.year = year

        for season in Season.instances:
            if season.year == year:
                Season.instances.remove(season)
        self.teams = Team.instances
        self.hagames = HomeAwayGame.instances
        self.stadiums = Stadium.instances
        self.finals = Final.instances
        self.players = Player.instances
        self.rounds = Round.instances
        self._tmstmp = pd.Timestamp(f'{self.year}-04-01')
        Season._welcome_message(self.year)

        if self.year in [2012,2013,2014,2015,2016,2017,2018,2019,2020]:
            self._data = Season.afl.loc[Season.afl.Year == self.year].loc[Season.afl.Round != 'EF'].loc[Season.afl.Round != 'PF'].loc[Season.afl.Round != 'SF'].loc[Season.afl.Round != 'QF'].loc[Season.afl.Round != 'GF']
            self._build_known_fixture()
        elif self.year >= 2021:
            self._build_future_fixture(self.year)
        Season.instances.append(self)

    def __repr__(self):
        return f'Season: {self.year}'

    # print ladder after specified round
    def ladder(self, round_num):
        rnd = round_num - 1
        print(self.rounds[rnd].ladder)

    # build fixture using known player data
    def _build_known_fixture(self):
        # create players and teams based on the year specified
        Season._format_df(self._data)
        Season._first_last_names(self._data)

        teams = pd.pivot_table(self._data, values=[
        # isolate players from each team    

            'Height', 'Weight', 'Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals',
            'Behinds', 'Hit_Outs', 'Tackles', 'Rebounds', 'Inside_50s',
            'Clearances', 'Clangers', 'Frees', 'Frees_Against', 'Brownlow_Votes',
            'Contested_Possessions', 'Uncontested_Possessions', 'Contested_Marks',
            'Marks_Inside_50', 'One_Percenters', 'Bounces', 'Goal_Assists'

            ], index=['Team', 'Player', 'First_Name', 'Last_Name', 'DOB'])\
                .reset_index()\
                .reindex(columns=[
                        
            'Player', 'First_Name', 'Last_Name', 'Team', 'DOB', 'Height', 'Weight', 
            'Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals',
            'Behinds', 'Hit_Outs', 'Tackles', 'Rebounds', 'Inside_50s',
            'Clearances', 'Clangers', 'Frees', 'Frees_Against', 'Brownlow_Votes',
            'Contested_Possessions', 'Uncontested_Possessions', 'Contested_Marks',
            'Marks_Inside_50', 'One_Percenters', 'Bounces', 'Goal_Assists'
            
            ]).round(2)

        # pivot DF to get access to individual game characteristics:
        fixturedf = self._data.loc[self._data.Year == self.year].pivot(index=['Round', 'Team', 'Player'], columns='Opposition')\
                    .stack().reset_index()\
                    .set_index(['Round', 'Team', 'Opposition', 'Day', 'Date', 'Start_Time', 'Venue', 'Attendance', 'Rainfall'])

        self._gen_Teams(teams)
        self._gen_Players(teams)
        self._create_stadiums()

        unique_games = []
        for val in fixturedf.index.unique():
            unique_games.append(val)
        unique_games = pd.DataFrame(unique_games).drop(columns=[7,8])
        unique_games[4] = unique_games[4].astype(np.datetime64)
        unique_games.rename(columns={0: 'round_num', 1: 'home_team', 2: 'away_team', 3: 'weekday', 4: 'date', 5: 'start_time', 6: 'stadium'}, inplace=True)
        unique_games.set_index('date', drop=True, inplace=True)
        fixture = unique_games.sort_index().drop_duplicates(subset=['round_num', 'weekday', 'stadium', 'start_time'], keep='first').reset_index().drop(columns='stadium')

        self._gen_Games(fixture)
        Round._assign_rounds()

    def _build_future_fixture(self, year):

        # create players and teams based on the year specified
        self._teams_data = Season.afl.loc[Season.afl.Year == 2020].loc[Season.afl.Round != 'EF'].loc[Season.afl.Round != 'PF'].loc[Season.afl.Round != 'SF'].loc[Season.afl.Round != 'QF'].loc[Season.afl.Round != 'GF']
        Season._format_df(self._teams_data)
        Season._first_last_names(self._teams_data)

        teams = pd.pivot_table(self._teams_data, values=[
        # isolate players from each team    

            'Height', 'Weight', 'Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals',
            'Behinds', 'Hit_Outs', 'Tackles', 'Rebounds', 'Inside_50s',
            'Clearances', 'Clangers', 'Frees', 'Frees_Against', 'Brownlow_Votes',
            'Contested_Possessions', 'Uncontested_Possessions', 'Contested_Marks',
            'Marks_Inside_50', 'One_Percenters', 'Bounces', 'Goal_Assists'

            ], index=['Team', 'Player', 'First_Name', 'Last_Name', 'DOB'])\
                .reset_index()\
                .reindex(columns=[
                        
            'Player', 'First_Name', 'Last_Name', 'Team', 'DOB', 'Height', 'Weight', 
            'Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals',
            'Behinds', 'Hit_Outs', 'Tackles', 'Rebounds', 'Inside_50s',
            'Clearances', 'Clangers', 'Frees', 'Frees_Against', 'Brownlow_Votes',
            'Contested_Possessions', 'Uncontested_Possessions', 'Contested_Marks',
            'Marks_Inside_50', 'One_Percenters', 'Bounces', 'Goal_Assists'
            
            ]).round(2)

        self._gen_Teams(teams)
        self._gen_Players(teams)
        self._create_stadiums()

        # use the 2019 fixture as a template for future seasons: same match-ups, at the same venue, on the same rounds
        self._fixture_data = Season.afl.loc[Season.afl.Year == 2019].loc[Season.afl.Round != 'EF'].loc[Season.afl.Round != 'PF'].loc[Season.afl.Round != 'SF'].loc[Season.afl.Round != 'QF'].loc[Season.afl.Round != 'GF']
        Season._format_df(self._fixture_data)
        Season._first_last_names(self._fixture_data)

        fixturedf = self._fixture_data.loc[self._fixture_data.Year == 2019].pivot(index=['Round', 'Team', 'Player'], columns='Opposition')\
                    .stack().reset_index()\
                    .set_index(['Round', 'Team', 'Opposition', 'Day', 'Date', 'Start_Time', 'Venue', 'Attendance', 'Rainfall'])

        # build fixture for in class dataset
        unique_games = []
        for val in fixturedf.index.unique():
            unique_games.append(val)
        unique_games = pd.DataFrame(unique_games).drop(columns=[7,8])
        unique_games[4] = unique_games[4].astype(np.datetime64)
        unique_games.rename(columns={0: 'round_num', 1: 'home_team', 2: 'away_team', 3: 'weekday', 4: 'date', 5: 'start_time', 6: 'stadium'}, inplace=True)
        unique_games.set_index('date', drop=True, inplace=True)
        fixture = unique_games.sort_index().drop_duplicates(subset=['round_num', 'weekday', 'stadium', 'start_time'], keep='first').reset_index()
        fixture = fixture.drop(columns=['date','weekday','start_time'])

        # store fixture in a dictionary; key=round_num, value=dataframe
        rounds = list(range(1,24))
        self._matches = {}
        for round_num in rounds:
            self._matches[round_num] = fixture.loc[fixture.round_num == round_num].reset_index(drop=True)

        timeslots = {
        'Thursday' : ['7:25pm'],
        'Friday' : ['7:50pm'],
        'Saturday' : ['1:45pm','4:05pm','7:25pm','7:45pm'],
        'Sunday' : ['1:10pm','3:20pm','5:10pm']
        }

        counter=1
        while counter <= 23:

            df = self._matches[counter]
            while self._tmstmp.strftime('%A') != 'Thursday':
                self._tmstmp += pd.Timedelta(1, 'day')

            if counter in [12,13,14]:
                for day,times in timeslots.items():
                    if day == 'Friday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[0], df.away_team[0], self._tmstmp.strftime('%A'), times)
                        self._tmstmp += pd.Timedelta(1, 'day')
                    elif day == 'Saturday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[1], df.away_team[1], self._tmstmp.strftime('%A'), times[0])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[2], df.away_team[2], self._tmstmp.strftime('%A'), times[1])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[3], df.away_team[3], self._tmstmp.strftime('%A'), times[2])
                        self._tmstmp += pd.Timedelta(1, 'day')
                    elif day == 'Sunday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[4], df.away_team[4], self._tmstmp.strftime('%A'), times[0])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[5], df.away_team[5], self._tmstmp.strftime('%A'), times[2])


                counter += 1
                continue

            else:
                for day,times in timeslots.items():
                    if day == 'Thursday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[0], df.away_team[0], self._tmstmp.strftime('%A'), times)
                        self._tmstmp += pd.Timedelta(1, 'day')
                    elif day == 'Friday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[1], df.away_team[1], self._tmstmp.strftime('%A'), times)
                        self._tmstmp += pd.Timedelta(1, 'day')
                    elif day == 'Saturday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[2], df.away_team[2], self._tmstmp.strftime('%A'), times[0])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[3], df.away_team[3], self._tmstmp.strftime('%A'), times[1])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[4], df.away_team[4], self._tmstmp.strftime('%A'), times[2])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[5], df.away_team[5], self._tmstmp.strftime('%A'), times[3])
                        self._tmstmp += pd.Timedelta(1, 'day')
                    elif day == 'Sunday':
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[6], df.away_team[6], self._tmstmp.strftime('%A'), times[0])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[7], df.away_team[7], self._tmstmp.strftime('%A'), times[1])
                        HomeAwayGame(self._tmstmp, df.round_num[0], df.home_team[8], df.away_team[8], self._tmstmp.strftime('%A'), times[2])

            counter += 1

        Final._set_finals()
        Round._assign_rounds()

    def _create_stadiums(self):
        # scrape current afl stadium data and construct DF:
        stadiums = pd.read_html('https://en.wikipedia.org/wiki/List_of_Australian_Football_League_grounds')[0]\
                    .drop(index=[14,15], columns=['Image', 'Other/sponsored names', 'State/territory', 'First used'])

        # present stadium names in the form to match afl_stats.csv:
        stad_mapper = {
            'Melbourne Cricket Ground' : 'M.C.G.',
            'Docklands Stadium' : 'Docklands',
            'Sydney Cricket Ground' : 'S.C.G.',
            'The Gabba' : 'Gabba',
            'Carrara Stadium' : 'Carrara',
            'Sydney Showground Stadium' : 'Sydney Showground'
        }
        stadiums.Ground = stadiums.Ground.replace(stad_mapper)

        # format values:
        stadiums.Capacity = [re.sub(r'\[.+\]', '', vals) for vals in stadiums.Capacity]
        stadiums['Current tenant(s)'] = [re.sub(r'\[.+\]', '', vals) for vals in stadiums['Current tenant(s)']]
        stadiums['Current tenant(s)'] = [re.sub(r"([a-z])([A-Z])", r"\1, \2", tenant).split(', ') for tenant in stadiums['Current tenant(s)']]
        stadiums.Capacity = stadiums.Capacity.str.replace(',', '').astype(int)
        stadiums.iat[5,3] = ['Brisbane Lions']
        self._gen_Stadiums(stadiums)
        self._create_stadium_weather()

    def _create_stadium_weather(self):
        # isolate the weather for each Stadium location as a DF:
        weather_urls = {
            'Wendouree' : 'https://www.eldersweather.com.au/climate-history/vic/wendouree',
            'Melbourne' : 'https://www.eldersweather.com.au/climate-history/vic/melbourne',
            'Perth' : 'https://www.eldersweather.com.au/climate-history/wa/perth',
            'Adelaide' : 'https://www.eldersweather.com.au/climate-history/sa/adelaide',
            'Sydney' : 'https://www.eldersweather.com.au/climate-history/nsw/sydney',
            'Brisbane' : 'https://www.eldersweather.com.au/climate-history/qld/brisbane',
            'Geelong' : 'https://www.eldersweather.com.au/climate-history/vic/geelong',
            'Gold Coast' : 'https://www.eldersweather.com.au/climate-history/qld/coolangatta',
            'Launceston' : 'https://www.eldersweather.com.au/climate-history/tas/launceston',
            'Hobart' : 'https://www.eldersweather.com.au/climate-history/tas/hobart',
            'Canberra' : 'https://www.eldersweather.com.au/climate-history/act/canberra',
            'Darwin' : 'https://www.eldersweather.com.au/climate-history/nt/darwin',
            'Alice Springs' : 'https://www.eldersweather.com.au/climate-history/nt/alice-springs'
        }

        # format _weather DFs attached to each Stadium object:
        weather_mapper = {
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9,
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
        }       

        # assign weather information to each Stadium based on location
        for city,url in weather_urls.items():
            for ven in self.stadiums:
                if ven.location == city:
                    ven._weather = pd.read_html(url, parse_dates=True, skiprows=1, index_col=0, header=0)[0]\
                                    .rename(weather_mapper, axis=1)\
                                    .reindex(columns=['Ann',1,2,3,4,5,6,7,8,9,10,11,12])

    # return the winner and top 10 of the brownlow medal
    def brownlow_medal(self):
        Player._brownlow_medal()

    def _gen_Players(self, df):   
        # build players using the Player_class 
        for row in df.values:
            Player(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28])
        for player in Player.instances:
            player._add_age(self._tmstmp)
        for team in Team.instances:
            team._season_stats()

    def _gen_Teams(self, df):    
        # build teams using the Team_class
        for team in df.Team.unique():
            Team(team)

    def _gen_Stadiums(self, df):
        # define how to construct a Stadium object
        for stadium in df.values:
            Stadium(stadium[0], stadium[1], stadium[2], stadium[3])

    def _gen_Games(self, df):  
        # read in games from fixture as Game objects  
        for game in df.values:
            HomeAwayGame(game[0], game[1], game[2], game[3], game[4], game[5])
        Final._set_finals()

    def play_homeaway_games(self):
        Game._play_homeaway_games()

    def play_round(self, round_num):
        for rounds in Round.instances:
            if rounds.round_num == round_num:
                Round.play_round(rounds)

    def round_ladder(self, round_num):
        for rnd in self.rounds:
            if rnd.round_num == round_num:
                print(rnd.ladder)

    def play_final_series(self):
        Final._play_final_series()

    def play_season(self):
        message8 = color.YELLOW + f"...Simulating the magnificent Season {self.year}..." + color.END
        print()
        print(color.CYAN + "-------------------------------------------------------------------------------------------------------------------" + color.END)
        print(f'\t\t\t\t\t{message8}')
        print(color.CYAN + "-------------------------------------------------------------------------------------------------------------------" + color.END)
        self.play_homeaway_games()
        self.play_final_series()

# accept command line options for help menu and year of season
argumentList = sys.argv[1:]
options = "hy:"
long_options = ["help", "year"]
 
try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("help: 'python3 -i afl_season.py [year]'")
            print("\nhelp: ensure year is between 2012-2100 and an integer")
            print("** years 2012-2020 utilize real player data")
        elif currentArgument in ("-y", "--year"):
            season = Season(int(currentValue))
            season.play_season()

except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
