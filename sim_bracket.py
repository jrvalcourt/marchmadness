###############################################################################
#                                                                             #
#  Simulate the NCAA Men's Tournament using the 538 win probabilities         #
#  because, let's be honest, you don't really sports.                         #
#                                                                             #
#  Copyright 2019 James Valcourt                                              #
#                                                                             #
#  Licensed under the Apache License, Version 2.0 (the "License");            #
#  you may not use this file except in compliance with the License.           #
#  You may obtain a copy of the License at                                    #
#                                                                             #
#      http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                             #
#  Unless required by applicable law or agreed to in writing, software        #
#  distributed under the License is distributed on an "AS IS" BASIS,          #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#  See the License for the specific language governing permissions and        #
#  limitations under the License.                                             #
#                                                                             #
#                                                                             #
###############################################################################

import random
import os

data_file = 'fivethirtyeight_ncaa_forecasts.csv'
if not os.path.exists(data_file):
    import wget
    wget.download('https://projects.fivethirtyeight.com/march-madness-api/2019/fivethirtyeight_ncaa_forecasts.csv')

# I'm not sure exactly how the 538 team rating translates 
# to win probabilty---it's not a simple Elo, for example---so I'm
# just picking teams based on the per-round advancement probabilities
def pick_a_winner(team1, team2, data, n):
    print(f"#{team_to_seed[team1]} {team1} v. #{team_to_seed[team2]} {team2}:")
    team1_prob = data[team1][n-1]
    team2_prob = data[team2][n-1]
    rnd = random.random()
    if rnd > (team1_prob / (team1_prob + team2_prob)):
        print(f"    {team2}")
        return team2
    else:
        print(f"    {team1}")
        return team1

# set up some data structures
data = {}
seed = {}
regions = ['South', 'West', 'East', 'Midwest']
for r in regions:
    seed[r] = {}
team_to_seed = {}
final_four = {}

# read in all of our data
with open(data_file) as fin:

    # read the header
    header = fin.readline().split(',')
    team_seed_idx = header.index('team_seed')
    region_idx = header.index('team_region')
    team_name_idx = header.index('team_name')
    playin_idx = header.index('playin_flag')
    rd2_idx = header.index('rd2_win')
    rd7_idx = header.index('rd7_win')

    # read each record
    for line in fin:
        e = line.strip().split(',')

        # pretty lame that not as many people fill out brackets 
        # for the women's tourney...
        if e[0] != 'mens':
            continue

        team_name = e[team_name_idx] 
        if int(e[playin_idx]) > 0:
            # if it's a play-in, resolve it arbitraily by just keeping the last 
            # team encountered with a given seed in a region
            team_seed = int(e[team_seed_idx][:-1])
        else:
            team_seed = int(e[team_seed_idx])
        region = e[region_idx]
        probs = [float(x) for x in e[rd2_idx:rd7_idx+1]]
        data[team_name] = probs
        seed[region][team_seed] = team_name
        team_to_seed[team_name] = team_seed

# do the simulation
for region in seed.keys():
    print(f"***************** {region} *****************")
    print("Round 1")
    w1v16 = pick_a_winner(seed[region][1], seed[region][16], data, 1)
    w2v15 = pick_a_winner(seed[region][2], seed[region][15], data, 1)
    w3v14 = pick_a_winner(seed[region][3], seed[region][14], data, 1)
    w4v13 = pick_a_winner(seed[region][4], seed[region][13], data, 1)
    w5v12 = pick_a_winner(seed[region][5], seed[region][12], data, 1)
    w6v11 = pick_a_winner(seed[region][6], seed[region][11], data, 1)
    w7v10 = pick_a_winner(seed[region][7], seed[region][10], data, 1)
    w8v9  = pick_a_winner(seed[region][8], seed[region][9],  data, 1)

    print("\nRound 2")
    w2_1 = pick_a_winner(w1v16, w8v9,  data, 2)
    w2_2 = pick_a_winner(w5v12, w4v13, data, 2)
    w2_3 = pick_a_winner(w6v11, w3v14, data, 2)
    w2_4 = pick_a_winner(w7v10, w2v15, data, 2)

    print("\nSweet 16")
    w3_1 = pick_a_winner(w2_1, w2_2, data, 3)
    w3_2 = pick_a_winner(w2_3, w2_4, data, 3)
   
    print("\nElite Eight")
    final_four[region] = pick_a_winner(w3_1, w3_2, data, 4)

print("*******************************************************")
print("Final Four")
semi1 = pick_a_winner(final_four['South'], final_four['West'], data, 5)
semi2 = pick_a_winner(final_four['East'], final_four['Midwest'], data, 5)

print("\nChampionship")
pick_a_winner(semi1, semi2, data, 6)
print("*******************************************************")
