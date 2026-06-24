import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DotMappers · Ticket Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "raw_result" not in st.session_state:
    st.session_state.raw_result = ""

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

/* ── Base ── */
.stApp {
    background-color: #F7F7F7;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 100% !important;
    padding: 2rem 3rem 2rem 3rem !important;
}

/* ── Header ── */
.page-title {
    font-size: 20px;
    font-weight: 600;
    color: #111111;
    letter-spacing: -0.2px;
    margin-bottom: 2px;
}
.page-sub {
    font-size: 13px;
    color: #AAAAAA;
    font-weight: 400;
    margin-bottom: 20px;
}

/* ── Column label ── */
.col-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #CCCCCC;
    margin-bottom: 12px;
}

/* ── Status line ── */
.status-line {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 13px;
    color: #333333;
    font-weight: 500;
    margin-bottom: 18px;
}
.dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
    display: inline-block;
}
.dot-green { background: #22C55E; }
.dot-red   { background: #EF4444; }

/* ── Metric block ── */
.metric-block {
    padding: 14px 0;
    border-top: 1px solid #E8E8E8;
}
.metric-block.last {
    border-bottom: 1px solid #E8E8E8;
}
.metric-num {
    font-size: 30px;
    font-weight: 700;
    color: #111111;
    line-height: 1;
    letter-spacing: -0.5px;
}
.metric-lbl {
    font-size: 11.5px;
    color: #AAAAAA;
    margin-top: 3px;
}

/* ── Answer panel ── */
.answer-panel {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-radius: 8px;
    padding: 22px 24px;
    min-height: 260px;
    margin-bottom: 14px;
}
.answer-panel-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #CCCCCC;
    margin-bottom: 12px;
}
.answer-text {
    font-size: 14.5px;
    color: #222222;
    line-height: 1.8;
}
.answer-placeholder {
    font-size: 13.5px;
    color: #DDDDDD;
    line-height: 1.8;
}

/* ── Raw result ── */
.raw-pre {
    background: #F5F5F5;
    border: 1px solid #E8E8E8;
    border-radius: 6px;
    padding: 12px 14px;
    font-family: monospace;
    font-size: 11px;
    color: #777777;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 140px;
    overflow-y: auto;
}

/* ── Search input ── */
.stTextInput > div > div > input {
    height: 44px !important;
    border-radius: 7px !important;
    border: 1px solid #E0E0E0 !important;
    font-size: 13.5px !important;
    padding: 0 14px !important;
    background: #FFFFFF !important;
    color: #111111 !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #CCCCCC !important;
}
.stTextInput > div > div > input:focus {
    border-color: #AAAAAA !important;
    box-shadow: none !important;
    outline: none !important;
}
.stTextInput > label { display: none !important; }

/* ── Button — scoped to stButton anywhere ── */
.stButton > button {
    height: 44px !important;
    border-radius: 7px !important;
    background: #111111 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border: none !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #333333 !important;
    border: none !important;
}
.stButton > button:focus {
    box-shadow: none !important;
    border: none !important;
}

/* ── Example items ── */
.example-item {
    padding: 9px 0;
    border-bottom: 1px solid #EBEBEB;
    font-size: 12.5px;
    color: #666666;
    line-height: 1.4;
}
.example-item:first-of-type { border-top: 1px solid #EBEBEB; }

/* ── Divider ── */
.thin-rule {
    border: none;
    border-top: 1px solid #E8E8E8;
    margin: 0 0 22px 0;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BACKEND DATA
# --------------------------------------------------

backend_status      = False
total_rows          = 0
total_anomalies     = 0
critical_unresolved = 0

try:
    health = requests.get(f"{API_URL}/health", timeout=3)
    if health.status_code == 200:
        backend_status = True
        total_rows = health.json().get("rows_loaded", 0)

    anomaly_resp = requests.get(f"{API_URL}/anomalies", timeout=5)
    anomaly_data = anomaly_resp.json()

    total_anomalies = anomaly_data.get(
    "total_anomalies",
    0
)

    long_resolution = anomaly_data.get(
    "long_resolution_count",
    0
)

    critical_unresolved = anomaly_data.get(
    "critical_unresolved_count",
    0
)
except Exception:
    pass
# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown('<div class="page-title">DotMappers Ticket Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Natural language analytics for your support data</div>', unsafe_allow_html=True)
st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)

# --------------------------------------------------
# LAYOUT  — no gap kwarg, simple ratios
# --------------------------------------------------

left_col, center_col, right_col = st.columns([1, 3, 1])

# ── LEFT: Status & Metrics ──────────────────────
with left_col:

    dot_cls = "dot-green" if backend_status else "dot-red"
    label   = "Connected" if backend_status else "Offline"

    st.markdown(f"""
    <div class="col-label">System</div>
    <div class="status-line">
        <span class="dot {dot_cls}"></span>
        {label}
    </div>
    <div class="metric-block">
        <div class="metric-num">{total_rows:,}</div>
        <div class="metric-lbl">Total Tickets</div>
    </div>
    <div class="metric-block">
        <div class="metric-num">{total_anomalies:,}</div>
        <div class="metric-lbl">Total Anomalies</div>
    </div>
    <div class="metric-block">
        <div class="metric-num">{long_resolution:,}</div>
        <div class="metric-lbl">Long Resolution</div>
    </div>
    <div class="metric-block last">
        <div class="metric-num">{critical_unresolved:,}</div>
        <div class="metric-lbl">Critical Unresolved</div>
    </div>
    """, unsafe_allow_html=True)

# ── CENTER: Answer + Search ─────────────────────
with center_col:

    # Answer panel
    if st.session_state.answer:
        body = f'<div class="answer-text">{st.session_state.answer}</div>'
    else:
        body = '<div class="answer-placeholder">Ask a question and the answer will appear here.</div>'

    st.markdown(f"""
    <div class="answer-panel">
        <div class="answer-panel-label">Answer</div>
        {body}
    </div>
    """, unsafe_allow_html=True)

    # Raw data expander
    if st.session_state.raw_result:
        with st.expander("Raw data", expanded=False):
            st.markdown(
                f'<div class="raw-pre">{st.session_state.raw_result}</div>',
                unsafe_allow_html=True,
            )

    # Search row — use container-level columns so they inherit center_col width
    st.markdown('<div class="col-label" style="margin-top:6px;">Ask a question</div>', unsafe_allow_html=True)

    q_col, btn_col = st.columns([5, 1])

    with q_col:
        question = st.text_input(
            "q",
            placeholder="e.g. Which agent has the highest rating?",
            label_visibility="collapsed",
            key="q_field",
        )

    with btn_col:
        run = st.button("Search", use_container_width=True)

# ── RIGHT: Examples ─────────────────────────────
with right_col:

    examples = [
        "How many tickets are open?",
        "How many tickets are resolved?",
        "Which agent has the highest rating?",
        "Are there unresolved critical tickets?",
        "What is the average resolution time?",
        "Which category has the most tickets?",
    ]

    st.markdown('<div class="col-label">Examples</div>', unsafe_allow_html=True)

    for ex in examples:
        st.markdown(f'<div class="example-item">{ex}</div>', unsafe_allow_html=True)

# --------------------------------------------------
# QUERY
# --------------------------------------------------

if run and question.strip():
    try:
        resp = requests.post(
            f"{API_URL}/query",
            json={"question": question.strip()},
            timeout=45,
        )
        data = resp.json()
        st.session_state.answer     = data.get("answer", "No answer returned.")
        st.session_state.raw_result = data.get("raw_result", "") or ""
    except Exception as e:
        st.session_state.answer     = f"Backend unreachable at {API_URL}. Error: {e}"
        st.session_state.raw_result = ""
    st.rerun()

elif run and not question.strip():
    st.warning("Please enter a question first.")
