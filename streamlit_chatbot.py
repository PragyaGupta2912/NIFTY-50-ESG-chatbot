import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API key

openai.api_key = "enter your API key"

# Load data
data = pd.read_csv('data.csv')

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
        response_placeholder.text(response)
    else:
        response_placeholder.text("Please enter a question.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chat History")
for message in st.session_state.messages:
    st.write(message)

if user_query:
    st.session_state.messages.append(f"User: {user_query}")
    st.session_state.messages.append(f"Assistant: {response}")
