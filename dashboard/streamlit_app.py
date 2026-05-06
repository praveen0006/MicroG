"""
🚀 Premium Sales Forecasting Dashboard
Interview-Ready Storytelling UI
"""

import os
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# --- CONFIG & THEME ---
API_URL = os.environ.get("API_URL", "http://localhost:8000")
HTTP_TIMEOUT = float(os.environ.get("HTTP_TIMEOUT", "60"))

st.set_page_config(
    page_title="Sales Forecast Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium "Midnight" Theme (High Contrast)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #0F172A; /* Midnight Blue instead of Black */
        color: #F8FAFC;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 1px solid #334155;
    }
    
    /* Metric Cards - High Visibility */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #38BDF8 !important; /* Sky Blue */
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8 !important;
    }
    
    /* Custom Container for sections */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }
    
    /* Titles */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .section-header {
        color: #F8FAFC;
        font-weight: 700;
        border-left: 4px solid #38BDF8;
        padding-left: 15px;
        margin: 25px 0 15px 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8;
        font-weight: 600;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #38BDF8 !important;
        background-color: #0F172A !important;
        border-radius: 8px;
    }

    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- DEMO DATA ---
DEMO_DATA = {
    "predict": {
        "state": "California", "selected_models": ["xgboost", "prophet"], "ci_method": "conformal",
        "forecast": [{"date": (datetime.now() + pd.Timedelta(weeks=i)).strftime('%Y-%m-%d'), "yhat": 650e6 + (i*10e6), "yhat_lower": 600e6, "yhat_upper": 700e6} for i in range(8)],
        "drift": {"psi": 0.05, "drifted": False}
    },
    "metrics": {
        "states": [{
            "state": "California", "selected_models": ["xgboost", "prophet"], "ensemble_weights": {"xgboost": 0.6, "prophet": 0.4},
            "aggregate_metrics": {
                "xgboost": {"rmse": 19e6, "mae": 15e6, "mape": 9.1},
                "prophet": {"rmse": 21e6, "mae": 17e6, "mape": 9.8},
                "arima": {"rmse": 25e6, "mae": 20e6, "mape": 11.5},
                "lstm": {"rmse": 22e6, "mae": 16e6, "mape": 10.2},
                "sarima": {"rmse": 28e6, "mae": 22e6, "mape": 12.8}
            }
        }]
    }
}

# --- API HELPERS ---
@st.cache_data(ttl=30)
def fetch_health() -> dict:
    try: return requests.get(f"{API_URL}/health", timeout=HTTP_TIMEOUT).json()
    except: return {"status": "offline"}

@st.cache_data(ttl=30)
def fetch_states() -> list[str]:
    try:
        r = requests.get(f"{API_URL}/states", timeout=HTTP_TIMEOUT)
        return r.json().get("states", []) if r.ok else []
    except: return []

@st.cache_data(ttl=30)
def fetch_metrics() -> dict:
    try:
        r = requests.get(f"{API_URL}/metrics", timeout=HTTP_TIMEOUT)
        return r.json() if r.ok else {}
    except: return {}

