import streamlit as st
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Mood AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: 800;
        margin-bottom: 5px;
        color: #ffffff;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    /* Mode cards */
    .mode-card {
        padding: 15px;
        border-radius: 15px;
        background: #1f2937;
        margin-bottom: 10px;
        border: 1px solid #374151;
    }

    /* Chat messages */
    .user-message {
        background: #2563eb;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0;
        margin-left: 20%;
    }

    .bot-message {
        background: #374151;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 20% 10px 0;
    }

    /* Input */
    .stChatInput {
        padding-bottom: 20px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Model
# --------------------------------------------------

@st.cache_resource
def load_model():

    return init_chat_model(
        "groq:openai/gpt-oss-120b"
    )


model = load_model()

# --------------------------------------------------
# Mood Configurations
# --------------------------------------------------

modes = {

    "😡 Angry Mode":
        "You are an angry AI agent. "
        "You respond aggressively and impatiently. "
        "However, do not use abusive, hateful, or threatening language.",

    "😂 Funny Mode":
        "You are a very funny AI agent. "
        "You respond with humor, jokes, and playful comments "
        "while still providing useful answers.",

    "😢 Sad Mode":
        "You are a very sad AI agent. "
        "You respond in a melancholic and emotional tone "
        "while still being helpful and respectful."
}

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "mode" not in st.session_state:

    st.session_state.mode = "😂 Funny Mode"


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🎭 AI Personality")

    selected_mode = st.radio(
        "Choose your AI mode:",
        list(modes.keys()),
        index=list(modes.keys()).index(
            st.session_state.mode
        )
    )

    # If mode changed
    if selected_mode != st.session_state.mode:

        st.session_state.mode = selected_mode

        # Reset conversation when mode changes
        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.markdown(
        f"""
        <div class="mode-card">
            <h3>Current Mode</h3>
            <p style="font-size:20px;">
                {st.session_state.mode}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button(
        "🗑️ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.markdown("### 💡 Available Modes")

    st.markdown("""
    **😡 Angry Mode**  
    Impatient and aggressive personality.

    **😂 Funny Mode**  
    Humorous and playful personality.

    **😢 Sad Mode**  
    Emotional and melancholic personality.
    """)


# --------------------------------------------------
# Main UI
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 Mood AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Chat with an AI that changes its personality 🎭'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# Welcome Message
# --------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:30px;
            background:#1f2937;
            border-radius:20px;
            margin-bottom:20px;
        ">

        <h2>👋 Welcome!</h2>

        <p style="font-size:18px;">
        You are currently chatting with
        <b>{st.session_state.mode}</b>
        </p>

        <p>
        Ask me anything to start the conversation.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        st.markdown(
            f"""
            <div class="user-message">
                <b>🧑 You</b><br><br>
                {message.content}
            </div>
            """,
            unsafe_allow_html=True
        )

    elif isinstance(message, AIMessage):

        st.markdown(
            f"""
            <div class="bot-message">
                <b>🤖 AI</b><br><br>
                {message.content}
            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input(
    "Type your message here..."
)


# --------------------------------------------------
# Generate Response
# --------------------------------------------------

if prompt:

    # Display user message
    st.markdown(
        f"""
        <div class="user-message">
            <b>🧑 You</b><br><br>
            {prompt}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add system message + conversation
    messages = [
        SystemMessage(
            content=modes[st.session_state.mode]
        )
    ]

    messages.extend(
        st.session_state.messages
    )

    messages.append(
        HumanMessage(content=prompt)
    )

    # Save user message
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # Generate AI response
    with st.spinner("🤖 AI is thinking..."):

        try:

            response = model.invoke(messages)

            answer = response.content

            # Save AI response
            st.session_state.messages.append(
                AIMessage(content=answer)
            )

            # Display AI response
            st.markdown(
                f"""
                <div class="bot-message">
                    <b>🤖 AI</b><br><br>
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )