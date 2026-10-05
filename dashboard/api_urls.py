from django.urls import path
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('missions/', api_views.MissionListAPI.as_view(), name='api-missions'),
    path('missions/<int:pk>/', api_views.MissionDetailAPI.as_view(), name='api-mission-detail'),
    path('submit_answer/', api_views.SubmitAnswerAPI.as_view(), name='api-submit-answer'),
    path('leaderboard/', api_views.LeaderboardAPI.as_view(), name='api-leaderboard'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
