import streamlit as st


def show_beginning():

    st.markdown("# 🤎")

    st.title("THE QUEST FOR My Bear")

    st.subheader("A little adventure made by Your Princess Lay")

    st.write("")

    st.markdown("### 04 • 04 • 2025")

    st.write("")
    st.write("")
    st.write("")

    left, middle, right = st.columns([1, 2, 1])

    with middle:
        if st.button(
            "✨ BEGIN THE ADVENTURE ✨",
            use_container_width=True,
        ):
            st.session_state.scene = "nickname_garden"
            st.rerun()