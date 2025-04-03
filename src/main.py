import streamlit as st
from database.connection import (
    get_practices, 
    get_okrs, 
    get_key_results,
    get_metrics,
    get_actions
)
from components.header import render_header
from components.executive_summary import render_executive_summary
from components.practice_view import render_practice_view
from components.okr_details import render_okr_details

# Page config
st.set_page_config(page_title="OKR Dashboard", layout="wide")

# Load data
practices_df = get_practices()
okrs_df = get_okrs()
krs_df = get_key_results()
metrics_df = get_metrics()
actions_df = get_actions()

# Render header
render_header()

# Navigation
page = st.sidebar.radio(
    "Select View",
    ["Executive Summary", "Practice View", "OKR Details"]
)

# Render selected page
if page == "Executive Summary":
    render_executive_summary(practices_df, okrs_df, krs_df, metrics_df)
elif page == "Practice View":
    render_practice_view(practices_df, okrs_df, krs_df, metrics_df)
elif page == "OKR Details":
    render_okr_details(practices_df, okrs_df, krs_df, metrics_df, actions_df)