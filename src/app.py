import streamlit as st
import os
import streamlit.components.v1 as components
# We import the prediction logic directly from your api.py file
from api import predict_internal 

st.set_page_config(
    page_title="Walmart Strategic Analytics",
    page_icon="🛒",
    layout="wide"
)

# --- TRUE ADAPTIVE EDGE-TO-EDGE UI ---
st.markdown("""
    <style>
    :root {
        --bg-1: #080c16;
        --bg-2: #111a2f;
        --panel: rgba(24, 31, 46, 0.82);
        --panel-border: #2f3c52;
        --brand: #0071ce;
        --brand-hover: #005fa3;
        --muted: #9aa9bc;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(0, 113, 206, 0.18), transparent 34%),
            radial-gradient(circle at 86% 16%, rgba(0, 181, 255, 0.12), transparent 30%),
            linear-gradient(120deg, var(--bg-1) 0%, var(--bg-2) 100%);
    }

    .main .block-container {
        width: min(1700px, 96vw) !important;
        max-width: min(1700px, 96vw) !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
        padding-right: clamp(0.9rem, 2.6vw, 2.2rem) !important;
        padding-left: clamp(0.9rem, 2.6vw, 2.2rem) !important;
        padding-bottom: 2rem !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(17, 24, 39, 0.84);
        padding: 10px;
        border-radius: 12px;
        border: 1px solid var(--panel-border);
        margin-bottom: 25px;
        width: 100%;
        max-width: 700px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        border-radius: 8px;
        color: var(--muted);
        border: none;
        padding: 0px clamp(14px, 2.2vw, 30px);
        font-size: clamp(14px, 1.3vw, 16px);
        flex: 1;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--brand) !important;
        color: white !important;
        font-weight: bold;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.stForm) {
        background-color: var(--panel);
        padding: clamp(1rem, 2.8vw, 2.5rem);
        border-radius: 15px;
        border: 1px solid var(--panel-border);
        width: 100%;
        backdrop-filter: blur(6px);
    }

    .prediction-card {
        background-color: rgba(16, 23, 35, 0.9);
        padding: clamp(22px, 3vw, 40px);
        border-radius: 15px;
        border: 1px solid var(--brand);
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .tech-card {
        background-color: rgba(16, 23, 35, 0.9);
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid var(--brand);
        height: 100%;
        margin-bottom: 20px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: var(--brand);
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: var(--brand-hover);
        transform: translateY(-2px);
    }

    @media (max-width: 1024px) {
        .main .block-container {
            width: min(100%, 98vw) !important;
            max-width: min(100%, 98vw) !important;
            padding-top: 0.7rem !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            max-width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

TYPE_MAP = {"Type A": "A", "Type B": "B", "Type C": "C"}

tab1, tab2 = st.tabs(["📊 Operational Forecast", "📉 Model Intelligence"])

# ==========================================
# TAB 1 → PREDICTION
# ==========================================
with tab1:
    st.title("Weekly Sales Forecasting Terminal")
    st.markdown("##### Strategic revenue projection with automated feature encoding.")
    st.markdown("<div id='results-top'></div>", unsafe_allow_html=True)
    
    col_input, col_display = st.columns([1, 1], gap="large")

    with col_input:
        with st.form("prediction_form", border=False):
            st.subheader("Input Parameters")
            
            store = st.slider("Store ID", 1, 45, 1)
            dept = st.slider("Department ID", 1, 99, 1)
            week = st.slider("Fiscal Week", 1, 52, 1)
            
            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                size = st.number_input("Store Size (sq ft)", min_value=1, value=150000, step=1000)
                selected_type_label = st.selectbox("Store Classification", list(TYPE_MAP.keys()))
            
            with c2:
                unemployment = st.number_input("Unemployment Rate (%)", min_value=0.0, max_value=20.0, value=7.0, format="%.2f")
                cpi = st.number_input("Consumer Price Index (CPI)", min_value=0.0, value=215.0, format="%.2f")

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Execute Analysis")

    with col_display:
        if submit:
            encoded_type = TYPE_MAP[selected_type_label]
            payload = {
                "Dept": dept, "Size": size, "Store": store, 
                "CPI": cpi, "Week": week, "Unemployment": unemployment, 
                "Type": encoded_type
            }

            with st.spinner("Processing Model Logic..."):
                try:
                    # DIRECT CALL to the api.py function (No request needed)
                    prediction = predict_internal(payload)

                    st.markdown(f"""
                        <div class="prediction-card">
                            <p style='color: #8b949e; text-transform: uppercase; letter-spacing: 2px;'>Forecasted Weekly Sales</p>
                            <h1 style='color: #00b5ff; font-size: clamp(30px, 5vw, 60px);'>${prediction:,.2f}</h1>
                            <p style='color: #3dd56d; font-weight: 500;'>✔ Prediction successful for {selected_type_label}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.table({
                        "Parameters": ["Location", "Timeframe", "Classification", "Economic Info"],
                        "Input Values": [f"Store {store}, Dept {dept}", f"Week {week}", selected_type_label, f"CPI: {cpi} | Unemp: {unemployment}%"]
                    })
                    
                    components.html(
                        """
                        <script>
                            const parentDoc = window.parent.document;
                            const target = parentDoc.querySelector('#results-top');
                            if (target) {
                                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        </script>
                        """,
                        height=0,
                    )
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
        else:
            st.info("Awaiting execution parameters. Adjust sliders and numeric inputs above.")

# ==========================================
# TAB 2 → MODEL INTELLIGENCE
# ==========================================
with tab2:
    st.title("Model Intelligence & Architecture")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MAE", "1,781.82", help="Mean Absolute Error")
    m2.metric("RMSE", "3,732.26", help="Root Mean Square Error")
    m3.metric("R² Score", "0.9711", help="Explained Variance")
    m4.metric("Algorithm", "Random Forest")

    st.divider()

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.markdown("""
        <div class="tech-card">
            <h3>How Random Forest Works 🌲</h3>
            <p>Random Forest is an <b>Ensemble Learning</b> method that constructs multiple decision trees during training. 
            It merges their outputs to get a more accurate and stable prediction.</p>
            <ul>
                <li><b>Bagging:</b> Trains each tree on a random subset of data.</li>
                <li><b>Feature Randomness:</b> Selects random features for each split.</li>
                <li><b>Voting:</b> Averages the results of all trees to reduce <i>overfitting</i>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="tech-card">
            <h3>Why Use Random Forest for Sales?</h3>
            <p>Sales data is often <b>non-linear</b> and influenced by outliers. Random Forest excels because:</p>
            <ul>
                <li><b>Handles Seasonality:</b> Captures interactions between 'Week' and 'Store Type'.</li>
                <li><b>Non-Parametric:</b> Doesn't assume a normal distribution of revenue.</li>
                <li><b>Robustness:</b> Less sensitive to noise in economic indicators.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Optimal Use Cases")
    st.info("""
    **1. Demand Planning:** Predicting inventory needs for specific departments.  
    **2. Dynamic Resource Allocation:** Identifying which store types react strongly to economic shifts.  
    **3. Anomaly Detection:** Flagging weeks where actual sales deviate from the forecast.
    """)

st.markdown("<br><hr><center><small>Walmart Sales Analytics Engine | Proprietary Model v2.3</small></center>", unsafe_allow_html=True)