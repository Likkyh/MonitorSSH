import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================
# Configure the Streamlit page details (title, icon, layout).
st.set_page_config(
    page_title="SSH Log Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DATA LOADING FUNCTIONS
# ==========================================

@st.cache_data
def load_data():
    """
    Loads the SSH log dataset from the CSV file.
    
    This function uses Streamlit's caching mechanism (@st.cache_data)
    to prevent reloading the data on every interaction, optimizing performance.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the log data, or None if error.
    """
    file_path = os.path.join("src", "datasetssh.csv")
    
    # Check if file exists before attempting to read
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return None
        
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(file_path)
        
        # Parse 'Date et Heure' column to datetime objects for time-series analysis
        # Format expected: dd/mm/yy - HH:MM:SS (e.g., 10/12/25 - 06:55:46)
        df['Date et Heure'] = pd.to_datetime(
            df['Date et Heure'], 
            format='%d/%m/%y - %H:%M:%S', 
            errors='coerce' # Handle invalid dates gracefully
        )
        return df
    except Exception as e:
        # Display valid error message on UI if loading fails
        st.error(f"Error loading data: {e}")
        return None

def convert_df_to_csv(df):
    """
    Converts a pandas DataFrame to a CSV string encoded in UTF-8.
    
    Args:
        df (pd.DataFrame): The dataframe to convert.
        
    Returns:
        bytes: The CSV data encoded as bytes.
    """
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================

def main():
    """
    Main function containing the dashboard layout and logic.
    """
    # Main Header
    st.title("🛡️ SSH Log Analysis Dashboard")
    st.markdown("Analyze SSH connection events, identify aggressive IPs, and monitor security trends.")

    # Load initial data
    df = load_data()

    if df is not None:
        # ------------------------------------------
        # SIDEBAR FILTERS
        # ------------------------------------------
        st.sidebar.header("🔍 Filter Options")
        
        # 1. Date Range Filter
        # Calculate min and max dates from dataset for default values
        min_date = df['Date et Heure'].min().date() if not df['Date et Heure'].isna().all() else datetime.date.today()
        max_date = df['Date et Heure'].max().date() if not df['Date et Heure'].isna().all() else datetime.date.today()
        
        # Widget to pick a start and end date
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # 2. Event ID Filter
        # Extract unique Event IDs and add an "All" option
        event_ids = df['Identifiant Evenement'].unique().tolist()
        event_ids.insert(0, "All")
        selected_event_id = st.sidebar.selectbox("Event ID", event_ids, index=0)

        # 3. Source IP Filter
        # Extract unique source IPs
        unique_ips = df['IP Source'].dropna().unique().tolist()
        selected_ips = st.sidebar.multiselect("Source IPs", sorted(unique_ips))

        # ------------------------------------------
        # DATA FILTERING LOGIC
        # ------------------------------------------
        df_filtered = df.copy()

        # Apply Date Filter if a valid range (start, end) is selected
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df_filtered[
                (df_filtered['Date et Heure'].dt.date >= start_date) & 
                (df_filtered['Date et Heure'].dt.date <= end_date)
            ]

        # Apply Event ID Filter
        if selected_event_id != "All":
            df_filtered = df_filtered[df_filtered['Identifiant Evenement'] == selected_event_id]

        # Apply IP Filter
        if selected_ips:
            df_filtered = df_filtered[df_filtered['IP Source'].isin(selected_ips)]

        # ------------------------------------------
        # DASHBOARD LAYOUT (TABS)
        # ------------------------------------------
        # Create two tabs: one for visual dashboard, one for raw data inspection
        tab1, tab2 = st.tabs(["📈 Dashboard", "📋 Raw Data"])

        # >>> TAB 1: VISUAL DASHBOARD <<<
        with tab1:
            # Handle empty results case
            if df_filtered.empty:
                st.warning("⚠️ No entries match the selected filters. Please adjust your selection.")
            else:
                # -- Key Metrics Section --
                total_events = len(df_filtered)
                unique_ips_count = df_filtered['IP Source'].nunique()
                
                # Calculate most frequent target user (handled for potential errors)
                try:
                    top_user = df_filtered['Utilisateur Vise'].mode()[0]
                except (IndexError, KeyError):
                    top_user = "N/A"

                st.subheader("Key Metrics")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Events", total_events)
                col2.metric("Unique IPs", unique_ips_count)
                col3.metric("Top Target User", top_user)

                st.divider()

                # -- Charts Section --
                col_left, col_right = st.columns(2)

                # Chart 1: Top Aggressive IPs
                with col_left:
                    st.subheader("🔥 Top 5 Aggressive IPs")
                    top_ips = df_filtered['IP Source'].value_counts().head(5)
                    if not top_ips.empty:
                        st.bar_chart(top_ips)
                    else:
                        st.info("No IP data available.")

                # Chart 2: Time Evolution
                with col_right:
                    st.subheader("📅 Attack Frequency Over Time")
                    if 'Date et Heure' in df_filtered.columns and not df_filtered['Date et Heure'].isna().all():
                        # Resample data by hour to count events
                        time_evolution = df_filtered.set_index('Date et Heure').resample('H').size()
                        st.line_chart(time_evolution)
                    else:
                        st.warning("Time data invalid or missing.")

        # >>> TAB 2: RAW DATA <<<
        with tab2:
            st.subheader("Filtered Log Data")
            st.markdown(f"**Showing {len(df_filtered)} rows**")
            
            # Display interactive dataframe
            st.dataframe(df_filtered, use_container_width=True)
            
            # Export Button
            csv = convert_df_to_csv(df_filtered)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name='filtered_ssh_logs.csv',
                mime='text/csv',
            )

# Entry point of the script
if __name__ == "__main__":
    main()
