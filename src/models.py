from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self, full_name, username, email, password):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    def __init__(self, full_name, climate, terrain, population):
        self.full_name = full_name
        self.climate = climate
        self.terrain = terrain
        self.population = population
    
    def __repr__(self):
        return '<Planet %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    history = db.Column(db.String(250), nullable=False)

    def __init__(self, full_name, hair_color, occupation, history):
        self.full_name = full_name
        self.hair_color = hair_color
        self.occupation = occupation
        self.history = history
    
    def __repr__(self):
        return '<Character %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "hair_color": self.hair_color,
            "occupation": self.occupation,
            "history": self.history,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User data
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(User)

    # Planet favorite
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship(Planet)

    # Character favorite
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    character = db.relationship(Character)

    def to_dict(self):
        return {}

User.favorites = db.relationship(Favorite, backref="user_favorites")