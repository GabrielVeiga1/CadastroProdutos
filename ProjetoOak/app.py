from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=False)


@app.route('/')
def listar_produtos():
    produtos = Produto.query.order_by(Produto.valor).all()
    return render_template('listagem.html', produtos=produtos)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        disponivel = request.form['disponivel'] == 'sim'

        novo_produto = Produto(nome=nome, descricao=descricao, valor=valor, disponivel=disponivel)
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('listar_produtos'))
    return render_template('cadastro.html')

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.valor = float(request.form['valor'])
        produto.disponivel = request.form['disponivel'] == 'sim'
        db.session.commit()
        return redirect(url_for('listar_produtos'))

    return render_template('atualiza_produto.html', produto=produto)

@app.route('/<int:id>/remover_produto', methods=['GET', 'POST'])
def remover_produto(id):
    produto = Produto.query.filter_by(id=id).first()
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('listar_produtos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
