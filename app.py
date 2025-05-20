import streamlit as st 
import requests 
from datetime import datetime
import json
import os


#====================CONFIGURATION========================
OPENROUTER_API_KEY = "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"
MODEL = "deepseek/deepseek-chat-v3-0324"
HEADERS = {
  "Authorization": f"Bearer {OPENROUTER_API_KEY}",
  "HTTP-Referer": "http://localhost:8501",
  "X-Title": "AI Chatbot Streamlit"
}
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Function to save chat history
def save_chat_history(chat_history):
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

# Function to load chat history
def load_chat_history():
    try:
        if os.path.exists('chat_history.json'):
            with open('chat_history.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading chat history: {e}")
    return []

#UI - Fixed Header
st.markdown(f"""
<div class="header-container">
    <p class="header-title">🧠 AI Chatbot Kasultanan Bulakan</p>
    <p class="header-subtitle">Powered by {MODEL} via OpenRouter 🤖</p>
</div>
""", unsafe_allow_html=True)

# Container for chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

#Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Custom CSS for chat bubbles and fixed header
st.markdown("""
<style>
/* Fixed Header Styles */
.header-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #f0f2f6;
    padding: 1rem 1rem 0.5rem;
    z-index: 1000;
    border-bottom: 1px solid #ddd;
}
.header-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
    padding: 0;
}
.header-subtitle {
    font-size: 0.8rem;
    color: #666;
    margin: 0;
    padding: 0;
}
.chat-container {
    margin-top: 100px;
    padding: 10px;
}
/* Chat Bubbles */
.user-bubble {
    background-color: #E3F2FD;
    border-radius: 15px;
    padding: 10px 15px;
    margin: 5px 0;
    max-width: 70%;
    margin-left: auto;
    margin-right: 20px;
}
.assistant-bubble {
    background-color: #FCE4EC;
    border-radius: 15px;
    padding: 10px 15px;
    margin: 5px 0;
    max-width: 70%;
    margin-right: auto;
    margin-left: 20px;
}
.timestamp {
    font-size: 0.8em;
    color: #888;
    margin-top: 4px;
    text-align: right;
}
.stMarkdown {
    all: unset;
}
</style>
""", unsafe_allow_html=True)

#Tampilkan chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        bubble_class = "user-bubble" if chat["role"] == "user" else "assistant-bubble"
        st.markdown(f"""
<div class="{bubble_class}">
    {chat['content']}
    <div class="timestamp">{chat.get('timestamp', '')}</div>
</div>
""", unsafe_allow_html=True)

# Close chat container
st.markdown('</div>', unsafe_allow_html=True)

#user input
user_input = st.chat_input("Silahkan Tulisan Pesan Hambaku...")

if user_input:
    current_time = datetime.now().strftime("%H:%M")
    with st.chat_message("user"):
        st.markdown(f"""
<div class="user-bubble">
    {user_input}
    <div class="timestamp">{current_time}</div>
</div>
""", unsafe_allow_html=True)
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": current_time
    })
    save_chat_history(st.session_state.chat_history)

#kirim pesan ke API
with st.spinner("Mengetik..."):
    payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a cheerfull assistant."},
                {"role": "user", "content": user_input}
            ]
        }
response = requests.post(API_URL, headers=HEADERS, json=payload)
if response.status_code == 200:
    bot_reply = response.json()['choices'][0]['message']['content']
else:
    bot_reply = "⚠️ Maaf, gagal mengambil respons dari OpenRouter."
current_time = datetime.now().strftime("%H:%M")
st.chat_message("assistant").markdown(f"""
<div class="assistant-bubble">
    {bot_reply}
    <div class="timestamp">{current_time}</div>
</div>
""", unsafe_allow_html=True)
st.session_state.chat_history.append({
    "role": "assistant", 
    "content": bot_reply,
    "timestamp": current_time
})
save_chat_history(st.session_state.chat_history)
#====================END========================
#====================CONFIGURATION========================