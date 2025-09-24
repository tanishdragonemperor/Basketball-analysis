import os
import sys
import json
import django
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.dbmodels.models import Team, Game, Player, Shot, Pass, Turnover


class Command(BaseCommand):
    help = 'Load sample basketball data into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample basketball data...')
        
        try:
            with transaction.atomic():
                self.load_teams()
                self.load_players()
                self.load_games()
                self.load_shots()
                self.load_passes()
                self.load_turnovers()
                
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded sample data!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading data: {str(e)}')
            )
            raise

    def load_teams(self):
        """Load teams data from teams.json"""
        self.stdout.write('Loading teams...')
        teams_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'teams.json')
        
        with open(teams_path, 'r') as f:
            teams_data = json.load(f)
        
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                team_id=team_data['team_id'],
                defaults={'name': team_data['name']}
            )
            if created:
                self.stdout.write(f'  Created team: {team.name}')
            else:
                self.stdout.write(f'  Team already exists: {team.name}')

    def load_players(self):
        """Load players data from players.json"""
        self.stdout.write('Loading players...')
        players_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'players.json')
        
        with open(players_path, 'r') as f:
            players_data = json.load(f)
        
        for player_data in players_data:
            # Get the team object first
            try:
                team = Team.objects.get(team_id=player_data['team_id'])
            except Team.DoesNotExist:
                self.stdout.write(f'  Warning: Team with ID {player_data["team_id"]} not found for player {player_data["name"]}')
                continue
                
            player, created = Player.objects.get_or_create(
                player_id=player_data['player_id'],
                defaults={
                    'name': player_data['name'],
                    'team': team
                }
            )
            if created:
                self.stdout.write(f'  Created player: {player.name}')
            else:
                self.stdout.write(f'  Player already exists: {player.name}')

    def load_games(self):
        """Load games data from games.json"""
        self.stdout.write('Loading games...')
        games_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'games.json')
        
        with open(games_path, 'r') as f:
            games_data = json.load(f)
        
        for game_data in games_data:
            game, created = Game.objects.get_or_create(
                game_id=game_data['id'],
                defaults={
                    'date': datetime.strptime(game_data['date'], '%Y-%m-%d').date()
                }
            )
            if created:
                self.stdout.write(f'  Created game: {game.game_id}')
            else:
                self.stdout.write(f'  Game already exists: {game.game_id}')

    def load_shots(self):
        """Load shots data from players.json"""
        self.stdout.write('Loading shots...')
        players_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'players.json')
        
        with open(players_path, 'r') as f:
            players_data = json.load(f)
        
        shot_count = 0
        for player_data in players_data:
            try:
                player = Player.objects.get(player_id=player_data['player_id'])
                for shot_data in player_data.get('shots', []):
                    try:
                        game = Game.objects.get(game_id=shot_data['game_id'])
                        shot, created = Shot.objects.get_or_create(
                            shot_id=shot_data['id'],
                            defaults={
                                'player': player,
                                'game': game,
                                'points': shot_data['points'],
                                'shooting_foul_drawn': shot_data['shooting_foul_drawn'],
                                'shot_loc_x': shot_data['shot_loc_x'],
                                'shot_loc_y': shot_data['shot_loc_y'],
                                'action_type': shot_data['action_type']
                            }
                        )
                        if created:
                            shot_count += 1
                    except Game.DoesNotExist:
                        self.stdout.write(f'  Warning: Game {shot_data["game_id"]} not found for shot {shot_data["id"]}')
                        continue
            except Player.DoesNotExist:
                self.stdout.write(f'  Warning: Player {player_data["player_id"]} not found for shots')
                continue
        
        self.stdout.write(f'  Loaded {shot_count} shots')

    def load_passes(self):
        """Load passes data from players.json"""
        self.stdout.write('Loading passes...')
        players_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'players.json')
        
        with open(players_path, 'r') as f:
            players_data = json.load(f)
        
        pass_count = 0
        for player_data in players_data:
            try:
                player = Player.objects.get(player_id=player_data['player_id'])
                for pass_data in player_data.get('passes', []):
                    try:
                        game = Game.objects.get(game_id=pass_data['game_id'])
                        pass_obj, created = Pass.objects.get_or_create(
                            pass_id=pass_data['id'],
                            defaults={
                                'player': player,
                                'game': game,
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
                            pass_count += 1
                    except Game.DoesNotExist:
                        self.stdout.write(f'  Warning: Game {pass_data["game_id"]} not found for pass {pass_data["id"]}')
                        continue
            except Player.DoesNotExist:
                self.stdout.write(f'  Warning: Player {player_data["player_id"]} not found for passes')
                continue
        
        self.stdout.write(f'  Loaded {pass_count} passes')

    def load_turnovers(self):
        """Load turnovers data from players.json"""
        self.stdout.write('Loading turnovers...')
        players_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'players.json')
        
        with open(players_path, 'r') as f:
            players_data = json.load(f)
        
        turnover_count = 0
        for player_data in players_data:
            try:
                player = Player.objects.get(player_id=player_data['player_id'])
                for turnover_data in player_data.get('turnovers', []):
                    try:
                        game = Game.objects.get(game_id=turnover_data['game_id'])
                        turnover, created = Turnover.objects.get_or_create(
                            turnover_id=turnover_data['id'],
                            defaults={
                                'player': player,
                                'game': game,
                                'tov_loc_x': turnover_data['tov_loc_x'],
                                'tov_loc_y': turnover_data['tov_loc_y'],
                                'action_type': turnover_data['action_type']
                            }
                        )
                        if created:
                            turnover_count += 1
                    except Game.DoesNotExist:
                        self.stdout.write(f'  Warning: Game {turnover_data["game_id"]} not found for turnover {turnover_data["id"]}')
                        continue
            except Player.DoesNotExist:
                self.stdout.write(f'  Warning: Player {player_data["player_id"]} not found for turnovers')
                continue
        
        self.stdout.write(f'  Loaded {turnover_count} turnovers')
