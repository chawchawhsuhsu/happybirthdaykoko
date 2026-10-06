import streamlit as st


def show_nickname_garden():

    st.title("🌸 THE NICKNAME GARDEN")

    st.subheader("Where little memories bloom...")

    st.markdown(
        "🤍 🌸 🤎 🌸 🤍"
    )

    st.divider()

    questions = [
        {
            "question": "What do you call me?",
            "answers": [
                "Princess Lay 🤍",
                "Little Flower 🌸",
                "My Queen 👑",
                "Baby Toto 🤎",
            ],
            "correct": 0,
        },
        {
            "question": "What do I call you?",
            "answers": [
                "Toto 🤎",
                "Prince Toto 👑",
                "Mr. Handsome ✨",
                "Little Bear 🧸",
            ],
            "correct": 0,
        },
        {
            "question": "When did our story begin?",
            "answers": [
                "April 4, 2025 💌",
                "October 9, 1999 🤎",
                "December 25, 2003 🎄",
                "February 14, 2025 💕",
            ],
            "correct": 0,
        },
    ]

    # Initialize state
    if "nickname_question" not in st.session_state:
        st.session_state.nickname_question = 0

    if "nickname_score" not in st.session_state:
        st.session_state.nickname_score = 0

    if "nickname_answered" not in st.session_state:
        st.session_state.nickname_answered = False

    if "nickname_finished" not in st.session_state:
        st.session_state.nickname_finished = False

    # ------------------------------------------
    # FINISHED
    # ------------------------------------------

    if st.session_state.nickname_finished:

        st.success("🌸 You remembered them all! 🤍")

        st.markdown(
            """
            ### 🤍 The garden has opened.

            The flowers remember the beginning of your story.

            **April 4, 2025** 💌

            Toto 🤎, another chapter is waiting...
            """
        )

        st.write("")

        if st.button(
            "🤍 ENTER THE WHITE HEART KINGDOM 🤍",
            use_container_width=True,
        ):
            st.session_state.scene = "white_heart"

            st.session_state.nickname_question = 0
            st.session_state.nickname_score = 0
            st.session_state.nickname_answered = False
            st.session_state.nickname_finished = False

            st.rerun()

        return

    # ------------------------------------------
    # CURRENT QUESTION
    # ------------------------------------------

    question_number = st.session_state.nickname_question

    question = questions[question_number]

    st.caption(
        f"MEMORY {question_number + 1} / {len(questions)}"
    )

    st.header(question["question"])

    st.write("Choose carefully... 🌸")

    st.write("")

    # ------------------------------------------
    # ANSWERS
    # ------------------------------------------

    columns = st.columns(2)

    for i, answer in enumerate(question["answers"]):

        with columns[i % 2]:

            if st.button(
                answer,
                key=f"nickname_{question_number}_{i}",
                use_container_width=True,
            ):

                if i == question["correct"]:

                    st.session_state.nickname_score += 1

                    st.session_state.nickname_answered = True

                    st.success(
                        "✨ Of course you remembered. 🤍"
                    )

                else:

                    st.session_state.nickname_answered = True

                    st.warning(
                        "🌸 Hmm... think about your Princess Lay 🤍"
                    )

    # ------------------------------------------
    # CONTINUE
    # ------------------------------------------

    if st.session_state.nickname_answered:

        st.write("")

        st.write(
            f"🌷 Memories remembered: "
            f"**{st.session_state.nickname_score} / {len(questions)}**"
        )

        if st.button(
            "🌷 Continue through the garden",
            use_container_width=True,
        ):

            if question_number + 1 >= len(questions):

                st.session_state.nickname_finished = True

            else:

                st.session_state.nickname_question += 1

            st.session_state.nickname_answered = False

            st.rerun()