from flask import render_template, request, url_for, redirect
from classes import Usuario, Cargo, Cliente

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
            return render_template('main/main.html', id_usuario=ID, adm=Usuario.verifica_gerente(ID))

    #retorna página de funcionarios
    @app.route('/home/<string:id>/funcionario', methods = ['GET'])
    def funcionario(id):
        if request.method == 'GET':
            tab = Usuario.get_tabela_func()
            if tab != None:
                cabecalho = ('Nome', 'Cargo', 'Data de Nascimento', 'CPF', 'Telefone')
                return render_template('main/funcionario.html', id_usuario=id, header=cabecalho, data=tab, adm=Usuario.verifica_gerente(id))
            else:
                return 'Não foi possível obter a tabela de Funcionarios'


    #retorna pagina de cadastro de funcionários
    @app.route('/home/<string:id>/funcionario/cadastro', methods = ['GET', 'POST'])
    def cadastro_funcionario(id):
        cargos = Usuario.get_cargos()

        if request.method == 'GET':
            return render_template('main/cadastro_funcionario.html', cargos=cargos, id_usuario=id, adm=Usuario.verifica_gerente(id))
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

    #retorna a pagina de gerenciamento da empresa
    @app.route('/home/<string:id>/ger', methods=['GET', 'POST'])
    def ger_empresa(id):      
        tab = Usuario.get_cargos()
        if tab != None:
            cabecalho = ('ID', 'Nome do Cargo')
            if request.method == 'GET':
                return render_template('main/empresa.html', id_usuario=id, adm=Usuario.verifica_gerente(id), header=cabecalho, data=tab)
            elif request.method == 'POST':
                nome_cargo = request.form.get('_nome')
                msg = Cargo.cadastra_cargo(nome_cargo)
                return redirect(url_for('ger_empresa', id=id, mensagem=msg))
        else:
            return render_template('Não foi possível recuperar a tabela de cargos')

    #retorna página de clientes
    @app.route('/home/<string:id>/cliente', methods = ['GET'])
    def cliente(id):
        if request.method == 'GET':
            tab = Cliente.getTab_Clientes()
            if tab != None:
                cabecalho = ('ID do Cliente', 'Nome', 'Telefone')
                return render_template('main/cliente.html', id_usuario=id, header=cabecalho, data=tab, adm=Usuario.verifica_gerente(id))
            else:
                return 'Não foi possível obter a tabela de Funcionarios'

    #retorna a página de cadastro dos clientes
    @app.route('/home/<string:id>/cliente/cadastro', methods = ['GET', 'POST'])
    def cadastro_cliente(id):
        if request.method == 'GET':
            return render_template('main/cadastro_cliente.html', id_usuario=id, adm=Usuario.verifica_gerente(id))
        elif request.method == 'POST':
            try:
                nome = request.form.get('_nome')
                telefone = request.form.get('_telefone')
                logradouro = request.form.get('_e_logradouro')
                numero = request.form.get('_e_numero')
                bairro = request.form.get('_e_bairro')
                cidade = request.form.get('_e_cidade')
                estado = request.form.get('_e_estado')
                cep = request.form.get('_e_cep')
                msg = Cliente.cadastra_cliente(nome,
                                               telefone,
                                               logradouro,
                                               numero,
                                               bairro,
                                               cidade,
                                               estado,
                                               cep)
                return redirect(url_for('cliente', id=id))
            except Exception as erro:
                return render_template('main/cadastro_cliente.html', id_usuario=id, mensagem=erro, adm=Usuario.verifica_gerente(id))