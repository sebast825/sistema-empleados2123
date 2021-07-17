
import re
from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from datetime import datetime

from pymysql import cursors

app= Flask(__name__)
#asdasdasdasdasfsdf
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema2123'
mysql.init_app(app)


@app.route('/')
def index():
    sql="SELECT * FROM `empleados`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    empleados = cursor.fetchall()#te trae todo
    
    
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/create')#PARA QUE AL PONER /CREATE TE REDIRIJA A LA CARPETA CREATE.HTML
def create():
   return render_template("empleados/create.html")

#para eliminar datos
@app.route('/destroy/<int:id>')#le estas diciendo que recibis un id
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect("/")

#para editar datos
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados = cursor.fetchall()
    conn.commit()
    return render_template("empleados/edit.html",empleados=empleados)

@app.route('/update', methods=["POST"])
def update():
    _nombre = request.form["txtNombre"]
    _correo = request.form["txtCorreo"]
    _foto = request.files["txtFoto"]
    id = request.form["txtId"]

    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s"
    datos=(_nombre, _correo, id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect("/")




@app.route('/store', methods=["POST"])#VIENE CON EL METODO POST
def storage():
    _nombre=request.form["txtNombre"]#se le pone el name que esta en create.html
    _correo=request.form["txtCorreo"]
    _foto=request.files["txtFoto"]

    #verificacion de foto
    #PARA QUE todas sean distintas se verifican con fecha y hora
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")#AÑO,HORA,MES,SEGUNDO

    #para verificar que haya foto,si no te rompe todo cuando le quiere unir la fecha y hora
    if _foto.filename!="":
        nuevoNombreFoto=tiempo+ _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)




    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL,%s,%s,%s);"
    datos=(_nombre, _correo, nuevoNombreFoto)

    conn=mysql.connect()#para conectar a mysql
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template("empleados/index.html")


if __name__=='__main__':
    app.run(debug=True)