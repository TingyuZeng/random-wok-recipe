import re
from random import randrange

from functools import wraps
from flask import session, request, redirect, url_for

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from model import Type, Style, Ingredient, Method

# SQLAlchemy configuration
engine = create_engine("sqlite:///recipes.db")
Base = automap_base()
Base.prepare(autoload_with=engine)
db = Session(engine)

# Constant variables
TYPES = {}
for (a, b) in db.query(Type.type, func.count(Type.ingredients)).\
                            join(Ingredient.type).\
                            group_by(Type.id).\
                            all():
    TYPES[a] = b

db.close()

# Admin requirs login
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None: #Only super admin can access
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Functions to get the index number within the working range
def random_ingredient(num, type):
    '''Translate the random integer to be an integer within the range of ingredients.\n
    It takes two arguments, an integer and the type name of the ingredient.'''
    if type in TYPES:
        return round(num) % (TYPES[type]) 
    else:
        return -1


def random_style(type):
    '''Generate an index number for a random cooking style.\n
    It takes the name of the ingredient type and returns an integer.'''
    db = Session(engine)
    if type in TYPES:
        try:
            methods = db.query(Method).join(Method.type).filter(Type.type == type).all()
            index = randrange(0, len(methods))
            db.close()
            return methods[index].style_id
        except: 
            db.close()
            return -3
            

# Translate the index to get the ingredients
def get_ingredients(dict):
    '''Translate the numbers passed by JS to ingredients.\n
    The function takes an argument of dictionary, the one parsed from JSON.\n
    Its keys should be the names of ingredients' types.\n
    It returns a dictionary (key=type, value=ingredient)'''
    
    db = Session(engine)

    new_dict = {}
    
    for key, value in dict.items():
        value = random_ingredient(value, key)
        if value == -1:
            return -1
    
        # Query the DB
        try:
            ingredient = db.query(Ingredient).\
                            join(Ingredient.type).\
                            filter(Type.type == key)\
                            [value]

            # if there is a repeated ingredient, generate a new random one
            while ingredient.name in new_dict.values():
                
                length = db.query(Ingredient).\
                            join(Ingredient.type).\
                            filter(Type.type == key).\
                            count()
                value = randrange(0, length)
                ingredient = db.query(Ingredient).\
                            join(Ingredient.type).\
                            filter(Type.type == key)\
                            [value]

            new_dict[key] = ingredient.name
            db.close()
        except:
            db.close()
            return -2

    return new_dict


# Get a random cooking method
def get_methods(dict):
    '''Generate instructions for each ingredients in the dictionary.\n
    It returns a dictionary (key=type, value=instruction)'''

    db = Session(engine)
    new_dict = {}

    for key, value in dict.items():
        random_style_id = random_style(key)
        if random_style_id == -1:
            return -3
        
        # Query the DB
        try:
            methods = db.query(Method).\
                        join(Method.type).\
                        filter(Method.style_id == random_style_id).\
                        filter(Type.type == key).\
                        all()
            index = randrange(0, len(methods))
            instruction = methods[index].instruction
            new_dict[key] = instruction
        except:
            db.close()
            return -4
    
    db.close()

    return new_dict


def get_recipe(dict_i, dict_m):
    '''Replace the placeholders in the instruction with the ingredient names.\n
    Returns a dict where each value is a list [ingredient name, instruction]'''

    new_dict = {}

    for mkey in dict_m:
        
        new_dict[mkey] = []
        new_dict[mkey].append(dict_i[mkey])

        instruction = dict_m[mkey]
        matches = re.findall(r'::[a-zA-Z]+::', instruction)

        for match in matches:
            ikey = re.sub(r"::", "", match)
            instruction = re.sub(match, dict_i[ikey], instruction)
        
        new_dict[mkey].append(instruction)

    return new_dict


def password_check(psw):
    """ Require users’ passwords to have some number of letters and numbers, and more than 6 chars"""

    if len(psw) >= 6:
        alpha = 0
        digit = 0

        # Counting
        for i in psw:
            if i.isalpha():
                alpha += 1
            elif i.isdigit():
                digit += 1

        # Condition
        if alpha >= 1 and digit >= 1:
            return True
        else:
            return False

    else:
        return False
