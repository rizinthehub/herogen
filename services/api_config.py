import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

GROQ_BASE_URL = "https://router.huggingface.co/v1"
GROQ_MODEL    = "meta-llama/Llama-3.3-70B-Instruct:groq"

IMAGE_MODEL   = "black-forest-labs/FLUX.1-dev"

MONGODB_URI   = os.getenv("MONGODB_URI")
