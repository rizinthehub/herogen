import openai
import json
import os


def _validate_story_data(story_data):
    pages = story_data.get("pages", [])
    for page in pages:
        options = page.get("options", [])
        if not isinstance(options, list) or len(options) != 2:
            page["options"] = ["Do the right thing", "Do the wrong thing"]

        page["correct_answer"] = 0

        if not page.get("quiz"):
            page["quiz"] = "What is the right thing to do?"

    return story_data


def generate_story(name, age, gender, moral):
    """Call OpenAI to generate a 5-page children's story as JSON."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if age <= 5:
        word_limit = 50
        complexity = (
            "very simple sentences with short words (1-2 syllables), "
            "focus on sensory details like colors, sounds, and feelings"
        )
    elif age <= 7:
        word_limit = 100
        complexity = (
            "compound sentences with cause-and-effect logic, "
            "some descriptive adjectives, simple dialogue"
        )
    else:
        word_limit = 150
        complexity = (
            "complex paragraphs with internal monologue, "
            "richer vocabulary, character emotions and growth"
        )

    system_prompt = f"""
You are an expert children's book author and illustrator director.

INPUTS:
- Child's Name: {name}
- Gender: {gender}
- Age: {age}
- Moral Theme: {moral}

TASK:
Write a 5-page children's story where {name} is the hero who learns about {moral}.

CONSTRAINTS:
- Use {complexity}.
- Maximum {word_limit} words per page.
- No violence, scary themes, or inappropriate content.
- {name} is a {gender.lower()} child aged {age}.
- For each page, write a detailed visual description for an illustrator.
- For each page, create 1 quiz question based ONLY on that page text.
- Each quiz must have exactly 2 options.
- Option 0 MUST be the correct answer.
- Option 1 MUST be the wrong answer.
- The correct answer must clearly match the page story.
- The wrong answer must be believable but incorrect.
- Keep the story structure clear: beginning, middle, end.

OUTPUT FORMAT:
Return ONLY valid JSON with this exact structure:
{{
  "title": "A Creative Story Title",
  "pages": [
    {{
      "page_num": 1,
      "text": "Story text for page 1...",
      "image_prompt": "A detailed visual scene description...",
      "quiz": "A question about page 1 only...",
      "options": ["Correct answer", "Wrong answer"],
      "correct_answer": 0
    }}
  ],
  "edu_sheet": {{
    "vocab": ["Word1 - definition", "Word2 - definition", "Word3 - definition"],
    "discussion": ["Discussion question 1?", "Discussion question 2?"]
  }}
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Create a magical children's story about {name}, "
                    f"a {age}-year-old {gender.lower()}, learning about {moral}."
                ),
            },
        ],
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    story_data = json.loads(response.choices[0].message.content)
    return _validate_story_data(story_data)