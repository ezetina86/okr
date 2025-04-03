import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.data_processing import get_okr_summary
from utils.styles import COLORS


# Define a professional color palette
COLOR_PALETTE = {
    'primary': '#1f77b4',    # Deep blue for primary elements
    'success': '#2ca02c',    # Muted green for good progress
    'warning': '#ff7f0e',    # Warm orange for warning
    'danger': '#d62728',     # Soft red for danger
    'background': '#f8f9fa', # Light background
    'text': '#2c3e50'        # Dark blue-grey for text
}

# Define progress thresholds
PROGRESS_THRESHOLDS = {
    'high': 80,
    'medium': 60,
    'low': 40
}

def render_executive_summary(practices_df, okrs_df, krs_df, metrics_df):
    # Add subtitle
    st.markdown(f'<div class="subtitle">Executive Summary</div>', unsafe_allow_html=True)
    st.subheader("OKR Overview")

    # Debug section
    if st.checkbox("Debug Data"):
        st.write("### Data Verification")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**OKRs Sample**")
            st.write(okrs_df[['okr_id', 'name']].head())
        
        with col2:
            st.write("**KRs Sample**")
            st.write(krs_df[['kr_id', 'okr_id', 'status']].head())
        
        with col3:
            st.write("**Status Counts**")
            st.write(krs_df['status'].value_counts())
        
        # Show sample data
        if st.checkbox("Show Raw Data"):
            st.write("#### Metrics Sample")
            st.dataframe(metrics_df.head())
            
            st.write("#### OKRs Sample")
            st.dataframe(okrs_df.head())
            
            # Show a sample calculation
            if not metrics_df.empty:
                st.write("### Sample Calculation")
                sample_metric = metrics_df.iloc[0]
                st.write(f"""
                Sample Metric:
                - OKR ID: {sample_metric['okr_id']}
                - KR ID: {sample_metric['kr_id']}
                - Value: {sample_metric['value']}
                - Target: {sample_metric['target']}
                - Status: {sample_metric['status']}
                """)
    
    # Get consolidated summary
    summary_data = get_okr_summary(practices_df, okrs_df, metrics_df)

    if not summary_data:
        st.warning("No data available for visualization")
        return
    
    # Create overall progress chart
    fig_overall = create_overall_progress_chart(summary_data)
    st.plotly_chart(fig_overall, use_container_width=True)
    
    # Create summary table
    create_summary_table(summary_data, krs_df)
    
    # Create practice heatmap
    fig_heatmap = create_practice_heatmap(summary_data)
    st.plotly_chart(fig_heatmap, use_container_width=True)

def get_progress_color(value):
    """Return appropriate color based on progress value"""
    if value >= PROGRESS_THRESHOLDS['high']:
        return COLOR_PALETTE['success']
    elif value >= PROGRESS_THRESHOLDS['medium']:
        return COLOR_PALETTE['warning']
    else:
        return COLOR_PALETTE['danger']

def create_overall_progress_chart(summary_data):
    """Create a bar chart showing overall progress for each OKR"""
    fig = go.Figure()
    
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font={'color': COLORS['text']},
        title_font_color=COLORS['sky']
    )
    
    # Update heatmap colors
    colorscale=[
        [0, COLORS['danger']],
        [0.5, COLORS['lilac']],
        [1, COLORS['mint']]
    ]
    
    okr_names = [okr['OKR Name'] for okr in summary_data]
    progress_values = [round(okr['Overall Progress'], 2) for okr in summary_data]
    
    # Debug print
    print("Progress values:", progress_values)
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=okr_names,
        y=progress_values,
        text=[f"{v}%" for v in progress_values],
        textposition='auto',
        marker_color=[get_progress_color(v) for v in progress_values]
    ))
    
    fig.update_layout(
        title={
            'text': "Overall OKR Progress",
            'font': {'color': COLOR_PALETTE['text']}
        },
        plot_bgcolor=COLOR_PALETTE['background'],
        paper_bgcolor=COLOR_PALETTE['background'],
        yaxis_title="Progress (%)",
        yaxis_range=[0, 100],  # Force y-axis to show 0-100%
        showlegend=False,
        height=400
    )
    
    return fig

