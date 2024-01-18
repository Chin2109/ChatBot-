import streamlit as st
from openai import OpenAI
import pandas as pd

st.title("Chat Bot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

file_read = st.file_uploader("")
if file_read is not None:
    file = pd.read_csv(file_read)
    st.write(file)

if prompt := st.chat_input("Nhập yêu cầu?"):
    if prompt == "Analyse":
        prompt = file.to_string()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        full_response = ""
        holder = st.empty()

        #
        # for word in prompt.split():
        #     full_response += word + " "
        #     time.sleep(0.1)
        #     holder.markdown(full_response + "_")
        # holder.markdown(full_response)

        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                    for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            holder.markdown(full_response + "_")
            holder.markdown(full_response)
        holder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
