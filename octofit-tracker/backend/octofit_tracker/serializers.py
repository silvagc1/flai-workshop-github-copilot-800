from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'full_name', 'team_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_id(self, obj):
        return str(obj._id)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.password = password  # In production, hash this properly
            user.save()
        return user


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'members', 'member_count']

    def get_id(self, obj):
        return str(obj._id)

    def get_member_count(self, obj):
        return len(obj.members) if obj.members else 0


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'calories_burned', 'distance', 'date', 'notes']

    def get_id(self, obj):
        return str(obj._id)


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'team_id', 'team_name', 'total_points', 'total_activities', 'total_calories', 'rank', 'updated_at']

    def get_id(self, obj):
        return str(obj._id)


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'duration', 'category', 'exercises', 'recommended_for']

    def get_id(self, obj):
        return str(obj._id)
