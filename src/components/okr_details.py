import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.styles import COLORS

def render_okr_details(practices_df, okrs_df, krs_df, metrics_df, actions_df):
    """Render detailed OKR view"""
    st.markdown(f'<div class="subtitle">OKR Details</div>', unsafe_allow_html=True)

    # OKR selector
    okr_names = okrs_df['name'].unique()
    selected_okr = st.selectbox("Select OKR", okr_names)

    # Get OKR data across all practices
    okr_data = okrs_df[okrs_df['name'] == selected_okr]

    # Get KRs status for selected OKRs
    kr_data = krs_df[krs_df['okr_id'].isin(okr_data['okr_id'])]

    # Overview metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Practices", len(okr_data))
    with col2:
        on_track = len(kr_data[kr_data['status'].isin(['On Track', 'Complete'])])
        st.metric("KRs On Track", on_track, 
                 delta=f"{(on_track/len(kr_data)*100):.0f}%" if len(kr_data) > 0 else "0%")
    with col3:
        at_risk = len(kr_data[kr_data['status'].isin(['At Risk', 'Not Started', 'In Progress'])])
        st.metric("KRs At Risk", at_risk,
                 delta=f"{(at_risk/len(kr_data)*100):.0f}%" if len(kr_data) > 0 else "0%",
                 delta_color="inverse")
    with col4:
        total_actions = len(actions_df[actions_df['kr_id'].isin(kr_data['kr_id'])])
        st.metric("Total Actions", total_actions)
    with col5:
        completed_actions = len(actions_df[
            (actions_df['kr_id'].isin(kr_data['kr_id'])) & 
            (actions_df['status'] == 'Complete')
        ])
        st.metric("Completed Actions", completed_actions,
                 delta=f"{(completed_actions/total_actions*100):.0f}%" if total_actions > 0 else "0%")

    # Overall Progress Chart
    st.subheader("Overall Progress by Practice")
    fig_overall = create_overall_progress_chart(okr_data, kr_data, metrics_df)
    st.plotly_chart(fig_overall, use_container_width=True)

    # Detailed breakdown by practice
    st.subheader("Practice Breakdown")
    
    for _, okr in okr_data.iterrows():
        practice = practices_df[practices_df['practice_id'] == okr['practice_id']].iloc[0]
        
        with st.expander(f"{practice['name']} Practice", expanded=True):
            render_practice_okr_details(okr, kr_data, metrics_df, actions_df, practice)

def create_overall_progress_chart(okr_data, kr_data, metrics_df):
    """Create overall progress chart for all practices"""
    fig = go.Figure()

    for _, okr in okr_data.iterrows():
        okr_krs = kr_data[kr_data['okr_id'] == okr['okr_id']]
        practice_metrics = metrics_df[metrics_df['kr_id'].isin(okr_krs['kr_id'])]
        
        if not practice_metrics.empty:
            latest_value = practice_metrics.sort_values('date').groupby('kr_id').last()['value'].mean()
            
            fig.add_trace(go.Bar(
                name=f"Practice: {okr['practice_name']}",
                x=['Current Progress'],
                y=[latest_value],
                text=[f"{latest_value:.1f}%"],
                textposition='auto',
            ))

    fig.update_layout(
        title="Progress Across Practices",
        yaxis_title="Progress (%)",
        showlegend=True,
        height=300,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font={'color': COLORS['text']},
        title_font_color=COLORS['sky']
    )
    
    return fig

def render_practice_okr_details(okr, kr_data, metrics_df, actions_df, practice):
    """Render OKR details for a specific practice"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write(f"**Owner:** {practice['owner']}")
        
        # Get KRs for this OKR
        okr_krs = kr_data[kr_data['okr_id'] == okr['okr_id']]
        
        # Show KR status breakdown with better styling
        st.write("**Key Results Status:**")
        for _, kr in okr_krs.iterrows():
            status_color = {
                'On Track': 'green',
                'Complete': 'green',
                'At Risk': 'red',
                'Not Started': 'gray',
                'In Progress': 'orange'
            }.get(kr['status'], 'gray')
            
            # Get actions for this KR
            kr_actions = actions_df[actions_df['kr_id'] == kr['kr_id']]
            completed_actions = len(kr_actions[kr_actions['status'] == 'Complete'])
            total_actions = len(kr_actions)
            
            st.markdown(f"""
                <div style='
                    padding: 10px;
                    border-left: 4px solid {status_color};
                    background-color: {COLORS['background']};
                    margin-bottom: 10px;
                '>
                    <strong>{kr['name']}</strong><br>
                    Status: <span style='color: {status_color}'>{kr['status']}</span><br>
                    Progress: {kr['current_value']}/{kr['target']}<br>
                    Actions: {completed_actions}/{total_actions} complete
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Progress charts
        okr_krs = kr_data[kr_data['okr_id'] == okr['okr_id']]
        
        # KR Progress Bar Chart
        fig_progress = go.Figure()
        
        for _, kr in okr_krs.iterrows():
            kr_metrics = metrics_df[metrics_df['kr_id'] == kr['kr_id']]
            if not kr_metrics.empty:
                latest_metric = kr_metrics.sort_values('date').iloc[-1]
                fig_progress.add_trace(go.Bar(
                    name=kr['name'],
                    x=[kr['name']],
                    y=[latest_metric['value']],
                    text=[f"{latest_metric['value']}%"],
                    textposition='auto',
                ))

        fig_progress.update_layout(
            title="Key Results Progress",
            yaxis_title="Progress (%)",
            showlegend=False,
            height=200,
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font={'color': COLORS['text']},
            title_font_color=COLORS['sky']
        )
        
        st.plotly_chart(fig_progress, use_container_width=True)

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
                
                # Add target line
                target_value = float(str(kr['target']).replace('≥', '').replace('≤', '').replace('%', ''))
                fig_timeline.add_hline(
                    y=target_value,
                    line_dash="dash",
                    line_color="gray",
                    annotation_text=f"{kr['name']} Target: {target_value}%",
                    annotation_position="bottom right"
                )

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
            ),
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['background'],
            font={'color': COLORS['text']},
            title_font_color=COLORS['sky']
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)