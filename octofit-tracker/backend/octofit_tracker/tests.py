from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='password123',
            full_name='Test User'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members=[]
        )

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertEqual(len(self.team.members), 0)

    def test_team_string_representation(self):
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='user123',
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=5.0,
            date=datetime.now()
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
        self.assertEqual(self.activity.distance, 5.0)


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            team_id='team123',
            team_name='Test Team',
            total_points=100,
            total_activities=10,
            total_calories=1000,
            rank=1
        )

    def test_leaderboard_creation(self):
        self.assertEqual(self.leaderboard.team_name, 'Test Team')
        self.assertEqual(self.leaderboard.total_points, 100)
        self.assertEqual(self.leaderboard.rank, 1)


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Yoga',
            description='A relaxing yoga session',
            difficulty='Beginner',
            duration=30,
            category='Yoga',
            exercises=[],
            recommended_for=[]
        )

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, 'Morning Yoga')
        self.assertEqual(self.workout.difficulty, 'Beginner')
        self.assertEqual(self.workout.duration, 30)


class UserAPITest(APITestCase):
    def test_get_users_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123',
            'full_name': 'New User'
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamAPITest(APITestCase):
    def test_get_teams_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        data = {
            'name': 'New Team',
            'description': 'A new team',
            'members': []
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    def test_get_activities_list(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_activity(self):
        data = {
            'user_id': 'user123',
            'activity_type': 'Running',
            'duration': 30,
            'calories_burned': 300,
            'distance': 5.0,
            'date': datetime.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITest(APITestCase):
    def test_get_leaderboard_list(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    def test_get_workouts_list(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workout(self):
        data = {
            'name': 'Test Workout',
            'description': 'A test workout',
            'difficulty': 'Beginner',
            'duration': 30,
            'category': 'Cardio',
            'exercises': [],
            'recommended_for': []
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class APIRootTest(APITestCase):
    def test_api_root_endpoint(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
