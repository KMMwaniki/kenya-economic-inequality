# =====================================================
# Kenya County Economic Inequality Analysis
# Streamlit Dashboard
# Author: Kimberly Muthoni Mwaniki
# Strathmore University
# =====================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Kenya County Economic Inequality Analysis",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection function
@st.cache_resource
def get_connection():
    return sqlite3.connect('kenya_counties.db')

# Load data with caching
@st.cache_data
def load_data():
    conn = get_connection()
    
    # Load all tables
    counties = pd.read_sql_query("SELECT * FROM counties", conn)
    demographics = pd.read_sql_query("SELECT * FROM demographics WHERE year = 2023", conn)
    infrastructure = pd.read_sql_query("SELECT * FROM infrastructure WHERE year = 2023", conn)
    health = pd.read_sql_query("SELECT * FROM health WHERE year = 2023", conn)
    education = pd.read_sql_query("SELECT * FROM education WHERE year = 2023", conn)
    
    # Remove duplicate columns before merging
    infrastructure = infrastructure.drop(columns=['year', 'id'], errors='ignore')
    health = health.drop(columns=['year', 'id'], errors='ignore')
    education = education.drop(columns=['year', 'id'], errors='ignore')
    demographics = demographics.drop(columns=['year', 'id'], errors='ignore')
    
    # Merge all data
    df = counties.merge(demographics, on='county_id')
    df = df.merge(infrastructure, on='county_id')
    df = df.merge(health, on='county_id')
    df = df.merge(education, on='county_id')
    
    # Calculate inequality score (composite index)
    df['inequality_score'] = (
        (df['poverty_rate'] / 100) * 0.3 +
        (1 - df['electricity_access'] / 100) * 0.3 +
        (1 - df['literacy_rate'] / 100) * 0.2 +
        (1 - df['doctors_per_1000'] / df['doctors_per_1000'].max()) * 0.2
    ) * 100
    
    conn.close()
    return df

