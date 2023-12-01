import unittest
from datetime import datetime
from cooking import create_app, db
from ..controllers.model import User, Recipe, Photo, Bookmark, Rating, QuantifiedIngredient, Step, Ingredient

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('cooking.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(email='test@example.com', username='testuser', password='password', salt=123, timestamp=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'test@example.com')

    def test_bookmark_creation(self):
        user = User(email='test@example.com', username='testuser', password='password', salt=123, timestamp=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        for i in range(3):
            recipe = Recipe(title=f'Test Recipe {i+1}', description=f'This is a test recipe {i+1}', user_id=user.id, servings=4, cook_time=30)
            db.session.add(recipe)
            db.session.commit()

            bookmark = Bookmark(user_id=user.id, recipe_id=recipe.id)
            db.session.add(bookmark)
        
        db.session.commit()

        saved_bookmarks = Bookmark.query.filter_by(user_id=user.id).all()
        self.assertEqual(len(saved_bookmarks), 3)


    def test_recipe_creation(self):
        user = User(email='test@example.com', username='testuser', password='password', salt=123, timestamp=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        for i in range(3):
            recipe = Recipe(title=f'Test Recipe {i+1}', description=f'This is a test recipe {i+1}', user_id=user.id, servings=4, cook_time=30)
            db.session.add(recipe)
        db.session.commit()

        saved_recipes = Recipe.query.filter_by(user_id=user.id).all()
        self.assertEqual(len(saved_recipes), 3)
        for saved_recipe, i in zip(saved_recipes, range(1, 4)):
            self.assertEqual(saved_recipe.title, f'Test Recipe {i}')

    def test_ingredient_creation(self):
        for i in range(3):
            ingredient = Ingredient(name=f'Ingredient {i+1}')
            db.session.add(ingredient)
        db.session.commit()

        saved_ingredients = Ingredient.query.all()
        self.assertEqual(len(saved_ingredients), 3)
        for saved_ingredient, i in zip(saved_ingredients, range(1, 4)):
            self.assertEqual(saved_ingredient.name, f'Ingredient {i}')

    def test_quantified_ingredient_creation(self):
        user = User(email='test@example.com', username='testuser', password='password', salt=123, timestamp=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(title='Test Recipe', description='This is a test recipe', user_id=user.id, servings=4, cook_time=30)
        db.session.add(recipe)
        db.session.commit()

        ingredient = Ingredient(name='Test Ingredient')
        db.session.add(ingredient)
        db.session.commit()

        for i in range(3):
            quantified_ingredient = QuantifiedIngredient(quantity=i+1, unit='units', ingredient_id=ingredient.id, recipe_id=recipe.id)
            db.session.add(quantified_ingredient)
        db.session.commit()

        saved_quantified_ingredients = QuantifiedIngredient.query.filter_by(recipe_id=recipe.id).all()
        self.assertEqual(len(saved_quantified_ingredients), 3)
        for saved_qi, i in zip(saved_quantified_ingredients, range(1, 4)):
            self.assertEqual(saved_qi.quantity, i)

    def test_step_creation(self):
        recipe = Recipe(title='Test Recipe', description='This is a test recipe', user_id=1, servings=4, cook_time=30)
        db.session.add(recipe)
        db.session.commit()

        for i in range(3):
            step = Step(seq_number=i+1, description=f'Test step {i+1}', recipe_id=recipe.id)
            db.session.add(step)
        db.session.commit()

        saved_steps = Step.query.filter_by(recipe_id=recipe.id).all()
        self.assertEqual(len(saved_steps), 3)

    def test_rating_creation(self):
        user = User(email='test@example.com', username='testuser', password='password', salt=123, timestamp=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(title='Test Recipe', description='This is a test recipe', user_id=user.id, servings=4, cook_time=30)
        db.session.add(recipe)
        db.session.commit()

        for i in range(3):
            rating = Rating(rating=i+1, recipe_id=recipe.id, user_id=user.id)
            db.session.add(rating)
        db.session.commit()

        saved_ratings = Rating.query.filter_by(user_id=user.id).all()
        self.assertEqual(len(saved_ratings), 3)
        for saved_rating, i in zip(saved_ratings, range(1, 4)):
            self.assertEqual(saved_rating.rating, i)

    def test_photo_creation(self):
        user = User(email='test@example.com', username='testuser', password='password', salt=123, timestamp=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(title='Test Recipe', description='This is a test recipe', user_id=user.id, servings=4, cook_time=30)
        db.session.add(recipe)
        db.session.commit()

        for i in range(3):
            photo = Photo(file_extension='jpeg', user_id=user.id, recipe_id=recipe.id)
            db.session.add(photo)
        db.session.commit()

        saved_photos = Photo.query.filter_by(user_id=user.id).all()
        self.assertEqual(len(saved_photos), 3)
        for saved_photo, i in zip(saved_photos, range(1, 4)):
            self.assertEqual(saved_photo.file_extension, 'jpeg')


if __name__ == '__main__':
    unittest.main()
