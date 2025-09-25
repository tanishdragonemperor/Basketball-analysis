#!/usr/bin/env python3

import os
import sys
import json
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from app.dbmodels.models import Team, Game, Player, Shot, Pass, Turnover


def load_teams():
    print("Loading teams...")
    teams_path = os.path.join(os.path.dirname(__file__), '..', 'raw_data', 'teams.json')
    
    with open(teams_path, 'r') as f:
        teams_data = json.load(f)
    
    for team_data in teams_data:
        team, created = Team.objects.get_or_create(
            team_id=team_data['team_id'],
            defaults={'name': team_data['name']}
        )
        if created:
            print(f"Created team: {team.name}")
        else:
            print(f"Team already exists: {team.name}")
    
    print(f"Loaded {len(teams_data)} teams")


def load_games():
    print("Loading games...")
    games_path = os.path.join(os.path.dirname(__file__), '..', 'raw_data', 'games.json')
    
    with open(games_path, 'r') as f:
        games_data = json.load(f)
    
    for game_data in games_data:
        game_date = datetime.strptime(game_data['date'], '%Y-%m-%d').date()
        game, created = Game.objects.get_or_create(
            game_id=game_data['id'],
            defaults={'date': game_date}
        )
        if created:
            print(f"Created game: {game}")
        else:
            print(f"Game already exists: {game}")
    
    print(f"Loaded {len(games_data)} games")


def load_players():
    """Load players data from players.json"""
    print("Loading players...")
    players_path = os.path.join(os.path.dirname(__file__), '..', 'raw_data', 'players.json')
    
    with open(players_path, 'r') as f:
        players_data = json.load(f)
    
    for player_data in players_data:
        player, created = Player.objects.get_or_create(
            player_id=player_data['player_id'],
            defaults={
                'name': player_data['name'],
                'team_id': player_data['team_id']
            }
        )
        if created:
            print(f"Created player: {player.name}")
        else:
            print(f"Player already exists: {player.name}")
    
    print(f"Loaded {len(players_data)} players")


def load_shots():
    """Load shots data from players.json"""
    print("Loading shots...")
    players_path = os.path.join(os.path.dirname(__file__), '..', 'raw_data', 'players.json')
    
    with open(players_path, 'r') as f:
        players_data = json.load(f)
    
    shots_loaded = 0
    for player_data in players_data:
        player_id = player_data['player_id']
        player = Player.objects.get(player_id=player_id)
        
        for shot_data in player_data.get('shots', []):
            shot, created = Shot.objects.get_or_create(
                shot_id=shot_data['id'],
                defaults={
                    'player': player,
                    'game_id': shot_data['game_id'],
                    'points': shot_data['points'],
                    'shooting_foul_drawn': shot_data['shooting_foul_drawn'],
                    'shot_loc_x': shot_data['shot_loc_x'],
                    'shot_loc_y': shot_data['shot_loc_y'],
                    'action_type': shot_data['action_type']
                }
            )
            if created:
                shots_loaded += 1
    
    print(f"Loaded {shots_loaded} shots")


def load_passes():
    """Load passes data from players.json"""
    print("Loading passes...")
    players_path = os.path.join(os.path.dirname(__file__), '..', 'raw_data', 'players.json')
    
    with open(players_path, 'r') as f:
        players_data = json.load(f)
    
    passes_loaded = 0
    for player_data in players_data:
        player_id = player_data['player_id']
        player = Player.objects.get(player_id=player_id)
        
        for pass_data in player_data.get('passes', []):
            pass_obj, created = Pass.objects.get_or_create(
                pass_id=pass_data['id'],
                defaults={
                    'player': player,
                    'game_id': pass_data['game_id'],
                    'completed_pass': pass_data['completed_pass'],
                    'potential_assist': pass_data['potential_assist'],
                    'turnover': pass_data['turnover'],
                    'ball_start_loc_x': pass_data['ball_start_loc_x'],
                    'ball_start_loc_y': pass_data['ball_start_loc_y'],
                    'ball_end_loc_x': pass_data['ball_end_loc_x'],
                    'ball_end_loc_y': pass_data['ball_end_loc_y'],
                    'action_type': pass_data['action_type']
                }
            )
            if created:
                passes_loaded += 1
    
    print(f"Loaded {passes_loaded} passes")


def load_turnovers():
    """Load turnovers data from players.json"""
    print("Loading turnovers...")
    players_path = os.path.join(os.path.dirname(__file__), '..', 'raw_data', 'players.json')
    
    with open(players_path, 'r') as f:
        players_data = json.load(f)
    
    turnovers_loaded = 0
    for player_data in players_data:
        player_id = player_data['player_id']
        player = Player.objects.get(player_id=player_id)
        
        for turnover_data in player_data.get('turnovers', []):
            turnover, created = Turnover.objects.get_or_create(
                turnover_id=turnover_data['id'],
                defaults={
                    'player': player,
                    'game_id': turnover_data['game_id'],
                    'tov_loc_x': turnover_data['tov_loc_x'],
                    'tov_loc_y': turnover_data['tov_loc_y'],
                    'action_type': turnover_data['action_type']
                }
            )
            if created:
                turnovers_loaded += 1
    
    print(f"Loaded {turnovers_loaded} turnovers")


def main():
    """Main function to load all data"""
    print("Starting data loading process...")
    
    try:
        # Load data in dependency order
        load_teams()
        load_games()
        load_players()
        load_shots()
        load_passes()
        load_turnovers()
        
        print("\nData loading completed successfully!")
        
        # Print summary statistics
        print(f"\nDatabase Summary:")
        print(f"Teams: {Team.objects.count()}")
        print(f"Games: {Game.objects.count()}")
        print(f"Players: {Player.objects.count()}")
        print(f"Shots: {Shot.objects.count()}")
        print(f"Passes: {Pass.objects.count()}")
        print(f"Turnovers: {Turnover.objects.count()}")
        
    except Exception as e:
        print(f"Error during data loading: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
