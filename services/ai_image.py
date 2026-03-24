import openai
import os
import time

USE_FACE_CLONING = False


def generate_images(image_prompts, face_photo_path=None):
    if USE_FACE_CLONING and face_photo_path:
        return _generate_with_replicate(image_prompts, face_photo_path)
    else:
        return _generate_with_dalle(image_prompts)


def _generate_with_dalle(image_prompts):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    image_urls = []
    for i, prompt in enumerate(image_prompts):
        full_prompt = (
            f"{prompt}, "
            "children's book illustration style, watercolor painting, "
            "soft vibrant colors, cute and friendly characters, "
            "masterpiece quality, safe for children"
        )
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=full_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_urls.append(response.data[0].url)
            print(f"Image {i+1}/5 generated successfully")
        except Exception as e:
            print(f"DALL-E Error on image {i+1}: {e}")
            image_urls.append(None)
        time.sleep(1)
    return image_urls


def _generate_with_replicate(image_prompts, face_photo_path):
    import replicate
    image_urls = []
    for i, prompt in enumerate(image_prompts):
        full_prompt = (
            f"{prompt}, "
            "watercolor style, children's book illustration, "
            "soft colors, vibrant, masterpiece"
        )
        try:
            with open(face_photo_path, "rb") as face_file:
                output = replicate.run(
                    "zsxkib/instant-id",
                    input={"image": face_file, "prompt": full_prompt},
                )
            if isinstance(output, list) and len(output) > 0:
                image_urls.append(str(output[0]))
            else:
                image_urls.append(str(output))
        except Exception as e:
            print(f"Replicate Error: {e}")
            image_urls.append(None)
        time.sleep(2)
    return image_urls