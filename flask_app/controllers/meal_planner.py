from flask_app import app
from flask_app.models import user, recipe, diet, cuisine, meal_type, schedule
from datetime import date
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
    recipes_rand = recipe.Recipe.get_suggestions()
    print(len(recipes))
    return render_template('recipes.html', recipes = recipes, cuisines = cuisines, recipes_rand = recipes_rand)

@app.route('/dashboard/<int:id>')
def view_recipe(id):
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    data = {
        'id':id
    }
    recipes = recipe.Recipe.get_single_recipe(data)
    return render_template('view_recipe.html', recipes = recipes)
    


@app.route('/dashboard/schedule')
def edit_schedule():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    user_schedule = schedule.Schedule.get_user_schedule({'user_id': session['user_id']})
    if not user_schedule or len(user_schedule) == 0:
        return redirect('/dashboard/add_schedule')
    
    return render_template('schedule.html', user_schedule = user_schedule)

    
@app.route('/dashboard/add_schedule', methods=['POST'])
def add_new_schedule():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')

    for day in range(7):
        data = {
            'user_id': session['user_id']
            ,'date': request.form['date']
        }
        schedule.Schedule.add_schedule(data)

    return redirect('/dashboard/schedule')

@app.route('/dashboard/edit_schedule', methods=['POST'])
def edit_schedule1():
    schedule.Schedule.edit_schedule()
    return redirect('/dashboard/schedule')