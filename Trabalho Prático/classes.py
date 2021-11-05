import psycopg2

class Conexao:
    """Classe para construir conexao com o banco de dados"""
    def __init__(self):
        try:
            self.conexao = psycopg2.connect(host="localhost",
                                            dbname="db_teste",
                                            user="postgres",
                                            password="123",
                                            port='45701')
                                                                                  
            self.cursor = self.conexao.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def fecha_con(con, cursor):
        cur.close()
        con.close()
        
class Usuario(Conexao):
    """Classe do usuário"""
    def valida_login(user, senha):
        con = Conexao()
        con.cursor.execute('SELECT id FROM users WHERE usuario=%s AND senha=%s', (user, senha))

        #se o usuario estiver contido no banco, retorna seu ID
        retorno = con.cursor.fetchone()
        if retorno != None:
            return retorno[0]
        else:
            return 0
        con.conexao.commit()
        Conexao.fecha_con(con.conexao, con.cursor)

    def get_tabela_func(id):
        con = Conexao()
        con.cursor.execute('SELECT * FROM users WHERE id=%s', (id))

        return con.cursor.fetchall()
        
        con.conexao.commit()
        Conexao.fecha_con(con.conexao, con.cursor)
