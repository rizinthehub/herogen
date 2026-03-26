import streamlit as st
import os
import base64


def show():
    # Logo
    splash_logo_path = os.path.join("assets", "HeroGenLogoText.png")
    if os.path.exists(splash_logo_path):
        with open(splash_logo_path, "rb") as f:
            splash_b64 = base64.b64encode(f.read()).decode()
        splash_html = (
            f'<img src="data:image/png;base64,{splash_b64}" '
            f'style="height:140px; margin-bottom:12px;">'
        )
    else:
        splash_html = (
            '<div style="font-size:48px; font-weight:800; margin-bottom:12px;">'
            '<span style="color:#2B6CB0;">Hero</span>'
            '<span style="color:#E67E22;">Gen</span>'
            '</div>'
        )

    st.markdown(
        f"""
        <div style="text-align: center; padding: 30px 0 8px 0;">
            {splash_html}
            <div style="font-size:15px; color:#E67E22; font-weight:500; margin-bottom:8px;">
                Be the Hero of Your Own Story
            </div>
            <div style="font-size:15px; color:#5A6B7D; max-width:500px; margin:0 auto;">
                Upload a photo, pick a moral value, and our AI creates a
                personalized storybook in under 60 seconds!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Create Story Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Create Story Now", type="primary", use_container_width=True):
            st.session_state.page = "create"
            st.rerun()

    st.write("")
    st.write("")

    # How It Works
    st.markdown(
        """
        <div style="text-align:center; margin-top:30px;">
            <div style="font-size:18px; font-weight:700; color:#2B3A4A; margin-bottom:4px;">
                How it works
            </div>
            <div style="width:60px; height:3px; background:#E67E22;
                        margin:0 auto 24px auto; border-radius:2px;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    hw1, hw2, hw3 = st.columns(3)

    with hw1:
        st.markdown(
            '<div style="text-align:center; padding:10px;">'
            '<div style="font-size:48px; margin-bottom:10px;">📝</div>'
            '<div style="font-size:14px; color:#5A6B7D; font-weight:500;">Enter details</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    with hw2:
        st.markdown(
            '<div style="text-align:center; padding:10px;">'
            '<div style="font-size:48px; margin-bottom:10px;">📖 ✨</div>'
            '<div style="font-size:14px; color:#5A6B7D; font-weight:500;">Generate story</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    with hw3:
        st.markdown(
            '<div style="text-align:center; padding:10px;">'
            '<div style="font-size:48px; margin-bottom:10px;">✅</div>'
            '<div style="font-size:14px; color:#5A6B7D; font-weight:500;">Complete tasks to continue</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="text-align:center; padding:30px 0 10px 0;">'
        '<p style="color:#5A6B7D; font-size:13px;">'
        'Powered by GPT-4o · DALL-E 3 · Computer Vision</p></div>',
        unsafe_allow_html=True,
    )
