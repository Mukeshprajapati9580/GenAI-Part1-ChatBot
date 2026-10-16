import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🎬 Movie Information Extractor")
st.write("Enter a movie paragraph and extract structured information using AI.")

# -----------------------------
# Schema
# -----------------------------
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


# -----------------------------
# Parser
# -----------------------------
parser = PydanticOutputParser(
    pydantic_object=Movie
)

# -----------------------------
# Prompt
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Extract movie information from the paragraph.

        {format_instructions}

        Extract only the information available in the paragraph.
        If some optional information is not available, return null.
        """
    ),
    (
        "human",
        "{paragraph}"
    )
]).partial(
    format_instructions=parser.get_format_instructions()
)

# -----------------------------
# Model
# -----------------------------
model = ChatGroq(
    model="openai/gpt-oss-120b"
)

# -----------------------------
# Text Area
# -----------------------------
paragraph = st.text_area(
    "📝 Enter Movie Paragraph",
    height=200,
    placeholder="Example: Interstellar is a visually stunning science fiction epic directed by Christopher Nolan..."
)

# -----------------------------
# Extract Button
# -----------------------------
if st.button("🔍 Extract Movie Information", type="primary"):

    if not paragraph.strip():
        st.warning("Please enter a movie paragraph first.")

    else:
        try:
            with st.spinner("Extracting movie information..."):

                # Create final prompt
                final_prompt = prompt.invoke({
                    "paragraph": paragraph
                })

                # Call model
                response = model.invoke(final_prompt)

                # Parse model response
                movie = parser.parse(response.content)

            st.success("Movie information extracted successfully!")

            # -----------------------------
            # Display Results
            # -----------------------------

            st.subheader("🎬 Movie Details")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Title**")
                st.write(movie.title)

                st.write("**Release Year**")
                st.write(movie.release_year)

                st.write("**Genre**")
                st.write(", ".join(movie.genre))

            with col2:
                st.write("**Director**")
                st.write(movie.director)

                st.write("**Rating**")
                st.write(movie.rating)

                st.write("**Cast**")
                st.write(", ".join(movie.cast))

            st.subheader("📖 Summary")
            st.write(movie.summary)

            # -----------------------------
            # Structured Output
            # -----------------------------
            with st.expander("🔧 View Structured Output"):
                st.json(movie.model_dump())

        except Exception as e:
            st.error("Something went wrong.")
            st.exception(e)