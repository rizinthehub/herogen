import openai
import json
import os


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

    system_prompt = f"""You are an expert children's book author and illustrator director.

INPUTS:
- Child's Name: {name}
- Gender: {gender}
- Age: {age}
- Moral Theme: {moral}

TASK: Write a 5-page children's story where {name} is the hero who learns about {moral}.

CONSTRAINTS:
- Use {complexity}.
- Maximum {word_limit} words per page of story text.
- No violence, scary themes, or inappropriate content whatsoever.
- {name} is a {gender.lower()} child aged {age}.
- For each page, write a DETAILED visual description for an illustrator.
- For each page, create a moral-related quiz question with exactly 2 options.
- The FIRST option (index 0) MUST always be the correct/moral answer.
- The story should have a clear beginning, middle, and end with a moral lesson.

OUTPUT FORMAT: Return ONLY valid JSON with this exact structure:
{{
  "title": "A Creative Story Title",
  "pages": [
    {{
      "page_num": 1,
      "text": "Story text for page 1...",
      "image_prompt": "A detailed visual scene description...",
      "quiz": "A question about the right thing to do...",
      "options": ["The correct moral answer", "The wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 2,
      "text": "Story text for page 2...",
      "image_prompt": "A detailed visual scene description...",
      "quiz": "Question for page 2...",
      "options": ["Correct answer", "Wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 3,
      "text": "Story text for page 3...",
      "image_prompt": "A detailed visual scene description...",
      "quiz": "Question for page 3...",
      "options": ["Correct answer", "Wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 4,
      "text": "Story text for page 4...",
      "image_prompt": "A detailed visual scene description...",
      "quiz": "Question for page 4...",
      "options": ["Correct answer", "Wrong answer"],
      "correct_answer": 0
    }},
    {{
      "page_num": 5,
      "text": "Story text for page 5...",
      "image_prompt": "A detailed visual scene description...",
      "quiz": "Question for page 5...",
      "options": ["Correct answer", "Wrong answer"],
      "correct_answer": 0
    }}
  ],
  "edu_sheet": {{
    "vocab": ["Word1 - definition", "Word2 - definition", "Word3 - definition"],
    "discussion": ["Discussion question 1?", "Discussion question 2?"]
  }}
}}"""

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
    return story_data