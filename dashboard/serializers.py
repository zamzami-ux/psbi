from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Mission, Question, Choice, UserAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'order', 'choices')


class MissionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = ('id', 'title', 'description', 'xp_reward', 'content', 'order', 'questions')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = ('user', 'xp', 'level', 'streak_days')
