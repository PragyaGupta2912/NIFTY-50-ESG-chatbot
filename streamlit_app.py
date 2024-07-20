import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API key
openai.api_key = 'enter your API Key'

# Load data
data = pd.read_csv("./data.csv")

# Set page configuration
st.set_page_config(page_title="ESG Dashboard Chatbot", page_icon="💬", layout="wide")

# Display title and description
st.title("ESG Dashboard NIFTY 50 💬")
st.markdown("Welcome to the ESG Dashboard chatbot. Ask questions about the filtered data to get insights.")

# Load and display data
st.write("### Data Used in the Dashboard")
st.dataframe(data)

# Simulate interactions
st.sidebar.header("Filter Options")
selected_industry = st.sidebar.selectbox("Select Industry", data['Industry'].unique())
min_risk_score = st.sidebar.slider("Minimum ESG Risk Score", min_value=0, max_value=100, value=10)

# Filter data based on interactions
filtered_data = data[(data['Industry'] == selected_industry) & (data['Total ESG Risk score'] >= min_risk_score)]
st.write("### Filtered Data")
st.dataframe(filtered_data)

# Placeholder for displaying the chatbot response
response_placeholder = st.empty()

# Function to generate chatbot response
def generate_response(filtered_data, user_query):
    prompt = f"Data: {filtered_data.to_dict()}\nUser: {user_query}\nAssistant:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that provides answers based on the data."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response['choices'][0]['message']['content'].strip()
    return answer

# Input for user queries
user_query = st.text_input("Ask a question about the filtered data:")

# Button to generate response
if st.button("Ask"):
    if user_query:
        response = generate_response(filtered_data, user_query)
        response_placeholder.markdown(f"**Response:** {response}")
    else:
        response_placeholder.text("Please enter a question.")

# Add some styling
st.markdown("""
<style>
.stButton button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 16px;
}

.stTextInput input {
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
    background-color: #f8f8f8;
    font-size: 16px;
    color: black;  /* Set text color to black */
}

.css-1oe5cao {
    margin-top: 20px;
}

.stAlert p {
    font-size: 16px;
    color: #333;
}

.stMarkdown p {
    font-size: 16px;
    color: #333;
}

body {
    background-color: #f0f2f6;  /* Set the background color */
}
</style>
""", unsafe_allow_html=True)