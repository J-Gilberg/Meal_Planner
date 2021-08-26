from flask_app import app
from flask_app.models import user, recipe, diet, cuisine, meal_type, schedule
from datetime import date, datetime, timedelta
from flask import render_template, redirect, request, session, flash


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    # if not user_schedule or len(user_schedule) == 0: # if the user schedule is blank we need to have a startup sequence
    #     return redirect('/dashboard/start_up')
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
def view_schedule():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    today = date.today()
    # weekstart = date.today() - timedelta(days=today)
    # print(weekstart)
    user_schedule = schedule.Schedule.get_user_schedule({'user_id': session['user_id']
    ,'start_date': today})
    print(user_schedule)
    if not user_schedule or len(user_schedule) == 0:
        return redirect('/dashboard/add_schedule')
    meal_types = meal_type.Meal_type.get_all_meal_types()
    print(user_schedule)
    return render_template('schedule.html', user_schedule = user_schedule, meal_types = meal_types)



    
@app.route('/dashboard/add_schedule')
def add_new_week():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    today = date.today()
    today_weekday = today.weekday()
    # weekstart = date.today() - timedelta(days=today)
    print(request.form)
    if len(request.form) == 0:
        for day in range(7):
            day_interval = timedelta(days=day)
            data = {
                'user_id': session['user_id']
                ,'date': today + day_interval
                ,'prep_time': '1 hr'
                ,'meal_type_id': '3'
            }
            # ,'weekday': (weekstart + day_interval).weekday() 
            schedule.Schedule.add_schedule(data)
    else:
        day_interval = timedelta(days=1)

    return redirect('/dashboard/schedule')

@app.route('/dashboard/edit_schedule', methods=['POST'])
def edit_schedule():
    schedule.Schedule.edit_schedule()
    return redirect('/dashboard/schedule')

@app.route('/dashboard/meal_preference')
def meal_preference():
    if not 'user_id' in session:
        flash('Please log in to view this page')
        return redirect('/')
    cuisines = cuisine.Cuisine.get_all_cuisine()
    diets = diet.Diet.get_all_diets()
    return render_template('meal_preferences.html', cuisines = cuisines, diets = diets)
    
