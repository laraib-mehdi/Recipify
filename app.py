from flask import Flask, render_template, request, redirect,g, session
import sqlite3
from flask_session import Session
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
DATABASE = 'recipes.db'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def apology(message, code=400):
    """Render message as an apology to user."""
    from flask import render_template
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

@app.route('/')
@login_required
def home():
    user = session["user_id"]
    db = get_db()
    cursor = db.cursor()
    rows = db.execute("select * from recipes;")
    return render_template("home.html",rows=rows)




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        pw1 = request.form.get("password")
        pw2 = request.form.get("re-password")
        if not name or not pw1 or not pw2:
            return apology("missing username and/or password!")
        if pw1 != pw2:
            return apology("passwords don't match")
        db = get_db()
        if db.execute("SELECT * FROM users WHERE username = ?", (name,)).fetchone():
            return apology("user exists!")
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, pw1))
        db.commit()
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        username = request.form.get("username")
        db = get_db()
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        # Ensure username exists and password is correct
        if rows is None or not request.form.get("password") == rows[2]:
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')
@login_required
@app.route('/new_recipe', methods=['GET', 'POST'])
def add_recipe():
    db = get_db()  # Connect to the database
    cursor = db.cursor()
    if request.method == 'POST':
        # Retrieve form data
        user_id = session.get('user_id')
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        steps = request.form.getlist('steps')
        ingredients = request.form.getlist('ingredients')

        # Insert the recipe into the recipes table
        cursor.execute("INSERT INTO recipes (name, description, category, user_id) VALUES (?, ?, ?,?)", (name, description, category, user_id))
        recipe_id = cursor.lastrowid

        steps = []
        i = 0
        j = 0
        # Iterate over the form data
        while f"steps[{i}]" in request.form:
            step = request.form[f"steps[{i}]"]
            steps.append(step)
            i += 1
        while f"ingredients[{j}]" in request.form:
            ingredient = request.form[f"ingredients[{j}]"]
            ingredients.append(ingredient)
            j +=1


        # Insert steps
        for index, step in enumerate(steps, start=1):
            cursor.execute("INSERT INTO steps (recipe_id, step_number, step_text) VALUES (?, ?, ?)",(recipe_id, index, step))

        # Insert ingredients
        for index, ingredient in enumerate(ingredients, start=1):
            cursor.execute("INSERT INTO ingredients (recipe_id, ingredient_number, ingredient_text) VALUES (?, ?, ?)",(recipe_id, index, ingredient))

        db.commit()

        return redirect('/')
    return render_template('new_recipe.html')

@login_required
@app.route('/view_recipe')
def view_recipe():
    db = get_db()
    cursor = db.cursor()

    # Fetch the names of all recipes from the database
    recipes = cursor.execute("SELECT distinct category FROM recipes")
    return render_template('view_recipe.html', recipes=recipes)

@app.route('/recipes')
def recipes():
    selected_category = request.args.get('category')

    db = get_db()
    cursor = db.cursor()

    # Perform SQL query to fetch recipes based on the selected category
    recipes = cursor.execute("SELECT name,category,description FROM recipes WHERE category = ?", (selected_category,)).fetchall()

    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe_details', methods=['GET'])
def recipe_details():
    db = get_db()
    cursor = db.cursor()
    # Get the name parameter from the query string
    recipe_name = request.args.get('name')

    # Retrieve the recipe details from the database
    cursor.execute("SELECT * FROM recipes WHERE name = ?", (recipe_name,))
    recipe = cursor.fetchone()

    # Retrieve the ingredients for the recipe
    cursor.execute("SELECT ingredient_text FROM ingredients WHERE recipe_id = ?", (recipe[0],))
    ingredients = cursor.fetchall()

    # Retrieve the steps for the recipe
    cursor.execute("SELECT step_number, step_text FROM steps WHERE recipe_id = ?", (recipe[0],))
    steps = cursor.fetchall()

    return render_template('recipe_details.html', recipe=recipe, ingredients=ingredients, steps=steps)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(debug=True)
