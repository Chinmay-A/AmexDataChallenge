import random

def lighting(row, data):
    if row['lighting'] == 'day/night match':
        return 1
    elif row['lighting'] == 'day match':
        return 0
    elif row['lighting'] == 'night match':
        return 2
    
def team1v2_win_prob(row, data):
    team1 = row['team1_id']
    team2 = row['team2_id']
    team1v2_matches = data['match'][(data['match']['team1_id'] == team1) & (data['match']['team2_id'] == team1)]
    team2v1_matches = data['match'][(data['match']['team1_id'] == team2) & (data['match']['team2_id'] == team1)]

    team1_wins = len(team1v2_matches[team1v2_matches['winner_id'] == team1])
    team1_wins += len(team2v1_matches[team2v1_matches['winner_id'] == team1])

    total_matches = len(team1v2_matches) + len(team2v1_matches)
    if total_matches == 0 or team1_wins == total_matches / 2:
        return 1
    elif team1_wins > total_matches / 2:
        return 2
    else:
        return 0

def team1_games_played(row, data):
    team1 = row['team1_id']
    team1_matches = data['match'][(data['match']['team1_id'] == team1) | (data['match']['team2_id'] == team1)]
    return len(team1_matches)

def team2_games_played(row, data):
    team2 = row['team2_id']
    team2_matches = data['match'][(data['match']['team1_id'] == team2) | (data['match']['team2_id'] == team2)]
    return len(team2_matches)

def team1_win_prob(row, data):
    team1 = row['team1_id']
    team1_matches = data['match'][(data['match']['team1_id'] == team1) | (data['match']['team2_id'] == team1)]
    team1_wins = len(team1_matches[team1_matches['winner_id'] == team1])
    if len(team1_matches) == 0:
        return 0.5
    return team1_wins / len(team1_matches)

def team2_win_prob(row, data):
    team2 = row['team2_id']
    team2_matches = data['match'][(data['match']['team1_id'] == team2) | (data['match']['team2_id'] == team2)]
    team2_wins = len(team2_matches[team2_matches['winner_id'] == team2])
    if len(team2_matches) == 0:
        return 0.5
    return team2_wins / len(team2_matches)

def played_more_games(row, data):
    team1 = row['team1_id']
    team2 = row['team2_id']
    team1_matches = data['match'][(data['match']['team1_id'] == team1) | (data['match']['team2_id'] == team1)]
    team2_matches = data['match'][(data['match']['team1_id'] == team2) | (data['match']['team2_id'] == team2)]
    return len(team1_matches) > len(team2_matches)

def more_win_percent(row, data):
    team1 = row['team1_id']
    team2 = row['team2_id']
    team1_matches = data['match'][(data['match']['team1_id'] == team1) | (data['match']['team2_id'] == team1)]
    team2_matches = data['match'][(data['match']['team1_id'] == team2) | (data['match']['team2_id'] == team2)]
    team1_wins = len(team1_matches[team1_matches['winner_id'] == team1])
    team2_wins = len(team2_matches[team2_matches['winner_id'] == team2])
    if len(team1_matches) == 0:
        team1_win_percent = 0.5
    else:
        team1_win_percent = team1_wins / len(team1_matches)
    if len(team2_matches) == 0:
        team2_win_percent = 0.5
    else:
        team2_win_percent = team2_wins / len(team2_matches)
    return team1_win_percent > team2_win_percent

def much_more_games_played(row, data):
    team1 = row['team1_id']
    team2 = row['team2_id']
    team1_matches = data['match'][(data['match']['team1_id'] == team1) | (data['match']['team2_id'] == team1)]
    team2_matches = data['match'][(data['match']['team1_id'] == team2) | (data['match']['team2_id'] == team2)]
    return (len(team1_matches) > 2 * len(team2_matches)) and (len(team1_matches) > len(team2_matches) + 8)