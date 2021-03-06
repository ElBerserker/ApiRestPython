######################################
# Nombre:  Raul Hernandez Lopez @Neo #
# Email:    freeenergy1975@gmail.com #
# fecha: domingo 5 de junio del 2022 #
######################################

############bibliotecas####################
from flask import Flask, jsonify, request #
from flask_sqlalchemy  import  SQLAlchemy #
from flask_marshmallow import Marshmallow #
###########################################

##################################Creadenciales de la base de datos#########################################
app = Flask(__name__)                                                                                      
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Berserker_db:db_maria1.1@localhost:3306/Prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                                       
                                                                                                           
db = SQLAlchemy(app)
ma = Marshmallow(app)

########################### Creacion de la tabla usuario ###################################################
class Usuario(db.Model):
	clv_usuario = db.Column(db.String(5), primary_key = True)
	nombre_usuario = db.Column(db.String(30), unique=True, nullable = False)
	contrasenia_usuario = db.Column(db.String(30), nullable = False)
	tipo_usuario = db.Column(db.String(15), nullable = False)
	
	def __init__(self, clv_usuario, nombre_usuario, contrasenia_usuario, tipo_usuario):
		self.clv_usuario = clv_usuario
		self.nombre_usuario = nombre_usuario
		self.contrasenia_usuario = contrasenia_usuario
		self.tipo_usuario = tipo_usuario

db.create_all()        
#########################   Creacion de la tabla encuesta de satisfaccion ##################################
class EncuestaSatisfaccion(db.Model):
    clv_satisfaccion = db.Column(db.String(3), primary_key = True)
    nivel_satisfaccion = db.Column(db.Integer, nullable = False)
    comentario_satisfaccion = db.Column(db.Text)

    def __init__(self, clv_satisfaccion, nivel_satisfaccion, comentario_satisfaccion):
        self.clv_satisfaccion = clv_satisfaccion
        self.nivel_satisfaccion = nivel_satisfaccion
        self.comentario_satisfaccion = comentario_satisfaccion

db.create_all()        
################################## Creacion de esquemas #####################################################
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('clv_usuario', 'nombre_usuario', 'contrasenia_usuario', 'tipo_usuario')

#Devuelve  los resgistros de un  usuario.
usuarioSchema = UsuarioSchema()
#Devuelve todos lo registros de usuarios.
usuarioSchemas = UsuarioSchema(many=True)

class EncuestaSchema(ma.Schema) :
    class Meta:
        fields = ('clv_satisfaccion' , 'nivel_satisfaccion', 'comentario_satisfaccion')

#Devuelve los registros de una encuesta        
encuestaSchema = EncuestaSchema()
#Devuelve todos los resgistros de la encuesta
encuestasSchemas = EncuestaSchema(many=True)

#########################################  Metodos web #######################################################GET USUARIOS
@app.route('/usuario', methods=['GET'])
def obtenerUsuarios():
    todos_los_usuarios = Usuario.query.all()
    consulta_usuarios = usuarioSchemas.dump(todos_los_usuarios) 
    return jsonify(consulta_usuarios)

#GET USUARIO
@app.route('/usuario/<clv>', methods=['GET'])
def obtenerUsuario(clv):
    un_usuario = Usuario.query.get(clv)
    return usuarioSchema.jsonify(un_usuario)

#GET ENCUESTAS
@app.route('/encuesta', methods=['GET'])
def obtenerEncuestas():
    todas_las_encuestas = EncuestaSatisfaccion.query.all()
    consulta_encuestas = encuestasSchemas.dump(todas_las_encuestas)
    return jsonify(consulta_encuestas)

#GET ENCUESTA
@app.route('/encuesta/<clv>', methods=['GET'])
def obtenerEncuesta(clv):
    una_encuesta = EncuestaSatisfaccion.query.get(clv)
    return encuestaSchema.jsonify(una_encuesta)

#POST
@app.route('/usuario/nuevo_usuario', methods=['POST'])
def insertar_usuario():
    datosJSON = request.get_json(force=True)

    clv_usuario = datosJSON ['clv_usuario']
    nombre_usuario = datosJSON ['nombre_usuario']
    contrasenia_usuario = datosJSON ['contrasenia_usuario']
    tipo_usuario = datosJSON ['tipo_usuario']

    nuevo_usuario = Usuario(clv_usuario, nombre_usuario, contrasenia_usuario, tipo_usuario)

    db.session.add(nuevo_usuario)
    db.session.commit()
    return usuarioSchema.jsonify(nuevo_usuario)

#POST 
@app.route('/nivel_satifaccion/nuevo_nivel_satifaccion', methods=['POST'])
def insertar_nivel_satisfaccion():
    datosJSON = request.get_json(force=True)

    clv_satisfaccion = datosJSON ['clv_satisfaccion']
    nivel_satisfaccion =  datosJSON['nivel_satisfaccion']
    comentario_satisfaccion = datosJSON['comentario_satisfaccion']

    nuevo_nivel_satisfaccion = EncuestaSatisfaccion(clv_satisfaccion, nivel_satisfaccion, comentario_satisfaccion)

    db.session.add(nuevo_nivel_satisfaccion)
    db.session.commit()
    return encuestaSchema.jsonify(nuevo_nivel_satisfaccion)

#PUT 
@app.route('/usuario/actualizar_usuario/<clv>', methods=['PUT'])
def actualizarUsuario(clv):
    actualizar_usuario = Usuario.query.get(clv)

    datosJSON = request.get_json(force=True)
    nombre_usuario = datosJSON['nombre_usuario']
    contrasenia_usuario = datosJSON['contrasenia_usuario']
    tipo_usuario = datosJSON['tipo_usuario']

    actualizar_usuario.nombre_usuario = nombre_usuario
    actualizar_usuario.contrasenia_usuarui = contrasenia_usuario
    actualizar_usuario.tipo_usuario = tipo_usuario

    db.session.commit()
    return usuarioSchema.jsonify(actualizar_usuario)

#GET
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje':'hola'})

#DELETE
@app.route('/usuario/eliminar_usuario/<clv>', methods=['DELETE'])
def eliminarUsuario(clv):
    eliminar_usuario = Usuario.query.get(clv)

    db.session.delete(eliminar_usuario)
    db.session.commit()

    return usuarioSchema.jsonify(eliminar_usuario)

if __name__=="__main__":
    app.run(debug=True, port="4000", host="192.168.1.80")
