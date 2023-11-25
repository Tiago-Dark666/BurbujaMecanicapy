from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# Aquí está la corrección: se elimina el espacio adicional antes de "templates"
template_dir = os.path.join(template_dir, 'templates')

app = Flask(__name__, template_folder='templates', static_url_path='/static')



# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

#Ver la tabla usuario
@app.route('/viewUser.html')
def viewUser():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    #Converitr datos a diccionario 
    insertObject = []
    columnNames = [column[0] for column in cursor.description] 
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()    
    return render_template('/viewUser.html', data=insertObject)
#Ver la tabla veterinario
@app.route('/viewMecanico.html')
def viewVet():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM vetuser")
    myresult = cursor.fetchall()
    #Converitr datos a diccionario 
    insertObject = []
    columnNames = [column[0] for column in cursor.description] 
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()    
    return render_template('/viewVet.html', data=insertObject)

#Seleccionar la tabla usuario
@app.route('/registerUser.html')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    #Converitr datos a diccionario 
    insertObject = []
    columnNames = [column[0] for column in cursor.description] 
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()    
    return render_template('/registerUser.html', data=insertObject)

#Seleccionar la tabla vetuser
@app.route('/registerVet.html')
def registerVet():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM vetuser")
    myresult = cursor.fetchall()
    #Converitr datos a diccionario 
    insertObject = []
    columnNames = [column[0] for column in cursor.description] 
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()    
    return render_template('/registerVet.html', data=insertObject)

# Ruta para guardar usuarios en la base de datos
@app.route('/user', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    documento = request.form['documento']
    passw = request.form['pass']
    correo = request.form['correo']
    telefono = request.form['telefono']
    ciudad = request.form['ciudad']

    if nombre and apellido and documento and passw and correo and telefono and ciudad:
        cursor = db.database.cursor()
        sql = "INSERT INTO usuario(nombre,apellido,documento,pass, correo, telefono, ciudad) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (nombre, apellido,documento, passw, correo, telefono, ciudad)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))
# Ruta para guardar veterinarios en la base de datos
@app.route('/vet', methods=['POST'])
def addVet():
    nameVet = request.form['nameVet']
    lastnameVet = request.form['lastnameVet']
    passwordVet = request.form['passwordVet']
    ciudadVet = request.form['ciudadVet']
    especializacionVet = request.form['especializacionVet']
    tienda = request.form['tienda']

    if nameVet and lastnameVet and passwordVet and ciudadVet and especializacionVet and tienda:
        cursor = db.database.cursor()
        sql = "INSERT INTO vetuser(nameVet,lastnameVet,passwordVet,ciudadVet, especializacionVet, tienda) VALUES (%s,%s,%s,%s,%s,%s)"
        data = (nameVet, lastnameVet, passwordVet, ciudadVet,especializacionVet,tienda)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('registerVet'))
#Ruta para borrar un usuario
@app.route('/delete/<int:id_usuario>')
def delete(id_usuario):
    cursor= db.database.cursor()
    sql = "DELETE FROM usuario WHERE id_usuario=%s"
    data = (int(id_usuario),)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#Ruta para borrar un veteriinario
@app.route('/deleteVet/<int:id_vet>')
def deleteVet(id_vet):
    cursor= db.database.cursor()
    sql = "DELETE FROM vetuser WHERE id_vet=%s"
    data = (int(id_vet),)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('registerVet'))


#Ruta para editar usuarios
@app.route('/edit/<int:id_usuario>', methods=['POST'])
def edit (id_usuario):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    documento = request.form['documento']
    passw = request.form['pass']
    correo = request.form['coreo']
    telefono = request.form['telefono']
    ciudad = request.form['ciudad']

    if nombre and apellido and documento and passw and correo and telefono and ciudad:
        cursor = db.database.cursor()
        sql = "UPDATE usuario SET nombre = %s, apellido =%s, documento=%s, pass = %s, correo =%s, telefono=%s, ciudad=%s WHERE id_user=%s"
        data = ( id_usuario,nombre, apellido ,documento, passw, correo, telefono, ciudad ) 
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home')) 

#Ruta para editar veterinaios
@app.route('/editVet/<int:id_vet>', methods=['POST'])
def editVet (id_vet):
    nameVet = request.form['nameVet']
    lastnameVet = request.form['lastnameVet']
    passwordVet = request.form['passwordVet']
    ciudadVet = request.form['ciudadVet']
    especializacionVet = request.form['especializacionVet']
    tienda = request.form['tienda']
    if nameVet and lastnameVet and passwordVet and ciudadVet and especializacionVet and tienda:
        cursor = db.database.cursor()
        sql = "UPDATE vetuser SET nameVet = %s, lastnameVet =%s, passwordVet = %s, ciudadVet =%s, especializacionVet =%s, tienda=%s WHERE id_vet=%s"
        data = ( id_vet,nameVet, lastnameVet , passwordVet, ciudadVet, especializacionVet, tienda ) 
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('registerVet')) 




   
        

    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
