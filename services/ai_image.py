import os
import time
from huggingface_hub import InferenceClient
from services.api_config import HF_TOKEN, IMAGE_MODEL

# Connect to Replicate through HuggingFace InferenceClient
client = InferenceClient(
    provider="replicate",
    api_key=HF_TOKEN,
)

def generate_images(image_prompts, face_photo_path=None):
    """Generate 5 story illustrations using Replicate via HuggingFace."""
    image_urls = []

    for i, prompt in enumerate(image_prompts):

        # Make the prompt better for children's book style
        full_prompt = (
            f"{prompt}, "
            "children's book illustration, "
            "watercolor painting style, "
            "soft vibrant colors, "
            "cute and friendly characters, "
            "safe for children, "
            "high quality"
        )

        negative_prompt = (
            "scary, dark, violent, adult, "
            "nsfw, ugly, deformed, "
            "watermark, text"
        )

        try:
            print(f"Generating image {i+1}/5...")

            image = client.text_to_image(
                prompt=full_prompt,
                model=IMAGE_MODEL,
                negative_prompt=negative_prompt,
            )

            # Save image to a temp file and get its path
            temp_path = f"temp_image_{i+1}.png"
            image.save(temp_path)
            image_urls.append(temp_path)
            print(f"✅ Image {i+1}/5 done")

        except Exception as e:
            print(f"❌ Error on image {i+1}: {str(e)}")
            image_urls.append(None)

        # Small delay to avoid hitting rate limits
        time.sleep(2)

    return image_urls