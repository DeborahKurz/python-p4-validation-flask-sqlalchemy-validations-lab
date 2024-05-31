from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 1:
            raise ValueError("Author must have a name longer than 0 characters") 
        if Author.query.filter_by(name=name).first() is not None:
            raise ValueError("Author's name must be unique")
        return name
    
    @validates('phone_number')
    def validate_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits long")
    
        if not phone_number.isdigit():
            raise ValueError("Phone number must only consist of digits")
        
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if len(title) < 1:
            raise ValueError("Title must be at least 1 character long.") 
        if "Won't Believe" not in title and "Secret" not in title and "Top" not in title and "Guess" not in title:
            raise ValueError("Title must contain clickbait-y words from approved list.")
        
    @validates('content')
    def validate_post(self, key, content):
        if len(content) < 250:
            raise ValueError("Post must be at least 250 characters long.")
        return content
        
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post cannot be over 250 charcters long.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
