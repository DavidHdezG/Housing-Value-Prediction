import streamlit as st
from DataUtils import predict_price, to_dataframe
import pandas as pd

st.set_page_config(page_title="California Housing Price Prediction", page_icon=":house_with_garden:",
                   initial_sidebar_state="expanded")

placeholder = st.empty()
placeholder.title("California Housing Price Prediction")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df.drop('median_house_value', axis=1)

    with st.spinner("Predicting the price"):
        df['predicted_median_house_value'] = predict_price(df)

    st.markdown("### Predicted Data")
    st.dataframe(df)

with st.expander("Enter the details manually"):
    form = st.form("Data")
    form.markdown("### Enter the details")
    longitude = form.number_input("longitude", min_value=-124.5, max_value=-114.5)
    latitude = form.number_input("latitude", min_value=32.5, max_value=42.5)
    housing_median_age = form.number_input("housing_median_age",min_value=0.0)
    total_rooms = form.number_input("total_rooms", min_value=1)
    total_bedrooms = form.number_input("total_bedrooms", min_value=1)
    population = form.number_input("population", min_value=0)
    households = form.number_input("households", min_value=1)
    median_income = form.number_input("median_income",min_value=0.0)
    ocean_proximity = form.selectbox("ocean_proximity", ["INLAND", "NEAR OCEAN", "NEAR BAY", "ISLAND"])

    submitted = form.form_submit_button("Submit")
    if submitted:
        price = predict_price(
            to_dataframe(longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population,
                         households, median_income, ocean_proximity))
        st.markdown("### Predicted Value: $" + str(price[0].round(3)))

footer = """<style>
a:link , a:visited{
color: white;
background-color: transparent;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0d1117;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p style='display: block; text-align: center;'>David Eduardo Hernández García - 338953</p>
<p> <a style='display: block; text-align: center;' href="https://github.com/DavidHdezG/Housing-Value-Prediction">Repositorio</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
