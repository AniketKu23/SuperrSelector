import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="SupeRR Selector Season 2 - Clutch Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sports analytics styling
st.markdown("""
<style>
    .reportview-container {
        background: #0B0F19;
    }
    .main {
        background: #0B0F19;
        color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 700;
    }
    .stMetric {
        background-color: #161F30;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #FF1493;
    }
    div[data-testid="stExpander"] {
        background-color: #161F30;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Resolve paths robustly whether executed from root or streamlit_app/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR) == 'streamlit_app' else CURRENT_DIR

def get_path(rel_path):
    p1 = os.path.join(ROOT_DIR, rel_path)
    if os.path.exists(p1):
        return p1
    p2 = os.path.join(CURRENT_DIR, rel_path)
    if os.path.exists(p2):
        return p2
    return rel_path

# Load data
@st.cache_data
def load_data():
    top_bat = pd.read_csv(get_path('top_batters_pressure.csv'))
    top_bowl = pd.read_csv(get_path('top_bowlers_pressure.csv'))
    return top_bat, top_bowl

top_batters, top_bowlers = load_data()

# Header
st.title("🏏 SupeRR Selector Season 2: Clutch Performance Engine")
st.markdown("### Identify the Most Reliable Players Under Pressure | Empirical Bayesian Hybrid Model")
st.markdown("**Author:** Aniket Kumar (Email: [kkaniket23@gamil.com](mailto:kkaniket23@gamil.com))  \nOfficial Rajasthan Royals Scouting Dossier & Decision Dashboard (2022–2026 IPL & T20I Dataset)")

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Deliveries Analyzed", "200,999", "883 Matches")
col2.metric("High-Pressure Deliveries", "94,841", "47.2% of dataset")
col3.metric("Win Prob Model AUC", "0.890", "Brier: 0.134")
col4.metric("#1 Clutch Batter", "Rinku Singh", "Rating: 77.1")
col5.metric("#1 Clutch Bowler", "M. Pathirana", "Rating: 79.7")

st.markdown("---")

# Sidebar Controls
st.sidebar.image(get_path("assets/top10_batters.png"), use_container_width=True)
st.sidebar.header("🔍 Selector Controls")
min_pressure_balls = st.sidebar.slider("Minimum High-Pressure Balls", 30, 150, 45, 5)
competition_scope = st.sidebar.selectbox("Competition Scope", ["All Competitions (IPL & T20I)", "IPL Only", "T20I Only"])
player_search = st.sidebar.text_input("Search Player Name", "")

# Filter data
filtered_bat = top_batters[top_batters['press_balls'] >= min_pressure_balls]
filtered_bowl = top_bowlers[top_bowlers['press_balls'] >= min_pressure_balls]

if player_search:
    filtered_bat = filtered_bat[filtered_bat['striker_name'].str.contains(player_search, case=False, na=False)]
    filtered_bowl = filtered_bowl[filtered_bowl['bowler_name'].str.contains(player_search, case=False, na=False)]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏏 Top 10 Batters Under Pressure", "🎯 Top 10 Bowlers Under Pressure", "⚡ Match Crunch Simulator", "📐 Methodology & Charts"])

with tab1:
    st.subheader("Top 10 Most Reliable Batters Under Pressure")
    st.markdown("Ranked by **Clutch Batting Rating (CBR)**: combining shrunk pressure strike rate, batting average, positive elevation over baseline ($\Delta$ SR), boundary %, and WPA.")
    
    top10_bat = filtered_bat.head(10)[['rank', 'striker_id', 'striker_name', 'press_balls', 'press_sr', 'press_avg', 'delta_sr', 'press_boundary_pct', 'press_wpa', 'clutch_rating']]
    st.dataframe(
        top10_bat.style.format({
            'press_sr': '{:.1f}',
            'press_avg': '{:.1f}',
            'delta_sr': '{:+.1f}',
            'press_boundary_pct': '{:.1f}%',
            'press_wpa': '{:+.2f}',
            'clutch_rating': '{:.1f}'
        }).background_gradient(subset=['clutch_rating'], cmap='Blues'),
        use_container_width=True
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.image(get_path("assets/top10_batters.png"), caption="Top 10 Batters Clutch Rating Breakdown", use_container_width=True)
    with col_b:
        st.image(get_path("assets/batting_matrix.png"), caption="Pressure Batting Matrix (SR vs Average)", use_container_width=True)

with tab2:
    st.subheader("Top 10 Most Reliable Bowlers Under Pressure")
    st.markdown("Ranked by **Clutch Bowling Rating (CBR)**: combining shrunk pressure economy suppression, wicket strike rate, dot ball %, boundary prevention, and bowling WPA.")
    
    top10_bowl = filtered_bowl.head(10)[['rank', 'bowler_id', 'bowler_name', 'press_balls', 'press_econ', 'press_wickets', 'delta_econ', 'press_dot_pct', 'press_wpa', 'clutch_rating']]
    st.dataframe(
        top10_bowl.style.format({
            'press_econ': '{:.2f}',
            'delta_econ': '{:+.2f}',
            'press_dot_pct': '{:.1f}%',
            'press_wpa': '{:+.2f}',
            'clutch_rating': '{:.1f}'
        }).background_gradient(subset=['clutch_rating'], cmap='Purples'),
        use_container_width=True
    )
    
    col_c, col_d = st.columns(2)
    with col_c:
        st.image(get_path("assets/top10_bowlers.png"), caption="Top 10 Bowlers Clutch Rating Breakdown", use_container_width=True)
    with col_d:
        st.image(get_path("assets/bowling_matrix.png"), caption="Pressure Bowling Matrix (Economy vs Wicket Strike Rate)", use_container_width=True)

with tab3:
    st.subheader("⚡ Live Match Situation Crunch Simulator")
    st.markdown("Test the analytical engine against any custom match situation.")
    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    with sim_col1:
        inn = st.selectbox("Innings", [2, 1], format_func=lambda x: "2nd Innings (The Chase)" if x == 2 else "1st Innings (Setting Target)")
        target = st.number_input("Target / Score", min_value=50, max_value=280, value=185)
    with sim_col2:
        score = st.number_input("Current Runs Scored", min_value=0, max_value=280, value=145)
        balls_rem = st.number_input("Balls Remaining", min_value=1, max_value=120, value=18)
    with sim_col3:
        wkts_down = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=5)
        stage = st.selectbox("Match Stage", ["League Match", "Knockout / Playoff Final (1.20x)", "IPL Match (1.10x)"])
        
    needed = max(0, target - score)
    rrr = (needed / balls_rem) * 6 if balls_rem > 0 else 0
    w_in_hand = max(1, 10 - wkts_down)
    
    if inn == 2:
        rrr_stress = 50.0 + (rrr - 8.5) * 7.5
        w_factor = 1.0 + (6 - w_in_hand) * 0.12 if w_in_hand <= 5 else 1.0
        phase = (30 - balls_rem) * 0.8 if balls_rem <= 30 else 0
        p_score = (rrr_stress * w_factor) + phase
        
        z = -0.0174 * needed - 0.0156 * balls_rem + 0.658 * w_in_hand - 0.363 * rrr
        wp = 1.0 / (1.0 + np.exp(-z)) * 100.0
    else:
        p_score = 38.0 + (25.0 if wkts_down >= 4 else 0) + (30.0 if balls_rem <= 30 else 0)
        wp = 50.0 + (score - (120 - balls_rem) * 1.4) * 0.5
        
    if "Knockout" in stage:
        p_score *= 1.20
    elif "IPL" in stage:
        p_score *= 1.10
        
    p_score = float(np.clip(p_score, 5.0, 100.0))
    wp = float(np.clip(wp, 0.5, 99.5))
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Situational Pressure Score", f"{p_score:.1f} / 100", "Extreme Crunch" if p_score >= 80 else ("High Pressure" if p_score >= 60 else "Moderate"))
    res_col2.metric("Chasing Win Probability", f"{wp:.1f}%", f"{needed} runs required from {balls_rem} balls")
    res_col3.metric("Required Run Rate", f"{rrr:.2f} RPO", f"Wickets in hand: {w_in_hand}")
    
    st.info(f"💡 **Tactical Recommendation**: In this scenario, Rajasthan Royals should deploy **Rinku Singh** or **Tristan Stubbs** to chase, and bowl **Matheesha Pathirana** or **Jasprit Bumrah** to defend.")

with tab4:
    st.subheader("Methodology, Population Stress Validation & Reproducibility")
    st.image(get_path("assets/pressure_validation.png"), caption="Empirical Validation: Batting Average plunges 35% in extreme pressure as bowling economy spikes", use_container_width=True)
    
    st.markdown("""
    ### Unstop Dropdown Verification & Selection
    Please ensure the Unstop dropdown selections match the exact names and IDs below:
    
    | Rank | Best-Performing Batters (Unstop) | Best-Performing Bowlers (Unstop) |
    | :--- | :--- | :--- |
    | **Rank 1** | **Rinku Singh** (ID: 4708) | **Matheesha Pathirana** (ID: 8661) |
    | **Rank 2** | **Suryakumar Yadav** (ID: 1699) | **Abrar Ahmed** (ID: 5979) |
    | **Rank 3** | **Tristan Stubbs** (ID: 20702) | **Mohammad Nawaz** (ID: 2490) |
    | **Rank 4** | **Namboori Tilak Varma** (ID: 7897) | **Jasprit Bumrah** (ID: 2933) |
    | **Rank 5** | **Tim David** (ID: 6396) | **Sunil Narine** (ID: 781) |
    | **Rank 6** | **David Miller** (ID: 1077) | **Sufiyan Muqeem** (ID: 34485) |
    | **Rank 7** | **Shashank Singh** (ID: 2756) | **Eshan Malinga** (ID: 39657) |
    | **Rank 8** | **Dinesh Karthik** (ID: 143) | **Mitchell Santner** (ID: 4101) |
    | **Rank 9** | **Nicholas Pooran** (ID: 3125) | **Arshdeep Singh** (ID: 6464) |
    | **Rank 10** | **Marcus Stoinis** (ID: 2639) | **Akeal Hosein** (ID: 2417) |
    
    ---
    *Developed by **Aniket Kumar** (Email: [kkaniket23@gamil.com](mailto:kkaniket23@gamil.com)) for Rajasthan Royals SupeRR Selector Season 2.*
    """)
