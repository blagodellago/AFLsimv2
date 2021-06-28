import pandas as pd
import numpy as np
from datetime import timedelta
from time import sleep
from random import randint, triangular, random, choice, choices, gauss
import heapq

# build a mechanism for searching through class instances
class InstanceList(list):
    def search(self, name):
        matches = []
        for instance in self:
            if name in instance.name:
                matches.append(instance)
        if len(matches) == 1:
            return matches[0]
        else:
            return matches


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Player:
    """Initialize a Player object with 'name' the only required parameter"""

    # class attributes:
    instances = InstanceList()

    # add players to Player.instances:
    @classmethod
    def _add_instance(cls, player):
        if player not in cls.instances:
            cls.instances.append(player)
        else:
            pass

    # when initializing Player objects they hold 12 attributes:
    def __init__(self, name, first_name=None, last_name=None, team=None, dob=None, height=None, weight=None, disposals=None, kicks=None, marks=None, handballs=None, goals=None, behinds=None, hit_outs=None, tackles=None, rebounds=None, inside_50s=None, clearances=None, clangers=None, frees_for=None, frees_against=None, brownlow_votes=None, contested_poss=None, uncontested_poss=None, contested_marks=None, marks_inside_50=None, one_percenters=None, bounces=None, goal_assists=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        for team_instance in Team.instances:
            if team_instance.name == team:
                self.team = team_instance
                team_instance.roster.append(self)
        self.dob = pd.Timestamp(dob)
        self.height = height
        self.weight = weight
        self.disposals = disposals
        self.kicks = kicks
        self.marks = marks
        self.handballs = handballs
        self.goals = goals
        self.behinds = behinds
        self.hit_outs = hit_outs
        self.tackles = tackles
        self.rebounds = rebounds
        self.inside_50s = inside_50s
        self.clearances = clearances
        self.clangers = clangers
        self.frees_for = frees_for
        self.frees_against = frees_against
        self.brownlow_votes = brownlow_votes
        self.contested_poss = contested_poss
        self.uncontested_poss = uncontested_poss
        self.contested_marks = contested_marks
        self.marks_inside_50 = marks_inside_50
        self.one_percenters = one_percenters
        self.bounces = bounces
        self.goal_assists = goal_assists
        self.games_played = 0
        self.games_injured = 0

        self.stamina = 100
        self.injured = False
        self.injury_duration = 0
        self._training_status = False
        self._injury_likelihood = 0

        self.ranking_points = round(
            (self.disposals)+
            (self.kicks*2)+
            (self.marks*3)+
            (self.handballs)+
            (self.goals*10)+
            (self.behinds*3)+
            (self.hit_outs*3)+
            (self.tackles*5)+
            (self.rebounds*3)+
            (self.inside_50s*4)+
            (self.clearances*6)-
            (self.clangers*4)+
            (self.frees_for*4)-
            (self.frees_against*5)+
            (self.contested_poss*4)+
            (self.uncontested_poss)+
            (self.contested_marks*8)+
            (self.marks_inside_50*6)+
            (self.one_percenters*3)+
            (self.bounces*2)+
            (self.goal_assists*8)
        )

        self.team.roster_ranking_points += self.ranking_points

        self.attributes = {
                    'kicks' : self.kicks,
                    'marks' : self.marks,
                    'handballs' : self.handballs,
                    'goals' : self.goals,
                    'behinds' : self.behinds,
                    'hit_outs' : self.hit_outs,
                    'tackles' : self.tackles,
                    'rebounds' : self.rebounds,
                    'inside_50s' : self.inside_50s,
                    'clearances' : self.clearances,
                    'clangers' : self.clangers,
                    'frees_for' : self.frees_for,
                    'frees_against' : self.frees_against,
                    'contested_poss' : self.contested_poss,
                    'uncontested_poss' : self.uncontested_poss,
                    'contested_marks' : self.contested_marks,
                    'marks_inside_50' : self.marks_inside_50,
                    'one_percenters' : self.one_percenters,
                    'bounces' : self.bounces,
                    'goal_assists' : self.goal_assists
        }

        self._jittered_stats = {}
        self.season_stats = {}
        self.season_averages = {}
        for attr,val in self.attributes.items():
            self.season_stats[attr] = 0
            self.season_averages[attr] = 0
            self._jittered_stats[attr] = 0

        Player._add_instance(self)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return self._name

    # defines names as string:
    @name.setter
    def name(self, name):
        if type(name) != str:
            raise TypeError("Names don't sound like that")
        else:
            self._name = name

    @property
    def height(self):
        return self._height

    # defines 'height' as between 160-220cms:
    @height.setter
    def height(self, height):
        if height < 160:
            raise ValueError("People are not that small")
        elif height > 220:
            raise ValueError("People are not that tall")
        else:
            self._height = height

    @property
    def weight(self):
        return self._weight

    # defines 'weight' as between 60-130kgs:
    @weight.setter
    def weight(self, weight):
        if weight < 60:
            raise ValueError("You're too skinny to play footy")
        elif weight > 130:
            raise ValueError("You're too heavy to cover the ground")
        else:
            self._weight = weight

    # randomize player stats using a gaussian distribution
    def _jitter_stats(self, val_modifier=float, variability_modifier=float, score_modifier=1.0):

        if self._training_status == True:
            val_modifier = val_modifier*1.05
            self.stamina -= 2
        else:
            self.stamina += 2

        for attr,val in self.attributes.items():
            if attr == 'goals':
                self._jittered_stats[attr] = round((val + gauss(val*val_modifier*score_modifier, val*variability_modifier)) / 2)
            elif attr == 'behinds':
                self._jittered_stats[attr] = round((val + gauss(val*val_modifier*score_modifier, val*variability_modifier)) / 2)
            else:
                self._jittered_stats[attr] = round((val + gauss(val*val_modifier, val*variability_modifier)) / 2)

        for attr,val in self._jittered_stats.items():
            self.season_stats[attr] += val

        self.season_stats['disposals'] = (self.season_stats['kicks']) + (self.season_stats['handballs'])

        self.games_played += 1

    # return season stat averages for player
    def _season_averages(self):
        if self.games_played >= 1:
            for attr,val in self.season_stats.items():
                self.season_averages[attr] = round(val/self.games_played, 2)

    # add player's age in years based on season being played
    def _add_age(self, timestamp):
        self.age = (timestamp.year - self.dob.year)

    # determine how players lose energy over the course of a season
    def _adjust_stamina(self):
        if self.age < 20:
            self.stamina -= 2
        if self.age < 30:
            self.stamina -= 1
        else:
            self.stamina -= 2.5

    # check for player injuries depending on age and stamina
    def _injury_check(self):
        self._injury_likelihood = int(round((101 - self.stamina) * 0.4))
        if self.age >= 30:
            self._injury_likelihood = int(round(self._injury_likelihood * 1.2))

        # determine whether injury occurs
        _injury_outcome_list = []
        for i in range(100 - self._injury_likelihood):
            _injury_outcome_list.append(False)
        for i in range(self._injury_likelihood):
            _injury_outcome_list.append(True)

        self.injured = choice(_injury_outcome_list)

        # determine extent of injury
        _injured_games_dict = {

                1 : 40,
                2 : 20,
                3 : 10,
                4 : 8,
                5 : 6,
                6 : 4,
                7 : 4,
                8 : 3,
                9 : 3,
                10 : 3,
                11 : 3,
                12 : 3,
                13 : 3,
                14 : 3,
                15 : 3,
                16 : 3

        }

        attr_list = list(_injured_games_dict.keys())
        val_list = list(_injured_games_dict.values())

        if self.injured == True:
            if self.age <= 23:
                val_list[0] += 40
            elif self.age >= 30:
                val_list[0] -= 20

            self.injury_duration = choices(population=attr_list,weights=val_list,k=1)[0]

    # define how players recover from injury
    def _manage_injury(self):
        self.injury_duration -= 1
        self.games_injured += 1
        if self.stamina <= 94:
            self.stamina += 6
        if self.injury_duration == 0:
            self.injured = False

    # return stats as a DataFrame
    def stats(self):
        self.season_stats = pd.DataFrame({"--------------" : self.season_stats.keys(), "season_totals" : self.season_stats.values()}).set_index("--------------")
        print(self.season_stats)

    # return average stats as a DataFrame
    def averages(self):
        self.season_averages = pd.DataFrame({"--------------" : self.season_averages.keys(), "season_totals" : self.season_averages.values()}).set_index("--------------")
        print(self.season_averages)

class Team:
    """Team objects are initialized with only the team name"""

    instances = InstanceList()
    ladder = None

    @classmethod
    def _add_instance(cls, team):
        # if team not in Team.instances, add team to Team.instances
        if team not in Team.instances:
            cls.instances.append(team)

    @classmethod
    def _refresh_ladder(cls):
        # declares how the ladder is updated. Called after each game is played
        Team.ladder = pd.DataFrame({
                          'Team' : [team.name for team in Team.instances],
                          'Games_Played' : [team.games_played for team in Team.instances],
                          'Wins' : [team.wins for team in Team.instances],
                          'Losses' : [team.losses for team in Team.instances],
                          'Draws' : [team.draws for team in Team.instances],
                          'PPoints' : [team.premiership_points for team in Team.instances],
                          'Points_For' : [team.points_for for team in Team.instances],
                          'Points_Against' : [team.points_against for team in Team.instances],
                          'Percentage' : [team.percentage for team in Team.instances]
                      }).sort_values(by=['PPoints', 'Percentage'], ascending=False).set_index(pd.RangeIndex(1,19), drop=True)

    def __init__(self, name):
        # defines the various attributes of Team objects
        self.name = name
        self.roster = []
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.premiership_points = 0
        self.games_played = 0
        self.finals_played = 0
        self.points_for = 0
        self.points_against = 0
        self.percentage = 0
        self.home_stadium = InstanceList()
        self.roster_ranking_points = 0
        self.best_22_ranking_points = 0
        self.best_22 = {}
        self.season_stats = {}
        self.season_averages = {}

        Team._add_instance(self)

    def __repr__(self):
        return self.name

    # assign team gameday ranking points based on their 22 highest ranked players
    def _generate_best22(self):
        gameday_player_ranking_points = {}
        for player in self.roster:
            if player.injured == False:
                player._injury_check()
            else:
                player._manage_injury()

        for player in self.roster:
            if player.injured == False:
                gameday_player_ranking_points[player] = round(gauss(player.ranking_points, player.ranking_points*.2),2)

        gameday_points_list = sorted(gameday_player_ranking_points.items(), key=lambda x:x[1], reverse=True)
        gameday_points_dict = dict(gameday_points_list)

        # store teams best22 player and their ranking points in dict
        self.best_22 = dict(heapq.nlargest(22, gameday_points_dict.items(), key=lambda i: i[1]))
        self._train_players()
        return self.best_22

    def _adjust_percentage(self):
        # calculate team percentage
        self.percentage = round(self.points_for / self.points_against * 100, 2)

    def _win(self):
        self.wins += 1
        self.premiership_points += 4

    def _loss(self):
        self.losses += 1

    def _draw(self):
        self.draws += 1
        self.premiership_points += 2

    # define the impacts of training before playing a game that week
    def _train_players(self):
        for player in self.best_22:
            if player.stamina >= 70:
                player._training_status = True
            else:
                player._training_status = False

    def _season_stats(self):
        for attr in self.roster[0].season_stats.keys():
            self.season_stats[attr] = 0
            self.season_averages[attr] = 0 

    # return season stat averages for team
    def _season_averages(self):
        for attr,val in self.season_stats.items():
            self.season_averages[attr] = round(val / (self.games_played + self.finals_played), 2)

    # return stats as a DataFrame
    def stats(self):
        self.season_stats = pd.DataFrame({"--------------" : self.season_stats.keys(), "season_totals" : self.season_stats.values()}).set_index("--------------")
        print(self.season_stats)

    # return average stats as a DataFrame
    def averages(self):
        self.season_averages = pd.DataFrame({"--------------" : self.season_averages.keys(), "season_totals" : self.season_averages.values()}).set_index("--------------")
        print(self.season_averages)

class Stadium:
    """Stadium object initialized with venue, location, capacity, and tenants"""

    instances = InstanceList()

    @classmethod
    def _add_instance(cls, stadium):
        # add Stadium object to Stadium.instances
        if stadium not in Stadium.instances:
            Stadium.instances.append(stadium) 


    def __init__(self, venue, location, capacity, tenants):
        # attributes of a Stadium object
        self.name = venue
        self.location = location
        self.capacity = capacity
        self._weather = pd.DataFrame()
        self._assign_home_stadium(tenants)
        Stadium._add_instance(self)

    def __repr__(self):
        return self.name

    def _assign_home_stadium(self, tenants):
        # associate Stadium objects with Team objects as home_stadium
        for tenant in tenants:
            for team in Team.instances:
                if tenant == team.name:
                    team.home_stadium.append(self)


class Game:
    """define the parent Game class that HomeAwayGames and FinalGames will inherit from"""

    instances = InstanceList()

    attribute_constraints = {
        'kicks' : [0,25],
        'marks' : [0,20],
        'handballs' : [0,30],
        'goals' : [0,10],
        'behinds' : [0,8],
        'hit_outs' : [0,50],
        'tackles' : [0,17],
        'rebounds' : [0,14],
        'inside_50s' : [0,12],
        'clearances' : [0,17],
        'clangers' : [0,10],
        'frees_for' : [0,6],
        'frees_against' : [0,6],
        'contested_poss' : [0,30],
        'uncontested_poss' : [0,35],
        'contested_marks' : [0,10],
        'marks_inside_50' : [0,10],
        'one_percenters' : [0,20],
        'bounces' : [0,10],
        'goal_assists' : [0,6]
    }

    @classmethod
    def _play_homeaway_games(cls):
        for rnd in Round.instances:
            rnd.play_round()
        for player in Player.instances:
            player._season_averages()
        Final._set_finalists()
        Team._refresh_ladder()
        print('\n\n\n\n')
        print(color.BLUE + "###################################################################################################################" + color.END)
        print("\n",Team.ladder)

    def __init__(self, date, weekday, start_time):
        self.date = pd.to_datetime(date).date()
        self.weekday = weekday
        self.start_time = start_time

        self.home_team = None
        self.away_team = None
        self.name = f'{self.home_team} vs {self.away_team}'
        self.stadium = None
        self.attendance = None
        self.home_22 = None
        self.away_22 = None
        self.homeranking = 0
        self.awayranking = 0

        # hold the final scores of the game for reference
        self.home_score = 0
        self.away_score = 0
        self.final_score = ''

        self.home_stats = {}
        self.away_stats = {}
        self.game_stats = {}

        self.home_player_stats = None
        self.away_player_stats = None

        # contain weather information for game based on Stadium and time of year
        self.temperature = None
        self._rain_likelihood = None
        self.rainfall = 0

    def __repr__(self):
        return f'{self.home_team} vs {self.away_team}'

    def _get_ranking_points(self):
        for val in self.home_22.values():
            self.homeranking += val
        for val in self.away_22.values():
            self.awayranking += val

        self.home_team.best_22_ranking_points = self.homeranking
        self.away_team.best_22_ranking_points = self.awayranking

    def _gen_gameday_stats(self):
        for attr in Game.attribute_constraints.keys():
            self.home_stats[attr] = 0
            self.away_stats[attr] = 0
            self.game_stats[attr] = 0

        for player in self.home_22.keys():
            if self.rainfall <= 2:
                player._jitter_stats(1.05, 0.25)
                for attr,val in player._jittered_stats.items():
                    self.home_stats[attr] += val
            elif self.rainfall >= 10:
                player._jitter_stats(1.05, 0.35, 0.6)
                for attr,val in player._jittered_stats.items():
                    self.home_stats[attr] += val
            else:
                player._jitter_stats(1.05, 0.3, 0.8)
                for attr,val in player._jittered_stats.items():
                    self.home_stats[attr] += val

        for player in self.away_22.keys():
            if self.rainfall <= 2:
                player._jitter_stats(0.95, 0.25)
                for attr,val in player._jittered_stats.items():
                    self.away_stats[attr] += val
            elif self.rainfall >= 10:
                player._jitter_stats(0.95, 0.35, 0.6)
                for attr,val in player._jittered_stats.items():
                    self.away_stats[attr] += val
            else:
                player._jitter_stats(0.95, 0.3, 0.8)
                for attr,val in player._jittered_stats.items():
                    self.away_stats[attr] += val

        for attr,val in self.home_stats.items():
            self.home_stats[attr] = round(val)

        for attr,val in self.away_stats.items():
            self.away_stats[attr] = round(val)

        self.home_score = (self.home_stats['goals']*6) + self.home_stats['behinds']
        self.away_score = (self.away_stats['goals']*6) + self.away_stats['behinds']

    # use player attributes to generate gameday statistics
    def _gameday_player_points(self, team):
        player_dict = {}
        for player in team.best_22.keys():
            player_dict[player] = player._jittered_stats

        player_df = pd.DataFrame((player_dict[i] for i in player_dict), index=player_dict.keys())

        return player_df

    def _get_stadium(self):
        pass

    def _assign_scores(self):
        # generate ranking points for each teams' best 22
        self.home_22 = self.home_team._generate_best22()
        self.away_22 = self.away_team._generate_best22()
        self._get_ranking_points()
        self._gen_gameday_stats()
        
        self.away_player_stats = self._gameday_player_points(self.away_team)
        self.home_player_stats = self._gameday_player_points(self.home_team)
        self._gen_stats()

    def _gen_weather(self):
        # generate game weather based on the month the game is played and the location it is played in
        for stad in Stadium.instances:
            if self.stadium == stad:
                if self.date.month in stad._weather.columns:
                    self.temperature = int(round(triangular(low=stad._weather.iloc[1,self.date.month], high=stad._weather.iloc[0,self.date.month], mode=stad._weather.iloc[0,self.date.month]*.9)))
                    self._rain_likelihood = stad._weather.iloc[3,self.date.month]/30
                    if self._rain_likelihood > random():
                        self.rainfall = (triangular(low=stad._weather.iloc[2,self.date.month]*.3, high=stad._weather.iloc[2,self.date.month]*10, mode=3)/30).round(1)

    def _gen_attendance(self):
        for stad in Stadium.instances:
            if self.stadium == stad:
                if stad.name != 'M.C.G.':
                    self.attendance = round(triangular(stad.capacity*self._mcg_lower, stad.capacity, stad.capacity*self._mcg_weight))
                else:
                    self.attendance = round(triangular(stad.capacity*self._stad_lower, stad.capacity, stad.capacity*self._stad_weight))

    def _gen_stats(self):
        self.home_stats = self.home_player_stats.sum()
        self.away_stats = self.away_player_stats.sum()

        for attr,val in self.home_stats.items():
            self.home_team.season_stats[attr] += val
        for attr,val in self.away_stats.items():
            self.away_team.season_stats[attr] += val

        df_home_stats = pd.DataFrame(self.home_stats).rename(columns = {0:self.home_team})
        df_away_stats = pd.DataFrame(self.away_stats).rename(columns = {0:self.away_team})

        self.game_stats = pd.merge(df_home_stats, df_away_stats, left_index=True, right_index=True)

    def _setup_game(self):
        # utlize assign_scores() and then update Team attributes depending on outcome
        self._gen_weather()
        self._assign_scores()
        self._gen_attendance()

class HomeAwayGame(Game):

    instances = InstanceList()
    fixture = InstanceList()
    games_scheduled = InstanceList()
    games_played = InstanceList()
    _mcg_lower = 0.4
    _mcg_weight = 0.5
    _stad_lower = 0.3
    _stad_weight = 0.5

    @classmethod
    def _add_instance(cls, game):
        # when initialized, add Game to Game.instances & Game.fixture
        if game not in HomeAwayGame.instances:
            HomeAwayGame.instances.append(game)
        if game not in HomeAwayGame.fixture:
            HomeAwayGame.fixture.append(f'{game.round_num}: {game}')
        if game not in HomeAwayGame.games_scheduled:
            HomeAwayGame.games_scheduled.append(game)

    def __init__(self, date, round_num, home_team, away_team, weekday, start_time):
        super().__init__(date, weekday, start_time)
        self.round_num = round_num
        self.home_team = home_team
        self.away_team = away_team

        #convert home_team and away_team into their Team object equivalents
        for team in Team.instances:
            if team.name == self.home_team:
                self.home_team = team
        for team in Team.instances:
            if team.name == self.away_team:
                self.away_team = team
        self._get_stadium()

        # add newly created games to Game.instances
        HomeAwayGame._add_instance(self)

    def _get_stadium(self):
        # choose a stadium from home_team home_stadiums
        self.stadium = choice(self.home_team.home_stadium)

    # how scores are assigned for each team:
    def _interpret_scores(self):                     
        # add to each individual team's attributes after playing game and adjust percentage:
        self.home_team.games_played += 1
        self.away_team.games_played += 1
        self.home_team.points_for += self.home_score
        self.away_team.points_for += self.away_score
        self.home_team.points_against += self.away_score
        self.away_team.points_against += self.home_score

    def _play_game(self):
        # utlize assign_scores() and then update Team attributes depending on outcome:
        if self.final_score == '':
            self._setup_game()
            self._interpret_scores()
            if self.home_score > self.away_score:
                Team._win(self.home_team)
                Team._loss(self.away_team)
                self.final_score += f'{self.home_team}: {self.home_score} beat {self.away_team}: {self.away_score}'
            elif self.home_score < self.away_score:
                Team._win(self.away_team)
                Team._loss(self.home_team)
                self.final_score += f'{self.home_team}: {self.home_score} lost to {self.away_team}: {self.away_score}'
            else:
                Team._draw(self.home_team)
                Team._draw(self.away_team)
                self.final_score += f'{self.home_team}: {self.home_score} drew with {self.away_team}: {self.away_score}'

            # update ladder with the outcome of the match including final scores:
            HomeAwayGame.games_scheduled.remove(self)
            HomeAwayGame.games_played.append(self)
            Team._adjust_percentage(self.home_team)
            Team._adjust_percentage(self.away_team)
            Team._refresh_ladder()


class Final(Game):
    """build Final objects inheriting from Game class"""
    instances = InstanceList()
    _mcg_lower = 0.7
    _mcg_weight = 0.9
    _stad_lower = 0.8
    _stad_weight = 0.9

    @classmethod
    def _add_instance(cls, final):
        if final not in Final.instances:
            Final.instances.append(final)

    @classmethod
    def _set_finals(cls):
        last_HA_game = HomeAwayGame.instances[-1].date
        finals_template = {
            'QF1' : [last_HA_game + timedelta(days=10), '7:10pm', 1], 
            'QF2' : [last_HA_game + timedelta(days=13), '3:10pm', 1], 
            'EF1' : [last_HA_game + timedelta(days=11), '7:10pm', 1], 
            'EF2' : [last_HA_game + timedelta(days=12), '7:25pm', 1], 
            'SF1' : [last_HA_game + timedelta(days=18), '7:10pm', 2], 
            'SF2' : [last_HA_game + timedelta(days=19), '7:25pm', 2], 
            'PF1' : [last_HA_game + timedelta(days=25), '7:10pm', 3], 
            'PF2' : [last_HA_game + timedelta(days=26), '7:25pm', 3], 
            'GF' : [last_HA_game + timedelta(days=33), '3:10pm', 4]
            }
        for fnl,values in finals_template.items():
            Final(fnl, values[0].strftime("%A"), values[0], values[1], values[2])

    @classmethod
    def _set_finalists(cls):
        # capture the top 8 sides from the ladder and assign them to Final objects
        finalists = Team.ladder.nlargest(8, columns=['PPoints', 'Percentage'])
        finals_mapper = {
            'QF1' : [finalists.Team[1], finalists.Team[4]],
            'QF2' : [finalists.Team[2], finalists.Team[3]],
            'EF1' : [finalists.Team[5], finalists.Team[8]],
            'EF2' : [finalists.Team[6], finalists.Team[7]]
        }
        for final in Final.instances:
            for game,teams in finals_mapper.items():
                if game == final.final_type:
                    final._set_teams(teams[0], teams[1])

    @classmethod
    def _play_final_round(cls, week_of_finals):
        # how a Finals Round is played in full
        for final in Final.instances:
            if final.week_of_finals == week_of_finals:
                final._play_final()


    @classmethod
    def _play_final_series(cls):
        Final._play_final_round(1)
        print()
        print()
        print(color.DARKCYAN + "###################################################################################################################" + color.END)
        [print(f'\t\t\t\t\t{final.final_type}: {final.final_score}') for final in Final.instances if final.week_of_finals == 1]
        Final._play_final_round(2)
        [print(f'\t\t\t\t\t{final.final_type}: {final.final_score}') for final in Final.instances if final.week_of_finals == 2]
        Final._play_final_round(3)
        [print(f'\t\t\t\t\t{final.final_type}: {final.final_score}') for final in Final.instances if final.week_of_finals == 3]
        print(color.DARKCYAN + "###################################################################################################################" + color.END)
        Final._play_final_round(4)
        [print(f'\n\n\n\033[1m\t\t\t\t\t{str(final.winner).upper()}\033[0m wins the premiership!\n\t\t\t\t\t({final.final_score})') for final in Final.instances if final.week_of_finals == 4]
        print()
        print()
        [print(f'{final.game_stats}') for final in Final.instances if final.week_of_finals == 4]
        print()
        print()
        for team in Team.instances:
            team._season_averages()

    def __init__(self, final_type, weekday, date, start_time, week_of_finals):
        super().__init__(date, weekday, start_time)
        self.final_type = final_type
        self.week_of_finals = week_of_finals
        self.winner = None
        self.loser = None
        Final._add_instance(self)

    def _get_stadium(self):
        # choose the first stadium, the primary, from home_team home_stadiums
        if self.week_of_finals == 4:
            self.stadium = Stadium.instances[0]
        else:
            self.stadium = self.home_team.home_stadium[0]

    # assigns teams and stadium to Final objects:
    def _set_teams(self, home_team, away_team):
        for team in Team.instances:
            if team.name == home_team:
                self.home_team = team
            if team.name == away_team:
                self.away_team = team
        self._get_stadium()

    # maps out the progression through the Finals:
    def _win(self, team):
        self.winner = team
        if self.final_type == 'QF1':
            Final.instances[6].home_team = self.winner
        elif self.final_type == 'EF1':
            Final.instances[4].away_team = self.winner
        elif self.final_type == 'EF2':
            Final.instances[5].away_team = self.winner
        elif self.final_type == 'QF2':
            Final.instances[7].home_team = self.winner
        elif self.final_type == 'SF1':
            Final.instances[7].away_team = self.winner
        elif self.final_type == 'SF2':
            Final.instances[6].away_team = self.winner
        elif self.final_type == 'PF1':
            Final.instances[8].home_team = self.winner
        elif self.final_type == 'PF2':
            Final.instances[8].away_team = self.winner
        self._get_stadium()
        self._gen_weather()
        self._gen_attendance()

    def _loss(self, team):
        self.loser = team
        if self.final_type == 'QF1':
            Final.instances[4].home_team = self.loser
        elif self.final_type == 'QF2':
            Final.instances[5].home_team = self.loser
        self._get_stadium()
        self._gen_weather()
        self._gen_attendance()

    # defines how a win or loss is determined and prevents outcomes from being draws:
    def _interpret_scores(self):
        if self.home_score > self.away_score:
            self._win(self.home_team)
            self._loss(self.away_team)
            self.final_score += f'{str(self.home_team).upper()}: {self.home_score} beat {self.away_team}: {self.away_score}'
        elif self.home_score < self.away_score:
            self._win(self.away_team)
            self._loss(self.home_team)
            self.final_score += f'{self.home_team}: {self.home_score} lost to {str(self.away_team).upper()}: {self.away_score}'
        else:
            self.home_score += randint(0,15)
            self.away_score += randint(0,14)
            self._interpret_scores()
        self.home_team.finals_played += 1
        self.away_team.finals_played += 1

    # defines the methods called when a Final is played:
    def _play_final(self):
        self._assign_scores()
        # self._setup_game()
        self._interpret_scores()

class Round:

    instances = InstanceList()

    @classmethod
    def _add_instance(cls, round):
        # add Stadium object to Stadium.instances
        if round not in Round.instances:
            Round.instances.append(round) 

    @classmethod        
    def _assign_rounds(cls):
        setrounds = set()
        for games in HomeAwayGame.instances:
            setrounds.add(games.round_num)
        for round_num in setrounds:
            Round(round_num)

    def __init__(self, round_num):
        self.round_num = round_num

        self.games = []
        for game in HomeAwayGame.instances:
            if game.round_num == self.round_num:
                self.games.append(game)

        self.ladder = None        
        Round._add_instance(self)

    def __repr__(self):
        return f'Round {self.round_num}'

    def play_round(self):
        for game in self.games:
            game._play_game()
        self.ladder = Team.ladder
