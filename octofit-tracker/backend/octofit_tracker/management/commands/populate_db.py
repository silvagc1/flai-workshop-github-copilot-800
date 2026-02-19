from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers assemble! The mightiest heroes united.',
            members=[]
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League - defenders of truth and justice.',
            members=[]
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        
        marvel_heroes = [
            {'username': 'ironman', 'full_name': 'Tony Stark', 'email': 'tony@stark.com'},
            {'username': 'captainamerica', 'full_name': 'Steve Rogers', 'email': 'steve@avengers.com'},
            {'username': 'thor', 'full_name': 'Thor Odinson', 'email': 'thor@asgard.com'},
            {'username': 'hulk', 'full_name': 'Bruce Banner', 'email': 'bruce@gamma.com'},
            {'username': 'blackwidow', 'full_name': 'Natasha Romanoff', 'email': 'natasha@shield.com'},
            {'username': 'spiderman', 'full_name': 'Peter Parker', 'email': 'peter@spidey.com'},
        ]
        
        dc_heroes = [
            {'username': 'superman', 'full_name': 'Clark Kent', 'email': 'clark@dailyplanet.com'},
            {'username': 'batman', 'full_name': 'Bruce Wayne', 'email': 'bruce@wayne.com'},
            {'username': 'wonderwoman', 'full_name': 'Diana Prince', 'email': 'diana@themyscira.com'},
            {'username': 'flash', 'full_name': 'Barry Allen', 'email': 'barry@flash.com'},
            {'username': 'aquaman', 'full_name': 'Arthur Curry', 'email': 'arthur@atlantis.com'},
            {'username': 'greenlantern', 'full_name': 'Hal Jordan', 'email': 'hal@greenlantern.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                username=hero['username'],
                full_name=hero['full_name'],
                email=hero['email'],
                password='password123',  # In production, use proper hashing
                team_id=str(team_marvel._id)
            )
            marvel_users.append(user)
            team_marvel.members.append(str(user._id))
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                username=hero['username'],
                full_name=hero['full_name'],
                email=hero['email'],
                password='password123',  # In production, use proper hashing
                team_id=str(team_dc._id)
            )
            dc_users.append(user)
            team_dc.members.append(str(user._id))
        
        team_marvel.save()
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(marvel_users) + len(dc_users)} users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'CrossFit']
        all_users = marvel_users + dc_users
        
        activities_count = 0
        for user in all_users:
            # Create 5-10 random activities per user
            num_activities = random.randint(5, 10)
            for _ in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 12)
                distance = round(random.uniform(2.0, 15.0), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    distance=distance,
                    date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'{user.full_name} completed {activity_type.lower()} session'
                )
                activities_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_count} activities'))
        
        # Calculate and create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        
        teams_stats = []
        for team, users in [(team_marvel, marvel_users), (team_dc, dc_users)]:
            total_points = 0
            total_activities = 0
            total_calories = 0
            
            for user in users:
                user_activities = Activity.objects.filter(user_id=str(user._id))
                total_activities += user_activities.count()
                total_calories += sum(a.calories_burned for a in user_activities)
                total_points += user_activities.count() * 10 + total_calories // 100
            
            teams_stats.append({
                'team': team,
                'total_points': total_points,
                'total_activities': total_activities,
                'total_calories': total_calories
            })
        
        # Sort by points and assign ranks
        teams_stats.sort(key=lambda x: x['total_points'], reverse=True)
        
        for rank, team_stat in enumerate(teams_stats, start=1):
            Leaderboard.objects.create(
                team_id=str(team_stat['team']._id),
                team_name=team_stat['team'].name,
                total_points=team_stat['total_points'],
                total_activities=team_stat['total_activities'],
                total_calories=team_stat['total_calories'],
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams_stats)} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'High-intensity training inspired by Captain America',
                'difficulty': 'Advanced',
                'duration': 60,
                'category': 'Strength',
                'exercises': ['Push-ups', 'Pull-ups', 'Shield throws', 'Sprint intervals'],
                'recommended_for': ['strength', 'endurance', 'military']
            },
            {
                'name': 'Web-Slinger Cardio',
                'description': 'Agility and cardiovascular workout like Spider-Man',
                'difficulty': 'Intermediate',
                'duration': 45,
                'category': 'Cardio',
                'exercises': ['Jump rope', 'Box jumps', 'Burpees', 'Mountain climbers'],
                'recommended_for': ['cardio', 'agility', 'endurance']
            },
            {
                'name': 'Amazonian Warrior Workout',
                'description': 'Strength and combat training from Themyscira',
                'difficulty': 'Advanced',
                'duration': 75,
                'category': 'Combat',
                'exercises': ['Sword drills', 'Shield training', 'Deadlifts', 'Battle ropes'],
                'recommended_for': ['strength', 'combat', 'power']
            },
            {
                'name': 'Speed Force Circuit',
                'description': 'Lightning-fast interval training',
                'difficulty': 'Intermediate',
                'duration': 30,
                'category': 'Speed',
                'exercises': ['Sprint intervals', 'Fast feet drills', 'Plyometrics', 'Agility ladder'],
                'recommended_for': ['speed', 'cardio', 'explosiveness']
            },
            {
                'name': 'Zen of the Dark Knight',
                'description': 'Meditation and recovery inspired by Batman',
                'difficulty': 'Beginner',
                'duration': 30,
                'category': 'Recovery',
                'exercises': ['Meditation', 'Stretching', 'Foam rolling', 'Breathing exercises'],
                'recommended_for': ['recovery', 'flexibility', 'mental']
            },
            {
                'name': 'Asgardian Strength',
                'description': 'Godly power training with Thor',
                'difficulty': 'Advanced',
                'duration': 90,
                'category': 'Strength',
                'exercises': ['Hammer swings', 'Overhead press', 'Squats', 'Farmer carries'],
                'recommended_for': ['strength', 'power', 'mass']
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workouts'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Database population completed! ==='))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
