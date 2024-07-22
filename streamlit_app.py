import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API key
openai.api_key = 'enter your API Key'

# Load data
data = pd.read_csv("./data.csv")

st.set_page_config(page_title="ESG Dashboard Chatbot", page_icon="💬", layout="wide")

st.title("ESG Dashboard NIFTY 50 💬")
st.markdown("Welcome to the ESG Dashboard chatbot. Ask questions about the filtered data to get insights.")

st.write("### Data Used in the Dashboard")
st.dataframe(data)

st.sidebar.header("Filter Options")
selected_industry = st.sidebar.selectbox("Select Industry", data['Industry'].unique())
min_risk_score = st.sidebar.slider("Minimum ESG Risk Score", min_value=0, max_value=100, value=10)

filtered_data = data[(data['Industry'] == selected_industry) & (data['Total ESG Risk score'] >= min_risk_score)]
st.write("### Filtered Data")
st.dataframe(filtered_data)

if "response" not in st.session_state:
    st.session_state.response = ""

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
        st.session_state.response = generate_response(filtered_data, user_query)
    else:
        st.session_state.response = "Please enter a question."

# Display the response
if st.session_state.response:
    st.markdown(f"**Response:** {st.session_state.response}")

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
    background-color: #333;  /* Dark background */
    color: white;  /* White text */
    font-size: 16px;
}

.css-1oe5cao {
    margin-top: 20px;
}

.stAlert p, .stMarkdown p {
    font-size: 16px;
    color: #d1d1d1;  /* Lighter text color for better readability */
}

body {
    background-color: #1e1e1e;  /* Dark background */
}

.stMarkdown h3, .stMarkdown h4 {
    color: #4CAF50;  /* Set the header color */
}

.response-container {
    background-color: #2c2c2c;  /* Darker background for the response box */
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    color: #d1d1d1;  /* Light text color for readability */
    font-size: 16px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)