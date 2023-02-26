import streamlit as st
from DataUtils import predict_price
import pandas as pd

st.set_page_config(page_title="California Housing Price Prediction", page_icon=":house_with_garden:",
                   initial_sidebar_state="expanded")

placeholder = st.empty()
placeholder.title("California Housing Price Prediction")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df = df.drop('median_house_value', axis=1, inplace=True)

    list_price = [0 for i in range(len(df))]
    with st.spinner("Predicting the price"):
        df['predicted_median_house_value'] = df.apply(
            lambda row: predict_price(row['longitude'], row['latitude'], row['housing_median_age'], row['total_rooms'],
                                      row['total_bedrooms'], row['population'], row['households'], row['median_income'],
                                      row['ocean_proximity']), axis=1)

    st.markdown("### Predicted Data")
    st.dataframe(df.head())

with st.expander("Enter the details manually"):
    form = st.form("Data")
    form.markdown("### Enter the details")
    longitude = form.number_input("longitude")
    latitude = form.number_input("latitude")
    housing_median_age = form.number_input("housing_median_age")
    total_rooms = form.number_input("total_rooms", min_value=1)
    total_bedrooms = form.number_input("total_bedrooms", min_value=1)
    population = form.number_input("population")
    households = form.number_input("households", min_value=1)
    median_income = form.number_input("median_income")
    ocean_proximity = form.selectbox("ocean_proximity", ["INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"])

    submitted = form.form_submit_button("Submit")
    if submitted:
        price = predict_price(longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population,
                              households, median_income, ocean_proximity)
        st.markdown("### Predicted Value: $" + str(price[0].round(3)))
