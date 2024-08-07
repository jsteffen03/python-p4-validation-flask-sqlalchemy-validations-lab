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
    @validates('name')
    def validate_name(self, key, value):
        authors = Author.query.all()
        author_name = [author.name for author in authors]
        if value and value not in author_name:
            return value
        else:
            raise ValueError('Name must be unique')
        
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if len(value) == 10 and value.isdigit():
            return value
        else:
            raise ValueError('Phone number must be 10 digits long')


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
            
    @validates("content", "summary")
    def validate_cs(self, key, value):
        if key == "content":
            if len(value) < 250:
                return value
            else:
                raise ValueError('Content must be greater than 250 characters')
        elif key == "summary":
            if len(value) > 250:
                return value
            else:
                raise ValueError('Summary must be less than 250 characters')
            
    @validates("category")
    def validate_category(self, key, value):
        if value in ["Fiction", "Non-Fiction", "Poetry"]:
            return value
        else:
            raise ValueError('Category must be one of: Fiction, Non-Fiction, Poetry')   
        
    @validates("title")
    def validate_title(self, key, value):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        for phrase in clickbait:
            if phrase in value and value:
                return value
            else:
                raise ValueError('Title must contain clickbait')
            

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
