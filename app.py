from flask import Flask, render_template , redirect ,session , request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import openai
import pickle
import os
import requests
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(app)

app.secret_key = 'secret_key'

EXCEL_FILE = "Expenses/Feb 25.xlsx"
SHEET_NAME = "Feb 25"

class User(db.Model):
    id = db.Column( db.Integer , primary_key=True )
    email = db.Column( db.String(50) , nullable = False ,unique =True)
    number = db.Column( db.String(10) , nullable = False ,unique =True )
    password = db.Column(db.String(40), nullable=False)
    
    def __init__(self,email,number,password):
        self.email = email
        self.number = number
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
        
    def check_password(self ,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all() 

# Load ML model
MODEL_PATH = "expense_classifier.pkl"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
else:
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    number = request.form['number']
    password = request.form['password']

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return render_template('login.html', error='User already exists')

    # Create new user
    new_user = User(email=email, number=number, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Auto-login after registration
    session['email'] = new_user.email
    return redirect('/transactions')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/transactions')
        else:
            return render_template('login.html', error='Invalid User')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(('/login'))


@app.route("/transactions")
def display_transactions():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        transactions = df.to_dict(orient="records") 
        return render_template("transactions.html", transactions=transactions)
    except Exception as e:
        return f"Error reading transactions: {e}"


@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not found'}), 500
    
    data = request.json.get("features", [])
    prediction = model.predict([data])
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
