# app.py
# Flowly: turns static forms into AI-driven conversational interviews
# latest update check
import os, json
from pathlib import Path
from datetime import datetime
import streamlit as st
from openai import OpenAI

ASSISTANT_NAME = "Flowly"

# ---------- PAGE ROUTING ----------
if "page" not in st.session_state:
    st.session_state.page = "form"

def get_page():
    return st.session_state.page

def set_page(page: str):
    st.session_state.page = page

# ========== CONFIG ==========
st.set_page_config(page_title="Flowly", layout="centered", page_icon="💬")

DATA_DIR = Path("data")
FORMS_DIR = DATA_DIR / "forms"
RESP_DIR = DATA_DIR / "responses"
for p in [FORMS_DIR, RESP_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Initialize OpenAI client
client = None
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ Missing OpenAI API key in secrets.toml")
    st.stop()

# ========== HELPERS ==========
def save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def generate_form_id() -> str:
    return datetime.now().strftime("form_%Y%m%d_%H%M%S")

# ========== HERO ==========
def hero():
    st.markdown("""
    <style>
    .stApp {
      background: linear-gradient(10deg, #08962c, #eeaae2);
      background-size: 400% 400%;
      animation: bgShift 18s ease infinite;
      font-family: 'Inter', sans-serif;
      color: #fff;
      overflow-x: hidden;
      margin: 0;
    }
    @keyframes bgShift {
      0% { background-position:68% 0%; }
      50% { background-position:33% 100%; }
      100% { background-position:68% 0%; }
    }
    .hero {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 65vh;
      text-align: center;
    }
    .hero h1 {
      font-size: clamp(3rem, 7vw, 5rem);
      font-weight: 800;
      letter-spacing: 2px;
      color: #ffffff;
      text-shadow: 0 0 25px rgba(0,0,0,0.15);
      margin-bottom: 0.3em;
    }
    .hero-tagline {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: .6ch;
      font-size: clamp(1.3rem, 2.6vw, 1.7rem);
      font-weight: 500;
      color: #fff;
      line-height: 1;
      white-space: nowrap;
    }
    .word-switch {
      position: relative;
      display: inline-block;
      width: 18ch;
      height: 1em;
      vertical-align: middle;
      overflow: hidden;
    }
    .word-switch span {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      opacity: 0;
      color: #c7ffd6;
      font-weight: 600;
      transition: opacity 1s ease-in-out;
      text-align: left;
    }
    .word-switch span:nth-child(1) { animation: fadeCycle 9s infinite; }
    .word-switch span:nth-child(2) { animation: fadeCycle 9s infinite; animation-delay: 3s; }
    .word-switch span:nth-child(3) { animation: fadeCycle 9s infinite; animation-delay: 6s; }
    @keyframes fadeCycle {
      0%, 10% { opacity: 0; }
      20%, 40% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }

    /* ---------- Minimal Glassy Button ---------- */
    div.stButton > button, .stDownloadButton > button {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: #ffffff;
    font-weight: 500;
    border-radius: 10px;
    padding: 0.5em 1.8em;
    border: 1px solid rgba(255, 255, 255, 0.3);
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: all 0.25s ease-in-out;
    }

    div.stButton > button:hover, .stDownloadButton > button:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    

    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    </style>

    <div class="hero">
      <h1>Flowly</h1>
      <div class="hero-tagline">
        Turning static forms into&nbsp;
        <div class="word-switch">
          <span>human-like conversations</span>
          <span>flowing interviews</span>
          <span>meaningful dialogue</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ========== PAGE 1 — FORM BUILDER ==========
def page_form_builder():
    hero()
    st.markdown("""
    <style>
    .form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: -3em;
        color: #ffffffcc;
    }

    .form-container h2 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5em;
        color: #ffffff;
    }

    .form-container p {
        font-size: 1.05rem;
        max-width: 600px;
        margin-bottom: 1.5em;
        color: rgba(255,255,255,0.85);
    }

    /*  Keep text inside text areas left-aligned */
    textarea, .stTextInput input {
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="form-container">
        <h2>Let’s bring your form to life! </h2>
        <p>Flowly turns your questions into natural, human-like conversations.</p>
    </div>
    """, unsafe_allow_html=True)

    goal = st.text_area(
        "What’s your Goal?",
        placeholder="Example: Gather customer feedback, evaluate job applicants, understand project challenges...",
        height=80,
    )

    text = st.text_area(
        "Your questions",
        placeholder="Write each question on a new line...",
        height=180,
    )

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    save_btn = st.button("Start the flow →")
    st.markdown("</div>", unsafe_allow_html=True)

    if save_btn:
        qs = [q.strip() for q in text.split("\n") if q.strip()]
        if not qs:
            st.warning("Please enter at least one question.")
            return
        fid = generate_form_id()
        save_json(FORMS_DIR / f"{fid}.json", {"form_id": fid, "goal": goal, "questions": qs})
        st.session_state.goal = goal
        st.session_state.questions = qs
        st.session_state.form_id = fid
        st.session_state.current_idx = 0
        set_page("chat")
        st.rerun()



# ========== PAGE 2 — CHAT ==========
def page_chat():
    hero()

    if "questions" not in st.session_state:
        st.warning("No form loaded yet. Create one first.")
        if st.button("← Back to builder"):
            set_page("form")
            st.rerun()
        return

    questions = st.session_state.questions
    form_id = st.session_state.get("form_id", "unsaved_demo")
    conv = st.session_state.setdefault("conversation", [])
    idx = st.session_state.setdefault("current_idx", 0)
    answered = st.session_state.setdefault("answered", set())

    # display full chat so far
    for turn in conv:
        speaker = ASSISTANT_NAME if turn["role"] == "assistant" else "You"
        st.markdown(f"**{speaker}:** {turn['content']}")

    # show ending screen if finished
    if st.session_state.get("conversation_complete", False):
        st.success("All set — your responses have been recorded")
        st.download_button(
            "Download conversation",
            data=json.dumps(conv, indent=2, ensure_ascii=False),
            file_name=f"{form_id}_conversation.json",
            mime="application/json",
        )
        if st.button("← Back to builder"):
            set_page("form")
            st.rerun()
        st.stop()

    # Determine remaining questions
    remaining = [q for q in questions if q not in answered]
    q = st.session_state.get("current_ai_question")

    # Generate new AI question if needed
    if not q:
        goal = st.session_state.get("goal", "")
        prompt = f"""
You are **Flowly** — a warm, curious AI interviewer who makes structured forms feel like real conversations.
Your role is to **understand the form’s goal** and **weave all listed questions** into a human-like dialogue.

---

### Context

**Form Goal:** {goal}  
**Remaining Questions (in order):** {json.dumps(remaining, ensure_ascii=False, indent=2)}  
**Conversation So Far:** {json.dumps(conv[-10:], ensure_ascii=False, indent=2)}

---

### Conversation Principles

1. **Start Genuinely**
   - If there’s no prior conversation, begin with:
     "Hey there! I’m Flowly — I’ll be guiding you through a few questions today."
   - Keep it friendly, warm, and human — not scripted or mechanical.

2. **Flow with Curiosity**
   - Read the **goal** and shape your curiosity around it.
   - Treat the conversation like a dialogue, not a checklist.
   - Each question should feel like a natural next thought.
   - Use emotional mirroring — acknowledge what the user says before moving on.
     Examples:  
     → “That’s awesome to hear!”  
     → “I totally get what you mean.”  
     → “That’s an interesting point — tell me more.”  
     → “Got it, that makes sense.”

3. **Question Coverage**
   - You must eventually cover **every question** in “Remaining Questions.”
   - Don’t rush — take your time and explore each topic conversationally.
   - Smoothly transition between questions (e.g. “Now that you mention that…” or “Speaking of that…”).

4. **Follow-ups**
   - Ask up to 2 follow-ups when the answer is vague, emotional, interesting, or negative.
   - Use short, gentle probes like “Could you tell me a bit more about that?” or “What makes you feel that way?”

5. **Tone**
   - Use warmth, empathy, and a slightly informal human tone.
   - Avoid sounding like a form or survey — be present, like a real person reacting.

6. **End Gracefully**
   - When all questions have been covered, close warmly with:
     “That was a great chat! Thanks for sharing your thoughts — your feedback really helps us improve 💬”
   - Don’t add anything else or continue after this.

---

Now continue the conversation naturally as **Flowly**.
"""


        try:
            res = client.chat.completions.create(
                model="o4-mini",
                messages=[{"role": "system", "content": "Friendly interviewer."},
                          {"role": "user", "content": prompt}],
            )
            q = res.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"⚠️ LLM error: {e}")
            return

        st.session_state.current_ai_question = q

    # display AI message
    st.markdown(f"**{ASSISTANT_NAME}:** {q}")

    # auto-close if Flowly ended the conversation
    if any(kw in q.lower() for kw in ["thanks so much for sharing","appreciate your time","That was a great chat! Thanks for sharing your thoughts — your feedback really helps us improve"]):
        st.session_state.conversation_complete = True
        st.session_state.current_ai_question = None
        st.stop() 

    # user input
    user_inp = st.text_input("Your answer:", key=f"answer_{idx}")

    if st.button("Send"):
        if not user_inp.strip():
            st.warning("Please write an answer.")
            st.stop()

        conv.append({"role": "assistant", "content": q})
        conv.append({"role": "user", "content": user_inp})

        if idx < len(questions):
            answered.add(questions[idx])
        st.session_state.current_idx += 1

        # end if all questions done
        if not remaining:
            st.session_state.conversation_complete = True
            st.session_state.current_ai_question = None
            st.rerun()

        # reset and continue
        st.session_state.current_ai_question = None
        st.rerun()

# ========== ROUTER ==========
def main():
    if get_page() == "chat":
        page_chat()
    else:
        page_form_builder()

if __name__ == "__main__":
    main()
