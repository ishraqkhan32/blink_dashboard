from app import db, Branch, Address, Capacity
from BlinkParser import BlinkParser
  
# clear tables if starting from scratch 
def refresh_tables():
    db.drop_all()
    db.create_all()
    
# adds and commits python objects mapped using ORM to SQLAlchemy database
def add_and_commit_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()

# store branch info dictionaries into db 
# parser.branch_info should have been populated prior using parser.parse() 
def main(parser):
    
    for branch in parser.branch_info:
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
        
# scrape capacity data from individual branch pages and store into database
def capacity(parser):
    capacities = parser.parse_capacity()
    
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
