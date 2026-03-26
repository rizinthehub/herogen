import streamlit as st
from services.pdf_maker import create_full_pdf, create_coloring_pdf, create_edu_pdf


def show():
    story = st.session_state.get("story_data")
    images = st.session_state.get("image_urls", [])
    child_name = st.session_state.get("child_name", "Hero")

    if not story:
        st.error("No story found!")
        if st.button("Create a Story"):
            st.session_state.page = "home"
            st.rerun()
        return

    st.balloons()

    story_title = story.get("title", "My Story")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <div style="font-size:32px; font-weight:700; color:#2B3A4A;">
                🎉 Great Job, {child_name}!
            </div>
            <div style="font-size:18px; color:#E67E22; font-weight:600; margin-top:4px;">
                Your story "{story_title}" is complete!
            </div>
            <div style="font-size:14px; color:#5A6B7D; margin-top:8px;">
                Download your personalized Edu-Pack below
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # Generate PDFs
    if "pdf_full" not in st.session_state:
        with st.spinner("Preparing your downloads..."):
            st.session_state.pdf_full = create_full_pdf(story, images)
            st.session_state.pdf_coloring = create_coloring_pdf(images)
            st.session_state.pdf_edu = create_edu_pdf(story)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div style="background:#FFFFFF; padding:28px 20px; border-radius:20px;'
            ' text-align:center; box-shadow:0 4px 16px rgba(43,108,176,0.10);'
            ' border:1px solid #E0ECF8; margin-bottom:16px;">'
            '<div style="font-size:48px; margin-bottom:12px;">📕</div>'
            '<div style="font-size:18px; font-weight:700; color:#2B3A4A; margin-bottom:6px;">'
            'Full Storybook</div>'
            '<div style="font-size:13px; color:#5A6B7D; margin-bottom:16px;">'
            "Story + Coloring + Teacher's Guide</div></div>",
            unsafe_allow_html=True,
        )
        st.download_button(
            "📥 Download",
            data=st.session_state.pdf_full,
            file_name=f"{child_name}_storybook.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with col2:
        st.markdown(
            '<div style="background:#FFFFFF; padding:28px 20px; border-radius:20px;'
            ' text-align:center; box-shadow:0 4px 16px rgba(43,108,176,0.10);'
            ' border:1px solid #E0ECF8; margin-bottom:16px;">'
            '<div style="font-size:48px; margin-bottom:12px;">🎨</div>'
            '<div style="font-size:18px; font-weight:700; color:#2B3A4A; margin-bottom:6px;">'
            'Coloring Pages</div>'
            '<div style="font-size:13px; color:#5A6B7D; margin-bottom:16px;">'
            'Black & white outlines</div></div>',
            unsafe_allow_html=True,
        )
        st.download_button(
            "📥 Download",
            data=st.session_state.pdf_coloring,
            file_name=f"{child_name}_coloring.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with col3:
        st.markdown(
            '<div style="background:#FFFFFF; padding:28px 20px; border-radius:20px;'
            ' text-align:center; box-shadow:0 4px 16px rgba(43,108,176,0.10);'
            ' border:1px solid #E0ECF8; margin-bottom:16px;">'
            '<div style="font-size:48px; margin-bottom:12px;">📝</div>'
            '<div style="font-size:18px; font-weight:700; color:#2B3A4A; margin-bottom:6px;">'
            "Teacher's Sheet</div>"
            '<div style="font-size:13px; color:#5A6B7D; margin-bottom:16px;">'
            'Vocab + Questions + Activities</div></div>',
            unsafe_allow_html=True,
        )
        st.download_button(
            "📥 Download",
            data=st.session_state.pdf_edu,
            file_name=f"{child_name}_teacher_sheet.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.write("")
    with st.expander("📖 Read the Story Again"):
        for i, pg in enumerate(story.get("pages", [])):
            st.subheader(f"Page {i + 1}")
            if i < len(images) and images[i]:
                st.image(images[i], width=400)
            st.write(pg.get("text", ""))
            st.divider()

    st.write("")
    if st.button(
        "🔄 Create Another Story",
        type="primary",
        use_container_width=True,
    ):
        for key in [
            "story_data", "image_urls", "current_page", "child_name",
            "child_age", "child_gender", "moral", "photo_path",
            "generating", "pdf_full", "pdf_coloring", "pdf_edu",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "home"
        st.rerun()
