# Random Wok Recipe
#### beta 0.1 (20210412)
#### Author: Tingyu Zeng (github: tienuur)
#### Video Demo:  https://youtu.be/Kc03eNIUNiM
#### Application Demo: https://random-wok-recipe.herokuapp.com/
#### Description:
This is a flask web application which generates random wok recipe. It contains two parts: the landing page for the user to get inspired and the admin page for the super admin to manage the ingredients from the front end.
#### :shallow_pan_of_food: Recipe Generator
The cooking ingredients are labeled with one or more of 5 categories. The random wok recipe generator selects one ingredient from each category and pairs it with a random cooking method.
The ingredient table and the method table are managed individually, therefore the generated recipe is fun, unpredictable and can be challenging.
The user requests a recipe by pressing the lucky button, which generates five random index number and sends them to the server. The server operates on the request and returns a response with ingredient name and cooking instruction. The UI is updated as soon as the data arrives.
#### :potato: Database Management
There are two ways to manage the database.
1. Via front-end CMS
   This is recommended for admins to update the ingredients in the databse. The admin can access the management console via /login or /ingredients. Currently it is not possible to register as a admin from the front end, to avoid intended harm on the database.
   However, via this way can the admin only update, add or delete ingredients.
2. Via SQLALchemy from back-end
   The file "create-databse.py" in the "database" directory can be used to modify the database. It requires the admin to provide two csv files: one for ingredients and the other cooking methods. The templates of csv files are provides, as well as a template of Google sheet to generate these two csv files.
   After running the python file, the database will be updated.
#### :cook: Admin
If you create a copy of this repo, you can add yourself as a super admin by accessing the file "admin.py". The file will help you to register as an admin. 
Please note the password needs to be longer than 6 charaters and it needs to contain at least one digit and one letter. Your password will be hashed and stored into the "admin.db".
#### :coffee: Future Update Plan
This is the first beta version of the app. Currently I am still working on enriching the database, drawing more graphics and a responsive web design. Please follow me if you would like to know the latest news on the app.