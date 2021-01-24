from flask import Flask
from extensions import db
        
def create_app(config_path='BLINK_CONFIG_PATH'):
    app = Flask(__name__)
    app.config.from_envvar(config_path)
    register_extensions(app)
    return app
    
def register_extensions(app):
    db.init_app(app)
 
# clear db tables if starting from scratch 
def refresh_db():
    db.drop_all()
    db.create_all()
 
# adds and commits python objects mapped using ORM to SQLAlchemy database
def add_and_commit_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()

app = create_app()

from models import Branch, Address, Capacity

# scrape capacity data from individual branch pages and store into database
def scrape_and_store_capacities(capacities):
    # use application context to avoid circular imports 
    with app.app_context():
        for cap in capacities:   
                # get branch ID from matching branch titles in Branch table and capacity data
                blink_branch_id = Branch.query.filter(Branch.title == cap['title']).first().id
                
                # raise error if no valid branch in Branch table
                if not blink_branch_id:
                    raise NameError('No valid blink branch id for capacity reading')
                
                # store capacity data as SQLAlchemy object
                new_capacity = Capacity(
                    branch_id = blink_branch_id,
                    status_code = cap['status_code'],
                    capacity = cap['capacity'],
                    timestamp = cap['timestamp']
                )
                
                add_and_commit_to_db(new_capacity)
 
# store branch info dictionaries into db 
# branches argument should be retrieved from BlinkParser.parse_branch_info() which stores data into BlinkParser.branch_info attribute
def main(branches):
    with app.app_context():
        for branch in branches:
            # Address data stored using separate db model (tied to Branch) for abstraction
            branch_address = Address(
                state = branch['state'],
                city = branch['city'],
                street = branch['street']
            )
            
            new_branch = Branch(
                title = branch['title'],
                address = branch_address,
                phone = branch['phone'],
                url = branch['url']
            )
            
            add_and_commit_to_db(new_branch)
                            
# query and format the branch data to be displayed by table in jinja template 
def get_branch_data():
    with app.app_context():
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

# queries capacity data and returns as dictionary
def get_capacity_data():
    with app.app_context():
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

