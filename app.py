import streamlit as st
import google.generativeai as genai

# --------------------------- CONFIG ---------------------------
st.set_page_config(page_title="🧠 Mental Health Companion", layout="centered")
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --------------------------- HELPER ---------------------------
def get_ai_response(prompt, model_name="gemini-2.5-flash-lite"):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error generating response: {e}"

# --------------------------- STYLING ---------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #b3d4fc, #e3d7f5, #fbd6e3, #c8e6c9, #b3d4fc);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite, fadeIn 2s ease forwards;
    background-attachment: fixed;
    opacity: 0;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeIn {
    to { opacity: 1; }
}

@keyframes float {
    0% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0); }
}

.floating-icon {
    position: absolute;
    animation: float 3s ease-in-out infinite;
    opacity: 0.6;
    font-size: 30px;
    top: 20px;
    left: 20px;
}

html, body {
    background-color: #4a148c !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px !important;
    overflow-x: hidden;
    color: #4a148c !important;
}

h1, h3, h4, h6 {
    color: #6a1b9a !important;
}
h2, h5 {
    color: #ad1457 !important;
}
p, span, div {
    color: #4a148c !important;
}

.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin-top: 50px;
    margin-bottom: 20px;
}

textarea[data-testid="chat-input"] {
    background-color: #ffffff !important;
    color: #4a148c !important;
    border: 2px solid #ad1457 !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-size: 16px !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.flip-card {
    background-color: transparent;
    width: 350px;
    height: 150px;
    perspective: 1000px;
    display: inline-block;
    margin: 15px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s;
    transform-style: preserve-3d;
    cursor: pointer;
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 15px;
    backface-visibility: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.flip-card-front {
    background-color: #b39ddb;
    color: #4a148c;
}

.flip-card-back {
    background-color: #9575cd;
    color: #4a148c;
    transform: rotateY(180deg);
}

.mood-container {
    text-align: center;
    margin-top: 20px;
}

.mood-btn {
    display: inline-block;
    margin: 10px;
    padding: 10px 16px;
    border-radius: 20px;
    background-color: #ede7f6;
    color: #4a148c;
    cursor: pointer;
    user-select: none;
    transition: all 0.3s;
}

.mood-btn:hover {
    background-color: #d1c4e9;
}

.mood-summary {
    margin-top: 15px;
    font-size: 1.1rem;
    color: #4a148c;
    font-weight: 600;
}
.footer {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: transparent;
    text-align: center;
    font-size: 13px;
    color: #ad1457;
    padding: 10px;
    width: fit-content;
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)

# --------------------------- HEADER ---------------------------
st.markdown("""
<div class="main-container">
    <h1>🧠 Mental Health Companion</h1>
    <h3>Welcome! I'm here to listen, support you, and share positive insights 💜</h3>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="floating-icon">🎈</div>', unsafe_allow_html=True)

# --------------------------- CHAT SECTION ---------------------------
chat_container = st.container()
chat_container.subheader("💭 Chat with me")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        with chat_container.chat_message("user"):
            st.markdown(msg)
    else:
        with chat_container.chat_message("assistant"):
            st.markdown(msg)

# Chat input inside container
user_input = chat_container.chat_input("Share your thoughts...", key="main_chat_input")

if user_input and user_input.strip():
    st.session_state.chat_history.append(("You", user_input))
    with chat_container.chat_message("user"):
        st.markdown(user_input)

    ai_reply = get_ai_response(user_input)
    st.session_state.chat_history.append(("AI", ai_reply))
    with chat_container.chat_message("assistant"):
        st.markdown(ai_reply)

    st.snow()

# --------------------------- FLASHCARDS ---------------------------
st.subheader("🌸 Wellness Tips")
st.markdown("Hover or tap on a card to reveal a gentle reminder:")

cards = [
    ("What does mindfulness mean?", "Mindfulness is being fully present in the moment 🌼"),
    ("How to calm anxiety?", "Take deep breaths and ground yourself 🌿"),
    ("What is self-love?", "Accept yourself as you are 💖"),
    ("Feeling tired?", "Rest is productive too 😴")
]

col1, col2 = st.columns(2)
for i, (front, back) in enumerate(cards):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">{front}</div>
            <div class="flip-card-back">{back}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------- MOOD TRACKER ---------------------------
st.markdown("<div class='mood-container'><h3>💬 How are you feeling today? (Tap an emoji)</h3></div>", unsafe_allow_html=True)

moods = [
    ("😊 Happy", "happy"),
    ("😔 Sad", "sad"),
    ("😰 Worried", "worried"),
    ("😴 Tired", "tired"),
    ("😌 Calm", "calm")
]

cols = st.columns(len(moods))

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = ""
if "mood_summary" not in st.session_state:
    st.session_state.mood_summary = ""

for i, (label, mood_keyword) in enumerate(moods):
    with cols[i]:
        if st.button(label):
            st.session_state.selected_mood = mood_keyword
            prompt = f"Summarize this mood in a positive and empathetic way: I am feeling {mood_keyword} right now."
            st.session_state.mood_summary = get_ai_response(prompt)

if st.session_state.selected_mood:
    st.markdown(f"<div class='mood-summary'>💜 Mood summary for '{st.session_state.selected_mood}':<br>{st.session_state.mood_summary}</div>", unsafe_allow_html=True)

# --------------------------- FOOTER ---------------------------
st.markdown("""
<style>
.footer-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: black !important;
  color: white !important;
  padding: 12px 16px;
  font-size: 0.9em;
  text-align: center;
  animation: fadeIn 2s ease-in;
  z-index: 999;
  font-family: 'Segoe UI', sans-serif;
}

.footer-fixed * {
  color: white !important;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<div class="footer-fixed">
  This chatbot offers emotional support and information only. Not a replacement for professional mental health care. If needed, reach out to a licensed therapist.<br>
  <span style="font-size: 0.8em; opacity: 0.7;">© 2025 Designed with care by Nivedha</span>
</div>
""", unsafe_allow_html=True)


st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
