from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import streamlit as st

@st.cache_resource
def init_connection():
    try:
        # Create database connection
        connection_string = "postgresql://okr_user:okr_password@db:5432/okr_database"
        engine = create_engine(connection_string)
        return engine
    except SQLAlchemyError as e:
        st.error(f"Database connection error: {e}")
        return None

def get_practices():
    engine = init_connection()
    if engine:
        return pd.read_sql("SELECT * FROM practices", engine)
    return pd.DataFrame()

def get_okrs():
    engine = init_connection()
    if engine:
        query = """
        SELECT 
            o.*,
            p.name as practice_name,
            COUNT(DISTINCT kr.kr_id) as kr_count,
            COUNT(DISTINCT m.metric_id) as metric_count
        FROM okrs o
        JOIN practices p ON o.practice_id = p.practice_id
        LEFT JOIN key_results kr ON o.okr_id = kr.okr_id
        LEFT JOIN metrics m ON kr.kr_id = m.kr_id
        GROUP BY o.okr_id, o.practice_id, o.name, o.description, o.year, o.owner, 
                 o.created_at, p.name
        """
        return pd.read_sql(query, engine)
    return pd.DataFrame()

def get_key_results(okr_id=None):
    engine = init_connection()
    if engine:
        query = """
        SELECT kr.*, o.practice_id 
        FROM key_results kr
        JOIN okrs o ON kr.okr_id = o.okr_id
        """
        if okr_id:
            query += f" WHERE kr.okr_id = '{okr_id}'"
        return pd.read_sql(query, engine)
    return pd.DataFrame()

def get_metrics():
    engine = init_connection()
    if engine:
        query = """
        SELECT 
            m.*,
            kr.okr_id,
            o.name as okr_name,
            o.practice_id
        FROM metrics m
        JOIN key_results kr ON m.kr_id = kr.kr_id
        JOIN okrs o ON kr.okr_id = o.okr_id
        ORDER BY m.date DESC
        """
        metrics_df = pd.read_sql(query, engine)
        print("Metrics data loaded:", len(metrics_df))  # Debug print
        return metrics_df
    return pd.DataFrame()

def get_actions(kr_id=None):
    engine = init_connection()
    if engine:
        query = "SELECT * FROM actions"
        if kr_id:
            query += f" WHERE kr_id = '{kr_id}'"
        query += " ORDER BY due_date"
        return pd.read_sql(query, engine)
    return pd.DataFrame()