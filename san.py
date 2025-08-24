# san.py - Enhanced Interactive Version
# Import necessary libraries
import streamlit as st
import google.generativeai as genai
import os
import json # Import the json library to parse the model's output
import io # Used for handling in-memory audio data
from gtts import gTTS # Google Text-to-Speech for audio output
from streamlit_mic_recorder import mic_recorder # For audio input

# --- Configuration ---
st.set_page_config(
    page_title="SanskritAI Chatbot",
    page_icon="🕉️",
    layout="wide", # Use wide layout for a more app-like feel
    initial_sidebar_state="auto",
)

# --- Enhanced Custom CSS for Modern Interactive Design ---
def load_css():
    """Injects custom CSS for a modern, interactive look with animations."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Sanskrit:ital,wght@0,400;1,400&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@300;400;600&display=swap');

            /* --- CSS Variables for Easy Theming --- */
            :root {
                --primary-color: #FF6B35;
                --secondary-color: #F7931E;
                --accent-color: #FFD23F;
                --text-dark: #2C3E50;
                --text-light: #FFFFFF;
                --bg-gradient-start: #FFF8F0;
                --bg-gradient-end: #FFE5CC;
                --shadow-light: 0 4px 20px rgba(255, 107, 53, 0.15);
                --shadow-medium: 0 8px 30px rgba(255, 107, 53, 0.25);
                --shadow-heavy: 0 15px 35px rgba(255, 107, 53, 0.3);
                --border-radius: 20px;
                --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            /* --- General Styles with Smooth Animations --- */
            html, body, [class*="st-"] {
                font-family: 'Poppins', sans-serif;
                scroll-behavior: smooth;
            }
            
            /* --- Animated Background with Floating Elements --- */
            [data-testid="stAppViewContainer"] > .main {
                background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
                position: relative;
                overflow: hidden;
            }

            [data-testid="stAppViewContainer"] > .main::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background-image: 
                    radial-gradient(circle at 20% 50%, rgba(255, 107, 53, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(247, 147, 30, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(255, 210, 63, 0.1) 0%, transparent 50%);
                animation: float 20s ease-in-out infinite;
                pointer-events: none;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }

            /* --- Main App Container with Glass Effect --- */
            .main .block-container {
                padding: 2rem 1rem;
                max-width: 1000px;
                position: relative;
                z-index: 1;
            }
            
            /* --- Spectacular App Title with Multiple Effects --- */
            h1 {
                font-family: 'Tiro Devanagari Sanskrit', serif;
                font-size: clamp(2.5rem, 5vw, 4rem);
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                font-weight: 700;
                letter-spacing: 3px;
                margin-bottom: 2rem;
                position: relative;
                animation: titleGlow 3s ease-in-out infinite alternate;
                text-shadow: 0 0 30px rgba(255, 107, 53, 0.3);
            }

            h1::after {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 100px;
                height: 4px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                border-radius: 2px;
                animation: underlineExpand 2s ease-out;
            }

            @keyframes titleGlow {
                0% { filter: brightness(1) drop-shadow(0 0 10px rgba(255, 107, 53, 0.3)); }
                100% { filter: brightness(1.2) drop-shadow(0 0 20px rgba(255, 107, 53, 0.5)); }
            }

            @keyframes underlineExpand {
                0% { width: 0; }
                100% { width: 100px; }
            }
            
            /* --- Advanced Chat Bubbles with 3D Effects --- */
            .st-emotion-cache-1c7y2kd {
                border-radius: var(--border-radius);
                padding: 1.5rem 2rem;
                margin-bottom: 1.5rem;
                max-width: 80%;
                animation: messageSlide 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
                box-shadow: var(--shadow-light);
                border: 1px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
                transition: var(--transition);
            }

            .st-emotion-cache-1c7y2kd:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-medium);
            }
            
            @keyframes messageSlide {
                0% { opacity: 0; transform: translateY(30px) scale(0.9); }
                60% { transform: translateY(-5px) scale(1.02); }
                100% { opacity: 1; transform: translateY(0) scale(1); }
            }

            /* AI message styling with gradient background */
            div[data-testid="stChatMessage"]:has(div[data-testid="stAvatar"]) .st-emotion-cache-1c7y2kd {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 245, 235, 0.95) 100%);
                color: var(--text-dark);
                border-left: 4px solid var(--primary-color);
            }

            /* User message styling with vibrant gradient */
            div[data-testid="stChatMessage"]:not(:has(div[data-testid="stAvatar"])) {
                display: flex; 
                justify-content: flex-end;
            }
            div[data-testid="stChatMessage"]:not(:has(div[data-testid="stAvatar"])) .st-emotion-cache-1c7y2kd {
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                color: var(--text-light);
                box-shadow: var(--shadow-medium);
            }

            /* --- Futuristic Chat Input --- */
            .st-emotion-cache-135i5lh {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 245, 235, 0.8));
                border-radius: 50px;
                padding: 1rem;
                box-shadow: var(--shadow-light);
                border: 2px solid transparent;
                backdrop-filter: blur(10px);
                transition: var(--transition);
                position: relative;
                overflow: hidden;
            }
            
            /* --- Enhanced Login/Signup Form --- */
            .login-container {
                max-width: 450px;
                margin: auto;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 245, 235, 0.9));
                border-radius: var(--border-radius);
                padding: 3rem 2rem;
                box-shadow: var(--shadow-heavy);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.3);
                position: relative;
                overflow: hidden;
                animation: containerFadeIn 1s ease-out;
            }

            @keyframes containerFadeIn {
                0% { opacity: 0; transform: translateY(30px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            .login-container h2 {
                text-align: center;
                color: var(--text-dark);
                font-weight: 700;
                margin-bottom: 2rem;
                position: relative;
                z-index: 1;
            }

            /* --- Spectacular Buttons --- */
            .stButton > button {
                border-radius: 15px;
                border: none;
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                color: var(--text-light);
                font-weight: 600;
                font-size: 1rem;
                padding: 0.8rem 2rem;
                transition: var(--transition);
                width: 100%;
                position: relative;
                overflow: hidden;
                box-shadow: var(--shadow-light);
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .stButton > button:hover {
                transform: translateY(-3px) scale(1.05);
                box-shadow: var(--shadow-heavy);
                background: linear-gradient(135deg, var(--secondary-color), var(--accent-color));
            }
        </style>
    """, unsafe_allow_html=True)

