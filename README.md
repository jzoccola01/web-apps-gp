## web-apps-gp
Web Applications Group Project

Uri Kreindler, Alec Morrison, Jonny Zoccola

Universidad Carlos III de Madrid

Fall 2023

# Recipe Roster

![Recipe Roster Logo](/cooking/static/header_logo.png)

## Description

A basic web application for viewing and creating recipes. Detailed functionality further below.

## Installation

1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Modify `__init__.py` onl ine 21 to point to your chosen database
4. If desired, run `setup.py` and `populate_db.py` to generate some test data
5. Run the app with `flask --app=cooking run`

## Functionality (Mandatory + Additional)

- [x] User accounts
    - Account Creation
    - Login
    - Logout
    - Error handling
    - Cryptographically secure password storage
    - Detailed user profile page
- [x] Recipe Creation
    - Logged in users can create new recipes
    - Recipes have a title, description, list of quantified ingredients, list of steps, serving size, cook time, category, and images (optional)
- [x] Reading Recipes
    - Recipes can be viewed by anyone
    - Recipes can be filtered by category
    - Recipes can be sorted by rating, number of reviews, and recency
    - Global searchbar allows for searching based on title, description, category, creator, and ingredients
- [x] Rating Recipes
    - Logged in users can rate recipes
    - Users can only rate a recipe once
    - Users have the option to leave a written review when rating
    - Users have the option to include an image with their review
    - Users can edit their existing reviews
    - Users can delete their existing reviews
- [x] Bookmarking Recipes
    - Logged in users can bookmark recipes
    - Users can remove a recipe from their bookmarks
    - Users can view their bookmarked recipes on their profile page
- [x] Uploading Photos
    - Logged in users can upload photos, either when creating a recipe or when leaving a review
    - Users can view their uploaded photos on their profile page

## Additional Functionality

- [x] Recipe Filtering
    - Recipes can be filtered by category
    - Category is selected when creating a recipe
    - Can be used in conjunction with sorting
- [x] Recipe Sorting
    - Recipes can be sorted by rating, number of reviews, and recency
    - Can be used in conjunction with filtering
- [x] Global Searchbar
    - Allows for searching based on title, description, category, creator, and ingredients
    - Can be used in conjunction with filtering and sorting
- [x] Written Reviews
    - Users have the option to leave a written review when rating
    - Users can edit their existing reviews
    - Users can delete their existing reviews
- [x] Login/Signup Overlay
    - Login and signup are handled in a modal overlay using JavaScript
- [x] JavaScript for Recipe Creation
    - Used to dynamically add and remove ingredients and steps
- [x] Brilliant UI
    - The UI is beautiful and intuitive
    - The UI is responsive
    - The UI is consistent
- [x] Ability to Upload Photos During Recipe Creation
    - Optional field when creating a recipe