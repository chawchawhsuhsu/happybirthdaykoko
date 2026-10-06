import streamlit as st

from scenes.beginning import show_beginning
from scenes.nickname_garden import show_nickname_garden
from scenes.white_heart import show_white_heart
from scenes.toto_forest import show_toto_forest
from scenes.princess_castle import show_princess_castle
from scenes.birthday import show_birthday_scene


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="The Quest for Toto 🤎",
    page_icon="🤎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "scene" not in st.session_state:
    st.session_state.scene = "beginning"

if "nickname_question" not in st.session_state:
    st.session_state.nickname_question = 0

if "nickname_score" not in st.session_state:
    st.session_state.nickname_score = 0

if "nickname_finished" not in st.session_state:
    st.session_state.nickname_finished = False


# --------------------------------------------------
# GLOBAL CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Hide Streamlit default UI */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 20% 20%,
                rgba(255, 190, 210, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 80% 10%,
                rgba(255, 220, 180, 0.10),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #180e30,
                #32152f,
                #54283f
            );

        color: #fff0eb;
    }

    /* Center content */
    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        min-height: 55px;

        border-radius: 18px;
        border: 1px solid rgba(255, 214, 140, 0.7);

        background:
            linear-gradient(
                135deg,
                rgba(90, 40, 80, 0.95),
                rgba(55, 25, 65, 0.95)
            );

        color: #fff0eb;

        font-size: 18px;
        font-weight: 600;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px);

        box-shadow:
            0 8px 25px rgba(255, 170, 190, 0.25);

        border-color: #ffd68c;
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SCENE ROUTER
# --------------------------------------------------

if st.session_state.scene == "beginning":

    show_beginning()

elif st.session_state.scene == "nickname_garden":

    show_nickname_garden()

elif st.session_state.scene == "white_heart":

    show_white_heart()

elif st.session_state.scene == "toto_forest":

    show_toto_forest()

elif st.session_state.scene == "princess_castle":

    show_princess_castle()

elif st.session_state.scene == "birthday":

    show_birthday_scene()