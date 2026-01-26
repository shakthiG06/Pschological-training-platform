import os
from openai import OpenAI

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_patient_reply(persona_prompt, user_message, conversation_history=None):
    """
    Generates an AI-simulated patient reply using ChatGPT.

    Parameters:
    - persona_prompt (str): Defines the patient's psychological persona
    - user_message (str): Latest message from the student
    - conversation_history (list): Optional previous messages for context

    Returns:
    - str: AI-generated patient reply
    """

    if conversation_history is None:
        conversation_history = []

    # System prompt = AI conditioning (this is your "training")
    system_prompt = f"""
You are a simulated psychology patient for training purposes.

PATIENT PERSONA:
{persona_prompt}

STRICT RULES:
- You are NOT a therapist, counselor, or doctor
- You do NOT provide advice, diagnosis, or solutions
- You only express thoughts, emotions, and experiences
- Responses should sound human and emotionally realistic
- Keep responses concise (1–3 sentences)
- Let the student guide the interaction
- This is a controlled training simulation, not real therapy
"""

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            *conversation_history,
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # recommended: low cost + strong reasoning
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Safe fallback for demo stability
        return (
            "I’m finding it hard to put my feelings into words right now. "
            "It feels uncomfortable to talk about this."
        )
