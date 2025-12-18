from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy(app)

class Paquete(db.Model):
    __tablename__='paquete'
    id = db.Column(db.Integer, primary_key=True)
    numeroenvio = db.Column(db.Integer, unique=False, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    nomdestinatario=db.Column(db.String(150),nullable=False)
    dirdestinatario=db.Column(db.String(150),nullable=False)
    entregado=db.Column(db.Boolean)
    observaciones=db.Column(db.String(150))#no pongo nullable porque es posible que quede en null
    idsucursal=db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    idtransporte=db.Column(db.Integer, db.ForeignKey('transporte.id'))
    idrepartidor=db.Column(db.Integer, db.ForeignKey('repartidor.id'))

class Transporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numerotransporte = db.Column(db.Integer, unique=False, nullable=False)
    fechahorasalida = db.Column(db.DateTime)
    fechahorallegada = db.Column(db.DateTime)
    idsucursal=db.Column(db.Integer, db.ForeignKey('sucursal.id'))

class Repartidor(db.Model):
    __tablename__='repartidor'
    id = db.Column(db.Integer, primary_key=True)
    numero=db.Column(db.Integer, unique=False, nullable=False)
    nombre=db.Column(db.String(100),nullable=False)
    dni=db.Column(db.Integer, nullable=False)
    idsucursal=db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    
    def __repr__(self):
        return f"numero : {self.numero}, DNI: {self.dni}"

class Sucursal(db.Model):
    __tablename__='sucursal'
    id = db.Column(db.Integer, primary_key=True)
    numero=db.Column(db.Integer, unique=False, nullable=False)
    provincia=db.Column(db.String(100),nullable=False)
    localidad=db.Column(db.String(100),nullable=False)
    direccion=db.Column(db.String(150),nullable=False)
    # id_repartidor=db.relationship('Repartidor', backref='sucursal')

    def __repr__(self):
        return f"N°{self.numero} {self.provincia}, {self.localidad}"