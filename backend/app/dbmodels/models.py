from django.db import models


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    
    class Meta:
        db_table = 'games'
        ordering = ['date']
    
    def __str__(self):
        return f"Game {self.game_id} - {self.date}"


class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    
    class Meta:
        db_table = 'players'
    
    def __str__(self):
        return self.name


class Shot(models.Model):
    ACTION_TYPES = [
        ('pickAndRoll', 'Pick and Roll'),
        ('isolation', 'Isolation'),
        ('postUp', 'Post Up'),
        ('offBallScreen', 'Off Ball Screen'),
    ]
    
    shot_id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='shots')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='shots')
    points = models.IntegerField()
    shooting_foul_drawn = models.BooleanField(default=False)
    shot_loc_x = models.FloatField()
    shot_loc_y = models.FloatField()
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    
    class Meta:
        db_table = 'shots'
    
    def __str__(self):
        return f"Shot {self.shot_id} by {self.player.name} - {self.points} points"


class Pass(models.Model):
    ACTION_TYPES = [
        ('pickAndRoll', 'Pick and Roll'),
        ('isolation', 'Isolation'),
        ('postUp', 'Post Up'),
        ('offBallScreen', 'Off Ball Screen'),
    ]
    
    pass_id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='passes')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='passes')
    completed_pass = models.BooleanField()
    potential_assist = models.BooleanField()
    turnover = models.BooleanField()
    ball_start_loc_x = models.FloatField()
    ball_start_loc_y = models.FloatField()
    ball_end_loc_x = models.FloatField()
    ball_end_loc_y = models.FloatField()
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    
    class Meta:
        db_table = 'passes'
    
    def __str__(self):
        return f"Pass {self.pass_id} by {self.player.name} - {'Completed' if self.completed_pass else 'Failed'}"


class Turnover(models.Model):
    ACTION_TYPES = [
        ('pickAndRoll', 'Pick and Roll'),
        ('isolation', 'Isolation'),
        ('postUp', 'Post Up'),
        ('offBallScreen', 'Off Ball Screen'),
    ]
    
    turnover_id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='turnovers')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='turnovers')
    tov_loc_x = models.FloatField()
    tov_loc_y = models.FloatField()
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    
    class Meta:
        db_table = 'turnovers'
    
    def __str__(self):
        return f"Turnover {self.turnover_id} by {self.player.name}"
