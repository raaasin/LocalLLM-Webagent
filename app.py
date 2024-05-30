import streamlit as st
import requests
import json


# Function to stream responses from the Mistral model
def stream_mistral_response(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": "mistral", "prompt": prompt}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, stream=True)

    if response.status_code == 200:
        result = ""
        for line in response.iter_lines():
            if line:
                line_data = json.loads(line.decode('utf-8'))
                result += line_data.get("response", "")
        return result
    else:
        st.error("Error: " + str(response.status_code))

st.title("Mistral Model Interaction")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I am your Llm web agent connected to internet. AMA! 😊"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg= stream_mistral_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    