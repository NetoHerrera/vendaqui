from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://netoherrera:toledo24@localhost:3306/meubanco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy (app)

class Usuario(db.Model):
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    cpf = db.Column('usu_cpf', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    end = db.Column('usu_end', db.String(256))

    def __init__(self, nome, email, cpf, senha, end):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.end = end

@app.route ("/")
def index():
    return render_template ('index.html')

@app.route("/cadastro/usuario")
def cadusuario():
    return render_template ('usuario.html', usuarios = Usuario.query.all(), titulo="Cadastro de Usuário")

@app.route("/cadastro/caduser", methods=['POST'])
def caduser():
    usuario=Usuario(request.form.get('user'), request.form.get('email'), request.form.get('cpf'), request.form.get('senha'), request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

@app.route("/cadastro/anuncio")
def anuncio():
    return render_template ('anuncio.html')

@app.route("/cadastro/cadanun", methods=['POST'])
def cadanun():
    return request.form

@app.route("/anuncio/pergunta")
def pergunta():
    return render_template ('pergunta.html')

@app.route("/anuncio/perguntaanun", methods=['POST'])
def perguntaanun():
    return request.form

@app.route("/anuncio/compra")
def compra():
    print("Compra efetuada")
    return ""

@app.route("/anuncio/favorito")
def favorito():
    print("Inserido à lista de favoritos")
    return ""

@app.route("/configuracoes/categoria")
def categoria():
    return render_template('categoria.html')

@app.route("/relatorios/vendas")
def rvendas():
    return render_template ('rvendas.html')

@app.route("/relatorios/compras")
def rcompras():
    return render_template ('rcompras.html')


if __name__ == 'vendaqui':
    with app.app_context():
        db.create_all()
    