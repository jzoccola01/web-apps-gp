from datetime import datetime
from random import randint, choice
from sqlalchemy.exc import IntegrityError
from cooking import create_app, db
from cooking.controllers.model import User, Bookmark, Recipe, Ingredient, QuantifiedIngredient, Step, Rating, Photo

# Create the Flask app and set up the configuration
app = create_app()
app.config.from_object('cooking.config.Config')

# Set up the Flask application context
app.app_context().push()

# Create or recreate all database tables
db.drop_all()
db.create_all()

def populate_database():
    # Create 5 users
    users = []
    for i in range(5):
        user = User(
            email=f'user{i + 1}@example.com',
            username=f'user{i + 1}',
            password=f'password{i + 1}',
            salt=randint(0, 100000),
            timestamp=datetime.utcnow()
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Create 5 ingredients
    ingredients = []
    for i in range(5):
        ingredient = Ingredient(name=f'Ingredient {i + 1}')
        ingredients.append(ingredient)
        db.session.add(ingredient)
    db.session.commit()

    # Create 5 recipes
    recipes = []
    for i in range(5):
        recipe = Recipe(
            title=f'Recipe {i + 1}',
            description=f'This is recipe {i + 1}',
            user_id=choice(users).id,
            servings=randint(2, 8),
            cook_time=randint(15, 60),
            timestamp=datetime.utcnow(),
            category=choice(['breakfast', 'lunch', 'dinner', 'none'])
        )
        recipes.append(recipe)
        db.session.add(recipe)
    db.session.commit()

    # Create 5 quantified ingredients for each recipe
    for recipe in recipes:
        for i in range(5):
            quantified_ingredient = QuantifiedIngredient(
                quantity=randint(1, 10),
                unit='units',
                ingredient_id=choice(ingredients).id,
                recipe_id=recipe.id
            )
            db.session.add(quantified_ingredient)
    db.session.commit()

    # Create 5 steps for each recipe
    for recipe in recipes:
        for i in range(5):
            step = Step(
                seq_number=i + 1,
                description=f'Step {i + 1} for {recipe.title}',
                recipe_id=recipe.id
            )
            db.session.add(step)
    db.session.commit()

    # Create 5 ratings for each recipe
    for recipe in recipes:
        for i in range(5):
            rating = Rating(
                rating=randint(1, 5),
                recipe_id=recipe.id,
                user_id=choice(users).id,
                comment=f'Comment for {recipe.title} - Rating {i + 1}'
            )
            db.session.add(rating)
    db.session.commit()

    # Create 5 photos for each recipe
    for recipe in recipes:
        for i in range(5):
            photo = Photo(
                file_extension='jpeg',
                user_id=choice(users).id,
                recipe_id=recipe.id
            )
            db.session.add(photo)
    db.session.commit()

    # Create 5 bookmarks for each user, since I added the unique constraint for 1 user booking the same recipe twice,
    # I added a try except block to handle the error and pass it. It isn't guaranteed that each user will have 5 bookmarked recipes


    # Since I have the unique constraint, I can't add the same recipe twice for the same user, not able to figure out how to get the exception to catch
    # so I commented out the code below

    # for user in users:
    #     for i in range(5):
    #         try:
    #             chosen_recipe = choice(recipes)
    #             bookmark = Bookmark(
    #                 user_id=user.id,
    #                 recipe_id=chosen_recipe.id
    #             )
    #             db.session.add(bookmark)
    #         except IntegrityError:
    #             # Handle the unique constraint violation (e.g., log the error)
    #             print(f'User {user.id} already bookmarked recipe {chosen_recipe.id}')
    #             pass

    # db.session.commit()

    # # Clean up the application context when done populating the database
    # if app.app_context().stack:
    #     app.app_context().pop()


if __name__ == "__main__":
    populate_database()