# Load data
df = load_data()

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/1200px-Flag_of_Kenya.svg.png", 
             width=100)
    st.markdown("## Kenya Economic Inequality Analysis")
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate to:",
        ["🏠 Dashboard Overview", 
         "🗺️ County Map", 
         "📊 County Comparison",
         "🔍 SQL Query Explorer",
         "📈 Top Underserved Counties"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This dashboard analyzes economic inequality across Kenya's 47 counties using data from:
    - Kenya National Bureau of Statistics
    - Ministry of Health
    - Ministry of Education
    - Kenya Power & Infrastructure Data
    """)
    
    st.markdown("---")
    st.markdown("### Key Findings")
    st.markdown("""
    - **Electricity access** is the strongest predictor of poverty reduction
    - **Regional disparities** are most pronounced in North Eastern and Coastal regions
    - **Education alone** doesn't guarantee poverty reduction without infrastructure
    - **Turkana, Mandera, and Wajir** counties require urgent multi-sectoral intervention
    """)

# Main content
if page == "🏠 Dashboard Overview":
    st.markdown('<h1 class="main-header">Kenya County Economic Inequality Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Poverty Rate", f"{df['poverty_rate'].mean():.1f}%", 
                  delta=f"±{df['poverty_rate'].std():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Electricity Access", f"{df['electricity_access'].mean():.1f}%",
                  delta=f"±{df['electricity_access'].std():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Literacy Rate", f"{df['literacy_rate'].mean():.1f}%",
                  delta=f"±{df['literacy_rate'].std():.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Counties with High Poverty (>50%)", 
                  f"{len(df[df['poverty_rate'] > 50])}",
                  delta=f"out of 47 counties")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Regional comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">Poverty Rate by Region</h3>', 
                    unsafe_allow_html=True)
        fig = px.box(df, x='region', y='poverty_rate', color='region',
                     title="Poverty Rate Distribution Across Regions",
                     labels={'poverty_rate': 'Poverty Rate (%)', 'region': 'Region'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="sub-header">Key Indicators Correlation</h3>', 
                    unsafe_allow_html=True)
        corr_df = df[['poverty_rate', 'electricity_access', 'literacy_rate', 
                      'doctors_per_1000', 'road_density']]
        corr_matrix = corr_df.corr()
        
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                        title="Correlation Matrix of Development Indicators")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top and bottom performers
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">Top 5 Counties (Lowest Poverty)</h3>', 
                    unsafe_allow_html=True)
        top_counties = df.nsmallest(5, 'poverty_rate')[['county_name', 'poverty_rate', 
                                                         'electricity_access', 'literacy_rate']]
        st.dataframe(top_counties, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="sub-header">Bottom 5 Counties (Highest Poverty)</h3>', 
                    unsafe_allow_html=True)
        bottom_counties = df.nlargest(5, 'poverty_rate')[['county_name', 'poverty_rate', 
                                                          'electricity_access', 'literacy_rate']]
        st.dataframe(bottom_counties, use_container_width=True)

elif page == "🗺️ County Map":
    st.markdown('<h1 class="main-header">County Map - Inequality Score</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Inequality Score**: Composite index combining poverty rate, infrastructure access, 
    education, and healthcare. Higher scores indicate greater inequality/need.
    """)
    
    # Bar chart for inequality scores
    fig = px.bar(df.sort_values('inequality_score', ascending=True),
                 x='county_name', y='inequality_score',
                 color='inequality_score',
                 title="County Inequality Score (Lower is Better)",
                 labels={'inequality_score': 'Inequality Score', 
                        'county_name': 'County'},
                 color_continuous_scale='RdYlGn_r')
    
    fig.update_layout(xaxis_tickangle=-45,
                      height=600,
                      showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # County selector for detailed view
    st.markdown("---")
    st.markdown('<h3 class="sub-header">County Details</h3>', unsafe_allow_html=True)
    
    selected_county = st.selectbox("Select a county to see detailed indicators:", 
                                   df['county_name'].sort_values())
    
    if selected_county:
        county_data = df[df['county_name'] == selected_county].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {selected_county} County")
            st.markdown(f"**Region:** {county_data['region']}")
            st.markdown(f"**Inequality Score:** {county_data['inequality_score']:.1f}")
            st.markdown(f"**Population:** {county_data['population']:,}")
            
            st.markdown("#### Economic Indicators")
            st.markdown(f"- Poverty Rate: {county_data['poverty_rate']:.1f}%")
            st.markdown(f"- Unemployment Rate: {county_data['unemployment_rate']:.1f}%")
            st.markdown(f"- Gini Coefficient: {county_data['gini_coefficient']:.3f}")
        
        with col2:
            st.markdown("#### Infrastructure")
            st.markdown(f"- Electricity Access: {county_data['electricity_access']:.1f}%")
            st.markdown(f"- Internet Access: {county_data['internet_access']:.1f}%")
            st.markdown(f"- Road Density: {county_data['road_density']:.1f} km/100km²")
            
            st.markdown("#### Health & Education")
            st.markdown(f"- Literacy Rate: {county_data['literacy_rate']:.1f}%")
            st.markdown(f"- Doctors per 1000: {county_data['doctors_per_1000']:.3f}")
            st.markdown(f"- School Enrollment: {county_data['school_enrollment']:.1f}%")
        
        # Radar chart for selected county
        metrics = ['poverty_rate', 'electricity_access', 'literacy_rate', 
                   'doctors_per_1000', 'road_density']
        normalized = []
        for metric in metrics:
            if metric == 'poverty_rate':
                normalized.append((1 - (county_data[metric] - df[metric].min()) / 
                                   (df[metric].max() - df[metric].min())) * 100)
            else:
                normalized.append(((county_data[metric] - df[metric].min()) / 
                                   (df[metric].max() - df[metric].min())) * 100)
        
        fig = go.Figure(data=go.Scatterpolar(
            r=normalized,
            theta=['Poverty Rate\n(Inverted)', 'Electricity Access', 
                   'Literacy Rate', 'Doctors per 1000', 'Road Density'],
            fill='toself',
            name=selected_county
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="County Performance Profile (100 = Best in Kenya)"
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "📊 County Comparison":
    st.markdown('<h1 class="main-header">Compare Two Counties</h1>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        county1 = st.selectbox("Select first county:", df['county_name'].sort_values(), 
                               index=0)
    
    with col2:
        county2 = st.selectbox("Select second county:", df['county_name'].sort_values(), 
                               index=1)
    
    if county1 and county2:
        data1 = df[df['county_name'] == county1].iloc[0]
        data2 = df[df['county_name'] == county2].iloc[0]
        
        metrics = ['poverty_rate', 'electricity_access', 'literacy_rate', 
                  'doctors_per_1000', 'road_density', 'school_enrollment']
        
        comparison_df = pd.DataFrame({
            'Metric': ['Poverty Rate (%)', 'Electricity Access (%)', 
                      'Literacy Rate (%)', 'Doctors per 1000', 
                      'Road Density (km/100km²)', 'School Enrollment (%)'],
            county1: [data1[m] for m in metrics],
            county2: [data2[m] for m in metrics]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        fig = go.Figure(data=[
            go.Bar(name=county1, x=comparison_df['Metric'], y=comparison_df[county1]),
            go.Bar(name=county2, x=comparison_df['Metric'], y=comparison_df[county2])
        ])
        
        fig.update_layout(barmode='group', 
                          title=f"{county1} vs {county2} - Development Indicators",
                          xaxis_title="Indicator",
                          yaxis_title="Value")
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "🔍 SQL Query Explorer":
    st.markdown('<h1 class="main-header">SQL Query Explorer</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Write SQL queries to explore the Kenya counties database. 
    Available tables: counties, demographics, infrastructure, health, education
    """)
    
    query_type = st.selectbox(
        "Select a predefined query or write your own:",
        ["Custom Query", 
         "Top 10 counties by poverty rate",
         "Counties with electricity access > 70%",
         "Regions with highest average literacy",
         "Correlation between doctors and poverty",
         "Infrastructure index ranking"]
    )
    
    if query_type == "Custom Query":
        query = st.text_area("Enter your SQL query:", height=150)
        if st.button("Execute Query"):
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
        queries = {
            "Top 10 counties by poverty rate": """
                SELECT c.county_name, d.poverty_rate, c.region
                FROM counties c
                JOIN demographics d ON c.county_id = d.county_id
                WHERE d.year = 2023
                ORDER BY d.poverty_rate DESC
                LIMIT 10;
            """,
            "Counties with electricity access > 70%": """
                SELECT c.county_name, i.electricity_access, d.poverty_rate
                FROM counties c
                JOIN infrastructure i ON c.county_id = i.county_id
                JOIN demographics d ON c.county_id = d.county_id
                WHERE i.year = 2023 AND i.electricity_access > 70
                ORDER BY i.electricity_access DESC;
            """,
            "Regions with highest average literacy": """
                SELECT c.region, AVG(e.literacy_rate) as avg_literacy,
                       AVG(d.poverty_rate) as avg_poverty
                FROM counties c
                JOIN education e ON c.county_id = e.county_id
                JOIN demographics d ON c.county_id = d.county_id
                WHERE e.year = 2023
                GROUP BY c.region
                ORDER BY avg_literacy DESC;
            """,
            "Correlation between doctors and poverty": """
                SELECT c.county_name, h.doctors_per_1000, d.poverty_rate,
                       CASE 
                           WHEN h.doctors_per_1000 >= 0.3 THEN 'Good'
                           WHEN h.doctors_per_1000 >= 0.2 THEN 'Fair'
                           ELSE 'Poor'
                       END as healthcare_status
                FROM counties c
                JOIN health h ON c.county_id = h.county_id
                JOIN demographics d ON c.county_id = d.county_id
                WHERE h.year = 2023
                ORDER BY h.doctors_per_1000 DESC;
            """,
            "Infrastructure index ranking": """
                SELECT c.county_name,
                       ROUND((i.electricity_access * 0.4 + 
                              i.internet_access * 0.3 + 
                              i.road_density / (SELECT MAX(road_density) FROM infrastructure) * 0.3), 1) as infra_score
                FROM counties c
                JOIN infrastructure i ON c.county_id = i.county_id
                WHERE i.year = 2023
                ORDER BY infra_score DESC;
            """
        }
        
        query = queries[query_type]
        st.code(query, language="sql")
        
        if st.button("Execute Query"):
            try:
                conn = get_connection()
                result = pd.read_sql_query(query, conn)
                st.success(f"Query executed successfully! {len(result)} rows returned.")
                st.dataframe(result, use_container_width=True)
                
                if len(result.columns) >= 2:
                    st.markdown("### Quick Visualization")
                    fig = px.bar(result, x=result.columns[0], y=result.columns[1],
                                 title=f"{result.columns[1]} by {result.columns[0]}")
                    st.plotly_chart(fig, use_container_width=True)
                conn.close()
            except Exception as e:
                st.error(f"Error executing query: {e}")

else:  # Top Underserved Counties
    st.markdown('<h1 class="main-header">Top 10 Most Underserved Counties</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Counties ranked by a composite score combining:
    - Health access (doctors per capita, child mortality)
    - Education outcomes (literacy, dropout rates)
    - Infrastructure (electricity, roads, internet)
    - Economic indicators (poverty, unemployment)
    """)
    
    df['underserved_score'] = (
        (1 - df['doctors_per_1000'] / df['doctors_per_1000'].max()) * 0.3 +
        (df['child_mortality'] / df['child_mortality'].max()) * 0.2 +
        (1 - df['literacy_rate'] / 100) * 0.2 +
        (1 - df['electricity_access'] / 100) * 0.2 +
        (df['poverty_rate'] / 100) * 0.1
    ) * 100
    
    underserved = df.nlargest(10, 'underserved_score')[
        ['county_name', 'region', 'poverty_rate', 'electricity_access', 
         'literacy_rate', 'doctors_per_1000', 'child_mortality', 'underserved_score']
    ].round(2)
    
    st.dataframe(underserved, use_container_width=True)
    
    fig = px.bar(underserved, x='county_name', y='underserved_score',
                 color='region',
                 title="Most Underserved Counties (Higher Score = More Underserved)",
                 labels={'underserved_score': 'Underserved Score', 
                        'county_name': 'County'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Detailed Indicators for Most Underserved Counties")
    
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
            
            with col2:
                st.markdown("**Recommended Interventions:**")
                st.markdown("1. Infrastructure development (electricity, roads)")
                st.markdown("2. Healthcare facility expansion")
                st.markdown("3. Educational support programs")
                st.markdown("4. Economic empowerment initiatives")