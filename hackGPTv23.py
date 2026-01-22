#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv, set_key
from openai import OpenAI

# -------------------------
# Streamlit config MUST be first
# -------------------------
st.set_page_config(
    page_title="𝚑𝚊𝚌𝚔🅶🅿🆃",
    page_icon="https://raw.githubusercontent.com/NoDataFound/hackGPT/main/res/hackgpt_fav.png",
    layout="wide",
)

# -------------------------
# Env + API key handling
# -------------------------
load_dotenv(".env")
stored_api_key = os.getenv("OPENAI_API_KEY", "")

api_key_input = st.sidebar.text_input(
    "OpenAI API key",
    value=stored_api_key,
    type="password",
    help="Enter your OpenAI API key. You can override the saved key at any time.",
)
save_api_key = st.sidebar.checkbox("Save API key to .env", value=False)

api_key = (api_key_input or "").strip()
if save_api_key and api_key:
    # Note: On Railway/Streamlit Cloud, writing .env may not persist.
    set_key(".env", "OPENAI_API_KEY", api_key)

if not api_key:
    st.sidebar.error("Please enter a valid OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# -------------------------
# UI / Branding
# -------------------------
CSS = """
img { box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.2); }
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

st.sidebar.image(
    "https://raw.githubusercontent.com/NoDataFound/hackGPT/main/res/hackGPT_logo.png",
    width=300,
)
github_logo = "https://raw.githubusercontent.com/NoDataFound/hackGPT/main/res/github.png"
hackGPT_repo = "https://github.com/NoDataFound/hackGPT"
st.sidebar.markdown(f"[![GitHub]({github_logo})]({hackGPT_repo} 'hackGPT repo')")

# -------------------------
# Persona setup (safe)
# -------------------------
def ensure_personas_dir():
    if not os.path.exists("personas"):
        os.makedirs("personas", exist_ok=True)

def get_persona_files():
    ensure_personas_dir()
    return sorted([f[:-3] for f in os.listdir("personas") if f.endswith(".md")])

persona_files = get_persona_files()
selected_persona = st.sidebar.selectbox(
    "👤 𝖲𝖾𝗅𝖾𝖼𝗍 𝖫𝗈𝖼𝖺𝗅 𝖯𝖾𝗋𝗌𝗈𝗇𝖺",
    ["None"] + persona_files
)

persona_text = ""
if selected_persona and selected_persona != "None":
    try:
        with open(os.path.join("personas", f"{selected_persona}.md"), "r", encoding="utf-8") as f:
            persona_text = f.read().strip()
    except FileNotFoundError:
        persona_text = ""

# -------------------------
# Model + params
# -------------------------
# Use current models (older davinci models are deprecated/retired)
MODEL = st.sidebar.selectbox(
    label="Model",
    options=[
        "gpt-4o-mini",
        "gpt-4o",
        # keep old ones ONLY if your account still supports them:
        # "gpt-4",
        # "gpt-3.5-turbo",
    ],
)

temperature = st.sidebar.slider(
    "𝗧𝗲𝗺𝗽𝗲𝗿𝗮𝘁𝘂𝗿𝗲 | 𝗖𝗿𝗲𝗮𝘁𝗶𝘃𝗲 <𝟬.𝟱",
    min_value=0.0,
    max_value=1.0,
    step=0.1,
    value=1.0
)

max_tokens = st.sidebar.slider(
    "𝗠𝗔𝗫 𝗢𝗨𝗧𝗣𝗨𝗧 𝗧𝗢𝗞𝗘𝗡𝗦",
    min_value=32,
    max_value=2048,
    step=32,
    value=512
)

# -------------------------
# Remote prompts (optional)
# -------------------------
url = "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv"
jailbreaks = "https://raw.githubusercontent.com/NoDataFound/hackGPT/main/jailbreaks.csv"

# Wrap remote reads to avoid app crash when GitHub is blocked/down
try:
    data = pd.read_csv(url)
    data = pd.concat([data, pd.DataFrame({"act": [" "], "prompt": [""]})], ignore_index=True)
except Exception:
    data = pd.DataFrame({"act": [" "], "prompt": [""]})

try:
    jailbreakdata = pd.read_csv(jailbreaks)
    jailbreakdata = pd.concat([jailbreakdata, pd.DataFrame({"hacker": [" "], "text": [""]})], ignore_index=True)
except Exception:
    jailbreakdata = pd.DataFrame({"hacker": [" "], "text": [""]})

# -------------------------
# Persona management UI (kept, but safer)
# -------------------------
expand_section = st.sidebar.expander("👤 Manage Personas", expanded=False)
with expand_section:
    if selected_persona and selected_persona != "None":
        persona_path = os.path.join("personas", f"{selected_persona}.md")
        persona_text_live = persona_text

        new_persona_name = st.text_input("Persona Name:", value=selected_persona)
        new_persona_prompt = st.text_area("Persona Prompt:", value=persona_text_live, height=100)

        if (new_persona_name != selected_persona) or (new_persona_prompt != persona_text_live):
            ensure_personas_dir()
            with open(os.path.join("personas", f"{new_persona_name}.md"), "w", encoding="utf-8") as f:
                f.write(new_persona_prompt)
            if new_persona_name != selected_persona and os.path.exists(persona_path):
                os.remove(persona_path)
            st.success("Persona updated. Reload/refresh if list doesn't update.")

        if st.button("➖ Delete Persona"):
            if os.path.exists(persona_path):
                os.remove(persona_path)
            st.warning("Persona Deleted. Reload/refresh to update list.")

expand_section = st.sidebar.expander("🥷 Import Remote Persona", expanded=False)
with expand_section:
    selected_act = st.selectbox("", data["act"])
    show_remote_prompts = st.checkbox("Show remote prompt options")
    if selected_act and str(selected_act).strip():
        selected_prompt = data.loc[data["act"] == selected_act, "prompt"].values[0]
        if st.button("Save Selected Persona"):
            ensure_personas_dir()
            with open(os.path.join("personas", f"{selected_act}_remote.md"), "w", encoding="utf-8") as f:
                f.write(str(selected_prompt))
            st.success("Saved remote persona.")

expand_section = st.sidebar.expander("🏴‍☠️ Jailbreaks", expanded=False)
with expand_section:
    selected_hacker = st.selectbox("", jailbreakdata["hacker"])
    show_hack_prompts = st.checkbox("Show jailbreak options")
    if selected_hacker and str(selected_hacker).strip():
        selected_jailbreak_prompt = jailbreakdata.loc[jailbreakdata["hacker"] == selected_hacker, "text"].values[0]
        if st.button("Save Selected Jailbreak"):
            ensure_personas_dir()
            with open(os.path.join("personas", f"{selected_hacker}_jailbreak.md"), "w", encoding="utf-8") as f:
                f.write(str(selected_jailbreak_prompt))
            st.success("Saved jailbreak persona.")

expand_section = st.sidebar.expander("➕ Add new Persona", expanded=False)
with expand_section:
    st.subheader("➕ Add new Persona")
    st.text("Press enter to update/save")
    persona_files_now = get_persona_files()
    new_persona_name = st.text_input("Persona Name:")
    if new_persona_name in persona_files_now:
        st.error("This persona name already exists. Please choose a different name.")
    else:
        new_persona_prompt = st.text_area("Persona Prompt:", height=100)
        if new_persona_name and new_persona_prompt:
            ensure_personas_dir()
            with open(os.path.join("personas", f"{new_persona_name}.md"), "w", encoding="utf-8") as f:
                f.write(new_persona_prompt)
            st.success("Persona saved. Reload/refresh to update list.")

if show_hack_prompts:
    st.write(jailbreakdata[["hacker", "text"]].style.hide(axis="index").set_properties(
        subset="text", **{"max-width": "100%", "white-space": "pre-wrap"}
    ))
elif "show_remote_prompts" in locals() and show_remote_prompts:
    st.write(data[["act", "prompt"]].style.hide(axis="index").set_properties(
        subset="prompt", **{"max-width": "100%", "white-space": "pre-wrap"}
    ))

# -------------------------
# Chat history + styles
# -------------------------
user_css = """
<style>
.user { display:inline-block; padding:8px; border-radius:10px; margin-bottom:1px;
border:1px solid #e90ce4; width:100%; height:100%; overflow-y:auto; }
</style>
"""
ai_css = """
<style>
.ai { display:inline-block; padding:10px; border-radius:10px; margin-bottom:1px;
border:1px solid #0ab5e0; width:100%; overflow-x:auto; height:100%; overflow-y:auto; }
</style>
"""
model_css = """
<style>
.model { display:inline-block; background-color:#f0e0ff; padding:1px; border-radius:5px;
margin-bottom:5px; width:100%; height:100%; overflow-y:auto; }
</style>
"""
st.markdown(user_css, unsafe_allow_html=True)
st.markdown(ai_css, unsafe_allow_html=True)
st.markdown(model_css, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def display_chat_history():
    for role, text in reversed(st.session_state.chat_history):
        col1, col2 = st.columns([2, 8])
        with col1:
            if role in ("user", "model"):
                st.markdown(f'<div class="{role}">{text}</div>', unsafe_allow_html=True)
            else:
                st.markdown("")
        with col2:
            if role in ("ai", "persona"):
                st.markdown(f'<div class="{role}">{text}</div>', unsafe_allow_html=True)

# -------------------------
# Single unified responder (no deprecated completions)
# -------------------------
def generate_reply(user_text: str) -> str:
    system_msg = "You are a helpful assistant."
    if persona_text:
        system_msg += "\n\nPersona:\n" + persona_text

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_text},
    ]

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content

# -------------------------
# Main input
# -------------------------
text_input = st.text_input(
    "",
    value="",
    key="text_input",
    placeholder="Type your message here...",
    help="Press Enter to send your message.",
)

if text_input:
    try:
        ai_response = generate_reply(text_input)
    except Exception as e:
        st.error(f"OpenAI error: {e}")
        st.stop()

    st.session_state.chat_history.append(("ai", ai_response))
    st.session_state.chat_history.append(("persona", selected_persona))
    st.session_state.chat_history.append(("user", f"You: {text_input}"))
    st.session_state.chat_history.append(("model", MODEL))

display_chat_history()

if st.button("Download Chat History"):
    chat_history_text = "\n".join([text for _, text in st.session_state.chat_history])
    st.download_button(
        label="Download Chat History",
        data=chat_history_text.encode("utf-8"),
        file_name="chat_history.txt",
        mime="text/plain",
    )
