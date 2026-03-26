import os
from dotenv import load_dotenv

load_dotenv()

# ── ONE TOKEN FOR EVERYTHING ───────────────────────────────────
HF_TOKEN = os.getenv("HF_TOKEN")

# ── GROQ via HuggingFace Router (Story Text Generation) ───────
GROQ_BASE_URL = "https://router.huggingface.co/v1"
GROQ_MODEL    = "meta-llama/Llama-3.3-70B-Instruct:groq"

# ── REPLICATE via HuggingFace (Image Generation) ──────────────
# image_to_image — takes child photo + prompt = cartoon scene
IMAGE_MODEL = "black-forest-labs/FLUX.2-klein-4B"

# ── MONGODB ───────────────────────────────────────────────────
MONGODB_URI = os.getenv("MONGODB_URI")
## mongodb+srv://herogen:herogen321@herogencluster.lycxwvm.mongodb.net/?retryWrites=true&w=majority&appName=HeroGenCluster
