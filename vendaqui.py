from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import url_for
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
import hashlib

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://netoherrera:toledo24@localhost:3306/meubanco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy (app)

app.secret_key = 'chavevendaqui'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model):
    __tablename__="usuario"
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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc


class Anuncio(db.Model):
    __tablename__="anuncio"
    id = db.Column('prod_id', db.Integer, primary_key=True)
    nome = db.Column('prod_nome', db.String(256))
    valor = db.Column('prod_valor', db.String(256))
    desc = db.Column('prod_desc', db.String(256))
    qnt = db.Column('prod_qnt', db.String(256))
    cond = db.Column('prod_cond', db.String(256))
    #cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    #usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, valor, desc, qnt, cond):
        self.nome = nome
        self.valor = valor
        self.desc = desc
        self.qnt = qnt
        self.cond = cond 

@app.errorhandler(404)              
def paginanaoencontrada(error):
    return render_template('paginanaoencontrada.html')

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(email=email, senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route ("/")
def index():
    return render_template ('index.html')

@app.route("/cadastro/usuario")
@login_required
def cadusuario():

    return render_template ('usuario.html', usuarios = Usuario.query.all(), titulo="Cadastro de Usuário")

@app.route("/cadastro/caduser", methods=['POST'])
@login_required
def caduser():
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    usuario=Usuario(request.form.get('user'), request.form.get('email'), request.form.get('cpf'), hash, request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

@app.route("/cadastro/usuario/detalhar/<int:id>")
def buscauser(id):
    usuario=Usuario.query.get(id)
    return usuario.nome

@app.route("/cadastro/usuario/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editauser(id):
    usuario=Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome=request.form.get('user')
        usuario.email=request.form.get('email')
        usuario.cpf=request.form.get('cpf')
        usuario.senha=hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
        usuario.end=request.form.get('end')
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('cadusuario'))
    return render_template ('editausuario.html', usuario = usuario, titulo="Cadastro de Usuário")


@app.route("/cadastro/usuario/deletar/<int:id>")
@login_required
def deletauser(id):
    usuario=Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))


@app.route("/cadastro/anuncio")
@login_required
def cadanuncio():
    return render_template ('anuncio.html', anuncios = Anuncio.query.all())

@app.route("/cadastro/anuncio/detalhar/<int:id>")
def buscaanun(id):
    anuncio=Anuncio.query.get(id)
    return anuncio.nome

@app.route("/cadastro/cadanun", methods=['POST'])
def cadanun():
    anuncio=Anuncio(request.form.get('anuncio'), request.form.get('valor'), request.form.get('descricao'), request.form.get('quantidade'), request.form.get('condicao'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('cadanuncio'))

@app.route("/cadastro/anuncio/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editaanun(id):
    anuncio=Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome=request.form.get('anuncio')
        anuncio.valor=request.form.get('valor')
        anuncio.desc=request.form.get('descricao')
        anuncio.qnt=request.form.get('quantidade')
        anuncio.cond=request.form.get('condicao')
        db.session.add(anuncio)
        db.session.commit()

        return redirect(url_for('cadanuncio'))
    return render_template ('editaanuncio.html', anuncio = anuncio )


@app.route("/cadastro/anuncio/deletar/<int:id>")
@login_required
def deletaanun(id):
    anuncio=Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('cadanun'))

@app.route("/cadastro/categoria")
@login_required
def cadcategoria():
    return render_template('categoria.html', categorias = Categoria.query.all())

@app.route("/cadastro/cadcat/", methods=['POST'])
def cadcat():
    categoria = Categoria(request.form.get('nome'), request.form.get('descri'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('cadcategoria'))

@app.route("/cadastro/categoria/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editarcategoria(id):
    categoria=Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome=request.form.get('nome')
        categoria.desc=request.form.get('descri')
        db.session.add(categoria)
        db.session.commit()

        return redirect(url_for('cadcategoria'))
    return render_template ('editacategoria.html', categoria = categoria )




@app.route("/cadastro/categoria/deletar/<int:id>")
@login_required
def deletacat(id):
    categoria=Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('cadcategoria'))



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

@app.route("/relatorios/vendas")
def rvendas():
    return render_template ('rvendas.html')

@app.route("/relatorios/compras")
def rcompras():
    return render_template ('rcompras.html')


if __name__ == 'vendaqui':
    with app.app_context():
        db.create_all()
    