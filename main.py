import pandas as pd
import numpy as np
from datetime import timedelta
from time import sleep
from random import randint, triangular, random, choice
import heapq

# build a mechanism for searching through class instances
class InstanceList(list):
    def search(self, name):
        matches = []
        for instance in self:
            if name in instance.name:
                matches.append(instance)
        return matches

class Player:
    """Initialize a Player object with 'name' the only required parameter"""

    # assign a unique ID to each Player instance
    player_id = 1

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
    def __init__(self, name, first_name=None, last_name=None, team=None, height=None, weight=None, disposals=None, kicks=None, marks=None, handballs=None, goals=None, behinds=None, hit_outs=None, tackles=None, rebounds=None, inside_50s=None, clearances=None, clangers=None, frees_for=None, frees_against=None, brownlow_votes=None, contested_poss=None, uncontested_poss=None, contested_marks=None, marks_inside_50=None, one_percenters=None, bounces=None, goal_assists=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        for team_instance in Team.instances:
            if team_instance.name == team:
                self.team = team_instance
                team_instance.roster.append(self)
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
            (self.brownlow_votes*20)+
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
                    'brownlow_votes' : self.brownlow_votes,
                    'contested_poss' : self.contested_poss,
                    'uncontested_poss' : self.uncontested_poss,
                    'contested_marks' : self.contested_marks,
                    'marks_inside_50' : self.marks_inside_50,
                    'one_percenters' : self.one_percenters,
                    'bounces' : self.bounces,
                    'goal_assists' : self.goal_assists
        }

        self.gameday_stats = {}
        self.id = Player.player_id
        Player.player_id += 1
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

class Team:
    """Team objects are initialized with only the team name"""

    # assign a unique ID to each Team instance
    team_id = 1

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
        self.points_for = 0
        self.points_against = 0
        self.percentage = 0
        self.home_stadium = InstanceList()
        self.roster_ranking_points = 0
        self.ranking_points = 0
        self.gameday_values = {}
        self.best_22 = {}

        self.attribute_constraints = {
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
            'brownlow_votes' : [0,3],
            'contested_poss' : [0,30],
            'uncontested_poss' : [0,35],
            'contested_marks' : [0,10],
            'marks_inside_50' : [0,10],
            'one_percenters' : [0,20],
            'bounces' : [0,10],
            'goal_assists' : [0,6]
        }

        self.id = Team.team_id
        Team.team_id += 1
        Team._add_instance(self)

    def __repr__(self):
        return self.name

    # assign team gameday ranking points based on their 22 highest ranked players
    def _gameday_ranking_points(self):
        gameday_player_ranking_points = {}
        for player in self.roster:
            gameday_player_ranking_points[player] = player.ranking_points

        gameday_points_list = sorted(gameday_player_ranking_points.items(), key=lambda x:x[1], reverse=True)
        gameday_points_dict = dict(gameday_points_list)

        # store teams best22 player and their ranking points in dict
        self.best_22 = dict(heapq.nlargest(22, gameday_points_dict.items(), key=lambda i: i[1]))

        gameday_ranking_points = 0
        for val in self.best_22.values():
            gameday_ranking_points += val
        self.ranking_points = gameday_ranking_points
        self._gameday_player_points()
        self._gameday_team_points()

    # use player attributes to generate gameday statistics
    def _gameday_player_points(self):
        player_dict = {}
        for player in self.best_22.keys():
            player_dict[player] = player.attributes

        player_stats = {}
        for player,attrs in player_dict.items():
            for attr,val in attrs.items():
                for attribute,constraints in self.attribute_constraints.items():
                    if attribute == attr:
                        player.gameday_stats[attr] = round(triangular(low=constraints[0], high=constraints[1], mode=val))

            player.gameday_stats['disposals'] = player.gameday_stats['kicks'] + player.gameday_stats['handballs']

    def _gameday_team_points(self):
        for attr in self.attribute_constraints.keys():
            self.gameday_values[attr] = 0

        for player in self.best_22.keys():
            for attr,val in player.attributes.items():
                self.gameday_values[attr] += val

        for attr,val in self.gameday_values.items():
            self.gameday_values[attr] = round(val)            

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

