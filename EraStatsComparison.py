# NBA Statistics Dataset Project: Who Had the Harder Road to Success, LeBron or Jordan?

#####   Functions   #####

def two_deci_round(x):

    # Rounds numbers to two decimal places if possible
    # Used to make dataframe data more readable for visuals

    if isinstance(x, float):
        return round(x, 2)
    else:
        return x
    
##### End of Functions #####

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# The basketball GOAT debate takes many perspectives. You may hear people say Kobe
# Bryant, Wilt Chamberlain, Bill Russell, or Kareem Abdul-Jabbar is their GOAT. Some
# people highly value championships, skill, awards, impact on the era, or talent. Yet,
# the clear-cut favorite for most people is either LeBron James or Michael Jordan.
# I do not plan to settle this debate here (though I do favor LeGreatness!), but I 
# will try to show who played in the more difficult era: LeBron's Era or
# Jordan's Era (will not consider Wizard's playing time since those teams
# were not expected to grow nor compete for a title). I will analyze the years
# starting in which either player began competiting in the playoffs for their 
# respective careers

# Put CSV file of basic stats per game into Panda Data Frame

dfP = pd.read_csv('Player Per Game.csv') # may be referred as main data frame in comments

# Put CSV file of advanced stats (i.e. True Shooting Percentage and Player
# Efficiency Rating) into Panda Data Frame

dfA = pd.read_csv('Advanced.csv')

#####   Player Stats Perspective: Which era had more competition?   #####
# - let's say a good player is someone who does well in their role, such as:
#    ~ Playoff Player  (To compare all plausible competition)
#    ~ Availability    (games played)
#    ~ Scoring         (points per game)
#    ~ Passings        (assist per game)
#    ~ Rebounding      (rebounds per game)
#    ~ Defense         (steals or blocks per game)

# These are the standards/cutoffs we will use to identify players who are at
# least nice role-players, feel free to change them!

type = "Good Role-"
games_played_standard = 55
scoring_floor = 10
scoring_standard = 17
passing_standard = 6.5
rebounding_standard = 7.5
stealing_standard = 0.5
blocking_standard = 0.5
field_percentage_standard = .550
three_percentage_standard = .350

## Optional standards for superstars! Uncomment these and comment previous

# type = "Superstars"
# games_played_standard = 58
# scoring_floor = 17
# scoring_standard = 23.5
# passing_standard = 12
# rebounding_standard = 12
# stealing_standard = 0.9
# blocking_standard = 0.8
# field_percentage_standard = .650
# three_percentage_standard = .400

# We will search through player per game data frame for qualified players,
# beginning by specifying the era, then qualifying statistics

lebron_competition_p = dfP [
    (dfP['season'] > 2005) & (dfP['season'] <= 2024) &
    (dfP['player'] != 'LeBron James') &
    (dfP['pts_per_game'] >= scoring_floor) &
    (dfP['g'] >= games_played_standard)
]

jordan_competition_p = dfP [
    (dfP['season'] != 1994) & # Jordan did not play this year
    (dfP['season'] > 1984) & (dfP['season'] <= 1998) &
    (dfP['player'] != 'Michael Jordan') &
    (dfP['pts_per_game'] >= scoring_floor) &
    (dfP['g'] >= games_played_standard)
]

lebron_competition_p = lebron_competition_p[
    (lebron_competition_p['pts_per_game'] >= scoring_standard) |
    (lebron_competition_p['ast_per_game'] >= passing_standard) |
    (lebron_competition_p['trb_per_game'] >= rebounding_standard) |
    (lebron_competition_p['stl_per_game'] >= stealing_standard) |
    (lebron_competition_p['blk_per_game'] >= blocking_standard) |
    (lebron_competition_p['fg_percent'] >= field_percentage_standard) |
    (lebron_competition_p['x3p_percent'] >= three_percentage_standard)
]

jordan_competition_p = jordan_competition_p[
    (jordan_competition_p['pts_per_game'] >= scoring_standard) |
    (jordan_competition_p['ast_per_game'] >= passing_standard) |
    (jordan_competition_p['trb_per_game'] >= rebounding_standard) |
    (jordan_competition_p['stl_per_game'] >= stealing_standard) |
    (jordan_competition_p['blk_per_game'] >= blocking_standard) |
    (jordan_competition_p['fg_percent'] >= field_percentage_standard) |
    (jordan_competition_p['x3p_percent'] >= three_percentage_standard)
]

# Calculate average statline for a player who is at least a good role player

lebron_comp_mean_p = lebron_competition_p.mean(numeric_only= True)
jordan_comp_mean_p = jordan_competition_p.mean(numeric_only= True)

# Calculate average number of qualified players per year

