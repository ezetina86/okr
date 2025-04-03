import pandas as pd

def calculate_okr_progress(okr_df, metrics_df):
    """Calculate progress for a specific OKR"""
    try:
        okr_id = okr_df['okr_id'].iloc[0]
        print(f"\nCalculating progress for OKR: {okr_id}")
        
        # Get metrics for this OKR
        okr_metrics = metrics_df[metrics_df['okr_id'] == okr_id].copy()
        
        if okr_metrics.empty:
            print(f"No metrics found for OKR: {okr_id}")
            return 0
        
        # Get latest metrics for each KR
        latest_metrics = okr_metrics.sort_values('date').groupby('kr_id').last()
        
        # Calculate progress for each KR
        progress_values = []
        for kr_id, row in latest_metrics.iterrows():
            try:
                value = float(row['value'])
                target = float(str(row['target']).replace('≥', '').replace('≤', '').replace('%', ''))
                
                if '≤' in str(row['target']):  # Lower is better
                    progress = max(0, min(100, (target - value) / target * 100))
                else:  # Higher is better
                    progress = max(0, min(100, (value / target * 100)))
                
                progress_values.append(progress)
                print(f"KR {kr_id}: {progress:.2f}% (value={value}, target={target})")
            except Exception as e:
                print(f"Error calculating progress for KR {kr_id}: {e}")
                continue
        
        if progress_values:
            avg_progress = sum(progress_values) / len(progress_values)
            print(f"Average progress: {avg_progress:.2f}%")
            return round(avg_progress, 2)
        
        return 0
        
    except Exception as e:
        print(f"Error in calculate_okr_progress: {e}")
        return 0

def get_okr_summary(practices_df, okrs_df, metrics_df):
    """Consolidate OKR data across all practices"""
    try:
        summary_data = []
        
        # Group OKRs by name
        unique_okrs = okrs_df['name'].unique()
        print(f"\nFound {len(unique_okrs)} unique OKRs")
        
        for okr_name in unique_okrs:
            print(f"\nProcessing OKR: {okr_name}")
            okr_data = {
                'OKR Name': okr_name,
                'Practices': {},
                'Overall Progress': 0
            }
            
            # Get data for each practice
            for _, practice in practices_df.iterrows():
                practice_okr = okrs_df[
                    (okrs_df['name'] == okr_name) & 
                    (okrs_df['practice_id'] == practice['practice_id'])
                ]
                
                if not practice_okr.empty:
                    progress = calculate_okr_progress(practice_okr, metrics_df)
                    okr_data['Practices'][practice['name']] = progress
                    print(f"Practice {practice['name']}: {progress}%")
            
            # Calculate overall progress
            if okr_data['Practices']:
                okr_data['Overall Progress'] = sum(okr_data['Practices'].values()) / len(okr_data['Practices'])
                print(f"Overall progress for {okr_name}: {okr_data['Overall Progress']}%")
            
            summary_data.append(okr_data)
        
        return summary_data
    
    except Exception as e:
        print(f"Error in get_okr_summary: {e}")
        import traceback
        print(traceback.format_exc())
        return []