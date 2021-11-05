from flask import render_template, request, url_for, request, redirect
from classes import Usuario

def init_app(app):
    """Inicialização de funções"""

    #renderiza a página de login e valida o [usuario] e [senha]
    @app.route('/')
    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if request.method == 'GET':
            return render_template('login/login.html')
        elif request.method == 'POST':
            usuario = request.form.get('_login')
            senha = request.form.get('_senha')
            ID = Usuario.valida_login(usuario, senha)
            if ID > 0:
                return redirect(url_for('home', ID=ID))
            else:
                return render_template('login/login.html', mensagem='Usuário ou senha incorretos!')   

    #página principal
    @app.route('/home/<ID>', methods = ['GET'])
    def home(ID):
        if request.method == 'GET':
            return render_template('main/main.html', id_usuario=ID)

    #passa a tabela de funcionarios
    @app.route('/home/<ID>/get_tab_funcionario', methods = ['GET'])
    def get_tab_funcionario(id):
        tab = Usuario.get_tabela_func(id)
        if tab != None:
            cabecalho = ('cab1', 'cab2', 'cab3')
            return render_template('main/funcionario.html', header=cabecalho, data=tab)
        else:
            return 'deu ruim'