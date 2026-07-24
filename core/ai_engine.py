"""
=========================================================
ATT Pro - AI Engine
Author : ATT Pro Team

Generates AI score and rating based on
technical strategy conditions.
=========================================================
"""


class AIEngine:

    def __init__(self):
        pass

    def calculate_ai_score(self, signal):

        score = int(signal["score"])

        ai_score = round((score / 4) * 100)

        if ai_score >= 80:
            rating = "⭐⭐⭐⭐⭐ Very Strong"

        elif ai_score >= 60:
            rating = "⭐⭐⭐⭐ Strong"

        elif ai_score >= 40:
            rating = "⭐⭐⭐ Moderate"

        elif ai_score >= 20:
            rating = "⭐⭐ Watch"

        else:
            rating = "⭐ Weak"

        reasons = []

        for condition, passed in signal["conditions"]:
            if passed:
                reasons.append(condition)

        return {
            "AI Score": ai_score,
            "Rating": rating,
            "Reasons": reasons
        }