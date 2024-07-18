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

    # Add validators 
    @validates("name")
    def validate_name(self,key,value):
        if not value:
            raise ValueError("Author must have a name")
        elif Author.query.filter_by(name = value).first():
            raise ValueError("Author name taken")
        return value
    
    @validates("phone_number")
    def validate_number(self,key,value):
        digits = 0
        for i in value:
            if i.isdigit():
                digits+=1
        if digits !=  10:
            raise ValueError("Number must be 10 digits")
        return value

   
    

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

    # Add validators  
    @validates("content")
    def validate_content(self,key,value):
        if len(value)<250:
            raise ValueError("Content must be at least 250 characters")
        return value

    @validates("summary")
    def validate_summary(self,key,value):
        if len(value)>250:
            raise ValueError("Summary must have a maximum of 250 characters")
        return value

    @validates("category")
    def validate_category(self,key,value):
        if value not in ["Non-Fiction","Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return value
    
    @validates("title")
    def validate_title(self,key,value):
        if ("Won't Believe" in value) or ("Secret" in value) or ("Top" in value) or ("Guess" in value):
            return value
        else:
            raise ValueError("Must have clickbait-y title")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
