drop table if exists Empresa CASCADE;
create table Empresa (
Id_Empresa Integer PRIMARY KEY,
Nome Varchar(50)
);	

drop table if exists Endereco CASCADE;
create table Endereco (
Id_Endereco Integer PRIMARY KEY,
Numero Varchar(6),
Bairro Varchar(30),
Cidade Varchar(30),
Estado Varchar(30),
CEP Varchar(8),
Logradouro Varchar(50)
);

drop table if exists Cargo CASCADE;
create table Cargo (
Id_Cargo Integer PRIMARY KEY,
Nome_Cargo Varchar(20)
);

drop table if exists Funcionario CASCADE;
create table Funcionario (
Id_Funcionario Integer PRIMARY KEY,
Nome Varchar(50) NOT NULL,
Data_Nascimento Date,
Id_Cargo Integer REFERENCES Cargo(Id_Cargo),
Salario Decimal(15,2),
CPF varchar(11) NOT NULL UNIQUE,
Telefone Varchar(11) NOT NULL,
Login Varchar(20) NOT NULL UNIQUE,
Senha Varchar(20) NOT NULL,
Id_Endereco Integer REFERENCES Endereco(Id_Endereco)
);

drop table if exists Trabalha_em CASCADE;
create table Trabalha_em (
Id_Empresa Integer REFERENCES Empresa(Id_Empresa),
Id_Funcionario Integer REFERENCES Funcionario(Id_Funcionario)
);

drop table if exists Cliente CASCADE;
create table Cliente (
Id_Cliente Integer PRIMARY KEY,
Nome Varchar(60),
Telefone Varchar(11),
Id_Endereco Integer REFERENCES Endereco(Id_Endereco) UNIQUE
);

drop table if exists Pedido CASCADE;
create table Pedido (
Id_Pedido Integer PRIMARY KEY,
Id_Cliente Integer REFERENCES Cliente(Id_Cliente),
Valor_Total Decimal(15,2),
Data_Pedido Date
);
drop table if exists Categoria CASCADE;
create table Categoria (
Id_Categoria Integer PRIMARY KEY,
Descricao Varchar(100)
);

drop table if exists Produto CASCADE;
create table Produto (
Id_Produto Integer PRIMARY KEY,
Descricao Varchar(100),
Preco Decimal(15,2),
Id_Categoria Integer REFERENCES Categoria(Id_Categoria)
);

drop table if exists Pedido_Item CASCADE;
create table Pedido_Item (
Quantidade Integer,
Id_Pedido Integer REFERENCES Pedido(Id_Pedido),
Id_Produto Integer REFERENCES Produto(Id_Produto),
Total_Unitario Decimal(15,2)
);

drop table if exists Fornecedor CASCADE;
create table Fornecedor (
Id_Fornecedor Integer PRIMARY KEY,
Descricao Varchar(100)
);

drop table if exists Ingrediente CASCADE;
create table Ingrediente (
Id_Ingrediente Integer PRIMARY KEY,
Quantidade_Estoque Integer,
Id_Fornecedor Integer REFERENCES Fornecedor(Id_Fornecedor)
);

drop table if exists Produtos_Ingredientes CASCADE;
create table Produtos_Ingredientes (
Id_Produto Integer REFERENCES Produto(Id_Produto),
Id_ingrediente Integer REFERENCES Ingrediente(Id_Ingrediente),
Quantidade Decimal (10,2)
);

drop table if exists Logs CASCADE;
create table Logs(
Descricao VARCHAR(255),
Data_Hora TIMESTAMP
);

--criando as sequências para os ID's

drop sequence if exists seq_cargo_id;
create sequence seq_cargo_id
increment 1
start 1;

ALTER TABLE cargo ALTER COLUMN id_cargo SET DEFAULT NEXTVAL('seq_cargo_id');

drop sequence if exists seq_funcionario_id;
create sequence seq_funcionario_id
increment 1
start 1;

ALTER TABLE funcionario ALTER COLUMN id_funcionario SET DEFAULT NEXTVAL('seq_funcionario_id');

drop sequence if exists seq_endereco_id;
create sequence seq_endereco_id
increment 1
start 1;

ALTER TABLE endereco ALTER COLUMN id_endereco SET DEFAULT NEXTVAL('seq_endereco_id');

drop sequence if exists seq_categoria_id;
create sequence seq_categoria_id
increment 1
start 1;

ALTER TABLE categoria ALTER COLUMN id_categoria SET DEFAULT NEXTVAL('seq_categoria_id');

drop sequence if exists seq_cliente_id;
create sequence seq_cliente_id
increment 1
start 1;

ALTER TABLE cliente ALTER COLUMN id_cliente SET DEFAULT NEXTVAL('seq_cliente_id');

drop sequence if exists seq_empresa_id;
create sequence seq_empresa_id
increment 1
start 1;

ALTER TABLE empresa ALTER COLUMN id_empresa SET DEFAULT NEXTVAL('seq_empresa_id');

drop sequence if exists seq_fornecedor_id;
create sequence seq_fornecedor_id
increment 1
start 1;

ALTER TABLE fornecedor ALTER COLUMN id_fornecedor SET DEFAULT NEXTVAL('seq_fornecedor_id');

drop sequence if exists seq_ingrediente_id;
create sequence seq_ingrediente_id
increment 1
start 1;

