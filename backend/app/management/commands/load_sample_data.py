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
                teamID=team_data['teamID'],
                defaults={
                    'name': team_data['name'],
                    'city': team_data['city']
                }
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
            player, created = Player.objects.get_or_create(
                playerID=player_data['playerID'],
                defaults={
                    'name': player_data['name'],
                    'teamID': player_data['teamID']
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
                gameID=game_data['gameID'],
                defaults={
                    'date': datetime.strptime(game_data['date'], '%Y-%m-%d').date(),
                    'homeTeamID': game_data['homeTeamID'],
                    'awayTeamID': game_data['awayTeamID']
                }
            )
            if created:
                self.stdout.write(f'  Created game: {game.gameID}')
            else:
                self.stdout.write(f'  Game already exists: {game.gameID}')

    def load_shots(self):
        """Load shots data from games.json"""
        self.stdout.write('Loading shots...')
        games_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'games.json')
        
        with open(games_path, 'r') as f:
            games_data = json.load(f)
        
        shot_count = 0
        for game_data in games_data:
            for shot_data in game_data.get('shots', []):
                shot, created = Shot.objects.get_or_create(
                    shotID=shot_data['shotID'],
                    defaults={
                        'gameID': game_data['gameID'],
                        'playerID': shot_data['playerID'],
                        'loc': shot_data['loc'],
                        'points': shot_data['points']
                    }
                )
                if created:
                    shot_count += 1
        
        self.stdout.write(f'  Loaded {shot_count} shots')

    def load_passes(self):
        """Load passes data from games.json"""
        self.stdout.write('Loading passes...')
        games_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'games.json')
        
        with open(games_path, 'r') as f:
            games_data = json.load(f)
        
        pass_count = 0
        for game_data in games_data:
            for pass_data in game_data.get('passes', []):
                pass_obj, created = Pass.objects.get_or_create(
                    passID=pass_data['passID'],
                    defaults={
                        'gameID': game_data['gameID'],
                        'playerID': pass_data['playerID'],
                        'startLoc': pass_data['startLoc'],
                        'endLoc': pass_data['endLoc'],
                        'isCompleted': pass_data['isCompleted'],
                        'isPotentialAssist': pass_data['isPotentialAssist'],
                        'isTurnover': pass_data['isTurnover']
                    }
                )
                if created:
                    pass_count += 1
        
        self.stdout.write(f'  Loaded {pass_count} passes')

    def load_turnovers(self):
        """Load turnovers data from games.json"""
        self.stdout.write('Loading turnovers...')
        games_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'raw_data', 'games.json')
        
        with open(games_path, 'r') as f:
            games_data = json.load(f)
        
        turnover_count = 0
        for game_data in games_data:
            for turnover_data in game_data.get('turnovers', []):
                turnover, created = Turnover.objects.get_or_create(
                    turnoverID=turnover_data['turnoverID'],
                    defaults={
                        'gameID': game_data['gameID'],
                        'playerID': turnover_data['playerID'],
                        'loc': turnover_data['loc']
                    }
                )
                if created:
                    turnover_count += 1
        
        self.stdout.write(f'  Loaded {turnover_count} turnovers')
