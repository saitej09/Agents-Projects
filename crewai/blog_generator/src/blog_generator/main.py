#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import BlogGenerator
import streamlit as st

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
st.set_page_config(page_icon="📝", layout="wide")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class BlogCrew:

    def __init__(self, topic, temperature=0.7, model="GPT-4o Mini"):
        self.topic = topic
        self.temperature = temperature
        self.model = model
        self.output = st.empty()
        pass

    def run(self):
        """
        Run the crew.
        """
        # "Vertical AI Agents"
        inputs = {"topic": self.topic}

        try:
            blog = (
                BlogGenerator(temperature=self.temperature, model=model)
                .crew()
                .kickoff(inputs=inputs)
            )
            self.output.markdown(blog)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

        return blog


if __name__ == "__main__":
    icon("📝 AI Blog Generator")

    with st.sidebar:
        st.header("👇 Enter your topic")
        topic = st.text_area(
            "topic", placeholder="Enter the topic you want to generate content about..."
        )
        st.header("Advanced Settings")
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=10.0, value=1.0, step=0.01
        )
        model = st.radio("Choose a model", ["Deepseek", "GPT-4o Mini", "Claude"])
        generate_button = st.button("Generate Content")

    st.title("AI Generated Blog")
    if generate_button:
        with st.status(
            "🤖 **Agents at work...**", state="running", expanded=True
        ) as status:
            with st.container(height=500, border=False):
                if model not in ["GPT-4o Mini"]:
                    st.error("Model Not Supported..!")

                blogcrew = BlogCrew(topic=topic, model=model, temperature=temperature)
                blog_content = blogcrew.run()
            status.update(label="✅ Content Ready!", state="complete", expanded=False)

        st.subheader("AI Blog", anchor=False, divider="rainbow")
        st.markdown(blog_content)
