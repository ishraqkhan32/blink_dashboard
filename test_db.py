from app import db, BlinkBranch
from BlinkParser import BlinkParser

def main():
    # clear database
    db.drop_all()
    db.create_all()
    
    parser = BlinkParser()
    parser.parse()
    
    for branch in parser.location_info:
        new_branch = BlinkBranch(
            title = branch['title'],
            status = branch['status'],
            state = branch['state'],
            city = branch['city'],
            address = branch['address'],
            phone = branch['phone'],
            url = branch['url']
        )
        
        db.session.add(new_branch)
        db.session.commit()

if __name__ == '__main__':
    main()
    