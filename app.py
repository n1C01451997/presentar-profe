from flask import Flask,render_template,redirect,request,url_for,flash,session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

#creamos una instancia de la clase flask
app = Flask(__name__)
app.secret_key='728203215'

#definir ruta
db= mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2024"
    )
#c
cursor = db.cursor()

#incapacidad medica 

@app.route('/password/<contraencrip>')

def encriptarcontra(contraencrip):
    # generar un hash de la contraseña
    #encriptar = bcrypt.hashpw(contraencrip.encode("utf-8"),bcrypt.gensalt())
   encriptar = generate_password_hash(contraencrip)
   valor = check_password_hash(encriptar,contraencrip)
  # return "Encriptado:{0} | coincide:{1}".format(encriptar,valor)
   return valor

#iniciar sesion
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        #verificar las credenciales del usuario
        username = request.form.get('txtusuario')
        #son los mismos campos de la variable
        password = request.form.get('txtcontrasena')
        cursor = db.cursor()
        cursor.execute("SELECT usuario,contraseña FROM personas WHERE  usuario = %s",(username,))
        resultado = cursor.fetchone()

        #el uno lo definimos con el que esta en la linea 35
        if resultado and check_password_hash(resultado[1],password):
           session['usuario']= username
           return redirect(url_for('lista'))
        else:
           print("credenciales invalidas")
           return render_template('login.html')

    return render_template('login.html')

#fin incapacidad medica

#ruta cierrede sesion

@app.route('/logout')
def logout():
    #eliminar el usuario de la sesion en otras palabras cerrar sesion 
    session.pop('usuario',None)
    print('cerro sesion')
    return redirect(url_for('login'))


#definir ruta
@app.route('/lista')
def lista():#item
    cursor = db.cursor()#permitir ejecutar
    cursor.execute('select * FROM personas')
    usuario = cursor.fetchall()#

    return render_template('index.html',personas=usuario)#esta renderizando el index.html, y le esta enviando argumentos osea "persosnas" y que la convierta en una variable 
#desde aqui empece a adelantarme ----------
@app.route('/Registrar', methods=['GET','POST'])
def registrar_usuario():
    if request.method == 'POST':
       nombres = request.form.get('nombre')
       apellidos = request.form.get('apellido')
       correo = request.form.get('email')
       direccion  = request.form.get('direccion')
       telefono = request.form.get('telefono')
       usuario = request.form.get('usuario')
       Contrasenas = request.form.get('contrasena')

       #encriptar contraseña
       Contrasenas = generate_password_hash(Contrasenas)

       #verificar usuario y correo si existe en la base de datos 

       cursor = db.cursor()
       cursor.execute(
           "SELECT * FROM personas WHERE usuario = %s or email_persona = %s", (usuario,correo))
       existing_user = cursor.fetchone()

       if existing_user:
           print('el usuario o correo ya esta registrado ')
           return render_template('Registrar.html')

        #insertar datos ala tabla personas

       cursor.execute("INSERT INTO personas(nombre_persona,apellido_persona,email_persona,direccion,telefono,usuario,contraseña)VALUES(%s,%s,%s,%s,%s,%s,%s)",
                      (nombres,apellidos,correo,direccion,telefono,usuario,Contrasenas))
       db.commit()
       #metodo para generar mensajes 
       ##flash('usuario credo correctamente','success')

        #en caso de que sea solicitud, redirige a la misma pagina cuando el metodo es POST
       return redirect(url_for('login'))
        # si es metodo get me renderiza el formulario
    return render_template('Registrar.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_usuario(id):
    cursor =db.cursor()
    if request.method  =='POST':
        nombper = request.form.get('nombreper')
        apelldoper = request.form.get('apellidoper')
        emailpers = request.form.get('emailper')
        direcper = request.form.get('direccionper')
        teleper = request.form.get('telefonoper')
        usuarper = request.form.get('usuarioper')
        passwper = request.form.get('passwordper')

        #sentencia para actualizar los datos en la base de datos
        sql = "UPDATE personas SET nombre_persona=%s, apellido_persona=%s, email_persona=%s, direccion=%s, telefono=%s, usuario=%s, contraseña=%s WHERE id_perso=%s"
        cursor.execute(sql, (nombper,apelldoper,emailpers,direcper,teleper,usuarper,passwper,id))
        db.commit()

        return redirect(url_for('lista'))#redirecciona a una url
    else:
        #obtener los datos de la persona que se va a editar
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s', (id,))
        data = cursor.fetchall() 

        if data:
            return render_template('editar.html',persona=data[0])#redirecciona a html
        else:
            flash ('usuario no encontrado', 'Error ')
            return redirect(url_for('lista'))
@app.route('/eliminar/<int:id>',methods=['GET','POST'])
def eliminar_usuario(id):
    cursor =db.cursor()
    if request.method  =='POST':
        sql = "DELETE FROM personas WHERE id_perso=%s"
        cursor.execute(sql,(id,))
        db.commit()
        return redirect (url_for('lista'))
    else:
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s', (id,))
        data = cursor.fetchall() 

        if data:
            return render_template('eliminar.html',persona=data[0])
        else:
            return ("Metodo Invalido")

        
        
#para ejecutar instalacion 

if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)

#hasta aqui -------------------


