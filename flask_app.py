from flask import Flask, render_template, request, redirect, flash
import pymongo, secrets
from pymongo import MongoClient


#initialize the flask app
flask_app = Flask(__name__)

flask_app.secret_key = secrets.token_hex(16)

#connecting to the mongo db
mongo_client=pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["Survey"]
User_input = database["Userinput"]

#routing the app
@flask_app.route('/')
def home():
    return render_template('Survey.html')

@flask_app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
    
            age = int(request.form['age'])
            gender = request.form['gender']
            total_income = request.form['income']
            
            expenses = {}
            expense_categories = {
                'utilities': 'utilities',
                'entertainment': 'entertainment',
                'school_fees': 'school_fees',
                'shopping': 'shopping',
                'healthcare': 'healthcare'
            }
            
            for category, checkbox in expense_categories.items():
                if request.form.get(checkbox): 
                    amount_str = request.form.get(category)
                    if amount_str: 
                        expenses[category] = float(amount_str)
                    else:
                        expenses[category] = 0.0

            # Insert into MongoDBatlas
            Userinput = {
                'age': age,
                'gender': gender,
                'total_income': total_income,
                'expenses': expenses
            }
          

    User_input.insert_one(Userinput)
    
    #flash a success message
    flash('Form submitted successfully!')
    return redirect('/')
    
if __name__ == '__main__':
    flask_app.run(debug=True)   
   