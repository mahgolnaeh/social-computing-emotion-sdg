TONE_TEMPLATES = {
    "Fear": "It's okay to feel afraid. You're not alone, and small steps make a difference.",
    "Anxiety": "Anxiety is a natural response to uncertainty. You're seen, and you're safe here.",
    "Frustration": "Your frustration is valid. Change begins with awareness and small actions.",
    "Sadness": "It’s okay to feel sad. You’re not alone in this. Healing takes time.",
    "Joy": "Your joy matters. Let it inspire others and fuel positive change.",
    "Hope": "Hold on to hope. Even small actions toward progress matter.",
    "Confusion": "It’s natural to feel confused. Let’s find clarity and support together.",
    "Anger": "Your anger shows you care. Let’s channel it into action for impact.",
    "Disgust": "It’s tough to see injustice. Your voice matters in building better systems."
}


def get_emotion_template(emotion: str) -> str | None:
    return TONE_TEMPLATES.get(emotion)