class Stadium:
    """Stadium object initialized with venue, location, capacity, and tenants"""

    # assign a unique ID to each Stadium instance
    stadium_id = 0

    instances = InstanceList()

    @classmethod
    def _add_instance(cls, stadium):
        # add Stadium object to Stadium.instances
        if stadium not in Stadium.instances:
            Stadium.instances.append(stadium) 


    def __init__(self, venue, location, capacity, tenants):
        # attributes of a Stadium object
        self.venue = venue
        self.location = location
        self.capacity = capacity
        self._weather = pd.DataFrame()
        self.id = Stadium.stadium_id
        Stadium.stadium_id += 1
        self._assign_home_stadium(tenants)
        Stadium._add_instance(self)

    def __repr__(self):
        return self.venue

    def _assign_home_stadium(self, tenants):
        # associate Stadium objects with Team objects as home_stadium
        for tenant in tenants:
            for team in Team.instances:
                if tenant == team.name:
                    team.home_stadium.append(self)


class Game:
    """define the parent Game class that HomeAwayGames and FinalGames will inherit from"""
    
    # assign a unique ID to each Game instance
    game_id = 0

    instances = InstanceList()

    @classmethod
    def _play_homeaway_games(cls):
        for rnd in Round.instances:
            rnd.play_round()
        Final._set_finalists()
        Team._refresh_ladder()
        print("\n",Team.ladder,"\n")

    @classmethod
    def _play_season(cls):
        Game._play_homeaway_games()
        Final._play_final_series()

    def __init__(self, date, weekday, start_time):
        self.date = pd.to_datetime(date).date()
        self.weekday = weekday
        self.start_time = start_time
        self.id = Game.game_id
        Game.game_id += 1

        self.home_team = None
        self.away_team = None
        self.name = f'{self.home_team} vs {self.away_team}'
        self.stadium = None
        self.attendance = None

        # hold the final scores of the game for reference
        self.home_score = 0
        self.away_score = 0
        self.final_score = ''
        self.home_team_stats = {
            'kicks' : 0,
            'marks' : 0,
            'handballs' : 0,
            'goals' : 0,
            'behinds' : 0,
            'hit_outs' : 0,
            'tackles' : 0,
            'rebounds' : 0,
            'inside_50s' : 0,
            'clearances' : 0,
            'clangers' : 0,
            'frees_for' : 0,
            'frees_against' : 0,
            'brownlow_votes' : 0,
            'contested_poss' : 0,
            'uncontested_poss' : 0,
            'contested_marks' : 0,
            'marks_inside_50' : 0,
            'one_percenters' : 0,
            'bounces' : 0,
            'goal_assists' : 0,
            'disposals' : 0
        }

        self.away_team_stats = {
            'kicks' : 0,
            'marks' : 0,
            'handballs' : 0,
            'goals' : 0,
            'behinds' : 0,
            'hit_outs' : 0,
            'tackles' : 0,
            'rebounds' : 0,
            'inside_50s' : 0,
            'clearances' : 0,
            'clangers' : 0,
            'frees_for' : 0,
            'frees_against' : 0,
            'brownlow_votes' : 0,
            'contested_poss' : 0,
            'uncontested_poss' : 0,
            'contested_marks' : 0,
            'marks_inside_50' : 0,
            'one_percenters' : 0,
            'bounces' : 0,
            'goal_assists' : 0,
            'disposals' : 0
        }

        # contain weather information for game based on Stadium and time of year
        self.temperature = None
        self._rain_likelihood = None
        self.rainfall = 0

    def __repr__(self):
        return f'{self.home_team} vs {self.away_team}'

    def _get_stadium(self):
        pass

    def _assign_scores(self):
        # generate ranking points for each teams' best 22
        self.home_team._gameday_ranking_points()
        self.away_team._gameday_ranking_points()
        self._gen_stats()

        # assign random integers weighted in the home team's favor
        if self.rainfall == 0:
            self.home_score += round(randint(40,120)*(self.home_team.ranking_points/self.away_team.ranking_points)*1.1)
            self.away_score += round(randint(40,120)*(self.away_team.ranking_points/self.home_team.ranking_points))
        elif self.rainfall < 3:
            self.home_score += round(randint(35,110)*(self.home_team.ranking_points/self.away_team.ranking_points)*1.1)
            self.away_score += round(randint(35,110)*(self.away_team.ranking_points/self.home_team.ranking_points))
        elif self.rainfall < 10:
            self.home_score += round(randint(30,80)*(self.home_team.ranking_points/self.away_team.ranking_points)*1.1)
            self.away_score += round(randint(30,80)*(self.away_team.ranking_points/self.home_team.ranking_points))     
        else:
            self.home_score += round(randint(25,60)*(self.home_team.ranking_points/self.away_team.ranking_points)*1.1)
            self.away_score += round(randint(25,60)*(self.away_team.ranking_points/self.home_team.ranking_points))  

    def _setup_game(self):
        # utlize assign_scores() and then update Team attributes depending on outcome
        self._gen_weather()
        self._assign_scores()
        self._gen_attendance()

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
                if stad.venue != 'M.C.G.':
                    self.attendance = round(triangular(stad.capacity*self._mcg_lower, stad.capacity, stad.capacity*self._mcg_weight))
                else:
                    self.attendance = round(triangular(stad.capacity*self._stad_lower, stad.capacity, stad.capacity*self._stad_weight))

    def _gen_stats(self):
        home_team_stats = {}
        for player in self.home_team.best_22.keys():
            for attr,stat in player.gameday_stats.items():
                self.home_team_stats[attr] += stat

        away_team_stats = {}
        for player in self.away_team.best_22.keys():
            for attr,stat in player.gameday_stats.items():
                self.away_team_stats[attr] += stat

        self.home_team_stats = pd.DataFrame(self.home_team_stats, index=[0]).stack().droplevel(0).to_string().upper()
        self.away_team_stats = pd.DataFrame(self.away_team_stats, index=[0]).stack().droplevel(0).to_string().upper()

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
        # how the entire Final series is played
        Final._play_final_round(1)
        print()
        print()
        print("---------------------------------------------------------------------------------------------------------------")
        [print(f'                                       {final.final_type}: {final.final_score}') for final in Final.instances if final.week_of_finals == 1]
        Final._play_final_round(2)
        [print(f'                                       {final.final_type}: {final.final_score}') for final in Final.instances if final.week_of_finals == 2]
        Final._play_final_round(3)
        [print(f'                                       {final.final_type}: {final.final_score}') for final in Final.instances if final.week_of_finals == 3]
        print("---------------------------------------------------------------------------------------------------------------")
        Final._play_final_round(4)
        [print(f'\n\n\n\033[1m                                         {str(final.winner).upper()}\033[0m wins the premiership!\n                                         ({final.final_score})') for final in Final.instances if final.week_of_finals == 4]
        print()
        print()

    def __init__(self, final_type, weekday, date, start_time, week_of_finals):
        super().__init__(date, weekday, start_time)
        self.final_type = final_type
        self.week_of_finals = week_of_finals
        self.winner = None
        self.loser = None
        Final._add_instance(self)

    def _get_stadium(self):
        # choose the first stadium, the primary, from home_team home_stadiums
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
            self.away_score += randint(0,15)
            self._interpret_scores()

    # defines the methods called when a Final is played:
    def _play_final(self):
        self._assign_scores()
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
