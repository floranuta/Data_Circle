import streamlit as st
import pandas as pd
import numpy as np
from predict import predict

st.write("""
# Water Pump Status Prediction App

This app predicts the functionality of water pump in Tanzania!

Data obtained from the [Data Driven](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/23/).
""")

st.sidebar.header('User Input Features')


# Collects user input features into dataframe

def user_input_features():
    pump_age = st.sidebar.slider('Age of pump (years)', 0, 55, 20)
    gps_height = st.sidebar.slider('Height (m)', -90, 10, 2770)
    region = st.sidebar.selectbox('Region',('Iringa','Mara', 'Manyara', 'Mtwara', 'Kagera', 'Tanga',
                                            'Shinyanga', 'Tabora', 'Pwani', 'Ruvuma', 'Kilimanjaro', 'Rukwa',
                                            'Mwanza', 'Kigoma', 'Lindi', 'Dodoma', 'Arusha', 'Mbeya',
                                            'Singida', 'Morogoro', 'Dar es Salaam'))
    water_quantity = st.sidebar.selectbox('Water quantity',('enough', 'insufficient', 'dry', 'seasonal', 'unknown'))
    payment_type = st.sidebar.selectbox('Payment type', ('Never pay', 'per bucket', 'monthly', 'annually', 'unknown', 
                                                   'on failure', 'other'))
    extraction_type = st.sidebar.selectbox('Extraction type', ('gravity', 'handpump', 'motorpump', 'other', 'rope pump',
                                                                'submersible', 'wind-powered'))
    source = st.sidebar.selectbox('source', ('spring', 'rainwater harvesting', 'dam', 'machine dbh', 'other',
                                            'shallow well', 'river', 'hand dtw', 'lake', 'unknown'))
    basin = st.sidebar.selectbox('basin', ('Lake Nyasa', 'Lake Victoria', 'Pangani',
                                            'Ruvuma / Southern Coast', 'Internal', 'Lake Tanganyika',
                                            'Wami / Ruvu', 'Rufiji', 'Lake Rukwa'))
    
    data = {
            'region': region,
            'pump_age': pump_age,
            'gps_height': gps_height,
            'quantity_group': water_quantity,
            'payment_type': payment_type,
            'extraction_type_class': extraction_type,
            'source': source,
            'basin': basin
            }
    
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()


# Displays the user input features
st.subheader('User input features')
st.write(input_df)


prediction, prediction_proba = predict(input_df)


st.subheader('Prediction')
st.write(prediction)

st.subheader('Prediction Probability')
st.write(prediction_proba)