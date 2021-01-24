from app import db

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