import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.styles import COLORS

def render_practice_view(practices_df, okrs_df, krs_df, metrics_df):
    """Render the practice-specific view"""
    st.markdown(f'<div class="subtitle">Practice View</div>', unsafe_allow_html=True)
    
    # Practice selector
    selected_practice = st.selectbox(
        "Select Practice",
        practices_df['name'].tolist()
    )

    # Get practice details
    practice_data = practices_df[practices_df['name'] == selected_practice].iloc[0]
    practice_okrs = okrs_df[okrs_df['practice_id'] == practice_data['practice_id']]

    # Get KRs for this practice
    practice_krs = krs_df[krs_df['okr_id'].isin(practice_okrs['okr_id'])]
    
    # Calculate KR metrics
    krs_on_track = len(practice_krs[practice_krs['status'].isin(['On Track', 'Complete'])])
    krs_at_risk = len(practice_krs[practice_krs['status'].isin(['At Risk', 'Not Started', 'In Progress'])])

    # Display practice information
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Practice", selected_practice)
    with col2:
        st.metric("Owner", practice_data['owner'])
    with col3:
        st.metric("Total OKRs", len(practice_okrs))
    with col4:
        st.metric("KRs On Track", krs_on_track, 
                 delta=f"{(krs_on_track/len(practice_krs)*100):.0f}%" if len(practice_krs) > 0 else "0%")
    with col5:
        st.metric("KRs At Risk", krs_at_risk,
                 delta=f"{(krs_at_risk/len(practice_krs)*100):.0f}%" if len(practice_krs) > 0 else "0%",
                 delta_color="inverse")

    # Create tabs for different OKRs
    if len(practice_okrs) > 0:
        tabs = st.tabs([f"{okr['name']}" for _, okr in practice_okrs.iterrows()])
        
        for idx, (_, okr) in enumerate(practice_okrs.iterrows()):
            with tabs[idx]:
                render_okr_tab(okr, krs_df, metrics_df)
    else:
        st.warning("No OKRs found for this practice")

def render_okr_tab(okr, krs_df, metrics_df):
    """Render individual OKR tab content"""
    # Get KRs for this OKR
    okr_krs = krs_df[krs_df['okr_id'] == okr['okr_id']]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write(f"**Description:** {okr['description']}")
        st.write(f"**Owner:** {okr['owner']}")
        
        # KR Status Summary
        st.subheader("Key Results Status")
        for _, kr in okr_krs.iterrows():
            status_color = {
                'On Track': 'green',
                'Complete': 'green',
                'At Risk': 'red',
                'Not Started': 'gray',
                'In Progress': 'orange'
            }.get(kr['status'], 'gray')
            
            st.markdown(f"""
                <div style='
                    padding: 10px;
                    border-left: 4px solid {status_color};
                    background-color: {COLORS['background']};
                    margin-bottom: 10px;
                '>
                    <strong>{kr['name']}</strong><br>
                    Status: <span style='color: {status_color}'>{kr['status']}</span><br>
                    Progress: {kr['current_value']}/{kr['target']}
                </div>
            """, unsafe_allow_html=True)

    with col2:
        # KR Progress Chart
        fig_kr_progress = go.Figure()
        
        for _, kr in okr_krs.iterrows():
            kr_metrics = metrics_df[metrics_df['kr_id'] == kr['kr_id']]
            if not kr_metrics.empty:
                fig_kr_progress.add_trace(go.Bar(
                    name=kr['name'],
                    x=[kr['name']],
                    y=[kr['current_value']],
                    text=[f"{kr['current_value']}%"],
                    textposition='auto',
                ))

        fig_kr_progress.update_layout(
            title="Key Results Progress",
            yaxis_title="Progress (%)",
            showlegend=True,
            height=300,
            barmode='group'
        )
        
        st.plotly_chart(fig_kr_progress, use_container_width=True)

        # Timeline Chart
        fig_timeline = go.Figure()
        
        for _, kr in okr_krs.iterrows():
            kr_metrics = metrics_df[metrics_df['kr_id'] == kr['kr_id']]
            if not kr_metrics.empty:
                fig_timeline.add_trace(go.Scatter(
                    x=kr_metrics['date'],
                    y=kr_metrics['value'],
                    mode='lines+markers',
                    name=kr['name'],
                    line=dict(width=2),
                    marker=dict(size=8)
                ))

        fig_timeline.update_layout(
            title="Progress Over Time",
            xaxis_title="Date",
            yaxis_title="Progress (%)",
            hovermode='x unified',
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Add target lines
        for _, kr in okr_krs.iterrows():
            target_value = float(str(kr['target']).replace('≥', '').replace('≤', '').replace('%', ''))
            fig_timeline.add_hline(
                y=target_value,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"Target: {target_value}%",
                annotation_position="bottom right"
            )

        st.plotly_chart(fig_timeline, use_container_width=True)