avg_qualified_lebron_p = int( round( lebron_competition_p.count().iloc[0] / (2024 - 2005) , 0))
avg_qualified_jordan_p = int( round( jordan_competition_p.count().iloc[0] / (1998 - 1984 + 1) , 0))

# Create comparison table

comparison_data_p = {
    'Era' : ['Lebron (05\'-24\')', 'Jordan (84\'-98\')'],
    'PPG' : [lebron_comp_mean_p['pts_per_game'], jordan_comp_mean_p['pts_per_game']],
    'APG' : [lebron_comp_mean_p['ast_per_game'], jordan_comp_mean_p['ast_per_game']],
    'RPG' : [lebron_comp_mean_p['trb_per_game'], jordan_comp_mean_p['trb_per_game']],
    'SPG' : [lebron_comp_mean_p['stl_per_game'], jordan_comp_mean_p['stl_per_game']],
    'BPG' : [lebron_comp_mean_p['blk_per_game'], jordan_comp_mean_p['blk_per_game']],
    'FG%' : [lebron_comp_mean_p['fg_percent'] * 100, jordan_comp_mean_p['fg_percent'] * 100], # 100 multiplier makes proportions into
    '3P%' : [lebron_comp_mean_p['x3p_percent'] * 100, jordan_comp_mean_p['x3p_percent'] * 100], # full numbers for percentages
    'PPY' : [avg_qualified_lebron_p, avg_qualified_jordan_p]
}

comparison_dataframe_p = pd.DataFrame(comparison_data_p)
comparison_dataframe_p = comparison_dataframe_p.map(two_deci_round)

# Creates figure & axes
fig, ax = plt.subplots(figsize=(11,2.7))

# Creates table
table = ax.table(cellText=comparison_dataframe_p.values, colLabels=comparison_dataframe_p.columns, cellLoc='center', loc='center')

# Changes table appearance
title = "Averages of " + type + "Players, Statistically! - Per Game Stats"
ax.axis('off')
ax.set_title(title)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(.8, 2.5)
plt.tight_layout()

plt.show()


#####   Advanced Player Stats Perspective: Which era had more competition?   #####
# - let's use advanced stats:
#    ~ Availability                   (games played, using previous variable)
#    ~ Player Efficiency Rating       (measures productivity per minute)
#    ~ True Shooting Percentage       (measures shooting efficiency while considering the different values
#                                      of threes, twos, and free throws)
#    ~ Assist Rate                    (percentage of team's shots a player assists while playing)
#    ~ Rebounding Rate                (percentage of missed shots a player rebounds while playing)
#    ~ Steal Rate                     (percentage of opposing team's possessions that end vis a player's steal while playing)
#    ~ Block Rate                     (percentage of opposing team's possessions that end via a player's block while playing)
#    ~ Box Plus Minus                 (estimated contribution to a team while playing)
#    ~ Value Over Replacement Player  (contributions of a player compared to an average "replacement" player in the same position)
#    x Win Shares (will not utilize since this statistic since it accounts for league-wide performance rather than a specific player's production in a game)

# These are the standards/cutoffs we will use to identify players who are at
# least nice role-players, feel free to change them!

# type = "Good Role-Players" # (declared in previous section, can change if desired here)
#games_played = ## (declared in previous section, can change if desired here)
per_floor = 15.0
per_standard = 20.0
tsp_standard = .600
a_rate_standard = 25.0
r_rate_standard = 22.5
s_rate_standard = 1.5
b_rate_standard = 2.0
bpm_standard = 2.0
vorp_standard = 1.0

## Optional standards for superstars! Uncomment these and comment previous

# # type = "Superstar " # (declared in previous section, can change if desired here)
# #games_played = ## (declared in previous section, can change if desired here)
# per_floor = 20.0
# per_standard = 25.0
# tsp_standard = .675
# a_rate_standard = 30.0
# r_rate_standard = 27.5
# s_rate_standard = 2.5
# b_rate_standard = 3.5
# bpm_standard = 2.4
# vorp_standard = 2.2

# We will search through advanced data frame for qualified players,
# beginning by specifying the era, then qualifying statistics

lebron_competition_a = dfA [
    (dfA['season'] > 2005) & (dfA['season'] <= 2024) &
    (dfA['player'] != 'LeBron James') &
    (dfA['g'] >= games_played_standard) &
    (dfA['per'] >= per_floor)
]

jordan_competition_a = dfA [
    (dfA['season'] != 1994) & # Jordan did not play this year
    (dfA['season'] > 1984) & (dfA['season'] <= 1998) &
    (dfA['player'] != 'Michael Jordan') &
    (dfA['g'] >= games_played_standard) &
    (dfA['per'] >= per_floor)
]

