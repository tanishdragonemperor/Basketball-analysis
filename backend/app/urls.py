
from django.urls import re_path
from app.views import players

urlpatterns = [
    re_path(r'^api/v1/playerSummary/(?P<playerID>[0-9]+)$', players.PlayerSummary.as_view(), name='player_summary'),
]
