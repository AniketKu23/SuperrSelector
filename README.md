# 🏏 SupeRR Selector Season 2: Identifying the Most Reliable Players Under Pressure

[![Rajasthan Royals](https://img.shields.io/badge/Rajasthan_Royals-SupeRR_Selector_S2-FF1493?style=for-the-badge&logo=cricket)](https://www.rajasthanroyals.com/)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel)](https://vercel.com)
[![Python 3.11](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Author](https://img.shields.io/badge/Author-Aniket_Kumar-2575FC?style=for-the-badge)](mailto:kkaniket23@gamil.com)

**Lead Analyst & Author:** Aniket Kumar  
**Email:** [kkaniket23@gamil.com](mailto:kkaniket23@gamil.com)  
**Competition:** SupeRR Selector Season 2 (Round 1 Problem Statement)  
**Organization:** Rajasthan Royals Analytics & Scouting Division  
**Dataset Scope:** 2022–2026 IPL & T20 Internationals (200,999 Deliveries Across 883 Matches)

---

## ⚡ Live Interactive Dashboard on Vercel

The live, interactive analytics dashboard with real-time match crunch simulation is hosted on Vercel:
> 🔗 **Live Dashboard:** [Deploy to Vercel in 1-Click](#-deploying-to-vercel) or open [`index.html`](index.html) locally.

---

## 📋 Official Unstop Submission Rankings (Dropdown Ready)

These rankings are strictly backed by historical ball-by-ball analysis, sample size qualification ($\ge 120$ total balls, $\ge 45$ pressure balls, $\ge 8$ matches), and empirical Bayesian shrinkage. Unstop Player IDs match [`competition_team_player_mapping.csv`](Data%20Pack/competition_team_player_mapping.csv).

### 🏏 Top 10 Batters Under Pressure
| Rank | Player Name | Unstop ID | Pressure Balls | Press SR | Base SR | Δ Strike Rate | Press Avg | Press WPA | Clutch Batting Rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rank 1** | **Rinku Singh** | `4708` | 459 | 194.8 | 152.7 | **+42.1** | 29.8 | **+3.77** | **77.1** |
| **Rank 2** | **Suryakumar Yadav** | `1699` | 430 | 202.1 | 166.4 | **+35.7** | 31.0 | **+2.04** | **77.1** |
| **Rank 3** | **Tristan Stubbs** | `20702` | 392 | 196.7 | 149.9 | **+46.8** | 33.5 | **+1.59** | **75.2** |
| **Rank 4** | **Namboori Tilak Varma** | `7897` | 561 | 187.7 | 143.0 | **+44.7** | 31.0 | -0.30 | **74.9** |
| **Rank 5** | **Tim David** | `6396` | 476 | 202.3 | 177.7 | **+24.7** | 31.1 | **+3.27** | **74.5** |
| **Rank 6** | **David Miller** | `1077` | 571 | 178.6 | 149.3 | **+29.3** | 31.9 | **+1.05** | **70.9** |
| **Rank 7** | **Shashank Singh** | `2756` | 288 | 184.4 | 161.6 | **+22.8** | 48.3 | **+0.89** | **70.2** |
| **Rank 8** | **Dinesh Karthik** | `143` | 354 | 200.6 | 167.3 | **+33.3** | 24.5 | -0.75 | **68.1** |
| **Rank 9** | **Nicholas Pooran** | `3125` | 405 | 192.3 | 157.0 | **+35.3** | 22.3 | -0.09 | **67.2** |
| **Rank 10** | **Marcus Stoinis** | `2639` | 394 | 193.7 | 153.6 | **+40.1** | 25.4 | -1.60 | **66.3** |

---

### 🎯 Top 10 Bowlers Under Pressure
| Rank | Player Name | Unstop ID | Pressure Balls | Press Econ | Base Econ | Δ Economy | Wickets | Press WPA | Clutch Bowling Rating |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rank 1** | **Matheesha Pathirana** | `8661` | 490 | 7.54 | 7.80 | **+0.25** | 53 | **+3.77** | **79.7** |
| **Rank 2** | **Abrar Ahmed** | `5979` | 138 | 4.65 | 6.57 | **+1.91** | 15 | **+1.05** | **77.3** |
| **Rank 3** | **Mohammad Nawaz** | `2490` | 120 | 4.75 | 7.04 | **+2.29** | 19 | **+0.97** | **77.0** |
| **Rank 4** | **Jasprit Bumrah** | `2933` | 507 | 7.14 | 6.85 | -0.28 | 46 | **+1.67** | **76.3** |
| **Rank 5** | **Sunil Narine** | `781` | 274 | 6.74 | 6.76 | **+0.01** | 27 | **+2.63** | **74.3** |
| **Rank 6** | **Sufiyan Muqeem** | `34485` | 136 | 5.74 | 5.92 | **+0.18** | 15 | **+0.63** | **71.5** |
| **Rank 7** | **Eshan Malinga** | `39657` | 289 | 7.95 | 8.59 | **+0.64** | 26 | **+1.68** | **70.7** |
| **Rank 8** | **Mitchell Santner** | `4101` | 253 | 6.90 | 7.20 | **+0.30** | 22 | **+1.22** | **70.6** |
| **Rank 9** | **Arshdeep Singh** | `6464` | 997 | 9.19 | 8.61 | -0.58 | 93 | **+8.48** | **70.2** |
| **Rank 10** | **Akeal Hosein** | `2417` | 101 | 5.23 | 7.53 | **+2.30** | 17 | **+1.53** | **70.1** |

---

## 📐 Analytical & Mathematical Framework

### 1. The Pressure Index (CPI)
Pressure is modeled as a continuous function on $[0, 100]$:
- **Innings 2 (The Chase):**
  $$\text{RRR Stress} = 50.0 + (\text{RRR} - 8.5) \times 7.5$$
  $$\text{Wicket Scarcity Factor} = 1.0 + \max(0, (6 - \text{Wickets in Hand}) \times 0.12)$$
  $$\text{Phase Stress} = \max(0, (30 - \text{Balls Remaining}) \times 0.80)$$
  $$\text{Closeness Multiplier} = +25.0 \quad (\text{if Runs Needed} \le 15 \text{ and Balls} \le 12)$$
- **Super Overs:** $100.0$ (maximum strain by definition).
- **Match Multipliers:** Knockouts ($1.20\times$), Tier-1 IPL / Top-8 International ($1.15\times$).

### 2. Logistic Win Expectancy (AUC: 0.8904)
Trained on 200,999 match states using Logistic Expectancy:
$$\text{Logit}(WP) = -0.0174 \cdot \text{RunsNeeded} - 0.0156 \cdot \text{BallsRem} + 0.6584 \cdot \text{WicketsInHand} - 0.3632 \cdot \text{RRR}$$
Leverage Index and Win Probability Added ($\text{WPA}$) are merged into:
$$\text{Hybrid Pressure Index (HPI)} = 0.70 \times \text{CPI} + 0.30 \times \text{LeverageScore}$$

### 3. Empirical Bayes Shrinkage
To prevent small-sample distortions ($N < 45$ balls), observed performance $\theta_{\text{sample}}$ is regressed toward the population mean $\mu_{\text{pop}}$ ($K=40$):
$$\hat{\theta}_{\text{adj}} = \frac{N \cdot \theta_{\text{sample}} + K \cdot \mu_{\text{pop}}}{N + K}$$

---

## 🚀 Deploying to Vercel

The root of this repository is configured strictly as a **Static Web Project** (`index.html` + `vercel.json`).

### Direct GitHub Import
1. Push this repository to your GitHub account:
   ```bash
   git add .
   git commit -m "Update Vercel static deployment"
   git push
   ```
2. In [Vercel](https://vercel.com/new), import your repository.
3. Keep the Framework Preset as **Other** (Static).
4. Click **Deploy**. Vercel will publish your dashboard to global CDN in seconds with zero build errors!

---

## 💻 Local Development & Usage

### 1. View the Web Dashboard locally
Double-click [`index.html`](index.html) or run:
```bash
npx serve .
```

### 2. Run the Interactive Streamlit Dashboard Locally
```bash
pip install -r scripts/requirements.txt
streamlit run scripts/app.py
```

### 3. Re-run Pipeline or Rebuild PDF Report
```bash
# Recompute ratings from raw data
python scripts/compute_rankings.py

# Generate visualization assets
python scripts/generate_charts.py

# Rebuild publication-grade PDF report
python scripts/generate_pdf_report.py
```

---

## 📁 Repository Structure

```
├── index.html                   # Vercel entry point (Interactive Web Dashboard)
├── dashboard.html               # Portable mirror of dashboard
├── vercel.json                  # Vercel configuration (cleanUrls, rewrites, headers)
├── .vercelignore                # Directs Vercel to ignore python files
├── .gitignore                   # Clean Git tracking configuration
├── SupeRR_Selector_Season_2_Methodology_Report.pdf  # Formal 6-Page PDF Submission
├── top_batters_pressure.csv     # Enriched batter ratings output
├── top_bowlers_pressure.csv     # Enriched bowler ratings output
├── report_screenshots/          # 6 HD screenshots of the PDF methodology report
├── assets/                      # HD dashboard screenshots and chart figures
└── scripts/                     # Python modeling, analytics & Streamlit scripts
    ├── requirements.txt         # Python dependencies
    ├── app.py                   # Local interactive Streamlit web application
    ├── compute_rankings.py      # Core modeling, win probability & shrinkage engine
    ├── build_model.py           # Feature extraction & situation parser
    ├── generate_charts.py       # Visualization generator
    ├── generate_pdf_report.py   # ReportLab PDF compilation script
    └── render_pdf_pages.py      # High-resolution PDF-to-PNG renderer
```

---

## 👤 Author Contact
**Aniket Kumar**  
- **Email:** [kkaniket23@gamil.com](mailto:kkaniket23@gamil.com)  
- **Hackathon:** Rajasthan Royals SupeRR Selector Season 2 (Round 1)
