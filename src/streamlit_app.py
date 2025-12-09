import streamlit as st

analysis_page = st.Page("analysis_page.py", title="Analysis", icon=":material/analytics:")
prediction_page = st.Page("prediction_page.py", title="Prediction", icon=":material/smart_toy:")

pg = st.navigation([analysis_page, prediction_page])
st.set_page_config(page_title="Water Pump Dashboard", page_icon=":material/dashboard:")
pg.run()