from flask import Flask, request, redirect, url_for, session
from flask.templating import render_template
from sqlalchemy import func
from datetime import datetime

import os
app = Flask(__name__)
app.debug = True

app.config.from_pyfile('config.py')
IMG_FOLDER=os.path.join("static", "img")
app.config["UPLOAD_FOLDER"] = IMG_FOLDER

from models import db
from models import Repartidor, Sucursal, Paquete, Transporte

# @app.route('/')
# def index():
#     sucursal = Sucursal.query.all()
#     repartidor = Repartidor.query.all()
#     transporte=Transporte.query.all()
#     paquete=Paquete.query.all()
#     return render_template('index.html', sucursal=sucursal, repartidor=repartidor, transporte=transporte, paquete=paquete)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_paquete', methods=['POST','GET'])
def agregar_paquete():
    if request.method=='POST':
        if not request.form['destino'] or not request.form['destinatario'] or not request.form['peso']:
            return render_template('cargar_paquete.html',msj='Error al cargar',idsucu=session['numero_actual'])
        else:
            destino = request.form.get("destino")
            destinatario = request.form.get("destinatario")
            peso = request.form.get("peso")
            max_numeroenvio = db.session.query(func.max(Paquete.numeroenvio)).scalar()
            if max_numeroenvio is None:
                max_numeroenvio = 0  # Si no hay registros, empezamos desde 0
            numeroenvio = max_numeroenvio + 1
            p = Paquete(numeroenvio=numeroenvio,peso=peso,nomdestinatario=destinatario,dirdestinatario=destino,entregado=False,observaciones='',idsucursal=session['numero_actual'],idtransporte=0,idrepartidor=0)
            db.session.add(p)
            db.session.commit()
            return render_template('cargar_paquete.html',msj='Cargado con Exito',idsucu=session['numero_actual'])
    else:
        return render_template('cargar_paquete.html',idsucu=session['numero_actual'])
        


@app.route('/despachante', methods=['POST','GET'])
def despachante():
    sucursales=Sucursal.query.order_by(Sucursal.numero).all()
    if request.method=='POST':
        id=request.form['sucursales']
        if id != '0':
            return redirect(url_for('opcionesdespachante',id=id))
        else:
            return render_template('eleccion_sucursal.html', listasucursales=sucursales)
    else:
        return render_template('eleccion_sucursal.html', listasucursales=sucursales)



@app.route('/opcionesdespachante/<int:id>')
def opcionesdespachante(id):
    session['numero_actual']=id
    sucursal=Sucursal.query.get(id)
    return render_template('opciones_despachante.html', sucursal=sucursal)


@app.route('/salida_transporte',methods=['POST','GET'])
def salida_transporte():
    filas_con_nulos = db.session.query(Paquete).\
    filter(Paquete.idrepartidor == 0).\
    filter(Paquete.entregado == 0).\
    all()
    sucursales=Sucursal.query.order_by(Sucursal.numero).all()
    if request.method=='POST':
        paquetes=request.form.getlist('paquetes[]')
        id=request.form.get('sucursales')
        if id != '0' and paquetes!=[]:
            for i in range(len(paquetes)):
                    datar = Paquete.query.get(paquetes[i])
                    datar.idsucursal=id
                    db.session.add(datar)
                    db.session.commit()
            max_numerotransporte = db.session.query(func.max(Transporte.numerotransporte)).scalar()
            if max_numerotransporte is None:
                max_numerotransporte = 0  # Si no hay registros, empezamos desde 0
            numerotransporte = max_numerotransporte + 1
            p = Transporte(numerotransporte=numerotransporte,fechahorasalida=datetime.now(),fechahorallegada=None,idsucursal=id)
            db.session.add(p)
            db.session.commit()
            return render_template('msj_transporte.html',msjexito='Cargado con Exito')
        else:
            return render_template('opcion_salida_transporte.html',paquetesnoentregado=filas_con_nulos,listasucursales=sucursales,msjerror='Error al cargar')
    else:
        return render_template('opcion_salida_transporte.html',paquetesnoentregado=filas_con_nulos,listasucursales=sucursales)
        

@app.route('/llegada_transporte', methods=['POST','GET'])
def llegada_transporte():
    llegadatransporte = db.session.query(Transporte).\
    filter(Transporte.fechahorallegada == None).\
    filter(Transporte.idsucursal == session['numero_actual']).\
    all()
    if request.method=='POST':
        llegada_tran=request.form.getlist('llegada[]')
        id=request.form.get('sucursales')
        if id != '0' and llegada_tran!=[]:
            for i in range(len(llegada_tran)):
                    datar = Transporte.query.get(llegada_tran[i])
                    datar.fechahorallegada=datetime.now()
                    db.session.add(datar)
                    db.session.commit()
                    return render_template('msj_transporte.html',msjexito='Carga Exitosa')
        else:
            return render_template('llegada_transporte.html',llegadatransporte=llegadatransporte,msjerror='Error al Cargar')
    else:
        return render_template('llegada_transporte.html',llegadatransporte=llegadatransporte)
    

@app.route('/actualizardato/<int:id>')
def actualizardato(id):
    datar = Transporte.query.get(id)
    datar.numerotransporte=datetime.now()
    db.session.add(datar)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def deleteSucursal(id):
    data = Sucursal.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

@app.route('/deleterepartidor/<int:id>')
def deleteRepartidor(id):
    datar = Repartidor.query.get(id)
    db.session.delete(datar)
    db.session.commit()
    return redirect('/')

@app.route('/deletepaquete/<int:id>')
def deletepaquete(id):
    datar = Paquete.query.get(id)
    db.session.delete(datar)
    db.session.commit()
    return redirect('/')


@app.route('/deletetransporte/<int:id>')
def deletetransporte(id):
    dataT = Transporte.query.get(id)
    db.session.delete(dataT)
    db.session.commit()
    return redirect('/')
if __name__ == '__main__':
    app.run()
