from app import db

class result(db.Model):
    """result is a class that will be used to represent a single search result based on the imdbID as obtained by OMDB api JSON data"""
    imdbID = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(200), index=True, unique=True)
    year = db.Column(db.String(4), index=True, unique=True)

    def __repr__(self):
        return '<imdbID {}>'.format(self.imdbID)