ALTER TABLE ingrediente ALTER COLUMN id_ingrediente SET DEFAULT NEXTVAL('seq_ingrediente_id');

drop sequence if exists seq_pedido_id;
create sequence seq_pedido_id
increment 1
start 1;

ALTER TABLE pedido ALTER COLUMN id_pedido SET DEFAULT NEXTVAL('seq_pedido_id');

drop sequence if exists seq_produto_id;
create sequence seq_produto_id
increment 1
start 1;

ALTER TABLE produto ALTER COLUMN id_produto SET DEFAULT NEXTVAL('seq_produto_id');

-----------------funções 


--função para cadastrar novo funcionário
drop function if exists cadastra_funcionario(_nome text, _cpf text, _telefone text, 
											 _salario decimal, _id_cargo int, _data_nasc date,
											 _login text, _senha text, _logradouro text, 
											 _numero text, _bairro text, _cidade text,
											 _estado text, _cep text);
CREATE OR REPLACE FUNCTION 
cadastra_funcionario(_nome text, _cpf text, _telefone text, 
					 _salario decimal, _id_cargo int, _data_nasc date,
					 _login text, _senha text, _logradouro text, 
					 _numero text, _bairro text, _cidade text,
					 _estado text, _cep text)
RETURNS TEXT AS $$
DECLARE
	registro funcionario%rowtype;
	aux_id_endereco INT;
	I INT;
BEGIN
	SELECT COUNT(*) INTO I FROM funcionario WHERE (cpf LIKE _cpf OR login LIKE _login);
	IF I != 0 THEN
		RETURN 'CPF ou login já cadastrado!';
	ELSE 
		INSERT INTO funcionario(nome, data_nascimento, id_cargo, salario, cpf, telefone, login, senha)
		VALUES(_nome, _data_nasc, _id_cargo, _salario, _cpf, _telefone, _login, _senha);
		INSERT INTO endereco(logradouro, numero, bairro, cidade, estado, cep)
		VALUES(_logradouro, _numero, _bairro, _cidade, _estado, _cep);
		SELECT id_endereco INTO aux_id_endereco FROM endereco WHERE cep LIKE _cep AND numero LIKE _numero;
		UPDATE funcionario SET id_endereco = aux_id_endereco WHERE cpf LIKE _cpf;
		
		RETURN 'Funcionário cadastrado com sucesso!';
	END IF;
END;
$$ LANGUAGE PLPGSQL;	


--função para cadastrar novo cliente
DROP FUNCTION IF EXISTS cadastra_cliente(_nome text, _telefone text,_logradouro text, 
										 _numero text, _bairro text, _cidade text,
										 _estado text, _cep text);
CREATE OR REPLACE FUNCTION 
cadastra_cliente(_nome text, _telefone text,_logradouro text, 
				 _numero text, _bairro text, _cidade text,
				 _estado text, _cep text)
RETURNS TEXT AS $$
DECLARE
	registro cliente%rowtype;
	aux_id_endereco INT;
	I INT;
BEGIN
	INSERT INTO cliente(nome, telefone)
	VALUES(_nome, _telefone);
	INSERT INTO endereco(logradouro, numero, bairro, cidade, estado, cep)
	VALUES(_logradouro, _numero, _bairro, _cidade, _estado, _cep);
	SELECT id_endereco INTO aux_id_endereco FROM endereco WHERE cep LIKE _cep AND numero LIKE _numero;
	UPDATE cliente SET id_endereco = aux_id_endereco WHERE id_cliente = (SELECT LAST_VALUE FROM seq_cliente_id);

	RETURN 'Funcionário cadastrado com sucesso!';
END;
$$ LANGUAGE PLPGSQL;

--função para indicar os eventos na tabela de clientes
DROP FUNCTION IF EXISTS f_logs_cli() CASCADE;
CREATE OR REPLACE FUNCTION f_logs_cli()
RETURNS TRIGGER AS $$
DECLARE
	tempo TIMESTAMP = now();
BEGIN
	IF TG_OP LIKE 'INSERT' THEN
		INSERT INTO Logs(descricao, data_hora)
		VALUES(CONCAT('O cliente ',  new.nome, ' foi cadastrado'), tempo);
	ELSIF TG_OP LIKE 'UPDATE' THEN
		INSERT INTO Logs(descricao, data_hora)
		VALUES(CONCAT('O cliente ', new.nome, ' foi atualizado'), tempo);
	ELSIF TG_OP LIKE 'DELETE' THEN
		INSERT INTO Logs(descricao, data_hora)
		VALUES(CONCAT('O cliente ', old.nome, ' foi excluído'), tempo);
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

--trigger

DROP TRIGGER IF EXISTS tr_logs_cli
ON Logs CASCADE;

CREATE TRIGGER tr_logs_cli AFTER
UPDATE OR DELETE OR INSERT
ON cliente FOR EACH ROW
EXECUTE FUNCTION f_logs_cli();

--cadastro padrão ao gerar o banco:

INSERT INTO empresa(nome) VALUES('MATRIZ');
INSERT INTO cargo(Nome_Cargo) VALUES('Administrador');
INSERT INTO funcionario(nome, id_cargo, salario, cpf, telefone, login, senha)
VALUES('Administrador', 1, 0, '0', '0', 'admin', 'admin');
INSERT INTO trabalha_em(id_empresa, id_funcionario)
VALUES(1, 1);