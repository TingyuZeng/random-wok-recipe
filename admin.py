from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.security import generate_password_hash

from helper import password_check
from model import Admin, Base_admin

# SA Configuration
engine = create_engine('sqlite:///admin.db')
db = Session(engine)

Base_admin.metadata.create_all(engine)

# Save Admin info into DB
username = input("Username: ")
admins = db.query(Admin).all()
admin_names = []
for item in admins:
    admin_names.append(item.username)

while username.strip() == "" or username in admin_names:
    username = input("Try another username: ")

password = input("Password: ")
while password.strip() == "" or password_check(password) != True:
    password = input("Try another password: ")

confirm = input("Confirm your password: ")
while confirm.strip() == "" or confirm != password:
    confirm = input("Try again: ")

p_hash = generate_password_hash(password)
new_admin = Admin(username=username, hashed_password=p_hash)
db.add(new_admin)
db.commit()
print("Admin created!")
db.close()