# --- Helper Functions ---
def text_to_audio(text):
    """Converts text to speech using gTTS and returns audio bytes."""
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp.read()
    except Exception as e:
        st.warning(f"Could not generate audio for the response. Error: {e}")
        return None

# --- Theme Application Function ---
def apply_theme(theme):
    """Apply different color themes based on selection."""
    theme_styles = {
        "🌙 Moonlight": {"primary": "#6C5CE7", "secondary": "#A29BFE", "accent": "#FD79A8", "bg_start": "#2D3436", "bg_end": "#636E72"},
        "🌸 Cherry Blossom": {"primary": "#FD79A8", "secondary": "#FDCB6E", "accent": "#E17055", "bg_start": "#FAB1A0", "bg_end": "#FF7675"},
        "🏔️ Mountain": {"primary": "#00B894", "secondary": "#00CEC9", "accent": "#55A3FF", "bg_start": "#DDA0DD", "bg_end": "#98D8C8"}
    }
    if theme in theme_styles:
        colors = theme_styles[theme]
        st.markdown(f"""
            <style>
                :root {{
                    --primary-color: {colors["primary"]};
                    --secondary-color: {colors["secondary"]};
                    --accent-color: {colors["accent"]};
                    --bg-gradient-start: {colors["bg_start"]};
                    --bg-gradient-end: {colors["bg_end"]};
                }}
            </style>
        """, unsafe_allow_html=True)

# --- Authentication ---
def show_login_page():
    """Displays the enhanced login and signup form."""
    st.title("🕉️ SanskritAI")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    if st.session_state.get('show_signup', False):
        st.markdown('<h2>✨ Create Your Sanskrit Journey</h2>', unsafe_allow_html=True)
        st.text_input("📛 Full Name", key="signup_name", placeholder="Enter your full name")
        st.text_input("📧 Email Address", key="signup_email", placeholder="your@email.com")
        st.text_input("📱 Phone Number", key="signup_phone", placeholder="+91 XXXXX XXXXX")
        st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Create a strong password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Sign Up"):
                st.session_state.logged_in = True
                st.session_state.show_signup = False
                st.rerun()
        with col2:
            if st.button("⬅️ Back to Login"):
                st.session_state.show_signup = False
                st.rerun()
    else:
        st.markdown('<h2>🙏 Welcome Back, Sanskrit Scholar!</h2>', unsafe_allow_html=True)
        st.text_input("📧 Email or 📱 Phone", key="login_id", placeholder="Enter your email or phone number")
        st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login"):
                if st.session_state.login_id and st.session_state.login_password:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("⚠️ Please enter your credentials.")
        with col2:
            if st.button("✨ Create Account"):
                st.session_state.show_signup = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Chatbot Interface ---
