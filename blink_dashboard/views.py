from flask import render_template, jsonify
from app import app, get_branch_data, get_capacity_data

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