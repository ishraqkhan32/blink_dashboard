from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

#app.config['SECRET_KEY'] = ''
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:password@blink-1.cgk5wllpkj9i.us-east-1.rds.amazonaws.com:3306/blink'
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

def get_branch_data():
     # query and format the data to be displayed by jinja template
    branches = db.session.query(Branch, Address).join(Address).all()
    
    data = []
    for branch in branches:
        data.append({
            'title': branch.Branch.title,
            'phone': branch.Branch.phone,
            'state': branch.Address.state,
            'region': branch.Address.city,
            'address': branch.Address.street,
            'url': branch.Branch.url
        })
        
    return data

# converts capacity string (parsed from branch homepage) to integer or NULL value
def capacity_to_percent(capacity_str):
    status_to_value = {
        "LESS THAN 25% FULL": 25,
        "ABOUT 50% FULL": 50,
        "ABOUT 75% FULL": 75,
        "AT CAPACITY": 100,
        "": None,
        "CAPACITY DATA UNAVAILABLE": None
    }
    
    return status_to_value[capacity_str]

def get_capacity_data():
    caps = db.session.query(Capacity, Branch).join(Branch).filter(Capacity.capacity != None).all()
    readings = {}

    # map list of queried capacities into dictonary of the form:
    # {
    #   branch_title_1: [(timestamp_1, capacity_1), ... , (timestamp_n, capacity_n)]   
    #   ....
    #   branch_title_n: [(timestamp_1, capacity_1), ... , (timestamp_n, capacity_n)]  
    # }
    for cap in caps:
        branch = f"{cap.Branch.address.state} - {cap.Branch.title}"
        timestamp = cap.Capacity.timestamp
        capacity = capacity_to_percent(cap.Capacity.capacity)

        # append capacity to appropriate list if branch already exists 
        if branch in readings.keys():
            readings[branch].append((timestamp, capacity))
        # else create new entry in dictionary
        else:
            readings[branch] = [(timestamp, capacity)]
            
    return readings

@app.route('/')
def home():
    return render_template("home.html", branches=get_branch_data())

# renders page containing table of all gyms + metadata (address, phone, url)
@app.route('/view_branches')
def view_branches():
    return render_template("table.html", branches=get_branch_data())

# renders table showing parsed capacities 
@app.route('/view_capacities')
def view_capacities():
    # time is currently hardcoded for sample presentation (will replace with timestamps once parsing is automated)
    time_headers = ["3:30 PM", "3:45 PM", "4:00 PM", "4:15 PM", "4:30 PM", "4:45 PM", "5:00 PM", "5:15 PM", "5:30 PM", "5:45 PM"]
    return render_template("capacity.html", data=get_capacity_data(), time_headers=time_headers)

@app.route('/api_branches', methods=['GET'])
def get_branches():
    return jsonify(get_branch_data())

@app.route('/api_capacities', methods=['GET'])
def get_capacities():
    return jsonify(get_capacity_data())

if __name__ == "__main__":
    app.run(debug=True)