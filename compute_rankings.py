import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from build_model import run_pipeline

def generate_full_rankings():
    print("--- Starting Full Pipeline ---")
    bbb, matches = run_pipeline()
    
    # Opposition Tier Definition
    tier1_teams = [
        'India', 'Australia', 'England', 'South Africa', 'New Zealand', 'Pakistan', 'West Indies',
        'Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals',
        'Sunrisers Hyderabad', 'Royal Challengers Bengaluru', 'Delhi Capitals', 'Punjab Kings',
        'Lucknow Super Giants', 'Gujarat Titans'
    ]
    tier2_teams = ['Sri Lanka', 'Afghanistan', 'Bangladesh']
    
    # Map batting team and bowling team names
    teams_df = pd.read_csv('Data Pack/teams.csv').drop_duplicates(subset=['team_id'])
    team_map = dict(zip(teams_df['team_id'], teams_df['team_name']))
    
    bbb['batting_team_name'] = bbb['batting_team_id'].map(team_map)
    bbb['bowling_team_name'] = bbb['bowling_team_id'].map(team_map)
    
    # Batter faces bowling team: opp tier
    def get_tier_weight(team_name):
        if team_name in tier1_teams:
            return 1.15
        elif team_name in tier2_teams:
            return 1.00
        else:
            return 0.85
            
    bbb['opp_weight_for_bat'] = bbb['bowling_team_name'].apply(get_tier_weight)
    bbb['opp_weight_for_bowl'] = bbb['batting_team_name'].apply(get_tier_weight)
    
    # Target and match win tracking
    bbb['is_batting_team_win'] = (bbb['batting_team_id'] == bbb['win_team_id']).astype(int)
    
    # Win Probability Modeling
    # Innings 2 Model
    inn2_mask = bbb['innings'] == 2
    features_inn2 = ['runs_required', 'balls_remaining', 'wickets_in_hand', 'rrr']
    X2 = bbb.loc[inn2_mask, features_inn2].fillna(0)
    y2 = bbb.loc[inn2_mask, 'is_batting_team_win']
    lr2 = LogisticRegression()
    lr2.fit(X2, y2)
    bbb.loc[inn2_mask, 'wp_before'] = lr2.predict_proba(X2)[:, 1]
    
    # Innings 1 Model
    inn1_mask = bbb['innings'] == 1
    bbb['crr'] = np.where(bbb['legal_balls_before'] > 0, (bbb['score_before'] / bbb['legal_balls_before']) * 6.0, 8.0)
    bbb['projected_score'] = bbb['score_before'] + (bbb['balls_remaining'] / 6.0) * np.maximum(6.0, bbb['crr'])
    features_inn1 = ['score_before', 'legal_balls_before', 'wickets_in_hand', 'projected_score']
    X1 = bbb.loc[inn1_mask, features_inn1].fillna(0)
    y1 = bbb.loc[inn1_mask, 'is_batting_team_win']
    lr1 = LogisticRegression()
    lr1.fit(X1, y1)
    bbb.loc[inn1_mask, 'wp_before'] = lr1.predict_proba(X1)[:, 1]
    
    # Super Overs
    bbb.loc[bbb['innings'] >= 3, 'wp_before'] = 0.50
    bbb['wp_before'] = bbb['wp_before'].fillna(0.50)
    
    # Win Probability After
    bbb['wp_after'] = bbb.groupby(['match_id', 'innings'])['wp_before'].shift(-1)
    bbb.loc[bbb['wp_after'].isna(), 'wp_after'] = bbb.loc[bbb['wp_after'].isna(), 'is_batting_team_win'].astype(float)
    
    # WPA
    bbb['wpa_bat'] = bbb['wp_after'] - bbb['wp_before']
    bbb['wpa_bowl'] = -bbb['wpa_bat']
    
    # Leverage Index
    bbb['leverage'] = np.abs(bbb['wpa_bat']) * 10.0
    lev_scaled = np.clip(bbb['leverage'] * 20.0, 0, 100)
    bbb['hybrid_pressure'] = 0.70 * bbb['pressure_score'] + 0.30 * lev_scaled
    
    # High Pressure definition: hybrid_pressure >= 60.0
    bbb['is_high_pressure'] = bbb['hybrid_pressure'] >= 60.0
    
    # Total context weight per ball
    bbb['ball_weight_bat'] = bbb['opp_weight_for_bat'] * np.where(bbb['is_knockout'], 1.20, 1.00)
    bbb['ball_weight_bowl'] = bbb['opp_weight_for_bowl'] * np.where(bbb['is_knockout'], 1.20, 1.00)
    
    # -------------------------------------------------------------
    # BATTING MODEL
    # -------------------------------------------------------------
    # Baseline
    bat_base = bbb[bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
        base_balls=('runs', 'count'),
        base_runs=('runs', 'sum'),
        base_dismissals=('is_striker_dismissed', 'sum'),
        base_dots=('runs', lambda s: (s == 0).sum()),
        base_fours=('is_four', 'sum'),
        base_sixes=('is_six', 'sum'),
        base_matches=('match_id', 'nunique'),
        base_wpa=('wpa_bat', 'sum')
    ).reset_index()
    
    bat_base['base_sr'] = (bat_base['base_runs'] / bat_base['base_balls']) * 100
    bat_base['base_avg'] = bat_base['base_runs'] / np.maximum(1, bat_base['base_dismissals'])
    bat_base['base_dot_pct'] = (bat_base['base_dots'] / bat_base['base_balls']) * 100
    bat_base['base_boundary_pct'] = ((bat_base['base_fours'] + bat_base['base_sixes']) / bat_base['base_balls']) * 100
    
    # Pressure
    bat_press = bbb[bbb['is_batter_ball'] & bbb['is_high_pressure']].groupby(['striker_id', 'striker_name']).agg(
        press_balls=('runs', 'count'),
        press_runs=('runs', 'sum'),
        press_dismissals=('is_striker_dismissed', 'sum'),
        press_dots=('runs', lambda s: (s == 0).sum()),
        press_fours=('is_four', 'sum'),
        press_sixes=('is_six', 'sum'),
        press_matches=('match_id', 'nunique'),
        press_wpa=('wpa_bat', 'sum'),
        weighted_press_balls=('ball_weight_bat', 'sum'),
        weighted_press_runs=('runs', lambda s: np.sum(s * bbb.loc[s.index, 'ball_weight_bat'])),
        avg_pressure_faced=('hybrid_pressure', 'mean')
    ).reset_index()
    
    bat_press['press_sr'] = (bat_press['press_runs'] / bat_press['press_balls']) * 100
    bat_press['press_avg'] = bat_press['press_runs'] / np.maximum(1, bat_press['press_dismissals'])
    bat_press['press_dot_pct'] = (bat_press['press_dots'] / bat_press['press_balls']) * 100
    bat_press['press_boundary_pct'] = ((bat_press['press_fours'] + bat_press['press_sixes']) / bat_press['press_balls']) * 100
    
    # Quality-adjusted pressure SR & Avg
    bat_press['qual_press_sr'] = (bat_press['weighted_press_runs'] / bat_press['weighted_press_balls']) * 100
    
    batters = bat_base.merge(bat_press, on=['striker_id', 'striker_name'], how='inner')
    
    # Qualification: >= 120 total balls, >= 45 pressure balls, >= 8 matches
    bat_qualified = batters[(batters['base_balls'] >= 120) & (batters['press_balls'] >= 45) & (batters['base_matches'] >= 8)].copy()
    
    # Differentials
    bat_qualified['delta_sr'] = bat_qualified['press_sr'] - bat_qualified['base_sr']
    bat_qualified['delta_avg'] = bat_qualified['press_avg'] - bat_qualified['base_avg']
    bat_qualified['delta_dot_pct'] = bat_qualified['base_dot_pct'] - bat_qualified['press_dot_pct']
    bat_qualified['delta_bnd_pct'] = bat_qualified['press_boundary_pct'] - bat_qualified['base_boundary_pct']
    
    # Bayesian Shrinkage (Prior hyperparameter K = 40)
    K_bat = 40.0
    pop_sr = bat_qualified['qual_press_sr'].mean()
    pop_avg = bat_qualified['press_avg'].mean()
    
    bat_qualified['shrunk_press_sr'] = (bat_qualified['press_balls'] * bat_qualified['qual_press_sr'] + K_bat * pop_sr) / (bat_qualified['press_balls'] + K_bat)
    bat_qualified['shrunk_press_avg'] = (bat_qualified['press_balls'] * bat_qualified['press_avg'] + K_bat * pop_avg) / (bat_qualified['press_balls'] + K_bat)
    
    # Match Consistency (Standard deviation across innings)
    match_bat = bbb[bbb['is_batter_ball'] & bbb['is_high_pressure']].groupby(['striker_id', 'match_id']).agg(
        m_runs=('runs', 'sum'),
        m_balls=('runs', 'count')
    ).reset_index()
    match_bat['m_sr'] = (match_bat['m_runs'] / match_bat['m_balls']) * 100
    bat_sd = match_bat.groupby('striker_id')['m_sr'].std().reset_index().rename(columns={'m_sr': 'sr_consistency_std'})
    bat_qualified = bat_qualified.merge(bat_sd, on='striker_id', how='left')
    bat_qualified['sr_consistency_std'] = bat_qualified['sr_consistency_std'].fillna(50.0)
    
    # Reliability Volume Factor: logarithmic scaling
    bat_qualified['volume_factor'] = np.clip(np.log(bat_qualified['press_balls']) / np.log(300), 0.70, 1.15)
    
    def min_max_norm(s):
        s_min, s_max = s.min(), s.max()
        return (s - s_min) / (s_max - s_min) if s_max > s_min else pd.Series(0.5, index=s.index)
        
    norm_sr = min_max_norm(bat_qualified['shrunk_press_sr'])
    norm_avg = min_max_norm(bat_qualified['shrunk_press_avg'])
    norm_delta_sr = min_max_norm(bat_qualified['delta_sr'])
    norm_bnd = min_max_norm(bat_qualified['press_boundary_pct'])
    norm_wpa = min_max_norm(bat_qualified['press_wpa'] / np.maximum(1, bat_qualified['press_matches']))
    norm_consistency = min_max_norm(-bat_qualified['sr_consistency_std'])
    
    # Composite Clutch Rating
    raw_bat_rating = (
        0.28 * norm_sr +
        0.18 * norm_avg +
        0.20 * norm_delta_sr +
        0.14 * norm_bnd +
        0.12 * norm_wpa +
        0.08 * norm_consistency
    ) * 100.0
    
    bat_qualified['clutch_rating'] = raw_bat_rating * bat_qualified['volume_factor']
    top_batters = bat_qualified.sort_values(by='clutch_rating', ascending=False).reset_index(drop=True)
    top_batters['rank'] = top_batters.index + 1
    
    # -------------------------------------------------------------
    # BOWLING MODEL
    # -------------------------------------------------------------
    bowl_base = bbb[bbb['is_bowler_legal_ball']].groupby(['bowler_id', 'bowler_name']).agg(
        base_balls=('runs', 'count'),
        base_runs_conceded=('bowler_runs_conceded', 'sum'),
        base_wickets=('is_bowler_wicket', 'sum'),
        base_dots=('bowler_runs_conceded', lambda s: (s == 0).sum()),
        base_boundaries=('runs', lambda s: ((s == 4) | (s == 6)).sum()),
        base_matches=('match_id', 'nunique'),
        base_wpa=('wpa_bowl', 'sum')
    ).reset_index()
    
    bowl_base['base_econ'] = (bowl_base['base_runs_conceded'] / bowl_base['base_balls']) * 6.0
    bowl_base['base_avg'] = bowl_base['base_runs_conceded'] / np.maximum(1, bowl_base['base_wickets'])
    bowl_base['base_dot_pct'] = (bowl_base['base_dots'] / bowl_base['base_balls']) * 100
    bowl_base['base_boundary_pct'] = (bowl_base['base_boundaries'] / bowl_base['base_balls']) * 100
    
    # Pressure
    bowl_press = bbb[bbb['is_bowler_legal_ball'] & bbb['is_high_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
        press_balls=('runs', 'count'),
        press_runs_conceded=('bowler_runs_conceded', 'sum'),
        press_wickets=('is_bowler_wicket', 'sum'),
        press_dots=('bowler_runs_conceded', lambda s: (s == 0).sum()),
        press_boundaries=('runs', lambda s: ((s == 4) | (s == 6)).sum()),
        press_matches=('match_id', 'nunique'),
        press_wpa=('wpa_bowl', 'sum'),
        weighted_press_balls=('ball_weight_bowl', 'sum'),
        weighted_press_runs=('bowler_runs_conceded', lambda s: np.sum(s * bbb.loc[s.index, 'ball_weight_bowl'])),
        avg_pressure_bowled=('hybrid_pressure', 'mean')
    ).reset_index()
    
    bowl_press['press_econ'] = (bowl_press['press_runs_conceded'] / bowl_press['press_balls']) * 6.0
    bowl_press['press_avg'] = bowl_press['press_runs_conceded'] / np.maximum(1, bowl_press['press_wickets'])
    bowl_press['press_wicket_sr'] = bowl_press['press_balls'] / np.maximum(1, bowl_press['press_wickets'])
    bowl_press['press_dot_pct'] = (bowl_press['press_dots'] / bowl_press['press_balls']) * 100
    bowl_press['press_boundary_pct'] = (bowl_press['press_boundaries'] / bowl_press['press_balls']) * 100
    
    # Quality-adjusted pressure economy
    bowl_press['qual_press_econ'] = (bowl_press['weighted_press_runs'] / bowl_press['weighted_press_balls']) * 6.0
    
    bowlers = bowl_base.merge(bowl_press, on=['bowler_id', 'bowler_name'], how='inner')
    
    # Qualification: >= 120 total balls, >= 45 pressure balls, >= 8 matches
    bowl_qualified = bowlers[(bowlers['base_balls'] >= 120) & (bowlers['press_balls'] >= 45) & (bowlers['base_matches'] >= 8)].copy()
    
    # Differentials
    bowl_qualified['delta_econ'] = bowl_qualified['base_econ'] - bowl_qualified['press_econ']
    bowl_qualified['delta_dot_pct'] = bowl_qualified['press_dot_pct'] - bowl_qualified['base_dot_pct']
    bowl_qualified['delta_bnd_pct'] = bowl_qualified['base_boundary_pct'] - bowl_qualified['press_boundary_pct']
    
    # Shrinkage
    K_bowl = 40.0
    pop_econ = bowl_qualified['qual_press_econ'].mean()
    pop_wsr = bowl_qualified['press_wicket_sr'].mean()
    
    bowl_qualified['shrunk_press_econ'] = (bowl_qualified['press_balls'] * bowl_qualified['qual_press_econ'] + K_bowl * pop_econ) / (bowl_qualified['press_balls'] + K_bowl)
    bowl_qualified['shrunk_press_wsr'] = (bowl_qualified['press_balls'] * bowl_qualified['press_wicket_sr'] + K_bowl * pop_wsr) / (bowl_qualified['press_balls'] + K_bowl)
    
    # Consistency
    match_bowl = bbb[bbb['is_bowler_legal_ball'] & bbb['is_high_pressure']].groupby(['bowler_id', 'match_id']).agg(
        m_runs=('bowler_runs_conceded', 'sum'),
        m_balls=('runs', 'count')
    ).reset_index()
    match_bowl['m_econ'] = (match_bowl['m_runs'] / match_bowl['m_balls']) * 6.0
    bowl_sd = match_bowl.groupby('bowler_id')['m_econ'].std().reset_index().rename(columns={'m_econ': 'econ_consistency_std'})
    bowl_qualified = bowl_qualified.merge(bowl_sd, on='bowler_id', how='left')
    bowl_qualified['econ_consistency_std'] = bowl_qualified['econ_consistency_std'].fillna(4.0)
    
    # Volume factor
    bowl_qualified['volume_factor'] = np.clip(np.log(bowl_qualified['press_balls']) / np.log(300), 0.70, 1.15)
    
    norm_econ = min_max_norm(-bowl_qualified['shrunk_press_econ'])
    norm_wsr = min_max_norm(-bowl_qualified['shrunk_press_wsr'])
    norm_delta_econ = min_max_norm(bowl_qualified['delta_econ'])
    norm_dot = min_max_norm(bowl_qualified['press_dot_pct'])
    norm_bowl_wpa = min_max_norm(bowl_qualified['press_wpa'] / np.maximum(1, bowl_qualified['press_matches']))
    norm_bowl_cons = min_max_norm(-bowl_qualified['econ_consistency_std'])
    
    raw_bowl_rating = (
        0.28 * norm_econ +
        0.24 * norm_wsr +
        0.18 * norm_delta_econ +
        0.14 * norm_dot +
        0.10 * norm_bowl_wpa +
        0.06 * norm_bowl_cons
    ) * 100.0
    
    bowl_qualified['clutch_rating'] = raw_bowl_rating * bowl_qualified['volume_factor']
    top_bowlers = bowl_qualified.sort_values(by='clutch_rating', ascending=False).reset_index(drop=True)
    top_bowlers['rank'] = top_bowlers.index + 1
    
    # Save enriched tables
    top_batters.to_csv('top_batters_pressure.csv', index=False)
    top_bowlers.to_csv('top_bowlers_pressure.csv', index=False)
    bbb.to_feather('bbb_enriched.feather')
    
    print("\n================== DEFINITIVE TOP 10 BATTERS UNDER PRESSURE ==================")
    print(top_batters[['rank', 'striker_id', 'striker_name', 'press_balls', 'press_sr', 'press_avg', 'delta_sr', 'press_wpa', 'clutch_rating']].head(10).to_string(index=False))
    
    print("\n================== DEFINITIVE TOP 10 BOWLERS UNDER PRESSURE ==================")
    print(top_bowlers[['rank', 'bowler_id', 'bowler_name', 'press_balls', 'press_econ', 'press_wickets', 'delta_econ', 'press_wpa', 'clutch_rating']].head(10).to_string(index=False))
    
    return top_batters, top_bowlers

if __name__ == '__main__':
    generate_full_rankings()
