import streamlit as st


def show_white_heart():

    # =========================================================
    # PAGE CONFIG & STYLES
    # =========================================================

    st.markdown(
        """
        <style>

        /* WHOLE PAGE */
        .stApp {
            background:
                radial-gradient(
                    circle at 50% 10%,
                    #34375f 0%,
                    #191a35 35%,
                    #0b0d20 75%,
                    #050611 100%
                );
            color: white;
        }

        /* Hide normal Streamlit decoration */
        #MainMenu, footer, header {
            visibility: hidden;
        }

        /* STAR FIELD */
        .stars {
            position: relative;
            height: 35px;
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 15px;
            letter-spacing: 22px;
            margin-bottom: 5px;
        }

        /* HERO */
        .kingdom-hero {
            position: relative;
            text-align: center;
            padding: 25px 20px 35px 20px;
        }

        .moon {
            font-size: 72px;
            line-height: 1;
            filter:
                drop-shadow(0 0 12px rgba(255,255,255,0.8))
                drop-shadow(0 0 35px rgba(214,220,255,0.7));
            animation: moonGlow 3s ease-in-out infinite alternate;
        }

        @keyframes moonGlow {
            from {
                transform: scale(1);
                filter:
                    drop-shadow(0 0 10px rgba(255,255,255,0.7))
                    drop-shadow(0 0 25px rgba(214,220,255,0.5));
            }
            to {
                transform: scale(1.06);
                filter:
                    drop-shadow(0 0 18px rgba(255,255,255,0.95))
                    drop-shadow(0 0 45px rgba(214,220,255,0.8));
            }
        }

        .hero-title {
            margin-top: 18px;
            font-size: 38px;
            font-weight: 700;
            letter-spacing: 5px;
            color: #ffffff;
            text-shadow:
                0 0 10px rgba(255,255,255,0.7),
                0 0 25px rgba(190,200,255,0.5);
        }

        .hero-subtitle {
            margin-top: 12px;
            font-size: 16px;
            color: #d9dcf7;
            letter-spacing: 2px;
        }

        /* FLOATING HEARTS */
        .floating-hearts {
            position: relative;
            height: 85px;
            overflow: hidden;
            margin-top: -10px;
        }

        .heart {
            position: absolute;
            font-size: 20px;
            opacity: 0.7;
            animation: floatHeart 5s ease-in-out infinite;
        }

        .heart.one { left: 12%; animation-delay: 0s; }
        .heart.two { left: 30%; animation-delay: 1.2s; }
        .heart.three { left: 55%; animation-delay: 2s; }
        .heart.four { left: 76%; animation-delay: 0.7s; }
        .heart.five { left: 90%; animation-delay: 2.7s; }

        @keyframes floatHeart {
            0% { transform: translateY(45px) scale(0.7); opacity: 0; }
            25% { opacity: 0.8; }
            50% { transform: translateY(0px) scale(1); opacity: 1; }
            100% { transform: translateY(-45px) scale(0.7); opacity: 0; }
        }

        /* STORY CARD */
        .story-card {
            max-width: 720px;
            margin: 10px auto 25px auto;
            padding: 30px;
            border-radius: 28px;
            background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.20);
            box-shadow: 0 20px 60px rgba(0,0,0,0.35), inset 0 0 30px rgba(255,255,255,0.03);
            backdrop-filter: blur(12px);
            text-align: center;
        }

        .story-label {
            color: #cfd4ff;
            font-size: 13px;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .story-title {
            margin-top: 12px;
            font-size: 26px;
            color: white;
        }

        .story-text {
            margin-top: 18px;
            line-height: 1.9;
            font-size: 16px;
            color: #e3e5f7;
        }

        /* MEMORY CARD */
        .memory-card {
            max-width: 650px;
            margin: 30px auto;
            padding: 28px;
            border-radius: 24px;
            background: radial-gradient(circle at 50% 0%, rgba(255,255,255,0.15), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.18);
            text-align: center;
            box-shadow: 0 0 35px rgba(190,200,255,0.10);
        }

        .memory-icon { font-size: 32px; margin-bottom: 8px; }

        .memory-date {
            font-size: 30px;
            font-weight: 700;
            letter-spacing: 3px;
            color: #ffffff;
            text-shadow: 0 0 12px rgba(255,255,255,0.6);
        }

        .memory-line {
            margin-top: 15px;
            color: #d7daf3;
            line-height: 1.8;
            font-size: 15px;
        }

        /* WHITE HEART */
        .big-heart {
            text-align: center;
            margin: 35px 0 20px 0;
            font-size: 70px;
            animation: heartPulse 2.2s ease-in-out infinite;
            filter: drop-shadow(0 0 12px rgba(255,255,255,0.9)) drop-shadow(0 0 35px rgba(210,220,255,0.7));
        }

        @keyframes heartPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.13); }
            100% { transform: scale(1); }
        }

        /* QUESTION AREA */
        .question-card {
            max-width: 720px;
            margin: 30px auto 15px auto;
            padding: 25px;
            border-radius: 25px;
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.16);
            text-align: center;
        }

        .question-title { font-size: 23px; color: white; }
        .question-subtitle { margin-top: 10px; color: #cdd1ed; font-size: 15px; }

        /* SURPRISE VIDEO HEADER */
        .surprise-header {
            text-align: center;
            margin: 25px 0 15px 0;
            font-size: 20px;
            color: #ffffff;
            letter-spacing: 2px;
            text-shadow: 0 0 12px rgba(255,255,255,0.7);
        }

        /* MAGIC PATH AFTER ANSWER */
        .path-card {
            max-width: 700px;
            margin: 30px auto;
            padding: 30px;
            border-radius: 26px;
            background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(211,218,255,0.04));
            border: 1px solid rgba(255,255,255,0.22);
            text-align: center;
            box-shadow: 0 0 45px rgba(205,215,255,0.12);
        }

        .path-heart {
            font-size: 50px;
            animation: pathGlow 1.8s ease-in-out infinite alternate;
        }

        @keyframes pathGlow {
            from { filter: drop-shadow(0 0 5px white); }
            to { filter: drop-shadow(0 0 25px white); }
        }

        .path-title { margin-top: 15px; font-size: 22px; letter-spacing: 2px; color: white; }
        .path-text { margin-top: 12px; color: #d9dcf4; line-height: 1.8; }

        /* STREAMLIT BUTTONS */
        .stButton > button {
            border-radius: 18px !important;
            border: 1px solid rgba(255,255,255,0.22) !important;
            background: rgba(255,255,255,0.08) !important;
            color: white !important;
            min-height: 52px;
            font-size: 15px !important;
            transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            background: rgba(255,255,255,0.16) !important;
            box-shadow: 0 8px 25px rgba(200,210,255,0.18);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # CONTENT SECTIONS
    # =========================================================

    st.markdown('<div class="stars">✦ · ✧ · ✦ · ✧ · ✦ · ✧ · ✦</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="kingdom-hero">
            <div class="moon">🌙</div>
            <div class="hero-title">THE WHITE HEART KINGDOM</div>
            <div class="hero-subtitle">where little memories glow in the dark</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="floating-hearts">
            <div class="heart one">🤍</div>
            <div class="heart two">✧</div>
            <div class="heart three">♡</div>
            <div class="heart four">🤍</div>
            <div class="heart five">✦</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="story-card">
            <div class="story-label">Chapter II</div>
            <div class="story-title">🌙 Beyond the Garden</div>
            <div class="story-text">
                Thank you so much for always being there for me , koko .<br>
                I love u so so much.<br><br>
                You are the most precious thing for me.
                <br><br>
                I will always love u koko...
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="memory-card">
            <div class="memory-icon">💌</div>
            <div class="story-label">The first page of the story</div>
            <div class="memory-date">04 • 04 • 2025</div>
            <div class="memory-line">
                The day two people who didn't know what was coming walked into the beginning of a story.
                <br><br>
                And somehow...<br>
                <strong>the story kept going. 🤍</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="big-heart">🤍</div>', unsafe_allow_html=True)

    # =========================================================
    # SESSION STATE & QUESTION
    # =========================================================

    if "white_heart_choice" not in st.session_state:
        st.session_state.white_heart_choice = None

    st.markdown(
        """
        <div class="question-card">
            <div class="question-title">🤍 The Kingdom asks you one question...</div>
            <div class="question-subtitle">What do you think keeps a little story alive?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================
    # ANSWERS
    # =========================================================

    choices = [
        "✨ The little memories",
        "🌙 Being there for each other",
        "🌸 The silly moments",
        "🤍 All of them",
    ]

    left, right = st.columns(2)

    with left:
        if st.button(choices[0], key="white_choice_0", use_container_width=True):
            st.session_state.white_heart_choice = 0
            st.rerun()

        if st.button(choices[2], key="white_choice_2", use_container_width=True):
            st.session_state.white_heart_choice = 2
            st.rerun()

    with right:
        if st.button(choices[1], key="white_choice_1", use_container_width=True):
            st.session_state.white_heart_choice = 1
            st.rerun()

        if st.button(choices[3], key="white_choice_3", use_container_width=True):
            st.session_state.white_heart_choice = 3
            st.rerun()

    # =========================================================
    # AFTER ANSWER (SURPRISE VIDEO UNLOCKED)
    # =========================================================

    if st.session_state.white_heart_choice is not None:

        choice = st.session_state.white_heart_choice

        st.write("")

        if choice == 3:
            st.success("🤍 Exactly. A story is made from all the little things.")
        else:
            st.success("🤍 Maybe you're right... but I think it's a little bit of everything.")

        # -----------------------------------------------------
        # 4 VIDEO MAPPING CONFIGURATION
        # -----------------------------------------------------

        video_config = {
            0: {
                "file": "Silly_song.mp4",
                "header": "✨ A gentle memory unlocked in the garden...",
            },
            1: {
                "file": "kisses.mp4",
                "header": "🌙 A special dance for always being there...",
            },
            2: {
                "file": "heartshape.mp4",
                "header": "🌸 A silly moment dancing in the garden...",
            },
            3: {
                "file": "all.mp4",
                "header": "🤍 A piece of everything... just for you!",
            },
        }

        selected_video = video_config[choice]

        st.markdown(
            f"""
            <div class="surprise-header">
                {selected_video["header"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            with open(selected_video["file"], "rb") as video_file:
                st.video(video_file.read(), format="video/mp4")
        except FileNotFoundError:
            st.error(
                f"Video file '{selected_video['file']}' was not found. "
                "Make sure it is placed in the project directory!"
            )

        # -----------------------------------------------------
        # MAGIC PATH
        # -----------------------------------------------------

        st.markdown(
            """
            <div class="path-card">
                <div class="path-heart">🤍</div>
                <div class="path-title">THE KINGDOM RECOGNIZES YOU</div>
                <div class="path-text">
                    The lights around you become brighter.<br><br>
                    One tiny white heart floats through the darkness...<br><br>
                    It moves slowly forward, as if it wants you to follow.<br><br>
                    ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; 🤍 &nbsp; ✦ &nbsp; ✦ &nbsp; ✦
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -----------------------------------------------------
        # NEXT SCENE
        # -----------------------------------------------------

        st.write("")

        if st.button(
            "🤍  FOLLOW THE WHITE HEART  →",
            key="follow_white_heart",
            use_container_width=True,
        ):
            st.session_state.scene = "toto_forest"
            st.session_state.white_heart_choice = None
            st.rerun()