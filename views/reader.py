import streamlit as st
import time
import random


def show():
    story = st.session_state.get("story_data")
    images = st.session_state.get("image_urls", [])

    if not story:
        st.error("No story found!")
        if st.button("Go to Create Page"):
            st.session_state.page = "create"
            st.rerun()
        return

    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    page_idx = st.session_state.current_page
    pages = story.get("pages", [])

    if page_idx >= len(pages):
        st.session_state.page = "dashboard"
        st.rerun()
        return

    page = pages[page_idx]

    st.markdown(
        f"<h2 style='text-align:center; color:#FF6B6B;'>{story['title']}</h2>"
        f"<p style='text-align:center; color:#888;'>Page {page_idx + 1} of {len(pages)}</p>",
        unsafe_allow_html=True,
    )
    st.progress((page_idx + 1) / len(pages))

    img_col, text_col = st.columns([2, 3])

    with img_col:
        if page_idx < len(images) and images[page_idx]:
            st.image(images[page_idx], use_column_width=True)

    with text_col:
        st.markdown(
            f"<div style='font-size:26px; line-height:1.9; padding:25px; "
            f"background-color:#FFFDF5; border-radius:12px; "
            f"border:2px solid #FFE5B4; color:#333; font-weight:500;'>"
            f"{page.get('text', '')}</div>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader(page.get("quiz", "What do you think?"))

    options = page.get("options", ["Option A", "Option B"])
    correct_idx = page.get("correct_answer", 0)
    correct_answer = options[correct_idx]

    shuffle_key = f"shuffled_{page_idx}"
    if shuffle_key not in st.session_state:
        shuffled = options.copy()
        random.shuffle(shuffled)
        st.session_state[shuffle_key] = shuffled

    shuffled_options = st.session_state[shuffle_key]
    answer = st.radio("Choose:", shuffled_options, key=f"quiz_{page_idx}")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Submit Answer", key=f"submit_{page_idx}", type="primary"):
            if answer == correct_answer:
                st.success("Correct! Great job!")
                st.session_state.current_page += 1
                time.sleep(1)
                st.rerun()
            else:
                st.error("Not quite! Try again!")
    with col2:
        if st.button("Skip", key=f"skip_{page_idx}"):
            st.session_state.current_page += 1
            st.rerun()