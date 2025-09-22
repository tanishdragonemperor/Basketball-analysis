import json
import os
import random

from app.dbmodels import models

def get_player_summary_stats(player_id: str):
    # TODO: Complete API response, replace placeholder below with actual implementation that sources data from database
    with open(os.path.dirname(os.path.abspath(__file__)) + '/sample_summary_data/sample_summary_data.json') as sample_summary:
        data = json.load(sample_summary)
    return data


def get_ranks(player_id: str, player_summary: dict):
    # TODO: replace with your implementation of get_ranks
    random.seed(player_id)
    return {
        "totalShotAttemptsRank": random.randint(1, 10),
        "totalPointsRank": random.randint(1, 10),
        "totalPassesRank": random.randint(1, 10),
        "totalPotentialAssistsRank": random.randint(1, 10),
        "totalTurnoversRank": random.randint(1, 10),
        "totalPassingTurnoversRank": random.randint(1, 10),
        'pickAndRollCountRank': random.randint(1, 10),
        'isolationCountRank': random.randint(1, 10),
        'postUpCountRank': random.randint(1, 10),
        'offBallScreenCountRank': random.randint(1, 10),
    }
