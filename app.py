from flask import Flask, render_template, request, redirect, jsonify, make_response, session, flash, url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import BooleanField, StringField, PasswordField, SelectMultipleField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, DataRequired

from sqlalchemy.orm import Session as sa_Session
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from helper import get_ingredients, get_methods, get_recipe, login_required
from model import Admin, Ingredient, Method, Type

import json

# Flask configuration
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# SQLAlchemy configuration
engine_admin = create_engine('sqlite:///admin.db')
engine_recipe = create_engine('sqlite:///recipes.db')
db1 = sa_Session(engine_admin)
db2 = sa_Session(engine_recipe)
Base1 = automap_base()
Base2 = automap_base()
Base1.prepare(autoload_with=engine_admin)
Base2.prepare(autoload_with=engine_recipe)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/get-a-recipe', methods=['POST'])
def get_a_recipe():

    if request.is_json:
        req = request.get_json()
        print(req)

        try:
            res = get_recipe(get_ingredients(req), get_methods(req))
            print(res)
            res = make_response(jsonify(res), 200)
            return res
        except:
            error = {
            "message": "Invalid input, please try again"
            }
            print(error)
            return make_response(jsonify(error), 400)
        
    else:
        error = {
            "message": "Cannot connect to the database, please try again"
        }
        print(error)
        return make_response(jsonify(error), 400)


@app.route('/ingredients', methods=['POST', 'GET'])
@login_required
def ingredients():
    # Query the ingredients data
    ingredients = db2.query(Ingredient).all()
    # Generate form to add ingredients
    form = IngredientForm(request.form)

    if form.validate_on_submit():
        new_ingredient = Ingredient(name=form.ingredient.data.strip().lower())
        new_ingredient.type = db2.query(Type).filter(Type.type == form.type.data).one()
        db2.add(new_ingredient)
        db2.commit()
        flash(('Successfully added ' + form.ingredient.data.strip().lower()), "success")
        return redirect(url_for('ingredients'))

    return render_template("ingredients.html", ingredients=ingredients, form=form)


@app.route('/ingredients/delete/<int:id>')
@login_required
def delete(id):
    try:
        ingredient_to_delete = db2.query(Ingredient).filter(Ingredient.id == id).one()
        name = ingredient_to_delete.name
        db2.delete(ingredient_to_delete)
        db2.commit()
        flash(("Successfully deleted " + name), "success")
    except:
        flash("Cannot delete this ingredient", "warning")
    return redirect(url_for('ingredients'))


@app.route('/ingredients/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    try:
        ingredient = db2.query(Ingredient).filter(Ingredient.id == id).one()
    except:
        flash("Cannot access this ingredient!", "warning")
        return redirect(url_for("ingredients"))
    
    form = IngredientForm(request.form)
    
    if form.validate_on_submit():
        
        try:
            ingredient.name = form.ingredient.data
            ingredient_type = db2.query(Type).filter(Type.type == form.type.data).one()
            ingredient.type = ingredient_type
            db2.commit()
        except:
            flash("Cannot modify this ingredient!", "warning")
        return redirect(url_for('ingredients'))

    return render_template("update.html", ingredient=ingredient, form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''Log admin in'''

    session.clear()
    form = AdminLoginForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
            
        # Check with DB
        admins = db1.query(Admin).all()
        
        for admin in admins:
            if admin.username == username and check_password_hash(admin.hashed_password, password):
                session["user_id"] = admin.id
                session["username"] = admin.username
                return redirect(url_for('ingredients'))
            
            else:
                flash('Access denied', category='warning')
                return redirect(url_for('login'))
    
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))


# Form class - add an ingredient
class IngredientForm(FlaskForm):
    ingredient = StringField('Ingredient Name', \
                            validators=[DataRequired(message="Ingredient Name required!"), \
                                        Length(min=1, max=50, message="Must be short than 50 characters")], \
                            render_kw={"placeholder": "Enter ingredient name..."}
    )
    type = SelectField('Type', \
                        choices=[('carbohydrate', 'carbohydrate'), \
                                ('protein', 'protein'), \
                                ('side', 'side'), \
                                ('sauce', 'sauce'), \
                                ('herb', 'herb')], \
                        validate_choice=True
    )


# Form class - admin login
class AdminLoginForm(FlaskForm):
    username = StringField('Username', \
                            validators=[DataRequired(message="Username required")], \
                            render_kw={"placeholder": "Enter username"}
    )
    password = PasswordField('Password', \
                            validators=[DataRequired(message="Password required")], \
                            render_kw={"placeholder": "Enter password"}
    )

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template('error.html', error_name = e.name, error_code = e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(debug=True)