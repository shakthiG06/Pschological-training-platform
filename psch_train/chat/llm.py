import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPTS = {
    "anxiety": """
You are simulating a patient with generalized anxiety disorder.
You must:
- Speak like a real patient
- Express worry, fear, overthinking
- Do NOT give medical advice
- Respond emotionally, not analytically
- Let the student guide the conversation
""",

    "depression": """
You are simulating a patient experiencing depression.
You must:
- Use low-energy language
- Express hopelessness and fatigue
- Avoid giving solutions
- Respond realistically
""",

    "stress": """
You are simulating a stressed individual.
You must:
- Express overwhelm and pressure
- Talk about workload and expectations
"""
}

def get_ai_response(scenario, conversation):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # cost-effective + strong
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[scenario]},
            *conversation
        ],
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]
