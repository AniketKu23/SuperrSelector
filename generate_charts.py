import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

os.makedirs('assets', exist_ok=True)

# Set high-end styling
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#444466'
plt.rcParams['axes.linewidth'] = 0.8

# Primary color palette (Rajasthan Royals & SupeRR Selector inspired)
COLOR_PINK = '#FF1493'      # Royal Rose / Neon Pink
COLOR_BLUE = '#2575FC'      # Deep Royal Blue
COLOR_GOLD = '#FFD700'      # Gold
COLOR_TEAL = '#00F2FE'      # Teal cyan
COLOR_PURPLE = '#6A11CB'    # Purple
COLOR_BG = '#0B0F19'        # Dark slate background
COLOR_CARD = '#161F30'      # Card background

# Load data
top_batters = pd.read_csv('top_batters_pressure.csv')
top_bowlers = pd.read_csv('top_bowlers_pressure.csv')
bbb = pd.read_feather('bbb_enriched.feather')

# -------------------------------------------------------------
# Chart 1: Pressure Validation (Batting Average & Bowling Economy by Tier)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=COLOR_BG)
ax1.set_facecolor(COLOR_CARD)
ax2.set_facecolor(COLOR_CARD)

# Batting data across tiers
tiers = ['Low (<45)', 'Medium (45-65)', 'High (65-80)', 'Extreme (80+)']
bat_avgs = [29.69, 28.23, 27.78, 19.27]
bat_srs = [136.2, 128.0, 139.6, 153.7]

x = np.arange(len(tiers))
width = 0.35

ax1.bar(x - width/2, bat_avgs, width, label='Batting Average', color=COLOR_PINK, alpha=0.9, edgecolor='white', linewidth=0.5)
ax1_twin = ax1.twinx()
ax1_twin.plot(x + width/2, bat_srs, color=COLOR_GOLD, marker='o', linewidth=2.5, markersize=8, label='Strike Rate')

ax1.set_title('Batting Stress: Average Drops as Required SR Soars', fontsize=13, fontweight='bold', pad=15, color='white')
ax1.set_xticks(x)
ax1.set_xticklabels(tiers, fontsize=10, color='#E2E8F0')
ax1.set_ylabel('Batting Average (Runs/Wkt)', color=COLOR_PINK, fontsize=11, fontweight='bold')
ax1_twin.set_ylabel('Strike Rate', color=COLOR_GOLD, fontsize=11, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.2, color='#666688')
ax1_twin.grid(False)

# Bowling data across tiers
bowl_econs = [8.47, 7.97, 8.72, 9.67]
bowl_avgs = [31.04, 29.93, 29.51, 21.18]

ax2.bar(x - width/2, bowl_econs, width, label='Economy Rate', color=COLOR_BLUE, alpha=0.9, edgecolor='white', linewidth=0.5)
ax2_twin = ax2.twinx()
ax2_twin.plot(x + width/2, bowl_avgs, color=COLOR_TEAL, marker='s', linewidth=2.5, markersize=8, label='Bowling Avg')

ax2.set_title('Bowling Crucible: Economy Spikes while Wickets Accelerate', fontsize=13, fontweight='bold', pad=15, color='white')
ax2.set_xticks(x)
ax2.set_xticklabels(tiers, fontsize=10, color='#E2E8F0')
ax2.set_ylabel('Economy Rate (Runs/Over)', color=COLOR_BLUE, fontsize=11, fontweight='bold')
ax2_twin.set_ylabel('Bowling Avg (Runs/Wicket)', color=COLOR_TEAL, fontsize=11, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.2, color='#666688')
ax2_twin.grid(False)

plt.tight_layout()
plt.savefig('assets/pressure_validation.png', dpi=300, facecolor=COLOR_BG)
plt.close()
print("Saved assets/pressure_validation.png")

# -------------------------------------------------------------
# Chart 2: Top 10 Batters Clutch Rating & Delta Strike Rate
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_CARD)

top10_bat = top_batters.head(10).iloc[::-1] # Reverse for bottom-to-top barh
y_pos = np.arange(len(top10_bat))

bars = ax.barh(y_pos, top10_bat['clutch_rating'], height=0.6, color=COLOR_PINK, alpha=0.85, edgecolor=COLOR_GOLD, linewidth=1)

# Annotate with stats
for idx, bar in enumerate(bars):
    row = top10_bat.iloc[idx]
    ax.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height()/2, 
            f"Rating: {row['clutch_rating']:.1f} | Press SR: {row['press_sr']:.1f} (Δ+{row['delta_sr']:.1f}) | {row['press_balls']}b", 
            va='center', ha='left', fontsize=9.5, fontweight='bold', color='#F8FAFC')

ax.set_yticks(y_pos)
ax.set_yticklabels(top10_bat['striker_name'], fontsize=11, fontweight='bold', color='white')
ax.set_xlim(0, 105)
ax.set_xlabel('Clutch Batting Rating (0 - 100)', fontsize=12, fontweight='bold', color='white', labelpad=10)
ax.set_title('Top 10 Most Reliable Batters Under Pressure (SupeRR Selector)', fontsize=14, fontweight='bold', color='white', pad=15)
ax.grid(True, axis='x', linestyle='--', alpha=0.2, color='#8888AA')

plt.tight_layout()
plt.savefig('assets/top10_batters.png', dpi=300, facecolor=COLOR_BG)
plt.close()
print("Saved assets/top10_batters.png")

