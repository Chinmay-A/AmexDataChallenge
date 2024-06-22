def winp_last5_categorized(row, data):
    winp_last5 = row['team_winp_last5']
    if winp_last5 < 0.5:
        return 0
    elif winp_last5 < 2:
        return 2
    else:
        return 1
