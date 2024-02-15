import streamlit as st
import openai
from gtts import gTTS
import tempfile
import base64
from io import BytesIO
# Set your OpenAI API key here
openai.api_key = "your_api_key"

# Custom CSS for iOS-style theme
custom_css = """
<style>
body {
    background-color: #f4f4f4;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
}
</style>
"""

class SessionState:
    def __init__(self):
        self.topic_input = ""
        self.name_input = ""
        self.grade = 1
        self.subject = "Mathematics"  # Default subject

# Create a session state instance
session_state = SessionState()

# List of CBSE subjects
cbse_subjects = [
    "Mathematics",
    "Science",
    "Social Studies",
    "Environmental Science",
    "English",
    "Telugu"
    "Hindi",
    "Sanskrit",
    "Computer Science",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Geography",
    "Civics",
    "Economics",
    "General",
]

def generate_lesson(topic, grade, subject, name):
    # Input validation
    if not topic:
        return "Please enter a topic."
    if grade < 1 or grade > 10:
        return "Invalid grade. Please select a grade between 1 and 10."

    prompt = f"I want you to teach me about {topic}, I am in {grade} grade, studying {subject}. You should be act like a {grade} teacher and explain this {topic} so that {grade} kid can understand easily"
    if name:
        prompt += f" My name is {name}."
    
    try:
        messages = [
            {"role": "assistant", "content": "You are a helpful AI tutor for kids."},  # Updated role here
            {"role": "user", "content": prompt}
        ]

        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=400  # Set a token limit of 250
        )
        lesson = completion.choices[0].message.content.strip()
        return lesson
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    st.set_page_config(
        page_title="AI Tutor for Kids",
        page_icon="🌟",
        layout="centered"
    )
    
    # Inject custom CSS for iOS-style theme
    st.markdown(custom_css, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 36px;'>AI Tutor for Kids</h1>", unsafe_allow_html=True)
    
    topic = st.text_input("Enter a topic for the lesson:", key="topic_input")
    name = st.text_input("Enter the child's name (optional):", value=session_state.name_input)
    session_state.topic_input = topic
    session_state.name_input = name
    
    grade = st.slider("Select the grade of the child:", min_value=1, max_value=10, value=1)
    subject = st.selectbox("Select the subject:", cbse_subjects, index=0)
    session_state.subject = subject
    lesson_type = st.radio("Select lesson type:", ("Text"))    
    generate_button = st.button("Generate Lesson", key="generate_button")
    
    if generate_button:
        if not name:
            session_state.name_input = "Nanu"
            topic = session_state.topic_input.capitalize() 
 
        if lesson_type == "Text":
            lesson = generate_lesson(topic, grade, session_state.subject, session_state.name_input)
            session_state.topic_input = ""
            st.markdown(f"<h2 style='text-align: center;'> {topic} Lesson Text</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{lesson}</p>", unsafe_allow_html=True)
      

if __name__ == "__main__":
    main()
