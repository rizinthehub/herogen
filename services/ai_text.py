import os
import json
from openai import OpenAI
from services.api_config import GROQ_BASE_URL, GROQ_MODEL, HF_TOKEN

# Connect to Groq through HuggingFace router
client = OpenAI(
    base_url=GROQ_BASE_URL,
    api_key=HF_TOKEN,
)

def generate_story(name, age, gender, moral):
    """Generate a professional 5-page children's story using Groq via HuggingFace."""

    # Age based complexity
    if age <= 5:
        word_limit = 80
        complexity = (
            "simple clear sentences, easy words, "
            "focus on feelings and colors, "
            "very relatable situations for toddlers"
        )
    elif age <= 7:
        word_limit = 150
        complexity = (
            "natural flowing sentences, simple dialogue between characters, "
            "cause and effect situations, "
            "relatable school or playground scenarios"
        )
    else:
        word_limit = 220
        complexity = (
            "rich descriptive paragraphs, character thoughts and emotions, "
            "meaningful dialogue, "
            "real life situations with depth and moral weight"
        )

    prompt = f"""You are a professional children's book author with 20 years of experience.
Write a high quality 5-page children's storybook where {name} 
(a {age}-year-old {gender.lower()}) learns about {moral}.

STORY REQUIREMENTS:
- The story must feel like a REAL published children's book
- Each page must have ONE full rich paragraph (around {word_limit} words)
- The story must have a clear beginning, rising action, climax, resolution and moral
- Use natural flowing language, not robotic or list-like
- Include meaningful dialogue between characters
- {name} must face a real challenge related to {moral} and grow through it
- The ending must feel warm, satisfying and inspiring
- No violence, scary themes, or inappropriate content whatsoever
- {name} is a {gender.lower()} child aged {age}

IMAGE REQUIREMENTS:
- Each image_prompt must be highly detailed for a cartoon illustrator
- Describe the scene, setting, time of day, colors, expressions, actions
- Always describe {name} as a cartoon {gender.lower()} child with a friendly face
- Make scenes feel warm, colorful and inviting

QUIZ REQUIREMENTS:
- Each quiz question must relate directly to what happened on that page
- Questions should make the child think about the moral lesson
- First option must always be the correct moral answer

Return ONLY valid JSON, absolutely no extra text before or after.

Required JSON format:
{{
  "title": "Creative Engaging Story Title Here",
  "pages": [
    {{
      "page_num": 1,
      "text": "One full rich paragraph that opens the story, introduces {name} and sets the scene. Around {word_limit} words. Natural book-like language.",
      "image_prompt": "Highly detailed cartoon scene: a cheerful {gender.lower()} child named {name} with bright eyes and a friendly smile, [describe exactly what is happening, where, what colors, what time of day, what expressions, what objects are around]",
      "quiz": "Thoughtful question about what happened on this page?",
      "options": ["correct moral answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 2,
      "text": "One full rich paragraph continuing the story, {name} encounters the main challenge. Around {word_limit} words.",
      "image_prompt": "Highly detailed cartoon scene: {name} the {gender.lower()} child [describe the challenge scene in detail with colors, expressions, setting]",
      "quiz": "Question about the challenge {name} faced?",
      "options": ["correct moral answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 3,
      "text": "One full rich paragraph, the story reaches its most important moment. {name} must make a choice. Around {word_limit} words.",
      "image_prompt": "Highly detailed cartoon scene: {name} the {gender.lower()} child at the key moment [describe the decision scene vividly]",
      "quiz": "Question about the choice {name} made?",
      "options": ["correct moral answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 4,
      "text": "One full rich paragraph showing the result of {name}'s choice and how it affected others. Around {word_limit} words.",
      "image_prompt": "Highly detailed cartoon scene: {name} the {gender.lower()} child [describe the positive outcome scene with warm colors and happy expressions]",
      "quiz": "Question about what {name} learned?",
      "options": ["correct moral answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 5,
      "text": "One full rich paragraph, warm satisfying ending. {name} reflects on the lesson and feels proud. Around {word_limit} words.",
      "image_prompt": "Highly detailed cartoon scene: {name} the {gender.lower()} child [describe the final heartwarming scene with bright warm colors and a big smile]",
      "quiz": "Final reflection question about the moral of {moral}?",
      "options": ["correct moral answer", "wrong answer"],
      "correct_answer": 0
    }}
  ],
  "edu_sheet": {{
    "vocab": [
      "Word1 - clear simple definition",
      "Word2 - clear simple definition",
      "Word3 - clear simple definition",
      "Word4 - clear simple definition",
      "Word5 - clear simple definition"
    ],
    "discussion": [
      "Deep discussion question 1 about {moral} related to real life?",
      "Deep discussion question 2 connecting the story to the child's own experience?",
      "Deep discussion question 3 about how to practice {moral} every day?"
    ]
  }}
}}"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional children's book author. "
                        "You write warm, rich, meaningful stories that feel like "
                        "real published books. Always respond with valid JSON only, "
                        "no extra text, no markdown backticks."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.85,
            max_tokens=4000
        )

        raw_text = response.choices[0].message.content

        # Safely extract JSON even if model adds any extra text
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        json_str = raw_text[start:end]

        story_data = json.loads(json_str)
        return story_data

    except json.JSONDecodeError as e:
        raise Exception(f"Story format error - try again: {str(e)}")
    except Exception as e:
        raise Exception(f"Story generation failed: {str(e)}")