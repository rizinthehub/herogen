import streamlit as st
import time
import random


def _normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


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

    # Title
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom:8px;">
            <div style="font-size:24px; font-weight:700; color:#2B3A4A;">
                {story.get('title', 'My Story')}
            </div>
            <div style="font-size:13px; color:#5A6B7D; margin-top:4px;">
                Page {page_idx + 1} of {len(pages)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Green progress bar
    progress_pct = int(((page_idx + 1) / len(pages)) * 100)
    st.markdown(
        f"""
        <div style="max-width:800px; margin:0 auto 20px auto;">
            <div style="font-size:12px; color:#5A6B7D; margin-bottom:4px;">Story Progress</div>
            <div style="background:#E0ECF8; height:8px; border-radius:4px; overflow:hidden;">
                <div style="background:#2ECC71; height:100%; width:{progress_pct}%;
                            border-radius:4px; transition:width 0.5s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Image and Text side by side
    img_col, text_col = st.columns([2, 3])

    with img_col:
        if page_idx < len(images) and images[page_idx]:
            st.image(images[page_idx], use_column_width=True)

    with text_col:
        st.markdown(
            f"""<div style="font-size:26px; line-height:1.9; padding:25px;
                background-color:#FFFDF5; border-radius:12px;
                border:2px solid #FFE5B4; color:#2B3A4A; font-weight:500;">
                {page.get('text', '')}</div>""",
            unsafe_allow_html=True,
        )

    # Quiz section
    quiz_question = page.get("quiz", "What do you think?")
    options = page.get("options", ["Option A", "Option B"])
    correct_idx = page.get("correct_answer", 0)

    if not isinstance(correct_idx, int):
        correct_idx = 0
    if correct_idx < 0 or correct_idx >= len(options):
        correct_idx = 0

    correct_answer = options[correct_idx]

    # Shuffle once per page
    shuffle_key = f"shuffled_{page_idx}"
    if shuffle_key not in st.session_state:
        shuffled = options.copy()
        random.shuffle(shuffled)
        st.session_state[shuffle_key] = shuffled

    shuffled_options = st.session_state[shuffle_key]

    # Quiz banner
    st.markdown(
        f"""
        <div style="text-align:center; margin:20px 0 8px 0;">
            <span style="background:#EBF4FF; color:#2B6CB0; font-weight:600;
                         font-size:15px; padding:8px 20px; border-radius:20px;
                         display:inline-block;">
                Complete the Task to Continue
            </span>
        </div>
        <div style="text-align:center; font-size:14px; color:#5A6B7D; margin-bottom:12px;">
            {quiz_question}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Colored option pills
    option_colors = ["#E74C3C", "#2B6CB0", "#27AE60"]
    pills_html = ""
    for i, opt in enumerate(shuffled_options):
        color = option_colors[i % 3]
        pills_html += (
            f'<span style="display:inline-block; border:2px solid {color};'
            f' border-radius:25px; padding:6px 18px; margin:4px 6px;'
            f' color:{color}; font-weight:600; font-size:13px;">'
            f'{opt}</span>'
        )

    st.markdown(
        f'<div style="text-align:center; margin-bottom:8px;">{pills_html}</div>',
        unsafe_allow_html=True,
    )

    # Functional radio
    answer = st.radio(
        "Choose your answer:",
        shuffled_options,
        key=f"quiz_{page_idx}",
        label_visibility="collapsed",
    )

    # Bottom buttons
    btn_l, btn_spacer, btn_r = st.columns([1, 2, 1])

    with btn_l:
        if st.button("📖 Re-read Page", key=f"reread_{page_idx}"):
            st.rerun()

    with btn_r:
        if st.button(
            "Continue ➡️",
            key=f"continue_{page_idx}",
            type="primary",
        ):
            if _normalize_text(answer) == _normalize_text(correct_answer):
                st.success("🎉 Correct!")
                st.session_state.current_page += 1
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Not quite right! Try a different answer. 💪")