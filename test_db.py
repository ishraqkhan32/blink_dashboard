from app import db, Branch, Address
from BlinkParser import BlinkParser

def main():
    # clear database
    db.drop_all()
    db.create_all()
    
    parser = BlinkParser()
    parser.parse()
    
    for branch in parser.branch_info:
        branch_address = Address(
            state = branch['state'],
            city = branch['city'],
            street = branch['street']
        )
        
        new_branch = Branch(
            title = branch['title'],
            status = branch['status'],
            address = branch_address,
            phone = branch['phone'],
            url = branch['url']
        )
        
        db.session.add(new_branch)
        db.session.commit()

if __name__ == '__main__':
    main()
    