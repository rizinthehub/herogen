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
    st.title(f"Great Job, {child_name}!")
    st.subheader(f'Your story "{story.get("title", "My Story")}" is complete!')
    st.write("Download your personalized Edu-Pack below")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Full Storybook")
        try:
            pdf_bytes = create_full_pdf(story, images)
            st.download_button(
                "Download Storybook",
                data=pdf_bytes,
                file_name=f"{child_name}_storybook.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Error: {e}")

    with col2:
        st.markdown("### Coloring Pages")
        try:
            coloring_bytes = create_coloring_pdf(images)
            st.download_button(
                "Download Coloring Pages",
                data=coloring_bytes,
                file_name=f"{child_name}_coloring.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Error: {e}")

    with col3:
        st.markdown("### Teacher's Sheet")
        try:
            edu_bytes = create_edu_pdf(story)
            st.download_button(
                "Download Teacher Sheet",
                data=edu_bytes,
                file_name=f"{child_name}_teacher_sheet.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()

    with st.expander("Read the Story Again"):
        for i, page in enumerate(story.get("pages", [])):
            st.subheader(f"Page {i + 1}")
            if i < len(images) and images[i]:
                st.image(images[i], width=400)
            st.write(page.get("text", ""))
            st.divider()

    if st.button("Create Another Story", type="primary"):
        for key in ["story_data", "image_urls", "current_page", "child_name",
                     "child_age", "child_gender", "moral", "photo_path", "generating"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "home"
        st.rerun()