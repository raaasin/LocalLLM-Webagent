import streamlit as st
from disai.disai_jazz import Agent, Task, Mistral, SequentialFlow, InputType, OutputType



#Define agent properties
expertise = "Webagent"
task = Task("Search web and answer accordingly")
input_type = InputType("Text")
output_type = OutputType("Text")
agent = Agent(expertise, task, input_type, output_type)
chat_history=[]
model = Mistral(chat_history=chat_history)
sequential_flow = SequentialFlow(agent, model)
st.title("Mistral")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I am your Llm web agent connected to internet. AMA! 😊"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("Browsing the web..."):
        context=sequential_flow.mistral_context(prompt)
    with st.chat_message("assistant"):
        response = st.write_stream(sequential_flow.mistral_webagent(user_prompt=prompt,search_context=context))
    st.session_state.messages.append({"role": "assistant", "content": response})
