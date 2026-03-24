import streamlit as st
import tempfile
import time


def show():
    """Display the story creation form OR the generation loading screen."""
    if st.session_state.get("generating", False):
        _run_generation()
        return

    st.title("Create Your Story")
    st.write("Fill in the details below and watch the magic happen!")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Child's Name", placeholder="e.g., Timmy")
        gender = st.selectbox("Gender", ["Boy", "Girl"])

    with col2:
        age = st.selectbox("Age", [4, 5, 6, 7, 8])
        morals_list = [
            "Bravery",
            "Sharing",
            "Kindness",
            "Honesty",
            "Patience",
            "Respect",
            "Gratitude",
            "Empathy",
            "Responsibility",
            "Friendship",
            "Type my own...",
        ]
        moral_choice = st.selectbox("Moral Theme", morals_list)

    if "Type my own" in moral_choice:
        moral = st.text_input(
            "Type your moral theme:",
            placeholder="e.g., Being helpful to others",
        )
    else:
        moral = moral_choice

    st.write("---")
    photo = st.file_uploader(
        "Upload Child's Photo (JPG or PNG, max 10 MB)",
        type=["jpg", "jpeg", "png"],
    )

    if photo:
        st.image(photo, caption="Uploaded Photo", width=200)

    st.write("---")
    if st.button("Generate Magic!", type="primary", use_container_width=True):
        if not name or not name.strip():
            st.error("Please enter the child's name!")
            return
        if not moral or moral == "Type my own...":
            st.error("Please select or type a moral theme!")
            return
        if not photo:
            st.error("Please upload a photo!")
            return
        if photo.size > 10 * 1024 * 1024:
            st.error("Photo must be under 10 MB!")
            return

        tmp_photo = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp_photo.write(photo.getvalue())
        tmp_photo.close()

        st.session_state.child_name = name.strip()
        st.session_state.child_age = age
        st.session_state.child_gender = gender
        st.session_state.moral = moral
        st.session_state.photo_path = tmp_photo.name
        st.session_state.generating = True
        st.rerun()

    st.write("")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


def _run_generation():
    """Run the AI generation pipeline with a loading screen."""
    name = st.session_state.child_name
    age = st.session_state.child_age
    gender = st.session_state.child_gender
    moral = st.session_state.moral
    photo_path = st.session_state.photo_path

    st.title("Creating Your Story...")
    st.write(f"Building a story about **{name}** learning about **{moral}**...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.markdown("### Writing the story...")
        progress_bar.progress(10)

        from services.ai_text import generate_story

        story_data = generate_story(name, age, gender, moral)
        st.session_state.story_data = story_data
        progress_bar.progress(25)

        status_text.markdown("### AI is painting the illustrations...")

        from services.ai_image import generate_images

        image_prompts = [p["image_prompt"] for p in story_data["pages"]]
        image_urls = generate_images(image_prompts, photo_path)
        st.session_state.image_urls = image_urls
        progress_bar.progress(85)

        status_text.markdown("### Saving your story...")
        try:
            from services.db import save_story

            save_story("demo_user", name, age, moral, story_data, image_urls)
        except Exception:
            pass
        progress_bar.progress(95)

        progress_bar.progress(100)
        status_text.markdown("### Your story is ready!")
        time.sleep(1)

        st.session_state.generating = False
        st.session_state.current_page = 0
        st.session_state.page = "reader"
        st.rerun()

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
        st.write(
            "**Common fixes:** Check your API keys in the .env file, "
            "make sure you have billing enabled on OpenAI, "
            "and that your internet connection is working."
        )
        st.session_state.generating = False
        if st.button("Try Again"):
            st.session_state.page = "create"
            st.rerun()