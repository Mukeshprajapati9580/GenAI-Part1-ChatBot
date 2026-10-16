# 🤖 AI Chatbot & LangChain Experiments

A Python project exploring conversational AI with LangChain. It includes a Streamlit chatbot with selectable AI personalities, command-line chat examples, integrations with hosted model providers, a local Hugging Face model example, and movie-information extraction using prompts and structured output.

## ✨ Features

- **Mood AI Chatbot UI** — Streamlit interface with Angry, Funny, and Sad modes.
- **Conversation memory within a session** — keeps chat messages during the current Streamlit session.
- **Groq chat model** — uses `openai/gpt-oss-120b` through LangChain.
- **CLI chatbot** — interact with the model from the terminal and choose a personality.
- **Hugging Face examples** — examples using a hosted Hugging Face endpoint and a local TinyLlama pipeline.
- **Movie information extraction** — extract fields such as title, release year, genre, director, cast, rating, and summary from a paragraph.
- **Structured output** — validates extracted movie information using a Pydantic model.

## 🧰 Tech Stack

- Python
- LangChain / LangChain Core
- LangGraph
- Streamlit
- Groq
- Hugging Face
- Pydantic
- python-dotenv

