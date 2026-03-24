import streamlit as st
import time


def show():
    """Display the interactive story reader with quizzes."""
    story = st.session_state.get("story_data")
    images = st.session_state.get("image_urls", [])

    if not story:
        st.error("No story found! Please create one first.")
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
        f"<h1 style='text-align:center; color:#FF6B6B;'>{story['title']}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center; color:#888;'>"
        f"Page {page_idx + 1} of {len(pages)}</p>",
        unsafe_allow_html=True,
    )

    st.progress((page_idx + 1) / len(pages))

    if page_idx < len(images) and images[page_idx]:
        st.image(images[page_idx], use_container_width=True)

    st.markdown(
        f"""
        <div style="font-size: 22px; line-height: 1.8; padding: 20px;
                    background-color: #FFFDF5; border-radius: 12px;
                    border: 2px solid #FFE5B4; margin: 15px 0;">
            {page.get('text', '')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(f"### {page.get('quiz', 'What do you think?')}")

    options = page.get("options", ["Option A", "Option B"])

    answer = st.radio(
        "Choose your answer:",
        options,
        key=f"quiz_page_{page_idx}",
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button(
            "Submit Answer",
            key=f"submit_{page_idx}",
            type="primary",
        ):
            correct_idx = page.get("correct_answer", 0)
            selected_idx = options.index(answer)

            if selected_idx == correct_idx:
                st.success("Correct! Great job! Moving to the next page...")
                st.session_state.current_page += 1
                time.sleep(1)
                st.rerun()
            else:
                st.error(
                    "Not quite! Think about what's the right thing to do "
                    "and try again!"
                )

    with col2:
        if st.button("Skip", key=f"skip_{page_idx}"):
            st.session_state.current_page += 1
            st.rerun()