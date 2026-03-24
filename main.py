import streamlit as st

st.set_page_config(
    page_title='HeroGen - AI Storybook Generator',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='collapsed',
)

import os
from dotenv import load_dotenv

load_dotenv()

import logging
logging.getLogger('streamlit').setLevel(logging.ERROR)

try:
    secrets_available = False
    try:
        if len(st.secrets) > 0:
            secrets_available = True
    except Exception:
        pass

    if secrets_available:
        for key in ['OPENAI_API_KEY', 'REPLICATE_API_TOKEN', 'MONGODB_URI']:
            if key in st.secrets:
                os.environ[key] = st.secrets[key]
except Exception:
    pass

css_path = os.path.join('assets', 'style.css')
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

current_page = st.session_state.page

if current_page == 'home':
    from views.home import show
    show()
elif current_page == 'create':
    from views.create import show
    show()
elif current_page == 'reader':
    from views.reader import show
    show()
elif current_page == 'dashboard':
    from views.dashboard import show
    show()
else:
    st.session_state.page = 'home'
