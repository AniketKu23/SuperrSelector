import pandas as pd
import numpy as np

def run_pipeline():
    print("Loading data...")
    bbb = pd.read_csv('Data Pack/ball_by_ball.csv')
    matches = pd.read_csv('Data Pack/matches.csv')
    comps = pd.read_csv('Data Pack/competitions.csv')
    
    # Merge competition info into matches
    matches = matches.merge(comps[['comp_id', 'comp_name', 'match_format', 'season']], on='comp_id', how='left')
    matches['is_ipl'] = matches['comp_name'].str.contains('IPL|Indian Premier League', case=False, na=False)
    matches['is_knockout'] = (matches['knock_out'] == 1) | matches['stage'].isin(['Final', 'Semi Final', 'Qualifier', 'Eliminator', 'Super 4'])

    # Determine total runs and extras on each delivery
    bbb['extras1_runs'] = bbb['extras1_runs'].fillna(0)
    bbb['extras_2_runs'] = bbb['extras_2_runs'].fillna(0)
    bbb['runs'] = bbb['runs'].fillna(0)
    
    # Batter balls faced: legal ball for batter is anything except wide
    bbb['is_batter_ball'] = bbb['extras_type'] != 'wide'
    
    # Bowler legal ball: anything except wide and Overstep (no ball)
    bbb['is_bowler_legal_ball'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
    
    # Total runs conceded on this ball
    bbb['total_ball_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']
    
    # Bowler runs conceded: batter runs + wide runs + noball runs (legbyes and byes are not charged to bowler)
    bbb['is_bye_or_legbye'] = bbb['extras_type'].isin(['byes', 'legbyes'])
    bbb['bowler_runs_conceded'] = np.where(bbb['is_bye_or_legbye'], 0, bbb['total_ball_runs'])
    
    # Bowler wicket: Bowled, Caught, LBW, Stump, Hit Wicket
    bowler_dismissals = ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']
    bbb['is_bowler_wicket'] = bbb['is_wicket'] & bbb['dismissal_type'].isin(bowler_dismissals)
    
    # Batter dismissal: striker is dismissed
    bbb['is_striker_dismissed'] = bbb['is_wicket'] & (bbb['dismissed_player_id'] == bbb['striker_id'])
    
    # Sort chronologically within match and innings
    bbb = bbb.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)
    
    # Cumulative stats per innings
    bbb['cum_innings_runs'] = bbb.groupby(['match_id', 'innings'])['total_ball_runs'].cumsum()
    bbb['cum_innings_wickets'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum()
    bbb['cum_legal_balls'] = bbb.groupby(['match_id', 'innings'])['is_bowler_legal_ball'].cumsum()
    
    # State BEFORE current ball
    bbb['score_before'] = bbb['cum_innings_runs'] - bbb['total_ball_runs']
    bbb['wickets_before'] = bbb['cum_innings_wickets'] - bbb['is_wicket'].astype(int)
    bbb['legal_balls_before'] = bbb.groupby(['match_id', 'innings'])['is_bowler_legal_ball'].cumsum() - bbb['is_bowler_legal_ball'].astype(int)
    bbb['wickets_in_hand'] = 10 - bbb['wickets_before']
    bbb['balls_remaining'] = np.maximum(0, 120 - bbb['legal_balls_before'])
    
    # Calculate Innings 1 totals to determine targets for Innings 2
    inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['total_ball_runs'].sum().reset_index()
    inn1_totals.rename(columns={'total_ball_runs': 'inn1_total_runs'}, inplace=True)
    
    bbb = bbb.merge(inn1_totals, on='match_id', how='left')
    bbb = bbb.merge(matches[['match_id', 'is_ipl', 'is_knockout', 'revised_target', 'win_team_id']], on='match_id', how='left')
    
    # Compute target for Innings 2
    bbb['target'] = np.where(
        bbb['revised_target'].notna() & (bbb['revised_target'] > 0),
        bbb['revised_target'],
        bbb['inn1_total_runs'] + 1
    )
    
    bbb['runs_required'] = np.maximum(0, bbb['target'] - bbb['score_before'])
    
    # Required run rate
    bbb['rrr'] = np.where(
        (bbb['innings'] == 2) & (bbb['balls_remaining'] > 0),
        (bbb['runs_required'] / bbb['balls_remaining']) * 6.0,
        0.0
    )
    
    # Pressure calculation
    # Base pressure index 0-100
    pressure_scores = []
    
    # Vectorized / fast array iteration for pressure logic
    for row in bbb.itertuples():
        inn = row.innings
        if inn >= 3:
            # Super over: maximum pressure
            pressure_scores.append(100.0)
            continue
            
        over = row.overid
        w_in_hand = max(1, row.wickets_in_hand)
        w_lost = row.wickets_before
        balls_rem = max(1, row.balls_remaining)
        
        if inn == 2:
            # Chasing
            rrr = row.rrr
            req_runs = row.runs_required
            
            # Base chase stress from RRR (par T20 RRR is ~8.5)
            # RRR 6 -> stress ~ 30, RRR 9 -> stress ~ 55, RRR 12 -> stress ~ 80, RRR 15+ -> stress ~ 95
            rrr_stress = 50.0 + (rrr - 8.5) * 7.5
            
            # Wicket scarcity stress: each lost wicket increases pressure non-linearly
            # Especially when <= 4 wickets in hand
            wicket_factor = 1.0
            if w_in_hand <= 5:
                wicket_factor = 1.0 + (6 - w_in_hand) * 0.12
            if w_in_hand <= 2:
                wicket_factor = 1.5
                
            # Phase stress: death overs (balls_rem <= 30)
            phase_stress = 0.0
            if balls_rem <= 30:
                phase_stress = (30 - balls_rem) * 0.8
            elif balls_rem <= 48:
                phase_stress = 10.0
                
            # Closeness factor: if contest is close
            closeness = 0.0
            if req_runs <= 36 and balls_rem <= 24:
                closeness = 15.0
            elif req_runs <= 15 and balls_rem <= 12:
                closeness = 25.0
                
            # If target already achieved or virtually impossible without wickets
            if req_runs <= 0:
                p = 10.0
            else:
                p = (rrr_stress * wicket_factor) + phase_stress + closeness
                
        else:
            # Innings 1: Setting total
            # Collapse pressure: wickets lost early
            collapse_stress = 0.0
            if over <= 6 and w_lost >= 2:
                collapse_stress = 20.0 + (w_lost - 2) * 15.0
            elif over <= 12 and w_lost >= 4:
                collapse_stress = 25.0 + (w_lost - 4) * 12.0
                
            # Death overs acceleration pressure (overs 16-20)
            death_stress = 0.0
            if over >= 16:
                death_stress = 25.0 + (over - 15) * 6.0
                
            # Baseline innings 1 pressure is around 35-45, ramping up in death overs or after collapse
            p = 38.0 + collapse_stress + death_stress
            
        # Match context adjustments
        if row.is_knockout:
            p *= 1.20
        if row.is_ipl:
            p *= 1.10
            
        pressure_scores.append(np.clip(p, 5.0, 100.0))
        
    bbb['pressure_score'] = pressure_scores
    
    # Classify pressure
    # 75th percentile / upper tier as high pressure
    print("Pressure score distribution:")
    print(bbb['pressure_score'].describe())
    
    # High pressure threshold: >= 60 (or >= 55)
    bbb['is_pressure'] = bbb['pressure_score'] >= 58.0
    print(f"High pressure ball count: {bbb['is_pressure'].sum()} ({bbb['is_pressure'].mean()*100:.2f}%)")
    
    return bbb, matches

if __name__ == '__main__':
    bbb, matches = run_pipeline()
