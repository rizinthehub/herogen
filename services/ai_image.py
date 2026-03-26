import os
from typing import List, Any
import replicate


USE_FACE_CLONING = True


def _normalize_output(output: Any) -> str:
    if isinstance(output, list):
        return str(output[0]) if output else ""
    return str(output) if output else ""


def generate_images(image_prompts: List[str], face_photo_path: str = None) -> List[str]:
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        print("❌ REPLICATE_API_TOKEN not found")
        return [""] * len(image_prompts)

    if USE_FACE_CLONING and face_photo_path:
        return _generate_with_ideogram_character(image_prompts, face_photo_path)

    return _generate_without_face_clone(image_prompts)


def _generate_with_ideogram_character(
    image_prompts: List[str],
    face_photo_path: str,
) -> List[str]:
    if not os.path.exists(face_photo_path):
        raise FileNotFoundError(f"Face photo not found: {face_photo_path}")

    image_urls: List[str] = []

    for i, prompt in enumerate(image_prompts):
        full_prompt = f"""
{prompt}

Create a children's storybook illustration in soft watercolor style.

IMPORTANT:
The main child must match the person in the reference photo.
Keep the same face shape, eyes, nose, smile, hair, and skin tone.
Do not create a different child.
Keep the same character identity across all pages.

Style:
- watercolor storybook
- cute but recognizable
- soft bright colors
- child-safe
""".strip()

        try:
            with open(face_photo_path, "rb") as ref_image:
                output = replicate.run(
                    "ideogram-ai/ideogram-character",
                    input={
                        "prompt": full_prompt,
                        "character_reference_image": ref_image,
                        "aspect_ratio": "1:1",
                        "rendering_speed": "Default",
                    },
                )

            image_url = _normalize_output(output)
            image_urls.append(image_url)
            print(f"✅ Ideogram image {i + 1}/{len(image_prompts)} generated")

        except Exception as e:
            print(f"❌ Ideogram error on image {i + 1}: {repr(e)}")
            print("↪ Falling back to Replicate FLUX without face cloning...")
            image_urls.append("")

    return image_urls


def _generate_without_face_clone(image_prompts: List[str]) -> List[str]:
    image_urls: List[str] = []

    for i, prompt in enumerate(image_prompts):
        full_prompt = f"""
{prompt}

Create a children's book watercolor illustration.
Soft vibrant colors, friendly, magical, safe for children.
""".strip()

        try:
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": full_prompt,
                    "aspect_ratio": "1:1",
                    "output_format": "jpg",
                    "output_quality": 90,
                },
            )

            image_url = _normalize_output(output)
            image_urls.append(image_url)
            print(f"✅ FLUX fallback image {i + 1}/{len(image_prompts)} generated")

        except Exception as e:
            print(f"❌ Replicate fallback error on image {i + 1}: {repr(e)}")
            image_urls.append("")

    return image_urls