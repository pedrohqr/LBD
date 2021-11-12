import psycopg2
from config import config

class Conexao:
    """Classe para construir conexao com o banco de dados"""

    #construtor da conexão com o banco
    def __init__(self):
        parametros_ini = config()
        self.conexao = psycopg2.connect(**parametros_ini)
                                                                                  
        self.cursor = self.conexao.cursor()
      
    #fecha a conexão dos componentes
    def fecha_con(con, cursor):
        cursor.close()
        con.close()
        
class Usuario(Conexao):
    """Classe do usuário"""

    #se o usuario estiver contido no banco, retorna seu ID
    def valida_login(user, senha):
        con = Conexao()
        con.cursor.execute('SELECT id_funcionario FROM funcionario WHERE login=%s AND senha=%s', (user, senha))

        retorno = con.cursor.fetchone()
        if retorno != None:
            return retorno[0]
        else:
            return 0
        con.conexao.commit()
        Conexao.fecha_con(con.conexao, con.cursor)

    #retorna todos os dados da tabela de funcionarios
    def get_tabela_func():
        con = Conexao()
        con.cursor.execute("SELECT f.nome, c.nome_cargo, TO_CHAR(f.data_nascimento :: DATE, 'dd Mon yyyy'), f.cpf, f.telefone "+
                           "FROM funcionario f INNER JOIN cargo c "+
                           "ON f.id_cargo = c.id_cargo;")

        return con.cursor.fetchall()
        
        con.conexao.commit()
        Conexao.fecha_con(con.conexao, con.cursor)

    #verifica se o usuario é gerente e retorna booleano
    def verifica_gerente(id):
        con = Conexao()
        con.cursor.execute("SELECT nome "+
                           "FROM funcionario "+
                           "WHERE id_cargo = 1 AND id_funcionario = %s;", (id))

        if con.cursor.fetchone() != None:
            return True
        else:
            return False
        
        con.conexao.commit()
        Conexao.fecha_con(con.conexao, con.cursor)

    #retorna tabela de cargos
    def get_cargos():
        con = Conexao()
        con.cursor.execute("SELECT * FROM cargo;")
                          
        return con.cursor.fetchall()
        
        con.conexao.commit()
        Conexao.fecha_con(con.conexao, con.cursor)

    #cadastra novo funcionário
    def cadastra_funcionario(nome, cpf, salario, id_cargo, data_nascimento, telefone, logradouro, numero, bairro, cidade, estado, cep, login, senha):
        try:
            con = Conexao()
            con.cursor.execute("SELECT cadastra_funcionario(%s, %s, %s, %s, %s, %s, %s, %s, "+
							   "%s, %s, %s, %s, %s, %s);",
                               (nome, cpf, telefone, salario, id_cargo, data_nascimento, login, senha, 
                                                        logradouro, numero, bairro, cidade, estado, cep))
            
            con.conexao.commit()

            return con.cursor.fetchone()[0]
            Conexao.fecha_con(con.conexao, con.cursor)
        except Exception as error:
            return error