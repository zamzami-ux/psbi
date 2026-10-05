from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Mission, Question, Choice, UserAnswer, UserProfile
from .serializers import MissionSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny


class MissionListAPI(generics.ListAPIView):
    queryset = Mission.objects.all().order_by('order')
    serializer_class = MissionSerializer
    permission_classes = [AllowAny]


class MissionDetailAPI(generics.RetrieveAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [AllowAny]


class SubmitAnswerAPI(APIView):
    """POST: {"username": "user1", "question_id": 1, "choice_id": 4}
    Records answer and returns whether correct and updated XP.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        question_id = request.data.get('question_id')
        choice_id = request.data.get('choice_id')

        if not (username and question_id and choice_id):
            return Response({'detail': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            question = Question.objects.get(id=question_id)
            choice = Choice.objects.get(id=choice_id, question=question)
        except (Question.DoesNotExist, Choice.DoesNotExist):
            return Response({'detail': 'Question or choice not found'}, status=status.HTTP_404_NOT_FOUND)

        is_correct = choice.is_correct

        ua, created = UserAnswer.objects.update_or_create(
            user=user, question=question,
            defaults={'choice': choice, 'is_correct': is_correct}
        )

        # simple xp reward: if correct add mission xp_reward (first try)
        try:
            mission = question.mission
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if is_correct:
                profile.xp += mission.xp_reward
                profile.save()
        except Exception:
            pass

        return Response({'is_correct': is_correct, 'xp': getattr(profile, 'xp', None)})


class LeaderboardAPI(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return UserProfile.objects.filter(show_in_leaderboard=True).order_by('-xp')[:20]
