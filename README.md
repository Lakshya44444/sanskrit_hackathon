# sanskrit_hackathon

SanskritAI Chatbot 🕉️
Welcome to SanskritAI, a modern, interactive, and AI-powered web application designed to make learning the ancient language of Sanskrit accessible, engaging, and fun. This application leverages the power of Google's Gemini large language models to create a dynamic and personalized learning experience.

Features:
SanskritAI is more than just a chatbot; it's a comprehensive learning platform packed with features to guide you on your journey with Sanskrit:

Secure User Authentication: A beautiful and secure login/signup page to personalize your learning experience.

Conversational AI Tutor: Engage in natural conversations to ask for translations, definitions, and grammar explanations.

Specialized AI Personas: Switch between different AI experts to get focused, citation-backed knowledge:

Pāṇini AI: A master of Sanskrit grammar.

Charak AI: An expert in Ayurvedic principles.

Vyasa AI: A storyteller versed in epic literature like the Mahabharata.

Yoga & Sankhya AI: Guides for profound philosophical concepts.

Interactive Quizzes: Test your knowledge with dynamically generated multiple-choice questions that provide instant feedback and explanations.

Shloka Recitation Practice: Receive a shloka to recite, record your voice, and get personalized AI feedback on your pronunciation and clarity.

On-Demand Audio Playback: Click a button next to any AI response to hear the correct pronunciation, giving you full control over your audio learning.

Voice-to-Text Input: Use your microphone to ask questions in your natural voice, which are then transcribed and sent to the AI.

Customizable Themes: Personalize the application's appearance with beautiful themes like "Sunrise," "Moonlight," and "Cherry Blossom."

Learning Statistics: Track your progress with a sidebar that shows your total messages sent and your quiz accuracy over time.

 Tech Stack
This project is built with a modern stack of Python libraries and APIs:

Frontend: Streamlit - For creating a beautiful, interactive web application with pure Python.

Core AI Logic: Google Gemini API (gemini-1.5-flash) - Powers the conversational AI, knowledge base, and transcription.

Audio Input: streamlit-mic-recorder - A custom component for capturing microphone audio in Streamlit.

Text-to-Speech: gTTS (Google Text-to-Speech) - For converting the AI's text responses into playable audio.

Setup and Installation
To run this project locally, follow these simple steps:

1. Prerequisites
Make sure you have Python 3.8+ and pip installed on your system.

2. Clone the Repository
git clone https://github.com/your-username/sanskrit-ai.git
cd sanskrit-ai

3. Install Dependencies
Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt

(Note: If you don't have a requirements.txt file, you can install the libraries manually: pip install streamlit google-generativeai gtts streamlit-mic-recorder)

4. Set Up Your API Key
For the application to connect to the Gemini API, you need to store your API key securely.

Create a folder named .streamlit in the root of your project directory.

Inside the .streamlit folder, create a file named secrets.toml.

Add your Gemini API key to the secrets.toml file as follows:

# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

5. Run the Application
Once the setup is complete, run the following command in your terminal from the project's root directory:

streamlit run san.py

Your web browser will automatically open with the SanskritAI application running!

📖 How to Use
Login/Sign Up: Create an account or log in to access the chatbot.

Choose a Persona: Use the sidebar to select an AI expert (e.g., Grammar, Ayurveda) to focus your learning session.

Interact:

Type a Message: Use the chat input at the bottom to ask questions.

Use Your Voice: Click the 🎤 button to activate the microphone and speak your query.

Learn with Tools:

Click "Start Quiz" to test your knowledge.

Click "Recite a Shloka" to practice your pronunciation.

Click the "Play Audio" button next to an AI message to hear it spoken.

آینده (Future Enhancements)
Database Integration: Store user progress and chat history in a database like Firestore.

Advanced Analytics: Provide more detailed learning analytics and progress tracking.

Direct Source Citations: Link AI responses directly to the original Sanskrit texts.

Developed with by Lakshya Gupta.
