"""
=========================================================
ATT Pro - Ranking Engine
Author : ATT Pro Team

Ranks stocks based on AI Score.
=========================================================
"""


class RankingEngine:

    def __init__(self):
        pass

    def rank(self, results):
        """
        Sort results by AI Score (highest first)
        """

        return sorted(
            results,
            key=lambda x: x["AI Score"],
            reverse=True
        )