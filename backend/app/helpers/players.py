import json
import os
import random
from collections import defaultdict

from app.dbmodels import models

def get_player_summary_stats(player_id: str):
    try:
        player_id = int(player_id)
        player = models.Player.objects.get(player_id=player_id)
    except (ValueError, models.Player.DoesNotExist):
        return {"error": "Player not found"}
    
    shots = models.Shot.objects.filter(player=player)
    
    passes = models.Pass.objects.filter(player=player)
    
    turnovers = models.Turnover.objects.filter(player=player)
    total_shot_attempts = shots.count()
    total_points = sum(shot.points for shot in shots)
    total_passes = passes.count()
    total_potential_assists = passes.filter(potential_assist=True).count()
    total_turnovers = turnovers.count()
    total_passing_turnovers = passes.filter(turnover=True).count()
    
    action_stats = defaultdict(lambda: {
        'totalShotAttempts': 0,
        'totalPoints': 0,
        'totalPasses': 0,
        'totalPotentialAssists': 0,
        'totalTurnovers': 0,
        'totalPassingTurnovers': 0,
        'shots': [],
        'passes': [],
        'turnovers': []
    })
    
    for shot in shots:
        action_type = shot.action_type
        action_stats[action_type]['totalShotAttempts'] += 1
        action_stats[action_type]['totalPoints'] += shot.points
        action_stats[action_type]['shots'].append({
            'loc': [shot.shot_loc_x, shot.shot_loc_y],
            'points': shot.points
        })
    
    # Process passes by action type
    for pass_obj in passes:
        action_type = pass_obj.action_type
        action_stats[action_type]['totalPasses'] += 1
        if pass_obj.potential_assist:
            action_stats[action_type]['totalPotentialAssists'] += 1
        if pass_obj.turnover:
            action_stats[action_type]['totalPassingTurnovers'] += 1
        
        action_stats[action_type]['passes'].append({
            'startLoc': [pass_obj.ball_start_loc_x, pass_obj.ball_start_loc_y],
            'endLoc': [pass_obj.ball_end_loc_x, pass_obj.ball_end_loc_y],
            'isCompleted': pass_obj.completed_pass,
            'isPotentialAssist': pass_obj.potential_assist,
            'isTurnover': pass_obj.turnover
        })
    
    for turnover in turnovers:
        action_type = turnover.action_type
        action_stats[action_type]['totalTurnovers'] += 1
        action_stats[action_type]['turnovers'].append({
            'loc': [turnover.tov_loc_x, turnover.tov_loc_y]
        })
    
    pick_and_roll_count = (
        action_stats['pickAndRoll']['totalShotAttempts'] +
        action_stats['pickAndRoll']['totalPasses'] +
        action_stats['pickAndRoll']['totalTurnovers']
    ) if 'pickAndRoll' in action_stats else 0
    
    isolation_count = (
        action_stats['isolation']['totalShotAttempts'] +
        action_stats['isolation']['totalPasses'] +
        action_stats['isolation']['totalTurnovers']
    ) if 'isolation' in action_stats else 0
    
    post_up_count = (
        action_stats['postUp']['totalShotAttempts'] +
        action_stats['postUp']['totalPasses'] +
        action_stats['postUp']['totalTurnovers']
    ) if 'postUp' in action_stats else 0
    
    off_ball_screen_count = (
        action_stats['offBallScreen']['totalShotAttempts'] +
        action_stats['offBallScreen']['totalPasses'] +
        action_stats['offBallScreen']['totalTurnovers']
    ) if 'offBallScreen' in action_stats else 0
    
    response = {
        'name': player.name,
        'playerID': player_id,
        'totalShotAttempts': total_shot_attempts,
        'totalPoints': total_points,
        'totalPasses': total_passes,
        'totalPotentialAssists': total_potential_assists,
        'totalTurnovers': total_turnovers,
        'totalPassingTurnovers': total_passing_turnovers,
        'pickAndRollCount': pick_and_roll_count,
        'isolationCount': isolation_count,
        'postUpCount': post_up_count,
        'offBallScreenCount': off_ball_screen_count,
        'pickAndRoll': action_stats.get('pickAndRoll', {
            'totalShotAttempts': 0, 'totalPoints': 0, 'totalPasses': 0,
            'totalPotentialAssists': 0, 'totalTurnovers': 0, 'totalPassingTurnovers': 0,
            'shots': [], 'passes': [], 'turnovers': []
        }),
        'isolation': action_stats.get('isolation', {
            'totalShotAttempts': 0, 'totalPoints': 0, 'totalPasses': 0,
            'totalPotentialAssists': 0, 'totalTurnovers': 0, 'totalPassingTurnovers': 0,
            'shots': [], 'passes': [], 'turnovers': []
        }),
        'postUp': action_stats.get('postUp', {
            'totalShotAttempts': 0, 'totalPoints': 0, 'totalPasses': 0,
            'totalPotentialAssists': 0, 'totalTurnovers': 0, 'totalPassingTurnovers': 0,
            'shots': [], 'passes': [], 'turnovers': []
        }),
        'offBallScreen': action_stats.get('offBallScreen', {
            'totalShotAttempts': 0, 'totalPoints': 0, 'totalPasses': 0,
            'totalPotentialAssists': 0, 'totalTurnovers': 0, 'totalPassingTurnovers': 0,
            'shots': [], 'passes': [], 'turnovers': []
        })
    }
    
    return response


