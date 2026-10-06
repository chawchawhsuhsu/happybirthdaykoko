import streamlit as st
from pathlib import Path


def show_toto_forest():

    # =========================================================
    # SESSION STATE
    # =========================================================

    if "toto_found" not in st.session_state:
        st.session_state.toto_found = set()

    if "toto_memory" not in st.session_state:
        st.session_state.toto_memory = None

    # =========================================================
    # PROJECT PATH
    # =========================================================

    BASE_DIR = Path(__file__).resolve().parent.parent
    IMAGE_DIR = BASE_DIR / "assets" / "images"

    # =========================================================
    # MEMORY DATA
    # =========================================================

    memories = [
        {
            "title": "our 3 monthsary",
            "subtitle": "04 • 06 • 2025",
            "image": IMAGE_DIR / "memory1.png",
            "message": (
                "The one of the first little pages of our story. "

            ),
            "symbol": "🌸",
        },
        {
            "title": "PRINCESS LAY",
            "subtitle": "YOUR PRINCESS 🤍",
            "image": IMAGE_DIR / "mypicturewithflowers.jpg",
            "message": (
                "A little piece of the girl who made "
                "this entire adventure for you. Thank you for the flowers"
            ),
            "symbol": "🤍",
        },
        {
            "title": "SPECIAL COMPANION",
            "subtitle": "THE ONE I'M LOOKING FOR 🤎",
            "image": IMAGE_DIR / "funny2.png",
            "message": (
                "Somewhere in this forest, a special friend is waiting..."
            ),
            "symbol": "🤎",
        },
        {
            "title": "OUR LITTLE WORLD",
            "subtitle": "YOU + ME",
            "image": IMAGE_DIR / "youandme.jpg",
            "message": (
                "Different days. Different places. "
                "But somehow, they became our memories."
            ),
            "symbol": "🦋",
        },
        {
            "title": "My Fav photo of you",
            "subtitle": "FOR YOU ✨",
            "image": IMAGE_DIR / "secretmemory.jpg",
            "message": (
                "You found the last butterfly. "
                "And the forest has one final secret..."
            ),
            "symbol": "✨",
        },
    ]

    # =========================================================
    # CSS STYLES
    # =========================================================

    st.markdown(
        """
        <style>

        /* MAIN PAGE */
        .stApp {
            background:
                radial-gradient(
                    circle at 50% 15%,
                    rgba(84, 66, 105, 0.35),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 15% 80%,
                    rgba(90, 56, 58, 0.35),
                    transparent 35%
                ),
                linear-gradient(
                    180deg,
                    #080a16 0%,
                    #101322 45%,
                    #151019 100%
                );
            color: #f8f3f8;
        }

        /* HIDE STREAMLIT UI */
        #MainMenu, header, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* STARS */
        .stars {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background-image:
                radial-gradient(
                    circle,
                    rgba(255,255,255,0.85) 1px,
                    transparent 1px
                ),
                radial-gradient(
                    circle,
                    rgba(255,255,255,0.45) 1px,
                    transparent 1px
                );
            background-size: 95px 95px, 155px 155px;
            background-position: 15px 25px, 70px 90px;
            opacity: 0.42;
        }

        /* MOON */
        .moon {
            position: fixed;
            top: 65px;
            right: 8%;
            width: 105px;
            height: 105px;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle at 35% 30%,
                    #ffffff,
                    #f4ead8 58%,
                    #d7cab9
                );
            box-shadow:
                0 0 25px rgba(255,245,220,0.65),
                0 0 70px rgba(255,235,205,0.25);
            z-index: 1;
        }

        /* HERO */
        .hero {
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 10px 20px 25px;
        }

        .eyebrow {
            color: #bcaaba;
            font-size: 0.75rem;
            letter-spacing: 0.35rem;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .title {
            font-size: clamp(2.5rem, 7vw, 5rem);
            font-weight: 700;
            letter-spacing: 0.1rem;
            margin: 0;
            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #ead9e7,
                    #c8aabd,
                    #ffffff
                );
            background-size: 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 7s ease infinite;
        }

        @keyframes shimmer {
            0% { background-position: 0%; }
            50% { background-position: 100%; }
            100% { background-position: 0%; }
        }

        .subtitle {
            color: #bfb2bd;
            font-size: 1rem;
            margin-top: 10px;
        }

        /* FOREST SCENE */
        .forest {
            position: relative;
            z-index: 2;
            height: 390px;
            overflow: hidden;
            border-radius: 32px;
            border: 1px solid rgba(255,255,255,0.08);
            background:
                radial-gradient(
                    ellipse at 50% 85%,
                    rgba(112,75,73,0.35),
                    transparent 45%
                ),
                radial-gradient(
                    ellipse at 50% 0%,
                    rgba(49,52,85,0.45),
                    transparent 55%
                ),
                linear-gradient(
                    180deg,
                    #11152b,
                    #11151e
                );
            box-shadow: 0 30px 80px rgba(0,0,0,0.45);
        }

        /* TREE SILHOUETTES */
        .tree {
            position: absolute;
            bottom: -35px;
            width: 0;
            height: 0;
            border-left: 60px solid transparent;
            border-right: 60px solid transparent;
            border-bottom: 180px solid rgba(18,32,29,0.96);
        }

        .tree::before {
            content: "";
            position: absolute;
            left: -50px;
            top: 45px;
            width: 0;
            height: 0;
            border-left: 50px solid transparent;
            border-right: 50px solid transparent;
            border-bottom: 135px solid rgba(20,39,34,0.96);
        }

        .tree::after {
            content: "";
            position: absolute;
            left: -38px;
            top: 100px;
            width: 0;
            height: 0;
            border-left: 38px solid transparent;
            border-right: 38px solid transparent;
            border-bottom: 105px solid rgba(23,43,36,0.96);
        }

        .tree1 { left: 3%; transform: scale(1.15); }
        .tree2 { left: 20%; transform: scale(0.7); }
        .tree3 { right: 18%; transform: scale(0.9); }
        .tree4 { right: 2%; transform: scale(1.25); }

        /* FOREST GROUND & LIGHTS */
        .ground {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 105px;
            background: radial-gradient(ellipse, rgba(91,61,65,0.55), transparent 70%);
        }

        .firelight {
            position: absolute;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: 220px;
            height: 110px;
            background: radial-gradient(ellipse, rgba(218,145,96,0.20), transparent 70%);
            filter: blur(10px);
        }

        /* FIREFLIES */
        .firefly {
            position: absolute;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: #fff2aa;
            box-shadow: 0 0 8px #ffe99a, 0 0 20px rgba(255,235,150,0.7);
            animation: fireflyFloat 4s ease-in-out infinite;
        }

        .ff1 { left: 12%; top: 40%; }
        .ff2 { left: 25%; top: 25%; animation-delay: 1s; }
        .ff3 { left: 39%; top: 55%; animation-delay: 2s; }
        .ff4 { right: 25%; top: 35%; animation-delay: 0.7s; }
        .ff5 { right: 12%; top: 58%; animation-delay: 1.5s; }
        .ff6 { left: 52%; top: 20%; animation-delay: 2.2s; }

        @keyframes fireflyFloat {
            0%, 100% { transform: translateY(0); opacity: 0.3; }
            50% { transform: translateY(-18px); opacity: 1; }
        }

        /* INTRO */
        .intro {
            position: relative;
            z-index: 2;
            max-width: 750px;
            margin: 25px auto;
            padding: 25px;
            text-align: center;
            border-radius: 24px;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
        }

        .intro-title { font-size: 1.4rem; color: #ead9e7; margin-bottom: 10px; }
        .intro-text { color: #bdb0bc; line-height: 1.7; }

        /* COUNTER & HEADINGS */
        .counter {
            position: relative;
            z-index: 2;
            text-align: center;
            color: #cbb9c8;
            letter-spacing: 0.15rem;
            font-size: 0.8rem;
            margin-bottom: 10px;
        }

        .hunt-title {
            position: relative;
            z-index: 2;
            text-align: center;
            color: #d7c5d4;
            font-size: 0.9rem;
            letter-spacing: 0.18rem;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        /* STREAMLIT BUTTONS */
        div.stButton > button {
            min-height: 85px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.12);
            background: linear-gradient(145deg, rgba(106,78,105,0.30), rgba(43,37,55,0.72));
            color: #f6edf5;
            font-size: 0.92rem;
            box-shadow: 0 10px 28px rgba(0,0,0,0.25);
            transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-5px) scale(1.02);
            border: 1px solid rgba(235,205,231,0.45);
            box-shadow: 0 15px 35px rgba(172,117,157,0.22);
            color: white;
        }

        /* MEMORY DISPLAY */
        .memory-wrapper {
            position: relative;
            z-index: 3;
            margin-top: 30px;
            padding: 30px;
            border-radius: 30px;
            background: linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.025));
            border: 1px solid rgba(255,255,255,0.14);
            box-shadow: 0 30px 80px rgba(0,0,0,0.42);
            backdrop-filter: blur(15px);
        }

        .memory-heading { text-align: center; font-size: 1.8rem; color: #f2e4f1; letter-spacing: 0.08rem; }
        .memory-subheading { text-align: center; color: #bca7b9; font-size: 0.75rem; letter-spacing: 0.22rem; margin-top: 5px; margin-bottom: 22px; }
        .memory-message { text-align: center; color: #d0c1cf; line-height: 1.7; font-size: 1rem; margin-top: 18px; margin-bottom: 5px; }

        /* IMAGE CONTAINER */
        [data-testid="stImage"] {
            border-radius: 22px;
            overflow: hidden;
            box-shadow: 0 15px 45px rgba(0,0,0,0.35);
        }

        /* FINAL CARD */
        .final-card {
            position: relative;
            z-index: 3;
            margin-top: 35px;
            padding: 40px 25px;
            text-align: center;
            border-radius: 30px;
            background: radial-gradient(circle at center, rgba(121,84,108,0.23), rgba(255,255,255,0.035));
            border: 1px solid rgba(240,214,237,0.18);
            box-shadow: 0 0 60px rgba(171,116,157,0.13);
        }

        .final-symbol {
            font-size: 4rem;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.12); }
        }

        .final-title { font-size: 2rem; color: #f5e8f3; margin-top: 10px; }
        .final-text { max-width: 650px; margin: 12px auto; color: #cbbbc8; line-height: 1.7; }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # BACKGROUND
    # =========================================================

    st.markdown('<div class="stars"></div><div class="moon"></div>', unsafe_allow_html=True)

    # =========================================================
    # HERO
    # =========================================================

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">CHAPTER III</div>
            <h1 class="title">THE ENCHANTED FOREST</h1>
            <div class="subtitle">Five little memories are hiding among the trees...</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # FOREST SCENE
    # =========================================================

    st.markdown(
        """
        <div class="forest">
            <div class="tree tree1"></div>
            <div class="tree tree2"></div>
            <div class="tree tree3"></div>
            <div class="tree tree4"></div>
            <div class="ground"></div>
            <div class="firelight"></div>
            <div class="firefly ff1"></div>
            <div class="firefly ff2"></div>
            <div class="firefly ff3"></div>
            <div class="firefly ff4"></div>
            <div class="firefly ff5"></div>
            <div class="firefly ff6"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # INTRO
    # =========================================================

    st.markdown(
        """
        <div class="intro">
            <div class="intro-title">🦋 THE MEMORY HUNT</div>
            <div class="intro-text">
                The forest keeps little pieces of our story.<br>
                Five butterflies have hidden them among the trees.<br><br>
                Find them all.<br>
                Each butterfly will reveal a memory.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # COUNTER & HUNT TITLE
    # =========================================================

    found = len(st.session_state.toto_found)

    st.markdown(
        f"""
        <div class="counter">🦋 MEMORIES DISCOVERED &nbsp; {found} / 5</div>
        <div class="hunt-title">✦ The butterflies are waiting ✦</div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # BUTTERFLY BUTTONS
    # =========================================================

    columns = st.columns(5)

    butterfly_labels = [
        "🦋\nFIRST MEMORY",
        "🤍\nPRINCESS LAY",
        "🤎\nCOMPANION",
        "🦋\nOUR WORLD",
        "✨\nSECRET",
    ]

    for i, column in enumerate(columns):
        with column:
            if i in st.session_state.toto_found:
                st.button(
                    "✨\nDISCOVERED",
                    key=f"toto_found_{i}",
                    use_container_width=True,
                    disabled=True,
                )
            else:
                if st.button(
                    butterfly_labels[i],
                    key=f"toto_butterfly_{i}",
                    use_container_width=True,
                ):
                    st.session_state.toto_found.add(i)
                    st.session_state.toto_memory = i
                    st.rerun()

    # =========================================================
    # MEMORY REVEAL
    # =========================================================

    active = st.session_state.toto_memory

    if active is not None:
        memory = memories[active]

        st.markdown(
            f"""
            <div class="memory-wrapper">
                <div class="memory-heading">
                    {memory["symbol"]} {memory["title"]}
                </div>
                <div class="memory-subheading">
                    {memory["subtitle"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if memory["image"].exists():
            st.image(str(memory["image"]), use_container_width=True)
        else:
            st.error(f"Could not find {memory['image'].name}")

        st.markdown(
            f"""
            <div class="memory-message">
                {memory["message"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================
    # ALL FIVE FOUND
    # =========================================================

    if found == 5:
        st.markdown(
            """
            <div class="final-card">
                <div class="final-symbol">🤎</div>
                <div class="final-title">THE FOREST REMEMBERS</div>
                <div class="final-text">
                    You found every butterfly.<br><br>
                    Five memories.<br>
                    One little story.<br><br>
                    But there is still one place you haven't discovered...<br>
                    <strong>The Princess Castle.</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        left, center, right = st.columns([1, 2, 1])
        with center:
            if st.button(
                "🏰 ENTER THE PRINCESS CASTLE →",
                use_container_width=True,
                key="forest_to_castle",
            ):
                st.session_state.scene = "princess_castle"
                st.session_state.toto_found = set()
                st.session_state.toto_memory = None
                st.rerun()