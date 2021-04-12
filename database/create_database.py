from pathlib import Path
import csv, sys

from sqlalchemy import create_engine, func
from sqlalchemy.orm import relationship, Session

# import all Tables from model.py
sys.path.append('..')
from model import Base, Type, Style, Ingredient, Method

# target_file path 
curdir = Path.cwd()
target_file = curdir.parent / 'recipes.db'
# Empty/Create the target database as preparation
open(target_file, 'w').close()
# 2 csv file paths
file_ingredients = curdir / 'ingredients - ingredients.csv'
file_methods = curdir / 'ingredients - methods.csv'

# SQLAlchemy configuration
engine = create_engine("sqlite:///" + str(target_file))
db = Session(engine)

Base.metadata.create_all(engine)

# Recording data into the Tables
with open(file_ingredients, 'r') as file:
    reader = csv.DictReader(file)
    
    # Insert records into Type
    types = reader.fieldnames[1:]
    types_dict = {}
    for item in types:
        types_dict[item] = Type(type=item)
        db.add(types_dict[item])
    db.commit()

    # Insert records into Ingredient
    for row in reader:
        for type in types:
            if row[type] == "TRUE":
                ingredient = Ingredient(name=row['name'])
                ingredient.type = types_dict[type]
                db.add(ingredient)
                db.commit()


with open(file_methods, 'r') as file:
    reader = list(csv.DictReader(file))
    
    # Insert records into Style
    styles = set()
    for row in reader:
        styles.add(row['style'])
    styles_dict = {}
    for item in styles:
        styles_dict[item] = Style(style=item)
        db.add(styles_dict[item])
    db.commit()

    # Insert records into Method
    for row in reader:
        method = Method(instruction=row['instruction'])
        method.type = types_dict[row['type']]
        method.style = styles_dict[row['style']]
        db.add(method)
        db.commit()


db.close()