lebron_competition_a = lebron_competition_a[
    (lebron_competition_a['per'] >= per_standard) |
    (lebron_competition_a['ts_percent'] >= tsp_standard) |
    (lebron_competition_a['ast_percent'] >= a_rate_standard) |
    (lebron_competition_a['trb_percent'] >= r_rate_standard) |
    (lebron_competition_a['stl_percent'] >= s_rate_standard) |
    (lebron_competition_a['blk_percent'] >= b_rate_standard) |
    (lebron_competition_a['bpm'] >= bpm_standard) |
    (lebron_competition_a['vorp'] >= vorp_standard)
]

jordan_competition_a = jordan_competition_a[
    (jordan_competition_a['per'] >= per_standard) |
    (jordan_competition_a['ts_percent'] >= tsp_standard) |
    (jordan_competition_a['ast_percent'] >= a_rate_standard) |
    (jordan_competition_a['trb_percent'] >= r_rate_standard) |
    (jordan_competition_a['stl_percent'] >= s_rate_standard) |
    (jordan_competition_a['blk_percent'] >= b_rate_standard) |
    (jordan_competition_a['bpm'] >= bpm_standard) |
    (jordan_competition_a['vorp'] >= vorp_standard)
]

# Calculate average advanced statistics for players in data base

lebron_comp_mean_a = lebron_competition_a.mean(numeric_only=True)
jordan_comp_mean_a = jordan_competition_a.mean(numeric_only=True)

# Calculate average number of qualified players per year

avg_qualified_lebron_a = int( round( lebron_competition_a.count().iloc[0] / (2024 - 2005) , 0))
avg_qualified_jordan_a = int( round( jordan_competition_a.count().iloc[0] / (1998 - 1984 + 1) , 0))

#Create comparison table

comparison_data_a = {
    'Era' : ['Lebron (05\'-24\')', 'Jordan (84\'-98\')'],
    'PER' : [lebron_comp_mean_a['per'], jordan_comp_mean_a['per']],
    'TS%' : [lebron_comp_mean_a['ts_percent'], jordan_comp_mean_a['ts_percent']],
    'AS%' : [lebron_comp_mean_a['ast_percent'], jordan_comp_mean_a['ast_percent']],
    'RB%' : [lebron_comp_mean_a['trb_percent'], jordan_comp_mean_a['trb_percent']],
    'ST%' : [lebron_comp_mean_a['stl_percent'], jordan_comp_mean_a['stl_percent']],
    'BK%' : [lebron_comp_mean_a['blk_percent'], jordan_comp_mean_a['blk_percent']],
    'BPM' : [lebron_comp_mean_a['bpm'], jordan_comp_mean_a['bpm']],
    'VORP' : [lebron_comp_mean_a['vorp'], jordan_comp_mean_a['vorp']],
    'PPY' : [avg_qualified_lebron_a, avg_qualified_jordan_a]
}

comparison_dataframe_a = pd.DataFrame(comparison_data_a)
comparison_dataframe_a = comparison_dataframe_a.map(two_deci_round)

fig2, ax2 = plt.subplots(figsize=(11,2.8))

table2 = ax2.table(cellText=comparison_dataframe_a.values, colLabels=comparison_dataframe_a.columns, cellLoc='center', loc='center')

title2 = "Averages of " + type + "Players, Statistically! - Advanced Stats"
ax2.axis('off')
ax2.set_title(title2)
table2.auto_set_font_size(False)
table2.set_fontsize(8)
table2.scale(0.9, 2.5)
plt.tight_layout()

plt.show()

# # Hmmmm......

# # Conclusion 1: Players who are at least role-players from each era average
# similar 'per game' numbers, with a slight edge to LeBron's era.

# Conclusion 2: According to the advanced statistics, players who are at least
# good role-players from LeBron's era are more efficient than those of Jordan's
# era.

# Conclusion 3: When considering mean 'per game' and advanced statistics from 
# both eras, LeBron has faced more players who are at least good role players!

# # Potential flaws or improvements?

# Flaw 1: During the years of both stars, there were moments of expansion for 
# the NBA. For example, the NBA had 23 teams during Jordan's rookie season. Now,
# it has 30! 
#   How to Address: To adjust for this, we can turn the Players Per Year (PPY) stat in
#   the table into a Players Per Team (PPT) stat. After all, the PPY stat was added to
#   address the fact that LeBron has/will play for much longer than Jordan!

# Flaw 2: With so many skilled in talented players from all over the globe who
# have been trained since they were in primary school, couldn't there be outliers
# or statistical phenoms in today's era (in which LeBron played/plays in)? Players 
# such as Luka Doncic, who has averaged nearly a triple double for many seasons, or
# James Harden, who has had historical scoring seasons. Couldn't they skew the mean?
#   How to Address: Why absolutely! There can be outliers in any large dataset, and
#   for this predicament we can look at the median statistics rather than the mean
#   statistics and compare those between the eras.
