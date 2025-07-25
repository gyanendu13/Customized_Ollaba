import streamlit as st
import requests
import json

# def llama3(prompt):
#     url = "http://localhost:3000/api/chat"
#     data = {
#         "model": "llama3",  # Ensure correct model name
#         "messages": [
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         "stream": False
#     }
    
#     headers = {
#         'Content-Type': 'application/json'
#     }
    
#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.json()['message']['content']
#     except requests.exceptions.RequestException as e:
#         return f"❌ Could not connect to LLaMA API: {str(e)}"
#     except KeyError:
#         return f"❌ Unexpected response: {response.text}"

def llama3(prompt):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['message']['content']
    except requests.exceptions.RequestException as e:
        return f"❌ Could not connect to LLaMA API: {e}"
    except KeyError:
        return f"❌ Unexpected response format: {response.text}"



# Streamlit UI
st.set_page_config(page_title="Deutsche Bank Bot", layout="centered")
st.title("💬 Deutsche Bank BOT")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # LLaMA3 response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = llama3(user_input)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
