from flask_app import app
from flask_app.models import user, recipe, diet, cuisine, meal_type, schedule
from flask import render_template, redirect, request, session, flash


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/dashboard/add_recipe')
def add_recipe():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')

    meal_types = meal_type.Meal_type.get_all_meal_types()
    cuisines = cuisine.Cuisine.get_all_cuisine()
    diets = diet.Diet.get_all_diets()
    return render_template('add_recipe.html', meal_types = meal_types, cuisines = cuisines, diets = diets)

@app.route('/dashboard/create_recipe', methods=['POST'])
def create_recipe():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    if not recipe.Recipe.recipe_validator(request.form):
        return redirect('/dashboard/add_recipe')
    recipe.Recipe.create_recipe(request.form)
    return redirect('/dashboard')

@app.route('/dashboard/recipes')
def recipes():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    recipes = recipe.Recipe.get_recipes()
    cuisines = cuisine.Cuisine.get_all_cuisine()
    print(len(recipes))
    return render_template('recipes.html', recipes = recipes, cuisines = cuisines)

@app.route('/dashboard/<int:id>')
def view_recipe(id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    


@app.route('/dashboard/schedule')
def schedule():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    
    return render_template('schedule.html')

    
@app.route('/dashboard/add_schedule', methods=['POST'])
def add_schedule():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    data = {
        
    }
    schedule.Schedule.add_schedule(data)

    return redirect('/dashboard/schedule')