def create_summary_table(summary_data, krs_df):
    """Create a summary table with key metrics"""
    table_data = []
    
    for okr in summary_data:
        # Get base OKR name (e.g., 'OKR1', 'OKR2', etc.)
        okr_base_name = okr['OKR Name'].split()[0]  # This will get 'People' from 'People Engagement'
        
        # Map OKR names to their base IDs
        okr_name_to_id = {
            'People Engagement': 'OKR1',
            'Operational Excellence': 'OKR2',
            'Delivery Excellence': 'OKR3',
            'Growing Business': 'OKR4',
            'Proactive Innovation': 'OKR5'
        }
        
        # Get the base OKR ID
        base_okr_id = None
        for key, value in okr_name_to_id.items():
            if key in okr['OKR Name']:
                base_okr_id = value
                break
        
        if base_okr_id:
            # Get all KRs for this OKR across all practices
            okr_krs = krs_df[krs_df['okr_id'].str.startswith(base_okr_id)]
            
            # Debug print
            print(f"\nProcessing {okr['OKR Name']}")
            print(f"Base OKR ID: {base_okr_id}")
            print(f"Found {len(okr_krs)} KRs")
            print(f"Status counts: {okr_krs['status'].value_counts().to_dict() if not okr_krs.empty else 'No KRs'}")
            
            row = {
                'OKR': okr['OKR Name'],
                'Overall Progress': round(okr['Overall Progress'], 2),
                'KRs On Track': len(okr_krs[okr_krs['status'].isin(['On Track', 'Complete'])]),
                'KRs At Risk': len(okr_krs[okr_krs['status'].isin(['At Risk', 'Not Started', 'In Progress'])]),
                'Total KRs': len(okr_krs)
            }
        else:
            # Fallback if no matching OKR ID is found
            row = {
                'OKR': okr['OKR Name'],
                'Overall Progress': round(okr['Overall Progress'], 2),
                'KRs On Track': 0,
                'KRs At Risk': 0,
                'Total KRs': 0
            }
        
        table_data.append(row)
        print(f"Row data: {row}")
    
    df = pd.DataFrame(table_data)
    
    # Add debug information
    if st.checkbox("Show Table Debug Info"):
        st.write("### KR Data Overview")
        st.write("Unique OKR IDs in KRs data:", krs_df['okr_id'].unique())
        st.write("Status distribution:", krs_df['status'].value_counts())
        
        st.write("### Detailed KR Status by OKR")
        for okr_id in krs_df['okr_id'].unique():
            kr_subset = krs_df[krs_df['okr_id'] == okr_id]
            st.write(f"\nOKR ID: {okr_id}")
            st.write("Status counts:", kr_subset['status'].value_counts())
    
    # Apply custom styling with colors
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'OKR': st.column_config.TextColumn(
                'Objective',
                help='Objective name'
            ),
            'Overall Progress': st.column_config.ProgressColumn(
                'Progress',
                help='Overall progress across practices',
                format="%.2f%%",
                min_value=0,
                max_value=100,
            ),
            'KRs On Track': st.column_config.NumberColumn(
                'KRs On Track',
                help='Number of Key Results that are on track or complete',
                format="%d"
            ),
            'KRs At Risk': st.column_config.NumberColumn(
                'KRs At Risk',
                help='Number of Key Results that are at risk or not started',
                format="%d"
            ),
            'Total KRs': st.column_config.NumberColumn(
                'Total KRs',
                help='Total number of Key Results',
                format="%d"
            )
        }
    )

def create_practice_heatmap(summary_data):
    """Create a heatmap showing progress by practice and OKR"""
    practices = list(summary_data[0]['Practices'].keys())
    okr_names = [okr['OKR Name'] for okr in summary_data]
    
    z_values = [[round(okr['Practices'].get(practice, 0), 2) for practice in practices] 
                for okr in summary_data]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=practices,
        y=okr_names,
        text=[[f"{val}%" for val in row] for row in z_values],
        texttemplate="%{text}",
        textfont={"size": 10},
        colorscale=[
            [0, COLOR_PALETTE['danger']],
            [0.5, COLOR_PALETTE['warning']],
            [1, COLOR_PALETTE['success']]
        ],
        colorbar_title="Progress %"
    ))
    
    fig.update_layout(
        title={
            'text': "Progress by Practice and OKR",
            'font': {'color': COLOR_PALETTE['text']}
        },
        plot_bgcolor=COLOR_PALETTE['background'],
        paper_bgcolor=COLOR_PALETTE['background'],
        xaxis_title="Practices",
        yaxis_title="OKRs",
        height=300,
        xaxis={'tickangle': 45}
    )
    
    return fig