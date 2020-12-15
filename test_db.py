from app import db, Branch, Address, Capacity
from BlinkParser import BlinkParser

  
        
def refresh_tables():
    db.drop_all()
    db.create_all()

def main(parser):
    refresh_tables()
    
    for branch in parser.branch_info:
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
        
        db.session.add(new_branch)
        db.session.commit()
        
    return

def capacity(parser):
    capacities = parser.parse_capacity()
    
    for cap in capacities:   
        blink_branch_id = Branch.query.filter(Branch.title == cap['title']).first().id
        
        # raise error if no valid branch 
        if not blink_branch_id:
            print(cap, 'does not exist in database')
            raise NameError('No valid blink branch id for capacity reading')
        
        print(blink_branch_id, cap['status_code'], cap['capacity'])
        
        new_capacity = Capacity(
            branch_id = blink_branch_id,
            status_code = cap['status_code'],
            capacity = cap['capacity']
        )
        
        db.session.add(new_capacity)
        db.session.commit()
    
    return    

if __name__ == '__main__':
    parser = BlinkParser()
    parser.parse()
    
    try:
        main(parser)
        capacity(parser)
    except:
        print('*********************** error parsing')