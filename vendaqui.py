from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask (__name__)

@app.route ("/")
def index():
    return render_template ('index.html')

@app.route("/cadastro/usuario")
def usuario():
    return render_template ('usuario.html', titulo="Cadastro de Usuário")

@app.route("/cadastro/caduser", methods=['POST'])
def caduser():
    return request.form

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