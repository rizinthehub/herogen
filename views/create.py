import streamlit as st
import tempfile
import time


def show():
    if st.session_state.get("generating", False):
        _run_generation()
        return

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #333;">✨ Create Your Story</h1>
            <p style="color: #666; font-size: 1.1em;">
                Fill in the details below and watch the magic happen!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            """<div style="background: white; padding: 30px; border-radius: 16px;
                          box-shadow: 0 2px 8px rgba(0,0,0,0.06);">""",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("👤 Child's Name", placeholder="e.g., Timmy")
            gender = st.selectbox("👦 Gender", ["Boy", "Girl"])

        with col2:
            age = st.selectbox("🎂 Age", [4, 5, 6, 7, 8])
            morals_list = [
                "Bravery", "Sharing", "Kindness", "Honesty",
                "Patience", "Respect", "Gratitude", "Empathy",
                "Responsibility", "Friendship", "Type my own...",
            ]
            moral_choice = st.selectbox("💛 Moral Theme", morals_list)

        if "Type my own" in moral_choice:
            moral = st.text_input("Type your moral theme:")
        else:
            moral = moral_choice

        st.write("")
        photo = st.file_uploader(
            "📸 Upload Child's Photo (JPG or PNG, max 10 MB)",
            type=["jpg", "jpeg", "png"],
        )

        if photo:
            st.image(photo, caption="Uploaded Photo ✅", width=150)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🪄 Generate Magic!", type="primary", use_container_width=True):
        if not name or not name.strip():
            st.error("❌ Please enter the child's name!")
            return
        if not moral or moral == "Type my own...":
            st.error("❌ Please select or type a moral theme!")
            return
        if not photo:
            st.error("❌ Please upload a photo!")
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

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()


def _run_generation():
    name = st.session_state.child_name
    age = st.session_state.child_age
    gender = st.session_state.child_gender
    moral = st.session_state.moral
    photo_path = st.session_state.photo_path

    st.markdown(
        f"""
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="color: #333;">🪄 Creating Your Story...</h1>
            <p style="color: #666; font-size: 1.1em;">
                Building a story about <strong>{name}</strong>
                learning about <strong>{moral}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress_bar = st.progress(0)
    status_text = st.empty()

    fun_facts = [
        "🌟 Did you know? Reading 20 minutes a day exposes kids to 1.8 million words per year!",
        "🎨 Your illustrations are being painted in watercolor style...",
        "📚 Personalized stories increase reading engagement by 40%!",
        "🧠 Stories help children develop empathy and emotional intelligence!",
        "✨ Each story is unique — no two are ever the same!",
    ]
    fun_fact_box = st.empty()

    try:
        # STEP 1: Generate story text
        status_text.info("📖 Writing the story...")
        fun_fact_box.caption(fun_facts[0])
        progress_bar.progress(5)

        from services.ai_text import generate_story
        story_data = generate_story(name, age, gender, moral)
        st.session_state.story_data = story_data
        progress_bar.progress(20)

        # STEP 2: Generate images one by one with progress updates
        from services.ai_image import generate_images

        image_prompts = [p["image_prompt"] for p in story_data["pages"]]
        image_urls = []

        for idx, prompt in enumerate(image_prompts):
            status_text.info(f"🎨 Painting illustration {idx + 1} of 5...")
            fun_fact_box.caption(fun_facts[idx % len(fun_facts)])
            progress_bar.progress(20 + (idx * 12))

            urls = generate_images([prompt], photo_path)
            image_urls.extend(urls)

        st.session_state.image_urls = image_urls
        progress_bar.progress(85)

        # STEP 3: Save to database
        status_text.info("💾 Saving your story...")
        fun_fact_box.empty()
        progress_bar.progress(90)

        try:
            from services.db import save_story
            save_story("demo_user", name, age, moral, story_data, image_urls)
        except Exception:
            pass

        progress_bar.progress(95)

        # STEP 4: Done
        progress_bar.progress(100)
        status_text.success("✅ Your story is ready! Opening the reader...")
        time.sleep(1)

        st.session_state.generating = False
        st.session_state.current_page = 0
        st.session_state.page = "reader"
        st.rerun()

    except Exception as e:
        st.error(f"❌ Something went wrong: {str(e)}")
        st.write(
            "**Common fixes:** Check your API keys in the .env file, "
            "make sure you have billing enabled on OpenAI, "
            "and that your internet connection is working."
        )
        st.session_state.generating = False
        if st.button("🔄 Try Again"):
            st.session_state.page = "create"
            st.rerun()