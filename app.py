import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Missing GOOGLE_API_KEY in .env")
    st.stop()

client = genai.Client(api_key=api_key)

# Page style and layout
st.set_page_config(page_title="AI Content Generator", layout="wide")
st.markdown("""
    <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            color: #f5f5f5;
        }
        .recommend-box {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #333;
            box-shadow: 0 0 10px rgba(0,0,0,0.4);
            color: #f5f5f5;
        }
        .stMarkdown, .stText, .stTextArea label, .stSlider label {
            color: #f5f5f5 !important;
        }
        .stTextInput > div > div > input, .stTextArea textarea {
            background-color: #1e1e1e;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='big-font'>🤖 AI-Powered Personalized Content Generator</div>", unsafe_allow_html=True)

# User Input
st.subheader("🧑‍💬 Tell us your interests")
user_input = st.text_area("Enter your preferences (e.g., AI, productivity, travel, etc.):", height=120)
num_items = st.slider("How many content pieces would you like?", 3, 7, 5)

# Content Generation
if st.button("✨ Generate AI-Powered Content"):
    if not user_input.strip():
        st.warning("Please enter some interests to generate content.")
    else:
        with st.spinner("Generating with Gemini..."):
            try:
                # Phase 1: Generate content ideas
                prompt_idea = f"""
You are a content creator AI.

User interests: {user_input}

Based on this, generate {num_items} content titles that would be engaging and informative.
For each, also provide a brief explanation of why it suits the user's interests.

Format:
Title: <title>
Why: <reason>
---
"""
                response_ideas = client.models.generate_content(
                    model="gemini-2.5-flash-preview-05-20",
                    contents=[prompt_idea]
                )

                ideas = response_ideas.text.strip().split("---")
                st.subheader("📌 Recommended Titles & Generated Content")

                for idea in ideas:
                    if not idea.strip():
                        continue
                    lines = idea.strip().split("\n")
                    if len(lines) < 2:
                        continue
                    title = lines[0].replace("Title:", "").strip()
                    reason = lines[1].replace("Why:", "").strip()

                    # Phase 2: Generate content for each title
                    content_prompt = f"""
Write a short engaging blog-style content (100-150 words) on the topic: "{title}".
Make it valuable for a person interested in: {user_input}.
Use a friendly tone and keep it clear and informative.
"""
                    content_response = client.models.generate_content(
                        model="gemini-2.5-flash-preview-05-20",
                        contents=[content_prompt]
                    )
                    content_text = content_response.text.strip()

                    # Display in card
                    st.markdown(f"""<div class="recommend-box">
<h4>📌 {title}</h4>
<p><b>Why Recommended:</b> {reason}</p>
<p>{content_text}</p>
</div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error occurred: {e}")