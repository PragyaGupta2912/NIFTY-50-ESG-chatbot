import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API key
openai.api_key = 'enter API Key'

# Load data
data = pd.read_csv("./data.csv")

# Display data in Streamlit
st.title("ESG Dashboard NIFTY 50")
st.write("Here is the data used in the dashboard:")
st.dataframe(data)

# Simulate interactions
selected_industry = st.selectbox("Select Industry", data['Industry'].unique())
min_risk_score = st.slider("Minimum ESG Risk Score", min_value=0, max_value=100, value=10)

# Filter data based on interactions
filtered_data = data[(data['Industry'] == selected_industry) & (data['Total ESG Risk score'] >= min_risk_score)]
st.write("Filtered Data:")
st.dataframe(filtered_data)

# Placeholder for displaying the description
description_placeholder = st.empty()

# Function to generate description
def generate_description(filtered_data):
    prompt = f"Generate a description for the following filtered data: {filtered_data.to_dict()}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that generates descriptions for data."},
            {"role": "user", "content": prompt}
        ]
    )
    description = response['choices'][0]['message']['content'].strip()
    return description

# Button to generate description
if st.button("Generate Description"):
    description = generate_description(filtered_data)
    description_placeholder.text(description)