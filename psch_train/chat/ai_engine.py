import os
from django.conf import settings

# Try to import Groq (free) first, then OpenAI as fallback
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def get_ai_client():
    """Get AI client - tries Groq (free) first, then OpenAI."""
    # Try Groq first (free tier)
    groq_key = os.getenv("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
    if groq_key and GROQ_AVAILABLE:
        return ("groq", Groq(api00_key=groq_key))
    
    # Fall back to OpenAI
    openai_key = os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)
    if openai_key and OPENAI_AVAILABLE:
        return ("openai", OpenAI(api_key=openai_key))
    
    return (None, None)


def generate_patient_reply(persona_prompt, user_message, conversation_history=None):
    provider, client = get_ai_client()
    
    if not client:
        return (
            "*The patient looks at you thoughtfully* "
            "I appreciate you taking the time to talk with me today. "
            "(Note: Please set GROQ_API_KEY for free AI - get one at console.groq.com)"
        )

    if conversation_history is None:
        conversation_history = []

    system_prompt = f'''You are a simulated psychology patient for training purposes.

PATIENT PERSONA:
{persona_prompt}

STRICT RULES:
- You are NOT a therapist, counselor, or doctor
- You do NOT provide advice, diagnosis, or solutions
- You only express thoughts, emotions, and experiences as the patient
- Responses should sound human and emotionally realistic
- Keep responses concise (1-3 sentences typically)
- Let the student guide the interaction
- Stay in character at all times
- This is a controlled training simulation, not real therapy
'''

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            *conversation_history,
            {"role": "user", "content": user_message}
        ]

        # Use appropriate model based on provider
        if provider == "groq":
            model = "llama-3.1-8b-instant"  # Free, fast, reliable
        else:
            model = "gpt-4o-mini"

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        error_msg = str(e)
        print(f"AI API Error ({provider}): {error_msg}")
        
        # Provide specific error messages based on error type
        if "insufficient_quota" in error_msg or "429" in error_msg or "rate_limit" in error_msg.lower():
            return (
                "*The patient pauses and looks away* "
                "(System Notice: API rate limit reached. Please wait a moment and try again.)"
            )
        elif "invalid_api_key" in error_msg or "401" in error_msg:
            return (
                "*The patient seems distracted* "
                "(System Notice: Invalid API key. Please check your configuration.)"
            )
        else:
            return (
                "I'm finding it hard to put my feelings into words right now. "
                f"(Error: {error_msg[:80]})"
            )
