from .. import db
import flask_login

class User(flask_login.UserMixin, db.Model,):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.Integer, nullable=False)
    recipes = db.relationship('Recipe', back_populates='user')
    photos = db.relationship('Photo', back_populates='user')
    bookmarks = db.relationship('Bookmark', back_populates='user')
    timestamp = db.Column(db.DateTime, nullable=False)
    ratings = db.relationship('Rating', back_populates='user')

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Added unique=True to the recipe_id column since no user should be able to bookmark the same recipe more than once
    # Uri: changed this back, because this logic is automatically handled by toggling the bookmark button
    # We actually need this to be false so that we can have multiple users bookmark the same recipe
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False, unique=False)
    user = db.relationship('User', back_populates='bookmarks')
    recipe = db.relationship('Recipe', back_populates='bookmarks')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')
    servings = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    quantified_ingredients = db.relationship('QuantifiedIngredient', back_populates='recipe')
    steps = db.relationship('Step', back_populates='recipe')
    ratings = db.relationship('Rating', back_populates='recipe')
    bookmarks = db.relationship('Bookmark', back_populates='recipe')
    photos = db.relationship('Photo', back_populates='recipe')
    timestamp = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(64), nullable=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    quantified_ingredients = db.relationship('QuantifiedIngredient', back_populates='ingredient')

class QuantifiedIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(64), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    ingredient = db.relationship('Ingredient', back_populates='quantified_ingredients')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='quantified_ingredients')

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seq_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='steps')

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='ratings')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='ratings')
    comment = db.Column(db.Text, nullable=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_extension = db.Column(db.String(8), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='photos')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='photos')
