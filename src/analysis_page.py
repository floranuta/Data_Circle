# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import sqlite3
from sqlalchemy import create_engine
from datetime import datetime

st.set_page_config(layout="wide", page_title="Water Pump Dashboard")

# ---- Helper functions ----
@st.cache_data
def load_data(values_path: str, labels_path: str):
    vals = pd.read_csv(values_path, parse_dates=['date_recorded'], dayfirst=True, low_memory=False)
    labs = pd.read_csv(labels_path, low_memory=False)
    # Ensure id column name consistent
    if 'id' not in vals.columns:
        vals.rename(columns={vals.columns[0]:'id'}, inplace=True)
    merged = pd.merge(vals, labs, on='id', how='left')
    return merged

def create_sqlite_from_df(df: pd.DataFrame, db_conn):
    df.to_sql('water_pumps', db_conn, if_exists='replace', index=False)

def run_sql(query: str, db_conn):
    return pd.read_sql_query(query, db_conn)

# ---- Load data ----
DATA_VALUES = "data/training_set_values.csv"
DATA_LABELS = "data/training_set_labels.csv"

st.title("💧 Water Pump — Streamlit Dashboard")
st.markdown("Interactive EDA, mapping, and SQL for the water pump dataset.")

with st.spinner("Loading data..."):
    df = load_data(DATA_VALUES, DATA_LABELS)

# Quick cleaning / cast
df['construction_year'] = pd.to_numeric(df['construction_year'], errors='coerce')
df['population'] = pd.to_numeric(df['population'], errors='coerce')
# normalize boolean-like cols if necessary
if 'public_meeting' in df.columns:
    df['public_meeting'] = df['public_meeting'].replace({True:'True', False:'False'})

# ---- Sidebar filters ----
st.sidebar.header("Filters")
regions = ["All"] + sorted(df['region'].dropna().unique().tolist())
region_sel = st.sidebar.selectbox("Region", regions)
status_options = ["All"] + sorted(df['status_group'].dropna().unique().tolist())
status_sel = st.sidebar.selectbox("Pump status", status_options)
min_year = int(df['date_recorded'].dt.year.min())
max_year = int(df['date_recorded'].dt.year.max())
year_range = st.sidebar.slider("Recorded year", min_year, max_year, (min_year, max_year))

# apply filters
df_filtered = df.copy()
if region_sel != "All":
    df_filtered = df_filtered[df_filtered['region'] == region_sel]
if status_sel != "All":
    df_filtered = df_filtered[df_filtered['status_group'] == status_sel]
df_filtered = df_filtered[(df_filtered['date_recorded'].dt.year >= year_range[0]) &
                          (df_filtered['date_recorded'].dt.year <= year_range[1])]

# ---- KPIs ----
st.header("Key Metrics")
col1, col2, col3, col4 = st.columns([1,1,1,1])

total_pumps = len(df_filtered)
functional = (df_filtered['status_group'] == 'functional').sum()
nonfunctional = (df_filtered['status_group'] == 'non functional').sum()
needs_repair = (df_filtered['status_group'] == 'functional needs repair').sum()

functional_pct = 0 if total_pumps==0 else round(functional/total_pumps*100,2)
nonfunctional_pct = 0 if total_pumps==0 else round(nonfunctional/total_pumps*100,2)
repair_pct = 0 if total_pumps==0 else round(needs_repair/total_pumps*100,2)

col1.metric("Total pumps", f"{total_pumps:,}")
# col2.metric("Functional %", f"{functional_pct}%", delta=f"{functional - (total_pumps-functional):,}")
col2.metric("Functional %", f"{functional_pct}%")
col3.metric("Non functional %", f"{nonfunctional_pct}%")
col4.metric("Needs repair %", f"{repair_pct}%")

# ---- Map view (pydeck) ----
st.subheader("Map — Pump Locations")
map_cols = st.columns([3,1])
with map_cols[0]:
    # sample to speed up when huge
    map_df = df_filtered.dropna(subset=['latitude','longitude'])
    if len(map_df) == 0:
        st.info("No coordinate data available for selected filters.")
    else:
        sample = map_df.sample(n=min(5000, len(map_df)), random_state=42)
        # color coding for status
        status_to_color = {
            'functional': [0, 200, 0],
            'functional needs repair': [255, 165, 0],
            'non functional': [200, 0, 0]
        }
        sample['color'] = sample['status_group'].apply(
        lambda x: status_to_color.get(x, [100, 100, 100])
        )
        view_state = pdk.ViewState(
            latitude=sample['latitude'].mean(),
            longitude=sample['longitude'].mean(),
            zoom=6,
            pitch=0
        )
        scatter = pdk.Layer(
            "ScatterplotLayer",
            data=sample,
            get_position='[longitude, latitude]',
            get_fill_color='color',
            get_radius=50,
            pickable=True,
            radius_min_pixels=2,
            radius_max_pixels=8,
        )
        tooltip = {"html": "<b>id:</b> {id} <br/> <b>status:</b> {status_group} <br/> <b>subvillage:</b> {subvillage}", "style": {"color": "white"}}
        r = pdk.Deck(layers=[scatter], initial_view_state=view_state, tooltip=tooltip)
        st.pydeck_chart(r)

