# Features defined for the Model

- Location Score: IF more teams won by wickets: '1' if team 1 is bowling first ELSE IF more team won by runs: '1' if team 1 is batting first
- Momentum Score: No. of most recent games won by team 1/No. of most recent games won by team 2
- Team 1 Batting Score: Average of Z-Score's of runs in last 3 matches considering last 10 matches
- Team 2 Batting Score: Average of Z-Score's of runs in last 3 matches considering last 10 matches
- Batting Score: 1 IF (Team 1 Batting Score/Team 2 Batting Score) > 1 else 0
- Team 1 Bowling Score: Average of Z-Score's of wickets in last 3 matches considering last 10 matches
- Team 2 Bowling Score: Average of Z-Score's of wickets in last 3 matches considering last 10 matches
- Bowling Score: 1 IF (Team 1 Bowling Score/Team 2 Bowling Score) > 1 else 0
- Team 1 Bowling Score B: Average of wickets by top 3 wicket takers from roster
- Team 2 Bowling Score B: Average of wickets by top 3 wicket takers from roster

Note: LookBack Period is 10 matches unless otherwise specified