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
    """Generate a 5-page children's story using Groq via HuggingFace."""

    # Age based complexity
    if age <= 5:
        word_limit = 50
        complexity = "very simple short sentences, 1-2 syllable words only"
    elif age <= 7:
        word_limit = 100
        complexity = "compound sentences, simple dialogue, cause-and-effect"
    else:
        word_limit = 150
        complexity = "complex paragraphs, richer vocabulary, character emotions"

    prompt = f"""You are a children's book author. Write a 5-page story where {name}
(a {age}-year-old {gender.lower()}) learns about {moral}.

Rules:
- Use {complexity}
- Max {word_limit} words per page
- No violence, scary themes, or inappropriate content
- {name} is a {gender.lower()} child aged {age}
- Each image_prompt must describe {name} as a friendly {gender.lower()} child
- Return ONLY valid JSON, no extra text before or after

Required JSON format:
{{
  "title": "Creative Story Title Here",
  "pages": [
    {{
      "page_num": 1,
      "text": "story text for page 1",
      "image_prompt": "detailed visual scene: a friendly {gender.lower()} child named {name}...",
      "quiz": "question about the right thing to do?",
      "options": ["correct moral answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 2,
      "text": "story text for page 2",
      "image_prompt": "detailed visual scene description...",
      "quiz": "question for page 2?",
      "options": ["correct answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 3,
      "text": "story text for page 3",
      "image_prompt": "detailed visual scene description...",
      "quiz": "question for page 3?",
      "options": ["correct answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 4,
      "text": "story text for page 4",
      "image_prompt": "detailed visual scene description...",
      "quiz": "question for page 4?",
      "options": ["correct answer", "wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 5,
      "text": "story text for page 5",
      "image_prompt": "detailed visual scene description...",
      "quiz": "question for page 5?",
      "options": ["correct answer", "wrong answer"],
      "correct_answer": 0
    }}
  ],
  "edu_sheet": {{
    "vocab": ["Word1 - definition", "Word2 - definition", "Word3 - definition"],
    "discussion": ["Discussion question 1 about {moral}?", "Discussion question 2?"]
  }}
}}"""

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a children's book author. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=3000
        )

        raw_text = response.choices[0].message.content

        # Safely extract JSON in case model adds any extra text
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        json_str = raw_text[start:end]

        story_data = json.loads(json_str)
        return story_data

    except Exception as e:
        raise Exception(f"Story generation failed: {str(e)}")