def get_ranks(player_id: str, player_summary: dict):
    """
    Calculate player ranks for each statistic against all players.
    Lower rank number means better performance (1st place, 2nd place, etc.)
    """
    try:
        player_id = int(player_id)
    except ValueError:
        return {"error": "Invalid player ID"}
    
    # Get all players' stats for comparison
    all_players = models.Player.objects.all()
    
    # Calculate stats for all players
    all_player_stats = []
    for player in all_players:
        shots = models.Shot.objects.filter(player=player)
        passes = models.Pass.objects.filter(player=player)
        turnovers = models.Turnover.objects.filter(player=player)
        
        pick_and_roll_actions = (
            shots.filter(action_type='pickAndRoll').count() +
            passes.filter(action_type='pickAndRoll').count() +
            turnovers.filter(action_type='pickAndRoll').count()
        )
        isolation_actions = (
            shots.filter(action_type='isolation').count() +
            passes.filter(action_type='isolation').count() +
            turnovers.filter(action_type='isolation').count()
        )
        post_up_actions = (
            shots.filter(action_type='postUp').count() +
            passes.filter(action_type='postUp').count() +
            turnovers.filter(action_type='postUp').count()
        )
        off_ball_screen_actions = (
            shots.filter(action_type='offBallScreen').count() +
            passes.filter(action_type='offBallScreen').count() +
            turnovers.filter(action_type='offBallScreen').count()
        )
        
        player_stats = {
            'player_id': player.player_id,
            'totalShotAttempts': shots.count(),
            'totalPoints': sum(shot.points for shot in shots),
            'totalPasses': passes.count(),
            'totalPotentialAssists': passes.filter(potential_assist=True).count(),
            'totalTurnovers': turnovers.count(),
            'totalPassingTurnovers': passes.filter(turnover=True).count(),
            'pickAndRollCount': pick_and_roll_actions,
            'isolationCount': isolation_actions,
            'postUpCount': post_up_actions,
            'offBallScreenCount': off_ball_screen_actions,
        }
        all_player_stats.append(player_stats)
    
    current_player_stats = None
    for stats in all_player_stats:
        if stats['player_id'] == player_id:
            current_player_stats = stats
            break
    
    if not current_player_stats:
        return {"error": "Player stats not found"}
    
    def calculate_rank(current_value, all_values, reverse=False):
        sorted_values = sorted(all_values, reverse=reverse)
        return sorted_values.index(current_value) + 1
    
    all_shot_attempts = [s['totalShotAttempts'] for s in all_player_stats]
    all_points = [s['totalPoints'] for s in all_player_stats]
    all_passes = [s['totalPasses'] for s in all_player_stats]
    all_potential_assists = [s['totalPotentialAssists'] for s in all_player_stats]
    all_turnovers = [s['totalTurnovers'] for s in all_player_stats]
    all_passing_turnovers = [s['totalPassingTurnovers'] for s in all_player_stats]
    all_pick_and_roll_counts = [s['pickAndRollCount'] for s in all_player_stats]
    all_isolation_counts = [s['isolationCount'] for s in all_player_stats]
    all_post_up_counts = [s['postUpCount'] for s in all_player_stats]
    all_off_ball_screen_counts = [s['offBallScreenCount'] for s in all_player_stats]
    
    ranks = {
        "totalShotAttemptsRank": calculate_rank(
            current_player_stats['totalShotAttempts'], all_shot_attempts, reverse=True
        ),
        "totalPointsRank": calculate_rank(
            current_player_stats['totalPoints'], all_points, reverse=True
        ),
        "totalPassesRank": calculate_rank(
            current_player_stats['totalPasses'], all_passes, reverse=True
        ),
        "totalPotentialAssistsRank": calculate_rank(
            current_player_stats['totalPotentialAssists'], all_potential_assists, reverse=True
        ),
        "totalTurnoversRank": calculate_rank(
            current_player_stats['totalTurnovers'], all_turnovers, reverse=False
        ),
        "totalPassingTurnoversRank": calculate_rank(
            current_player_stats['totalPassingTurnovers'], all_passing_turnovers, reverse=False
        ),
        'pickAndRollCountRank': calculate_rank(
            current_player_stats['pickAndRollCount'], all_pick_and_roll_counts, reverse=True
        ),
        'isolationCountRank': calculate_rank(
            current_player_stats['isolationCount'], all_isolation_counts, reverse=True
        ),
        'postUpCountRank': calculate_rank(
            current_player_stats['postUpCount'], all_post_up_counts, reverse=True
        ),
        'offBallScreenCountRank': calculate_rank(
            current_player_stats['offBallScreenCount'], all_off_ball_screen_counts, reverse=True
        ),
    }
    
    return ranks