def show_chatbot_page():
    """Displays the enhanced main chatbot interface after login."""
    st.title("🕉️ SanskritAI Chatbot")
    
    # API Key Management
    try:
        google_api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except (KeyError, FileNotFoundError):
        st.error("🚨 ERROR: API key not found.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error configuring the Gemini API: {e}")
        st.stop()
    
    # Initialize session state variables
    if "chat" not in st.session_state: st.session_state.chat = None
    if "total_questions" not in st.session_state: st.session_state.total_questions = 0
    if "correct_answers" not in st.session_state: st.session_state.correct_answers = 0
    if "messages_sent" not in st.session_state: st.session_state.messages_sent = 0
    if "quiz_mode" not in st.session_state: st.session_state.quiz_mode = False
    if "recitation_mode" not in st.session_state: st.session_state.recitation_mode = False
    if "shloka_to_recite" not in st.session_state: st.session_state.shloka_to_recite = None
    if "ai_persona" not in st.session_state: st.session_state.ai_persona = "General"
    if "voice_input_mode" not in st.session_state: st.session_state.voice_input_mode = False

    # --- Persona Definitions ---
    personas = {
        "General": "You are 'SanskritAI', a helpful and encouraging AI tutor for the Sanskrit language.",
        "Grammar (Pāṇini AI)": "You are Pāṇini AI, an expert in Sanskrit grammar based on the Aṣṭādhyāyī. Explain concepts with precision and cite sutras where possible.",
        "Ayurveda (Charak AI)": "You are Charak AI, an expert on Ayurveda based on the Charaka Samhita. Answer questions about health, herbs, and principles, citing your source text.",
        "Literature (Vyasa AI)": "You are Vyasa AI, a master of Sanskrit literature like the Mahabharata and Puranas. Recount stories and explain literary concepts, citing the epic you are referencing."
    }
    
    # Initialize chat based on persona
    if st.session_state.chat is None:
        st.session_state.chat = model.start_chat(history=[
            {'role': 'user', 'parts': [personas[st.session_state.ai_persona]]},
            {'role': 'model', 'parts': ["नमस्ते! 🙏 Welcome to SanskritAI! How can I assist you today? ✨📚"]}
        ])

    def generate_quiz_question():
        with st.spinner("🧠 Generating a new question..."):
            try:
                quiz_prompt = 'Generate a JSON object for a simple Sanskrit quiz question with keys: "question", "options", "answer", "explanation".'
                response = model.generate_content(quiz_prompt)
                json_response = response.text.replace("```json", "").replace("```", "").strip()
                st.session_state.quiz_question = json.loads(json_response)
                st.session_state.quiz_mode = True
            except Exception as e:
                st.error("😅 Sorry, I couldn't generate a quiz question.")
                st.session_state.quiz_mode = False

    def get_shloka_for_recitation():
        with st.spinner("📜 Choosing a shloka for you..."):
            try:
                shloka_prompt = "Provide a short, well-known Sanskrit shloka in Devanagari script for a user to practice reciting."
                response = model.generate_content(shloka_prompt)
                st.session_state.shloka_to_recite = response.text
                st.session_state.recitation_mode = True
            except Exception as e:
                st.error("😅 Sorry, I couldn't fetch a shloka right now.")

    # Display chat history or special modes
    if st.session_state.quiz_mode:
        q = st.session_state.quiz_question
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        st.info(f"🧩 **Quiz Time!**\n\n{q['question']}")
        cols = st.columns(len(q.get('options', [])))
        for i, option in enumerate(q.get('options', [])):
            if cols[i].button(f"{chr(65+i)}. {option}", key=f"opt_{i}", use_container_width=True):
                st.session_state.total_questions += 1
                if option == q['answer']: 
                    st.session_state.correct_answers += 1
                    st.success(f"🎉 Excellent! The answer is **{q['answer']}**.")
                else: 
                    st.error(f"🤔 Not quite. The correct answer was **{q['answer']}**.")
                if 'explanation' in q: st.info(f"💡 **Explanation:** {q['explanation']}")
                st.session_state.quiz_mode = False
                if st.button("🔄 Next Question", key="next_q"): 
                    generate_quiz_question()
                    st.rerun()
                st.stop()
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.recitation_mode:
        st.info(f"**Recitation Practice!**\n\nPlease recite the following shloka:\n\n### {st.session_state.shloka_to_recite}")
        recitation_audio = mic_recorder(start_prompt="🎤 Start Recitation", stop_prompt="⏹️ Stop", key='recite_recorder')
        if recitation_audio:
            with st.spinner("🧘 Analyzing your recitation..."):
                try:
                    audio_io = io.BytesIO(recitation_audio['bytes'])
                    audio_file = genai.upload_file(audio_io, mime_type="audio/wav")
                    feedback_prompt = f"A user recited this Sanskrit shloka: '{st.session_state.shloka_to_recite}'. This is their audio recording. Please listen and provide constructive feedback on their pronunciation and clarity in a friendly tone."
                    response = model.generate_content([feedback_prompt, audio_file])
                    st.success("**Feedback on your recitation:**")
                    st.markdown(response.text)
                    genai.delete_file(audio_file.name)
                    st.session_state.recitation_mode = False
                    if st.button("Try another shloka"):
                        get_shloka_for_recitation()
                        st.rerun()
                except Exception as e:
                    st.error(f"😅 Could not analyze your recitation: {str(e)}")
    else:
        # Display chat history
        for i, message in enumerate(st.session_state.chat.history[1:]):
            with st.chat_message("SanskritAI" if message.role == "model" else "user", avatar="🤖" if message.role == "model" else "👤"):
                st.markdown(message.parts[0].text)
                if message.role == "model":
                    if st.button("🔊 Play Audio", key=f"play_audio_{i}"):
                        audio_output = text_to_audio(message.parts[0].text)
                        if audio_output:
                            st.audio(audio_output, format='audio/mp3', autoplay=True)

    # User Input Section with Audio
    if st.session_state.voice_input_mode:
        st.info("Please record your message now.")
        audio_bytes = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="⏹️ Stop Recording", key='recorder')
        if st.button("Cancel"):
            st.session_state.voice_input_mode = False
            st.rerun()
        user_prompt = None
    else:
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            user_prompt = st.chat_input("Ask me anything about Sanskrit... 💬")
        with col2:
            if st.button("🎤", key="activate_voice"):
                st.session_state.voice_input_mode = True
                st.rerun()
        audio_bytes = None

    final_user_input = None
    if user_prompt:
        final_user_input = user_prompt
    elif audio_bytes:
        st.session_state.voice_input_mode = False # Exit voice mode after recording
        with st.spinner("🎧 Transcribing your voice..."):
            try:
                audio_io = io.BytesIO(audio_bytes['bytes'])
                audio_file = genai.upload_file(audio_io, mime_type="audio/wav")
                feedback_prompt = "Transcribe this audio recording."
                response = model.generate_content([feedback_prompt, audio_file])
                final_user_input = response.text.strip()
                genai.delete_file(audio_file.name)
            except Exception as e:
                st.error(f"😅 Could not transcribe your audio: {str(e)}")

    if final_user_input:
        st.session_state.messages_sent += 1
        try:
            st.session_state.chat.send_message(final_user_input)
        except Exception as e: 
            st.error(f"⚠️ An error occurred: {e}")
        st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown("### 🧠 Choose AI Persona")
        selected_persona = st.selectbox("Select AI Expert", options=list(personas.keys()))
        if selected_persona != st.session_state.ai_persona:
            st.session_state.ai_persona = selected_persona
            st.session_state.chat = None # Reset chat to apply new persona
            st.rerun()

        st.markdown("### 🚀 Quick Actions")
        if st.button("🧩 Start Quiz", use_container_width=True):
            generate_quiz_question()
            st.rerun()
        if st.button("🗣️ Recite a Shloka", use_container_width=True):
            get_shloka_for_recitation()
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Learning Stats")
        st.metric("💬 Messages Sent", st.session_state.messages_sent)
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
            st.metric("🎯 Quiz Accuracy", f"{accuracy:.1f}%")
        else:
            st.metric("🎯 Quiz Accuracy", "No quizzes yet")
        st.markdown("---")
        st.markdown("### 🎨 Theme")
        theme = st.selectbox("Choose Theme", ["🌅 Sunrise (Default)", "🌙 Moonlight", "🌸 Cherry Blossom", "🏔️ Mountain"])
        if theme != "🌅 Sunrise (Default)":
            apply_theme(theme)

# --- App Logic ---
load_css()
if not st.session_state.get("logged_in", False):
    show_login_page()
else:
    show_chatbot_page()
