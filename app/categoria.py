from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_description = db.Column(db.String(100))

    def __init__(self,cat_nom, cat_description):
        self.cat_nom = cat_nom
        self.cat_description = cat_description
with app.app_context():
    db.create_all()

#Eschema Categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_description')           
#una sola respuesta
categoria_schema = CategoriaSchema()

#muchas respuestas
categorias_schema = CategoriaSchema(many=True)

#get
@app.route('/categorias',methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)

    return jsonify(result)

#get x ID
@app.route('/categorias/<id>',methods=['GET'])
def get_categorias_x_id(id):
    categoriaReturn = Categoria.query.get(id)
    return categoria_schema.jsonify(categoriaReturn)

#Post
@app.route('/categoria', methods=['POST'])
def post_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_description = data['cat_description']

    nueva_categoria = Categoria(cat_nom, cat_description)

    db.session.add(nueva_categoria)
    db.session.commit()

    return categoria_schema.jsonify(nueva_categoria)

#Put data
@app.route('/categoria/<id>', methods=['PUT'])
def put_categoria(id):
    data = request.get_json(force=True)
    registroActualizado = Categoria.query.get(id)

    cat_nom = data['cat_nom']
    cat_description = data['cat_description']   

    registroActualizado.cat_nom = cat_nom
    registroActualizado.cat_description = cat_description

    db.session.commit() 
    return categoria_schema.jsonify(registroActualizado)

#Delete categoria
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    registroEliminado = Categoria.query.get(id)

    db.session.delete(registroEliminado)
    db.session.commit()

    return categoria_schema.jsonify(registroEliminado)


#Mensaje de Bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenio desde Python'})

if __name__ == '__main__':
    app.run(debug=True)