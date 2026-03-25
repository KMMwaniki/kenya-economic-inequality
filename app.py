# =====================================================
# Kenya County Economic Inequality Analysis
# Streamlit Dashboard
# Author: Kimberly Muthoni Mwaniki
# Strathmore University
# =====================================================

import os
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Kenya County Economic Inequality Analysis",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0066B3;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0066B3;
        padding: 0.5rem;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_database():
    if not os.path.exists('kenya_counties.db'):
        st.info("Setting up database for first use...")
        try:
            if os.path.exists('run_database.py'):
                with open('run_database.py', 'r') as f:
                    exec(f.read())
            else:
                with open('setup.sql', 'r') as f:
                    sql = f.read()
                conn = sqlite3.connect('kenya_counties.db')
                conn.executescript(sql)
                conn.commit()
                conn.close()
            st.success("Database created successfully!")
        except Exception as e:
            st.error(f"Database creation failed: {e}")
            return False
    return True

db_ready = init_database()
if not db_ready:
    st.error("Database not available. Please check logs.")
    st.stop()

@st.cache_resource
def get_connection():
    return sqlite3.connect('kenya_counties.db')

@st.cache_data
def load_data():
    try:
        conn = get_connection()
        counties = pd.read_sql_query("SELECT * FROM counties", conn)
        demographics = pd.read_sql_query("SELECT * FROM demographics WHERE year = 2023", conn)
        infrastructure = pd.read_sql_query("SELECT * FROM infrastructure WHERE year = 2023", conn)
        health = pd.read_sql_query("SELECT * FROM health WHERE year = 2023", conn)
        education = pd.read_sql_query("SELECT * FROM education WHERE year = 2023", conn)
        
        counties = counties[['county_id', 'county_name', 'region', 'sub_region']]
        demographics = demographics[['county_id', 'population', 'poverty_rate', 'unemployment_rate', 'gini_coefficient']]
        infrastructure = infrastructure[['county_id', 'road_density', 'electricity_access', 'internet_access', 'paved_roads_percentage']]
        health = health[['county_id', 'hospital_count', 'doctors_per_1000', 'child_mortality', 'health_facilities_per_10000']]
        education = education[['county_id', 'literacy_rate', 'school_enrollment', 'dropout_rate', 'primary_completion_rate']]
        
        df = counties.merge(demographics, on='county_id')
        df = df.merge(infrastructure, on='county_id')
        df = df.merge(health, on='county_id')
        df = df.merge(education, on='county_id')
        
        if df['doctors_per_1000'].max() > 0:
            df['inequality_score'] = (
                (df['poverty_rate'] / 100) * 0.3 +
                (1 - df['electricity_access'] / 100) * 0.3 +
                (1 - df['literacy_rate'] / 100) * 0.2 +
                (1 - df['doctors_per_1000'] / df['doctors_per_1000'].max()) * 0.2
            ) * 100
        else:
            df['inequality_score'] = 50
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.error("No data loaded. Please check database.")
    st.stop()

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/1200px-Flag_of_Kenya.svg.png", width=100)
    st.markdown("## Kenya Economic Inequality Analysis")
    st.markdown("---")
    page = st.radio("Navigate to:", ["Dashboard Overview", "County Map", "County Comparison", "SQL Query Explorer", "Top Underserved Counties"])
    st.markdown("---")
    st.markdown("### About")
    st.markdown("**Author:** Kimberly Muthoni Mwaniki  \n**Institution:** Strathmore University  \n\nAnalyzing economic inequality across Kenya's 47 counties using KNBS data.")
    st.markdown("---")
    st.markdown("### Key Findings")
    st.markdown("""
    - Electricity access is the strongest predictor of poverty reduction
    - Regional disparities are most pronounced in North Eastern and Coastal regions
    - Turkana, Mandera, and Wajir require urgent intervention
    """)

