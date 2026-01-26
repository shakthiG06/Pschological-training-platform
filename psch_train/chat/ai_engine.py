import random

def generate_patient_reply(persona_prompt, student_message):
    """
    Rule + persona based simulated patient response
    (Academic / MVP version)
    """

    msg = student_message.lower()

    # Emotion-based responses
    if any(word in msg for word in ["how are you", "how do you feel"]):
        responses = [
            "I feel low most of the time… it’s hard to feel motivated.",
            "Honestly, I feel tired and empty.",
            "I don’t really feel okay these days."
        ]

    elif any(word in msg for word in ["sleep", "sleeping"]):
        responses = [
            "My sleep is very disturbed. I wake up a lot.",
            "I don’t sleep properly… my mind keeps racing.",
            "Some nights I barely sleep at all."
        ]

    elif any(word in msg for word in ["sad", "depressed", "hopeless"]):
        responses = [
            "Yes… I often feel hopeless.",
            "That word describes me very well.",
            "I feel like nothing will get better."
        ]

    elif any(word in msg for word in ["family", "friends", "people"]):
        responses = [
            "I don’t really talk to people much anymore.",
            "I feel disconnected from everyone.",
            "Even around others, I feel alone."
        ]

    elif any(word in msg for word in ["why", "reason"]):
        responses = [
            "I don’t really know why… it just feels heavy inside.",
            "I can’t explain it clearly.",
            "I wish I knew the reason."
        ]

    else:
        # Generic depressive responses
        responses = [
            "I’m not sure how to explain it.",
            "I don’t have the energy to think much.",
            "I feel exhausted emotionally.",
            "It’s difficult to talk about."
        ]

    return random.choice(responses)
