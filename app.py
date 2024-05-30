import streamlit as st
import requests
import json


global chat_history
chat_history = []

# Function to stream responses from the Mistral model
def stream_mistral_response():
    url = "http://localhost:11434/api/chat"
    payload = {"model": "mistral", "messages": chat_history}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, stream=True)

    if response.status_code == 200:
        content = ""
        total = " "
        for line in response.iter_lines():
            if line:
                line_data = json.loads(line.decode('utf-8'))
                content = line_data.get("message", {}).get("content", "")
                total+=content
                yield content
        chat_history.append({
            "role": "assistant",
            "content": total
        })

    else:
        st.error("Error: " + str(response.status_code))

st.title("Mistral")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I am your Llm web agent connected to internet. AMA! 😊"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    chat_history.append({
      "role": "user",
      "content": prompt
    })
    print(chat_history)
    with st.chat_message("assistant"):
        response = st.write_stream(stream_mistral_response())
    st.session_state.messages.append({"role": "assistant", "content": response})
