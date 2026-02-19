from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    team_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return self.username


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.JSONField(default=list)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.IntegerField()
    distance = models.FloatField(null=True, blank=True)  # in km
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'activities'
        indexes = [
            models.Index(fields=['user_id'], name='user_id_idx'),
            models.Index(fields=['date'], name='date_idx'),
        ]

    def __str__(self):
        return f"{self.activity_type} - {self.user_id}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    team_id = models.CharField(max_length=100)
    team_name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        indexes = [
            models.Index(fields=['team_id'], name='team_id_idx'),
            models.Index(fields=['rank'], name='rank_idx'),
        ]

    def __str__(self):
        return f"{self.team_name} - Rank {self.rank}"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    category = models.CharField(max_length=100)
    exercises = models.JSONField(default=list)
    recommended_for = models.JSONField(default=list)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