with map_cols[1]:
    st.markdown("**Map controls**")
    st.write(f"Showing {len(sample):,} points (sample). Change filters to zoom in.")
    if st.button("Reset filters"):
        st.experimental_rerun()

# ---- Charts ----
st.subheader("Charts & Distributions")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Status counts bar chart
    st.markdown("**Pump status distribution**")
    status_counts = df_filtered['status_group'].value_counts().reset_index()
    status_counts.columns = ['status_group', 'count']
    fig1 = px.bar(status_counts, x='status_group', y='count', color='status_group',
                  labels={'count':'Number of pumps', 'status_group':'Status'},
                  title="Number of pumps by status")
    st.plotly_chart(fig1, use_container_width=True)

    # Pumps by region stacked
    st.markdown("**Pumps by region and status**")
    region_status = df_filtered.groupby(['region','status_group']).size().reset_index(name='count')
    fig2 = px.bar(region_status, x='region', y='count', color='status_group', barmode='stack',
                  title="Pumps by region and status")
    st.plotly_chart(fig2, use_container_width=True)

with chart_col2:
    st.markdown("**Numeric distributions**")
    # population histogram
    fig3 = px.histogram(df_filtered, x='population', nbins=50, title='Population distribution (per pump)')
    st.plotly_chart(fig3, use_container_width=True)
    # construction year vs status (box)
    fig4 = px.box(df_filtered[df_filtered['construction_year'].notna()], x='status_group', y='construction_year',
                  title='Construction year by pump status')
    st.plotly_chart(fig4, use_container_width=True)

# ---- SQL Query interface (sqlite) ----
st.subheader("Run SQL queries (SQLite)")
st.markdown("We create a temporary SQLite DB from the filtered DataFrame and run SELECT queries. Use predefined queries or write your own (SELECT only).")

# create sqlite in memory
conn = sqlite3.connect(":memory:")
create_sqlite_from_df(df_filtered.fillna(''), conn)

pre_q = st.selectbox("Select a predefined query", [
    "Choose...",
    "Total pumps by region",
    "Functional % by region",
    "Top 10 extraction types",
    "Average population by region",
    "Pumps by management_group"
])

if pre_q == "Total pumps by region":
    q = "SELECT region, COUNT(*) AS total FROM water_pumps GROUP BY region ORDER BY total DESC;"
elif pre_q == "Functional % by region":
    q = """
    SELECT region,
      SUM(CASE WHEN status_group='functional' THEN 1 ELSE 0 END)*100.0/COUNT(*) AS functional_pct
    FROM water_pumps
    GROUP BY region
    ORDER BY functional_pct DESC;
    """
elif pre_q == "Top 10 extraction types":
    q = "SELECT extraction_type, COUNT(*) AS cnt FROM water_pumps GROUP BY extraction_type ORDER BY cnt DESC LIMIT 10;"
elif pre_q == "Average population by region":
    q = "SELECT region, AVG(CAST(population AS INTEGER)) AS avg_pop FROM water_pumps GROUP BY region ORDER BY avg_pop DESC;"
elif pre_q == "Pumps by management_group":
    q = "SELECT management_group, COUNT(*) AS cnt FROM water_pumps GROUP BY management_group ORDER BY cnt DESC;"
else:
    q = ""

custom_q = st.text_area("Or write a custom SQL SELECT query (reads from table `water_pumps`):", value=q if q else "")

if st.button("Run SQL"):
    try:
        if not custom_q.strip().lower().startswith("select"):
            st.error("Only SELECT queries allowed.")
        else:
            res = run_sql(custom_q, conn)
            st.dataframe(res)
            csv = res.to_csv(index=False).encode('utf-8')
            st.download_button("Download SQL result as CSV", csv, file_name="sql_result.csv", mime="text/csv")
    except Exception as e:
        st.error(f"SQL error: {e}")

# ---- Data download and show sample ----
st.subheader("Data sample & download")
st.dataframe(df_filtered.sample(n=min(100, len(df_filtered)), random_state=42))
csv_all = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download filtered data (CSV)", csv_all, file_name="filtered_data.csv", mime="text/csv")