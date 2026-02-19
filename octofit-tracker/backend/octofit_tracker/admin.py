from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'team_id', 'created_at')
    list_filter = ('team_id', 'created_at')
    search_fields = ('username', 'email', 'full_name')
    readonly_fields = ('created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'user_id', 'duration', 'calories_burned', 'distance', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('user_id', 'activity_type', 'notes')
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'rank', 'total_points', 'total_activities', 'total_calories', 'updated_at')
    list_filter = ('rank', 'updated_at')
    search_fields = ('team_name', 'team_id')
    readonly_fields = ('updated_at',)
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration', 'category')
    list_filter = ('difficulty', 'category')
    search_fields = ('name', 'description', 'category')
