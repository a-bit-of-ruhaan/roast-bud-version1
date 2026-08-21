import streamlit as st
from pathlib import Path
from roast_bud_api import roast_code

# Standard page configurations
st.set_page_config(
    page_title="ROAST BUD — Code Reviewer",

  layout="centered",
    initial_sidebar_state="collapsed"
)

# Load the clean design architecture
css_path = Path(__file__).with_name("style.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <header class="topbar">
      <div class="brand-lockup">
        <div class="brand-mark">RB</div>
        <div>
          <div class="brand-name">Roast Bud</div>
          <div class="brand-status"><span></span> Online · Code reviewer</div>
        </div>
      </div>
      <div class="topbar-note">Brutal feedback. Useful fixes.</div>
    </header>
    <section class="welcome-block">
      <div class="eyebrow">YOUR PERSONAL ROASTBUDDY</div>
      <h1>What are we roasting today?</h1>
      <p>Drop your code below and get brutal Feedback from Roast Bud</p>
    </section>
    
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"], avatar="user" if message["role"] == "user" else "🔥"):
    if message["role"] == "user":
      st.markdown("**Code submitted**")
      st.code(message["content"], language=message.get("language", "python"))
    else:
      st.markdown(message["content"])

user_code = st.chat_input("Paste code here and ask Roast Bud...")

if user_code:
  st.session_state.messages.append({"role": "user", "content": user_code, "language": "python"})
  with st.chat_message("user", avatar="user"):
    st.markdown("**Code submitted**")
    st.code(user_code, language="python")

  with st.chat_message("assistant", avatar="assistant"):
    with st.spinner("Bud is sharpening the roast..."):
      try:
        result = roast_code(user_code)
        st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
      except Exception as error:
        st.error(f"Something went wrong: {error}")
