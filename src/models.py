from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    fecha_subscripcion = db.Column(db.DateTime, nullable=False)
    favoritos = db.relationship('Favorito', back_populates='usuario')
    def __repr__(self):
        return '<Usuario %r>' % self.email
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_subscripcion": self.fecha_subscripcion
        }

class Planeta(db.Model):
    __tablename__ = 'planeta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    clima = db.Column(db.String, nullable=True)
    terreno = db.Column(db.String, nullable=True)
    favoritos = db.relationship('Favorito', back_populates='planeta')
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "clima": self.clima,
            "terreno": self.terreno
        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    especie = db.Column(db.String, nullable=True)
    afiliacion = db.Column(db.String, nullable=True)
    favoritos = db.relationship('Favorito', back_populates='personaje')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "especie": self.especie,
            "afiliacion": self.afiliacion
        }
    
class Favorito(db.Model):
    __tablename__ = 'favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'), nullable=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=True)

    usuario = db.relationship('Usuario', back_populates='favoritos')
    planeta = db.relationship('Planeta', back_populates='favoritos')
    personaje = db.relationship('Personaje', back_populates='favoritos')

    def __repr__(self):
        return '<Favorito %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id
        }
