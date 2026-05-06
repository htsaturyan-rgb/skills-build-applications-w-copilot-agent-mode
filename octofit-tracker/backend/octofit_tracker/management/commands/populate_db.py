from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient, ASCENDING

# Sample data
USERS = [
    {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
    {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
    {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
]
TEAMS = [
    {"name": "Marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
    {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
]
ACTIVITIES = [
    {"user": "Superman", "activity": "Flight", "duration": 60},
    {"user": "Batman", "activity": "Martial Arts", "duration": 45},
    {"user": "Iron Man", "activity": "Suit Training", "duration": 30},
]
LEADERBOARD = [
    {"user": "Superman", "score": 100},
    {"user": "Iron Man", "score": 90},
    {"user": "Batman", "score": 80},
]
WORKOUTS = [
    {"name": "Strength", "description": "General strength workout"},
    {"name": "Agility", "description": "Agility and speed drills"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB using pymongo
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']
        # Drop collections if they exist
        for col in ["users", "teams", "activities", "leaderboard", "workouts"]:
            db[col].delete_many({})
        # Insert data
        db["users"].insert_many(USERS)
        db["teams"].insert_many(TEAMS)
        db["activities"].insert_many(ACTIVITIES)
        db["leaderboard"].insert_many(LEADERBOARD)
        db["workouts"].insert_many(WORKOUTS)
        # Ensure unique index on email
        db["users"].create_index([("email", ASCENDING)], unique=True)
        self.stdout.write(self.style.SUCCESS("octofit_db populated with test data."))
