from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['ENV'] = 'development'
#app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database setup
db = SQLAlchemy(app)

class BlinkBranch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.String(30))
    
    # TODO: abstract address into separate DB table
    state = db.Column(db.String(2), nullable=False) # TODO: make this limited to state abbreviations
    city = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(100), unique=True, nullable=False)
    
    phone = db.Column(db.String(12), unique=True, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"{self.state} - {self.title.title()}"