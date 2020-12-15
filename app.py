from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['ENV'] = 'development'
#app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database setup
db = SQLAlchemy(app)

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    address = db.relationship('Address', backref='branch', lazy=True, uselist=False)
    
    def __repr__(self):
        return f"Branch: {self.title.title()}"
    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    state = db.Column(db.String(2), nullable=False) # TODO: make this limited to state abbreviations
    city = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"Address: {self.street}, {self.city}, {self.state}"
    
class Capacity(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    capacity = db.Column(db.String(100))
    status_code = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

@app.route('/')
def home():
    # query and format the data to be displayed by jinja template
    branches = db.session.query(Branch, Address).join(Address).all()
    
    data = []
    for branch in branches:
        data.append({
            'title': branch.Branch.title,
            'phone': branch.Branch.phone,
            'state': branch.Address.state,
            'address': branch.Address.street,
            'url': branch.Branch.url
        })
        
    # render base.html (parent template) with branches data loaded into bootstrap table
    return render_template("base.html", branches=data)

@app.route('/view_branches')
def view_branches():
    # TODO: grab the data as a object that can be parsed by jinja
    branches = db.session.query(Branch, Address).join(Address).all()
    
    data = []
    for branch in branches:
        data.append({
            'title': branch.Branch.title,
            'phone': branch.Branch.phone,
            'state': branch.Address.state,
            'address': branch.Address.street,
            'url': branch.Branch.url
        })
        
    # TODO: pass object into response
    return render_template("base.html", branches=data)

if __name__ == "__main__":
    app.run(debug=True)