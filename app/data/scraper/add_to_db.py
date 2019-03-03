from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import json

""" 
    This file takes the recipe database and transfers it to a mongodb collection.
    In addition a first user will be inserted to the user collection and filter
    keywords will be extracted from the database and stored in a filters collection
    for easy and quick queries and to be used to create menus and options.
"""

# assign mongo client
client = MongoClient("localhost", 27017)

# database / collections
db = client.foodie
recipes = db.recipes
users = db.users
filters = db.filters


# ============================================ #


def add_recipes():
    """
        add recipes to recipe collection
    """

    with open('app/data/scraper/db.json') as db_file:
        data = json.load(db_file)
        recipes.insert_many(data['recipes'])


# ============================================ #


def add_user():
    """
        add first user to user collection
    """

    with open('app/data/schemas/user.json') as users_file:
        user = json.load(users_file)
        user['username'] = 'sean'
        user['password'] = generate_password_hash('password')
        users.insert_one(user)


# ============================================ #


def add_filters():
    """
        create collection for menu items and mega filter
    """

    with open('app/data/scraper/db.json') as db_file:
        data = json.load(db_file)

        cuisine = []
        planning = []
        skill = []
        mood = []
        course = []
        diet = []

        # Iterate over Recipes
        for i in data['recipes']:

            # cuisine
            if not i['recipe_filters']['cuisine'] in cuisine:
                if not i['recipe_filters']['cuisine'] == '':
                    cuisine.append(i['recipe_filters']['cuisine'])

            # planning
            if not i['recipe_filters']['planning'] in planning:
                if not i['recipe_filters']['planning'] == '':
                    planning.append(i['recipe_filters']['planning'])

            # skill
            if not i['recipe_filters']['skill'] in skill:
                if not i['recipe_filters']['skill'] == '':
                    skill.append(i['recipe_filters']['skill'])

            # mood
            if not i['recipe_filters']['mood'] in mood:
                if not i['recipe_filters']['mood'] == '':
                    mood.append(i['recipe_filters']['mood'])

            # diet
            if not i['recipe_filters']['diet'] in diet:
                if not i['recipe_filters']['diet'] == '':
                    diet.append(i['recipe_filters']['diet'])

            # course
            for courses in i['recipe_filters']['course']:
                if not courses in course:
                    if not courses == '':
                        course.append(courses)

        # insert document into mongo collection - filters
        filters.insert_one({
            "cuisine": cuisine,
            "course": course,
            "planning": planning,
            "mood": mood,
            "diet": diet,
            "skill": skill
        })


# ============================================ #


""" 
    run file
"""
add_recipes()
add_user()
add_filters()