# -------------------------------------------------------------
# Chart 3: Top 10 Bowlers Clutch Rating & Economy Suppression
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_CARD)

top10_bowl = top_bowlers.head(10).iloc[::-1]
y_pos = np.arange(len(top10_bowl))

bars = ax.barh(y_pos, top10_bowl['clutch_rating'], height=0.6, color=COLOR_BLUE, alpha=0.85, edgecolor=COLOR_TEAL, linewidth=1)

for idx, bar in enumerate(bars):
    row = top10_bowl.iloc[idx]
    delta_str = f"Δ{row['delta_econ']:+.2f}" if row['delta_econ'] != 0 else "0.00"
    ax.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height()/2, 
            f"Rating: {row['clutch_rating']:.1f} | Econ: {row['press_econ']:.2f} ({delta_str}) | {row['press_wickets']} Wkts | {row['press_balls']}b", 
            va='center', ha='left', fontsize=9.5, fontweight='bold', color='#F8FAFC')

ax.set_yticks(y_pos)
ax.set_yticklabels(top10_bowl['bowler_name'], fontsize=11, fontweight='bold', color='white')
ax.set_xlim(0, 105)
ax.set_xlabel('Clutch Bowling Rating (0 - 100)', fontsize=12, fontweight='bold', color='white', labelpad=10)
ax.set_title('Top 10 Most Reliable Bowlers Under Pressure (SupeRR Selector)', fontsize=14, fontweight='bold', color='white', pad=15)
ax.grid(True, axis='x', linestyle='--', alpha=0.2, color='#8888AA')

plt.tight_layout()
plt.savefig('assets/top10_bowlers.png', dpi=300, facecolor=COLOR_BG)
plt.close()
print("Saved assets/top10_bowlers.png")

# -------------------------------------------------------------
# Chart 4: Quadrant Scatter Plot (Batting: SR vs Average under Pressure)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_CARD)

qualified_bat = top_batters[top_batters['press_balls'] >= 45]
scatter = ax.scatter(qualified_bat['press_sr'], qualified_bat['press_avg'], 
                     s=qualified_bat['press_balls']*0.8, c=qualified_bat['clutch_rating'], 
                     cmap='plasma', alpha=0.75, edgecolors='white', linewidth=0.5)

# Highlight Top 10
top10_ids = top_batters.head(10)['striker_id'].tolist()
for _, r in top_batters.head(10).iterrows():
    ax.annotate(r['striker_name'], (r['press_sr'], r['press_avg']),
                xytext=(6, 6), textcoords='offset points', fontsize=9, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.2", fc=COLOR_BG, ec=COLOR_PINK, alpha=0.8))

ax.axvline(qualified_bat['press_sr'].median(), color='#8888AA', linestyle='--', alpha=0.5)
ax.axhline(qualified_bat['press_avg'].median(), color='#8888AA', linestyle='--', alpha=0.5)

ax.set_title('Pressure Batting Matrix: Strike Rate vs Batting Average (Bubble Size = Balls Faced)', fontsize=12, fontweight='bold', color='white', pad=15)
ax.set_xlabel('Pressure Strike Rate', fontsize=11, fontweight='bold', color='white')
ax.set_ylabel('Pressure Batting Average', fontsize=11, fontweight='bold', color='white')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Clutch Batting Rating', color='white', fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.15)

plt.tight_layout()
plt.savefig('assets/batting_matrix.png', dpi=300, facecolor=COLOR_BG)
plt.close()
print("Saved assets/batting_matrix.png")

# -------------------------------------------------------------
# Chart 5: Quadrant Scatter Plot (Bowling: Economy vs Wicket Strike Rate)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7), facecolor=COLOR_BG)
ax.set_facecolor(COLOR_CARD)

qualified_bowl = top_bowlers[top_bowlers['press_balls'] >= 45]
scatter_b = ax.scatter(qualified_bowl['press_econ'], qualified_bowl['press_wicket_sr'], 
                       s=qualified_bowl['press_balls']*0.6, c=qualified_bowl['clutch_rating'], 
                       cmap='viridis', alpha=0.75, edgecolors='white', linewidth=0.5)

# Highlight Top 10
for _, r in top_bowlers.head(10).iterrows():
    ax.annotate(r['bowler_name'], (r['press_econ'], r['press_wicket_sr']),
                xytext=(6, 6), textcoords='offset points', fontsize=9, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.2", fc=COLOR_BG, ec=COLOR_TEAL, alpha=0.8))

ax.set_title('Pressure Bowling Matrix: Economy Rate vs Wicket Strike Rate (Bubble Size = Balls Bowled)', fontsize=12, fontweight='bold', color='white', pad=15)
ax.set_xlabel('Pressure Economy Rate (Runs/Over - Lower is Better)', fontsize=11, fontweight='bold', color='white')
ax.set_ylabel('Pressure Wicket Strike Rate (Balls/Wicket - Lower is Better)', fontsize=11, fontweight='bold', color='white')
ax.invert_xaxis() # Lower economy on right
ax.invert_yaxis() # Lower strike rate on top
cbar_b = plt.colorbar(scatter_b, ax=ax)
cbar_b.set_label('Clutch Bowling Rating', color='white', fontsize=10, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.15)

plt.tight_layout()
plt.savefig('assets/bowling_matrix.png', dpi=300, facecolor=COLOR_BG)
plt.close()
print("Saved assets/bowling_matrix.png")