if page == "Dashboard Overview":
    st.markdown('<h1 class="main-header">Kenya County Economic Inequality Dashboard</h1>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Poverty Rate", f"{df['poverty_rate'].mean():.1f}%", delta=f"±{df['poverty_rate'].std():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Electricity Access", f"{df['electricity_access'].mean():.1f}%", delta=f"±{df['electricity_access'].std():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Literacy Rate", f"{df['literacy_rate'].mean():.1f}%", delta=f"±{df['literacy_rate'].std():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        high_poverty = len(df[df['poverty_rate'] > 50])
        st.metric("High Poverty Counties (>50%)", f"{high_poverty}", delta=f"out of 47")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h3 class="sub-header">Poverty Rate by Region</h3>', unsafe_allow_html=True)
        fig = px.box(df, x='region', y='poverty_rate', color='region', title="Poverty Rate Distribution Across Regions", labels={'poverty_rate': 'Poverty Rate (%)', 'region': 'Region'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<h3 class="sub-header">Correlation Matrix</h3>', unsafe_allow_html=True)
        corr_df = df[['poverty_rate', 'electricity_access', 'literacy_rate', 'doctors_per_1000', 'road_density']]
        corr_matrix = corr_df.corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="How Indicators Relate to Each Other")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h3 class="sub-header">Top 5 Counties (Lowest Poverty)</h3>', unsafe_allow_html=True)
        top_counties = df.nsmallest(5, 'poverty_rate')[['county_name', 'poverty_rate', 'electricity_access', 'literacy_rate']]
        st.dataframe(top_counties, use_container_width=True)
    with col2:
        st.markdown('<h3 class="sub-header">Bottom 5 Counties (Highest Poverty)</h3>', unsafe_allow_html=True)
        bottom_counties = df.nlargest(5, 'poverty_rate')[['county_name', 'poverty_rate', 'electricity_access', 'literacy_rate']]
        st.dataframe(bottom_counties, use_container_width=True)

elif page == "County Map":
    st.markdown('<h1 class="main-header">County Inequality Scores</h1>', unsafe_allow_html=True)
    st.markdown("**Inequality Score**: Composite index combining poverty rate, infrastructure access, education, and healthcare. **Lower scores = Better conditions**")
    fig = px.bar(df.sort_values('inequality_score', ascending=True), x='county_name', y='inequality_score', color='inequality_score', title="Inequality Score by County (Lower is Better)", labels={'inequality_score': 'Inequality Score', 'county_name': 'County'}, color_continuous_scale='RdYlGn_r')
    fig.update_layout(xaxis_tickangle=-45, height=600)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown('<h3 class="sub-header">County Details</h3>', unsafe_allow_html=True)
    selected_county = st.selectbox("Select a county to see detailed indicators:", df['county_name'].sort_values())
    if selected_county:
        county_data = df[df['county_name'] == selected_county].iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### {selected_county} County")
            st.markdown(f"**Region:** {county_data['region']}")
            st.markdown(f"**Inequality Score:** {county_data['inequality_score']:.1f}")
            st.markdown(f"**Population:** {county_data['population']:,}")
            st.markdown(f"**Poverty Rate:** {county_data['poverty_rate']:.1f}%")
            st.markdown(f"**Unemployment Rate:** {county_data['unemployment_rate']:.1f}%")
        with col2:
            st.markdown(f"**Electricity Access:** {county_data['electricity_access']:.1f}%")
            st.markdown(f"**Internet Access:** {county_data['internet_access']:.1f}%")
            st.markdown(f"**Literacy Rate:** {county_data['literacy_rate']:.1f}%")
            st.markdown(f"**Doctors per 1000:** {county_data['doctors_per_1000']:.3f}")
            st.markdown(f"**School Enrollment:** {county_data['school_enrollment']:.1f}%")

elif page == "County Comparison":
    st.markdown('<h1 class="main-header">Compare Two Counties</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        county1 = st.selectbox("Select first county:", df['county_name'].sort_values(), index=0)
    with col2:
        county2 = st.selectbox("Select second county:", df['county_name'].sort_values(), index=1)
    if county1 and county2:
        data1 = df[df['county_name'] == county1].iloc[0]
        data2 = df[df['county_name'] == county2].iloc[0]
        metrics = ['poverty_rate', 'electricity_access', 'literacy_rate', 'doctors_per_1000', 'road_density', 'school_enrollment']
        comparison_df = pd.DataFrame({'Metric': ['Poverty Rate (%)', 'Electricity Access (%)', 'Literacy Rate (%)', 'Doctors per 1000', 'Road Density (km/100km²)', 'School Enrollment (%)'], county1: [data1[m] for m in metrics], county2: [data2[m] for m in metrics]})
        st.dataframe(comparison_df, use_container_width=True)
        fig = go.Figure(data=[go.Bar(name=county1, x=comparison_df['Metric'], y=comparison_df[county1]), go.Bar(name=county2, x=comparison_df['Metric'], y=comparison_df[county2])])
        fig.update_layout(barmode='group', title=f"{county1} vs {county2} - Development Indicators", xaxis_title="Indicator", yaxis_title="Value", height=500)
        st.plotly_chart(fig, use_container_width=True)

elif page == "SQL Query Explorer":
    st.markdown('<h1 class="main-header">SQL Query Explorer</h1>', unsafe_allow_html=True)
    st.markdown("Write SQL queries to explore the Kenya counties database.\n\n**Available tables:** counties, demographics, infrastructure, health, education\n\n**Example Query:**\n```sql\nSELECT county_name, poverty_rate, electricity_access \nFROM counties \nJOIN demographics ON counties.county_id = demographics.county_id \nJOIN infrastructure ON counties.county_id = infrastructure.county_id \nLIMIT 10\n```")
    example_query = "SELECT c.county_name, d.poverty_rate, i.electricity_access, e.literacy_rate\nFROM counties c\nJOIN demographics d ON c.county_id = d.county_id\nJOIN infrastructure i ON c.county_id = i.county_id\nJOIN education e ON c.county_id = e.county_id\nWHERE d.year = 2023\nLIMIT 10"
    query = st.text_area("Enter your SQL query:", height=200, value=example_query)
    if st.button("Run Query", type="primary"):
        try:
            conn = get_connection()
            result = pd.read_sql_query(query, conn)
            st.success(f"Query executed successfully! {len(result)} rows returned.")
            st.dataframe(result, use_container_width=True)
            csv = result.to_csv(index=False)
            st.download_button("Download as CSV", csv, "query_results.csv", "text/csv")
            conn.close()
        except Exception as e:
            st.error(f"Error executing query: {e}")

else:
    st.markdown('<h1 class="main-header">Top 10 Most Underserved Counties</h1>', unsafe_allow_html=True)
    st.markdown("Counties ranked by a composite score combining:\n- Health access (doctors per capita, child mortality)\n- Education outcomes (literacy, dropout rates)\n- Infrastructure (electricity, roads, internet)\n- Economic indicators (poverty, unemployment)\n\nHigher score = More underserved = Needs more intervention")
    df['underserved_score'] = ((1 - df['doctors_per_1000'] / df['doctors_per_1000'].max()) * 0.3 + (df['child_mortality'] / df['child_mortality'].max()) * 0.2 + (1 - df['literacy_rate'] / 100) * 0.2 + (1 - df['electricity_access'] / 100) * 0.2 + (df['poverty_rate'] / 100) * 0.1) * 100
    underserved = df.nlargest(10, 'underserved_score')[['county_name', 'region', 'poverty_rate', 'electricity_access', 'literacy_rate', 'doctors_per_1000', 'child_mortality', 'underserved_score']].round(2)
    st.dataframe(underserved, use_container_width=True)
    fig = px.bar(underserved, x='county_name', y='underserved_score', color='region', title="Most Underserved Counties (Higher Score = More Underserved)", labels={'underserved_score': 'Underserved Score', 'county_name': 'County'}, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown('<h3 class="sub-header">Detailed Analysis of Top 5 Most Underserved</h3>', unsafe_allow_html=True)
    top_underserved = underserved.head(5)['county_name'].tolist()
    detailed_data = df[df['county_name'].isin(top_underserved)]
    for county in top_underserved:
        county_data = detailed_data[detailed_data['county_name'] == county].iloc[0]
        with st.expander(f"{county} - Detailed Analysis"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Key Challenges:**")
                st.markdown(f"- High poverty rate: {county_data['poverty_rate']:.1f}%")
                st.markdown(f"- Low electricity access: {county_data['electricity_access']:.1f}%")
                st.markdown(f"- Limited doctors: {county_data['doctors_per_1000']:.3f} per 1000")
                st.markdown(f"- High child mortality: {county_data['child_mortality']:.1f} per 1000")
            with col2:
                st.markdown("**Recommended Interventions:**")
                st.markdown("1. Infrastructure development (electricity, roads)")
                st.markdown("2. Healthcare facility expansion")
                st.markdown("3. Educational support programs")
                st.markdown("4. Economic empowerment initiatives")