def fetch_predict(state: str, horizon: int, conformal: bool) -> dict:
    r = requests.get(f"{API_URL}/predict", params={"state": state, "horizon": horizon, "conformal": str(conformal).lower()}, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()

def fetch_breakdown(state: str, horizon: int, conformal: bool) -> dict:
    r = requests.get(f"{API_URL}/predict/breakdown", params={"state": state, "horizon": horizon, "conformal": str(conformal).lower()}, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()

def fetch_backtest(state: str) -> dict:
    r = requests.get(f"{API_URL}/backtest", params={"state": state}, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()

def fetch_holiday(state: str) -> dict:
    r = requests.get(f"{API_URL}/holiday_impact", params={"state": state}, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h2 style="color: white; margin-bottom: 0;">🔮 Sales Pro</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #38BDF8; font-weight: 600;">Enterprise Forecasting Platform</p>', unsafe_allow_html=True)
    st.divider()
    
    # API Health
    health = fetch_health()
    if health["status"] == "ok":
        st.success(f"API Online | v`{health.get('registry_version', '—')[:8]}`")
    else:
        st.error("API Offline")
    
    demo_mode = st.toggle("🎯 Demo Mode (Offline)", value=False, help="Show sample data without backend connection")
    
    st.markdown("### Controls")
    states = fetch_states()
    if demo_mode:
        state = "California"
        st.info("Demo: California selected")
    elif not states:
        st.warning("No states found. Run training first.")
        state = None
    else:
        state = st.selectbox("Select State", states, index=0)
    
    horizon = st.slider("Horizon (weeks)", 1, 24, 8)
    use_conformal = st.toggle("Conformal Intervals", value=True)
    
    st.divider()
    st.caption(f"Refreshed: {datetime.now().strftime('%H:%M:%S')}")

# --- MAIN APP ---
if not state and not demo_mode:
    st.title("Welcome to Sales Forecast Pro")
    st.info("Please start the API and train at least one state to begin, or enable 'Demo Mode' in the sidebar.")
    st.stop()

tab_ov, tab_fc, tab_comp, tab_bt, tab_hol, tab_all = st.tabs([
    "🏠 Overview", "📈 Forecast", "🤖 Models", "🔁 Backtest", "🎉 Holidays", "📊 National"
])

# 1. OVERVIEW
with tab_ov:
    st.markdown('<p class="hero-title">Forecasting Intelligence</p>', unsafe_allow_html=True)
    st.markdown("##### Production-Grade End-to-End Pipeline")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("DATASET", "43 States", "5 Years")
    m2.metric("ALGORITHMS", "5 Models", "Ensemble")
    m3.metric("DEPLOYMENT", "FastAPI", "Docker")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🧱 System Architecture
    This system is designed as a modular **microservice** for large-scale retail forecasting.
    
    - **Engineering**: Irregular weekly data is resampled and imputed using a hybrid linear/forward-fill strategy.
    - **Models**: We benchmark **ARIMA, SARIMA, Prophet, XGBoost, and PyTorch LSTM** for every state.
    - **Validation**: Strict **Walk-Forward Cross-Validation** ensures zero data leakage.
    - **Ensemble**: A dynamic Top-2 ensemble is selected per state based on historical accuracy.
    - **Safety**: **Conformal Prediction Intervals** and **Drift Detection** ensure reliability in production.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. FORECAST
with tab_fc:
    st.markdown(f'<h3 class="section-header">{state} — 8-Week Prediction</h3>', unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading intelligence..."):
            pred = DEMO_DATA["predict"] if demo_mode else fetch_predict(state, horizon, use_conformal)
            df = pd.DataFrame(pred["forecast"])
            df["date"] = pd.to_datetime(df["date"])
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Selected", ", ".join(pred["selected_models"]))
            c2.metric("CI Method", pred.get("ci_method", "Native"))
            c3.metric("Avg Forecast", f"${df['yhat'].mean()/1e6:.1f}M")
            c4.metric("Total Sales", f"${df['yhat'].sum()/1e6:.1f}M")
            
            # Status Banner
            drift = pred.get("drift", {})
            if drift.get("drifted"):
                st.warning(f"⚠️ MODEL DRIFT: PSI {drift.get('psi'):.2f} exceeds threshold.")
            else:
                st.info("✅ STABLE: No distribution shift detected.")

            fig = go.Figure()
            if use_conformal and "yhat_upper" in df.columns:
                fig.add_trace(go.Scatter(
                    x=df["date"].tolist() + df["date"].tolist()[::-1],
                    y=df["yhat_upper"].tolist() + df["yhat_lower"].tolist()[::-1],
                    fill='toself', fillcolor='rgba(56,189,248,0.1)',
                    line=dict(color='rgba(255,255,255,0)'), name="Prediction Interval"
                ))
            
            fig.add_trace(go.Scatter(
                x=df["date"], y=df["yhat"],
                mode='lines+markers', line=dict(color='#38BDF8', width=4),
                marker=dict(size=10, line=dict(color="white", width=2)),
                name="Forecast"
            ))
            
            fig.update_layout(
                template="plotly_dark", height=500, margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(30,41,59,0.5)',
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#334155')
            )
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Prediction unavailable: {e}")

# 3. MODELS
with tab_comp:
    st.markdown('<h3 class="section-header">Performance Benchmark</h3>', unsafe_allow_html=True)
    
    try:
        metrics_data = DEMO_DATA["metrics"] if demo_mode else fetch_metrics()
        state_metrics = next((s for s in metrics_data.get("states", []) if s["state"] == state), None)
        
        if state_metrics:
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                st.write("**Weight Distribution**")
                w = state_metrics["ensemble_weights"]
                fig_w = px.pie(values=list(w.values()), names=list(w.keys()), hole=0.7,
                               color_discrete_sequence=['#38BDF8', '#818CF8', '#34D399'])
                fig_w.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_w, use_container_width=True)
            
            with col_b:
                st.write("**Accuracy (RMSE)**")
                agg = state_metrics["aggregate_metrics"]
                m_df = pd.DataFrame(agg).T.reset_index().rename(columns={"index": "model"}).sort_values("rmse")
                fig_m = px.bar(m_df, x="model", y="rmse", color="rmse", color_continuous_scale="Blues")
                fig_m.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                    coloraxis_showscale=False)
                st.plotly_chart(fig_m, use_container_width=True)
                
            st.dataframe(m_df.style.format({"rmse": "{:,.0f}", "mae": "{:,.0f}", "mape": "{:.1f}%"}), use_container_width=True)
        else:
            st.info("No metrics for this state. Ensure training is complete.")
    except Exception as e:
        st.error(f"Metrics error: {e}")

# 4. BACKTEST
with tab_bt:
    st.markdown('<h3 class="section-header">Backtest History</h3>', unsafe_allow_html=True)
    try:
        bt = fetch_backtest(state)
        df_bt = pd.DataFrame(bt["rows"])
        df_bt["date"] = pd.to_datetime(df_bt["date"])
        
        fig_bt = go.Figure()
        fig_bt.add_trace(go.Scatter(x=df_bt["date"], y=df_bt["y_true"], name="Realized Sales", line=dict(color="#F8FAFC", width=3)))
        for col in [c for c in df_bt.columns if c not in ["date", "y_true"]]:
            fig_bt.add_trace(go.Scatter(x=df_bt["date"], y=df_bt[col], name=col, line=dict(dash='dot', width=1)))
            
        fig_bt.update_layout(template="plotly_dark", height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(30,41,59,0.3)')
        st.plotly_chart(fig_bt, use_container_width=True)
    except:
        st.info("Historical backtest data not available.")

# 5. HOLIDAYS
with tab_hol:
    st.markdown('<h3 class="section-header">Seasonal Lift Factors</h3>', unsafe_allow_html=True)
    try:
        h = fetch_holiday(state)
        h1, h2, h3 = st.columns(3)
        h1.metric("Non-Holiday", f"${h['non_holiday_avg']/1e6:.1f}M")
        h2.metric("Holiday Week", f"${h['holiday_avg']/1e6:.1f}M")
        h3.metric("Average Lift", f"{h['holiday_lift_pct']:.1f}%")
        
        per = h.get("per_holiday", {})
        if per:
            h_df = pd.DataFrame(per).T.reset_index().rename(columns={"index": "holiday"}).sort_values("lift_vs_non_holiday_pct")
            fig_h = px.bar(h_df, x="holiday", y="lift_vs_non_holiday_pct", color="lift_vs_non_holiday_pct", 
                           color_continuous_scale="Tealgrn")
            fig_h.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
            st.plotly_chart(fig_h, use_container_width=True)
    except:
        st.info("Holiday seasonality analysis not available for this state.")

# 6. NATIONAL
with tab_all:
    st.markdown('<h3 class="section-header">National Performance Map</h3>', unsafe_allow_html=True)
    try:
        all_metrics = DEMO_DATA["metrics"] if demo_mode else fetch_metrics()
        if all_metrics.get("states"):
            national_df = pd.DataFrame([
                {"state": s["state"], "model": m, **v} 
                for s in all_metrics["states"] 
                for m, v in s["aggregate_metrics"].items()
            ])
            
            fig_box = px.box(national_df, x="model", y="rmse", points="all", color="model",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_box.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)
            
            pivot = national_df.pivot(index="state", columns="model", values="rmse")
            st.dataframe(pivot.style.format("{:,.0f}").highlight_min(axis=1, color="#1E293B"), use_container_width=True)
    except:
        st.info("Aggregated national metrics not yet available.")

st.markdown("---")
st.markdown('<p style="text-align: center; color: #64748B; font-size: 0.8rem;">Sales Forecast Pro | Powered by XGBoost, PyTorch & Prophet | 2026</p>', unsafe_allow_html=True)
