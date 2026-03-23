import os
import time
from PIL import Image
from huggingface_hub import InferenceClient
from services.api_config import HF_TOKEN, IMAGE_MODEL

# Connect to Replicate through HuggingFace
client = InferenceClient(
    provider="replicate",
    api_key=HF_TOKEN,
)

def _prepare_face_image(face_photo_path):
    """Resize and optimize face photo before sending."""
    try:
        img = Image.open(face_photo_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize((512, 512), Image.LANCZOS)
        optimized_path = "temp_face_optimized.jpg"
        img.save(optimized_path, "JPEG", quality=95)
        print("Face photo optimized successfully")
        return optimized_path
    except Exception as e:
        print(f"Could not optimize face photo: {e}")
        return face_photo_path


def generate_images(image_prompts, face_photo_path=None):
    """Generate 5 cartoon story illustrations using image_to_image."""
    image_urls = []

    # Optimize face photo if provided
    optimized_face = None
    if face_photo_path and os.path.exists(face_photo_path):
        optimized_face = _prepare_face_image(face_photo_path)
        print("Using face reference for character generation")
    else:
        print("No face photo — generating without face reference")

    for i, prompt in enumerate(image_prompts):

        full_prompt = (
            prompt + ", "
            "digital cartoon illustration style, "
            "Pixar-like 3D cartoon rendering, "
            "warm vibrant colors, "
            "soft friendly lighting, "
            "professional children's book quality, "
            "expressive cartoon faces, "
            "safe and cheerful atmosphere"
        )

        try:
            print(f"Generating image {i+1}/5...")

            if optimized_face:
                # image_to_image — child's face + scene prompt
                with open(optimized_face, "rb") as image_file:
                    input_image = image_file.read()

                image = client.image_to_image(
                    input_image,
                    prompt=full_prompt,
                    model=IMAGE_MODEL,
                )
            else:
                # Fallback — text to image only
                image = client.text_to_image(
                    prompt=full_prompt,
                    model="black-forest-labs/FLUX.1-schnell",
                )

            temp_path = f"temp_image_{i+1}.png"
            image.save(temp_path)
            image_urls.append(temp_path)
            print(f"Image {i+1}/5 saved")

        except Exception as e:
            print(f"Error on image {i+1}: {str(e)}")
            print("Trying text-to-image fallback...")

            try:
                image = client.text_to_image(
                    prompt=full_prompt,
                    model="black-forest-labs/FLUX.1-schnell",
                )
                temp_path = f"temp_image_{i+1}.png"
                image.save(temp_path)
                image_urls.append(temp_path)
                print(f"Fallback image {i+1}/5 saved")

            except Exception as fallback_error:
                print(f"Fallback also failed: {str(fallback_error)}")
                image_urls.append(None)

        time.sleep(2)

    # Cleanup optimized face temp file
    if os.path.exists("temp_face_optimized.jpg"):
        try:
            os.remove("temp_face_optimized.jpg")
        except:
            pass

    return image_urls