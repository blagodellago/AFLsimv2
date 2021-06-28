Leveraging player stats to build a full AFL season simulation

python3 -i afl_season.py [year]


The following instances are stored as season attributes:

.players:
	.name
	.first_name
	.last_name
	.dob
	.height
	.weight

	.attributes
	.season_stats
	.season_averages
	.disposals
	.kicks
	.marks
	.handballs
	.goals
	.behinds
	.hit_outs
	.tackles
	.rebounds
	.inside_50s
	.clearances
	.clangers
	.frees_for
	.frees_against
	.brownlow_votes
	.contested_poss
	.uncontested_poss
	.contested_marks
	.marks_inside_50
	.one_percenters
	.bounces
	.goal_assists

	.games_played
	.games_injured
	.stamina
	.injured
	.injury_duration

.teams:
	.name
	.roster
	.wins
	.losses
	.draws
	.premiership_points
	.games_played
	.finals_played
	.points_for
	.points_against
	.percentage
	.home_stadium
	.roster_ranking_points
	.best_22_ranking_points
	.season_stats
	.season_averages

.hagames & .finals:
	.name
	.date
	.weekday
	.start_time
	.home_team
	.away_team
	.stadium
	.attendance
	.home_22
	.away_22
	.homeranking
	.awayranking
	.home_score
	.away_score
	.final_score
	.home_stats
	.away_stats
	.game_stats
	.home_player_stats
	.away_player_stats
	.temperature
	.rainfall

.hagames:
	.round_num

.finals:
	.final_type
	.week_of_finals
	.winner
	.loser

.stadiums:
	.name
	.location
	.capacity

.rounds:
	.round_num
	.games