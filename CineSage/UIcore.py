import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# -----------------------------
# Model
# -----------------------------
model = ChatGroq(model="openai/gpt-oss-120b")

# -----------------------------
# Prompt
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional Movie Information Extraction Assistant.

Your task:
Extract useful structured information from a movie paragraph and present it in a clean readable format.

Rules:
- Do NOT add explanations
- Do NOT add extra commentary
- Follow the exact format
- If information is missing -> write NULL
- Keep summary short (2-3 lines max)
- Do NOT guess unknown facts

Output Format:

Movie Title:
Release Year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""
    ),
    (
        "human",
        """
Extract information from this paragraph:

{paragraph}
"""
    )
])

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎬 Movie Information Extractor")
st.write("Enter a movie paragraph to extract useful information.")

paragraph = st.text_area(
    "Enter Movie Paragraph",
    height=200,
    placeholder="Enter your movie paragraph here..."
)

if st.button("Extract Information"):

    if paragraph.strip():

        final_prompt = prompt.invoke(
            {"paragraph": paragraph}
        )

        response = model.invoke(final_prompt)

        st.subheader("Extracted Movie Information")
        st.write(response.content)

    else:
        st.warning("Please enter a movie paragraph.")

