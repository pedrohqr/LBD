from flask import render_template, request, url_for, redirect
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

    #retorna página de funcionarios
    @app.route('/home/<string:id>/funcionario', methods = ['GET', 'POST'])
    def funcionario(id):
        if request.method == 'GET':
            tab = Usuario.get_tabela_func()
            if tab != None:
                cabecalho = ('Nome', 'Cargo', 'Data de Nascimento', 'CPF', 'Telefone')
                return render_template('main/funcionario.html', id_usuario=id, header=cabecalho, data=tab, gerente=Usuario.verifica_gerente(id))
            else:
                return 'Não foi possível obter a tabela de Funcionarios'


    #retorna pagina de cadastro de funcionários
    @app.route('/home/<string:id>/funcionario/cadastro', methods = ['GET', 'POST'])
    def cadastro_funcionario(id):
        cargos = Usuario.get_cargos()

        if request.method == 'GET':
            return render_template('main/cadastro_funcionario.html', cargos=cargos, id_usuario=id)
        elif request.method == 'POST':
            try:
                nome = request.form.get('_nome')
                cpf = request.form.get('_cpf')
                salario = request.form.get('_salario')
                id_cargo = request.form.get('_cargo')
                login = request.form.get('_login')
                senha = request.form.get('_senha')
                data_nascimento = request.form.get('_data_nascimento')
                telefone = request.form.get('_telefone')
                logradouro = request.form.get('_e_logradouro')
                numero = request.form.get('_e_numero')
                bairro = request.form.get('_e_bairro')
                cidade = request.form.get('_e_cidade')
                estado = request.form.get('_e_estado')
                cep = request.form.get('_e_cep')
                msg = Usuario.cadastra_funcionario(nome,
                                                   cpf,
                                                   salario,
                                                   id_cargo,
                                                   data_nascimento,
                                                   telefone,
                                                   logradouro,
                                                   numero,
                                                   bairro,
                                                   cidade,
                                                   estado,
                                                   cep,
                                                   login,
                                                   senha)
                return redirect(url_for('funcionario', id=id))
            except Exception as erro:
                return render_template('main/cadastro_funcionario.html', cargos=cargos, id_usuario=id, mensagem=erro)
          
            
