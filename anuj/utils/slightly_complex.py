def winp_last5_categorized(row, data):
    winp_last5 = row['team_winp_last5']
    if winp_last5 < 0.5:
        return 0
    elif winp_last5 < 2:
        return 2
    else:
        return 1

def inning1_perf(row, data):
    team1 = row['team1_id']
    team1_matches = data['match'][(data['match']['team1_id'] == team1)]

    team1_avg = team1_matches['inning1_runs'].mean()
    general_avg = data['match']['inning1_runs'].mean()
    if team1_avg > general_avg * 1.2:
        return 2
    elif team1_avg < general_avg * 0.8:
        return 0
    else:
        return 1
    
def inning2_perf(row, data):
    team2 = row['team2_id']
    team2_matches = data['match'][(data['match']['team2_id'] == team2)]

    team2_avg = team2_matches['inning2_runs'].mean()
    general_avg = data['match']['inning2_runs'].mean()
    if team2_avg > general_avg * 1.2:
        return 2
    elif team2_avg < general_avg * 0.8:
        return 0
    else:
        return 1
    
def has_good_bowlers(row,data):

    bowlers=data['bowl']

    players=row['team2_roster_ids'].split(':')

    good_bowlers=0

    for player in players:

        player_matches=bowlers[bowlers['bowler_id']==float(player)]
        matches_satisfying_criteria=player_matches[player_matches['wicket_count']>=4]

        if(len(matches_satisfying_criteria)>=1):
            good_bowlers+=1
    
    if(good_bowlers<1):
        return 0
    elif(good_bowlers<3):
        return 1
    
    return 2

def has_good_batsmen(row,data):

    batsman=data['bat']

    players=row['team1_roster_ids'].split(':')

    good_batsman=0

    for player in players:

        player_matches=batsman[batsman['batsman_id']==float(player)]
        matches_satisfying_criteria=player_matches[player_matches['runs']>=50]

        if(len(matches_satisfying_criteria)>=1):
            good_batsman+=1
    
    if(good_batsman<2):
        return 0
    elif(good_batsman<4):
        return 1
    
    return 2

def usual_wins(row,data):

    matches=data['match']

    team1_games=matches[matches['team1_id']==row['team1_id']]
    team2_games=matches[matches['team2_id']==row['team1_id']]

    team1_won_by_runs=team1_games[team1_games['by']=='runs']
    team1_won_by_wickets=team2_games[team2_games['by']=='wickets']

    if(len(team1_won_by_runs)>len(team1_won_by_wickets)):
        return 1

    return 0

def experience_score(row,data):

    team1exp=0
    team2exp=0

    bowlers=data['bowl']
    batsmen=data['bat']

    team1players=row['team1_roster_ids'].split(':')
    team2players=row['team2_roster_ids'].split(':')

    for player in team1players:
        
        rel_bowlers=bowlers[bowlers['bowler_id']==float(player)]
        rel_batsmen=batsmen[batsmen['batsman_id']==float(player)]

        satis_batsmen=rel_batsmen[rel_batsmen['runs']>=30]
        satis_bowlers=rel_bowlers[rel_bowlers['wicket_count']>=2]
        
        team1exp+=len(satis_batsmen)+len(satis_bowlers)
    
    for player in team2players:
        
        rel_bowlers=bowlers[bowlers['bowler_id']==float(player)]
        rel_batsmen=batsmen[batsmen['batsman_id']==float(player)]

        satis_batsmen=rel_batsmen[rel_batsmen['runs']>=30]
        satis_bowlers=rel_bowlers[rel_bowlers['wicket_count']>=2]
        
        team2exp+=len(satis_batsmen)+len(satis_bowlers)
    
    if(team1exp>team2exp):
        return 1
    
    return 0