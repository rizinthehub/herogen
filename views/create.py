import streamlit as st
import tempfile
import time
import os
import base64


def show():
    if st.session_state.get("generating", False):
        _run_generation()
        return

    # Centered Form
    col_l, col_m, col_r = st.columns([1, 3, 1])

    with col_m:
        with st.container():
            st.markdown(
                """
                <div style="font-size:28px; font-weight:700; color:#2B3A4A; margin-bottom:4px;">
                    ✨ Create Your Story
                </div>
                <div style="font-size:14px; color:#5A6B7D; margin-bottom:12px;">
                    Fill out the details to get started.
                </div>
                <hr style="border:none; height:1px; background:#E0ECF8; margin-bottom:20px;">
                """,
                unsafe_allow_html=True,
            )

            name = st.text_input("Child Name", placeholder="e.g., Timmy")

            c1, c2 = st.columns(2)
            with c1:
                age = st.selectbox("Age", [4, 5, 6, 7, 8])
                gender = st.selectbox("Gender", ["Boy", "Girl"])
            with c2:
                morals_list = [
                    "Bravery", "Sharing", "Kindness", "Honesty",
                    "Patience", "Respect", "Gratitude", "Empathy",
                    "Responsibility", "Friendship", "Type my own...",
                ]
                moral_choice = st.selectbox("Moral Theme", morals_list)

            if "Type my own" in moral_choice:
                moral = st.text_input("Type your moral theme:")
            else:
                moral = moral_choice

            photo = st.file_uploader(
                "Upload Child Photo (JPG or PNG)",
                type=["jpg", "jpeg", "png"],
            )

            if photo:
                st.image(photo, caption="Uploaded Photo ✅", width=150)

            st.write("")
            if st.button("🚀 Start", type="primary", use_container_width=True):
                if not name or not name.strip():
                    st.error("Please enter the child's name!")
                    return
                if not moral or moral == "Type my own...":
                    st.error("Please select or type a moral theme!")
                    return
                if not photo:
                    st.error("Please upload a photo!")
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
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


def _run_generation():
    name = st.session_state.child_name
    age = st.session_state.child_age
    gender = st.session_state.child_gender
    moral = st.session_state.moral
    photo_path = st.session_state.photo_path

    # Pulsing logo animation
    logo_path = os.path.join("assets", "HeroGenLogo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:80px;">'
    else:
        logo_html = '<div style="font-size:60px;">📚</div>'

    col_l, col_m, col_r = st.columns([1, 3, 1])

    with col_m:
        st.markdown(
            f"""
            <style>
            @keyframes herogen-pulse {{
                0%, 100% {{ transform: scale(1); opacity: 1; }}
                50% {{ transform: scale(1.15); opacity: 0.7; }}
            }}
            @keyframes herogen-float {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
            }}
            @keyframes herogen-glow {{
                0%, 100% {{ filter: drop-shadow(0 0 8px rgba(43,108,176,0.3)); }}
                50% {{ filter: drop-shadow(0 0 20px rgba(230,126,34,0.5)); }}
            }}
            .loading-animation {{
                text-align: center;
                animation: herogen-pulse 2s ease-in-out infinite,
                           herogen-float 3s ease-in-out infinite,
                           herogen-glow 2s ease-in-out infinite;
                margin-bottom: 20px;
            }}
            @keyframes shimmer {{
                0% {{ background-position: -200% 0; }}
                100% {{ background-position: 200% 0; }}
            }}
            .loading-title-shimmer {{
                font-size: 28px;
                font-weight: 700;
                background: linear-gradient(90deg, #2B6CB0, #E67E22, #2B6CB0);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: shimmer 3s linear infinite;
                text-align: center;
            }}
            @keyframes dot-blink {{
                0%, 20% {{ opacity: 0; }}
                50% {{ opacity: 1; }}
                80%, 100% {{ opacity: 0; }}
            }}
            .loading-dots span {{
                animation: dot-blink 1.4s infinite;
                font-size: 28px;
                font-weight: 700;
                color: #E67E22;
            }}
            .loading-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
            .loading-dots span:nth-child(3) {{ animation-delay: 0.4s; }}
            </style>
            <div style="text-align:center; padding:40px 20px;">
                <div class="loading-animation">{logo_html}</div>
                <div class="loading-title-shimmer">
                    Creating Your Story
                    <span class="loading-dots">
                        <span>.</span><span>.</span><span>.</span>
                    </span>
                </div>
                <div style="font-size:14px; color:#5A6B7D; margin-top:12px;">
                    Building a story about <strong>{name}</strong>
                    learning about <strong>{moral}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        progress_bar = st.progress(0)
        status_text = st.empty()

        fun_facts = [
            "🌟 Did you know? Reading 20 min/day exposes kids to 1.8 million words per year!",
            "🎨 Your illustrations are being painted in watercolor style...",
            "📚 Personalized stories increase reading engagement by 40%!",
            "🧠 Stories help children develop empathy and emotional intelligence!",
            "✨ Each story is unique — no two are ever the same!",
        ]
        fun_fact_box = st.empty()

        try:
            status_text.info("📖 Writing the story...")
            fun_fact_box.caption(fun_facts[0])
            progress_bar.progress(5)

            from services.ai_text import generate_story
            story_data = generate_story(name, age, gender, moral)
            st.session_state.story_data = story_data
            progress_bar.progress(20)

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

            status_text.info("💾 Saving your story...")
            fun_fact_box.empty()
            progress_bar.progress(90)

            try:
                from services.db import save_story
                save_story("demo_user", name, age, moral, story_data, image_urls)
            except Exception:
                pass

            progress_bar.progress(95)
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
