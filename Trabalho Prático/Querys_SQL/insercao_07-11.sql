create sequence if not exists seq_cargo_id
increment 1
start 1;

ALTER TABLE cargo ALTER COLUMN id_cargo SET DEFAULT NEXTVAL('seq_cargo_id');

create sequence if not exists seq_funcionario_id
increment 1
start 1;

ALTER TABLE funcionario ALTER COLUMN id_funcionario SET DEFAULT NEXTVAL('seq_funcionario_id');

create sequence if not exists seq_endereco_id
increment 1
start 1;

ALTER TABLE endereco ALTER COLUMN id_endereco SET DEFAULT NEXTVAL('seq_endereco_id');

insert into cargo(nome_cargo)
values('Gerente');
insert into cargo(nome_cargo)
values('Padeiro');
insert into cargo(nome_cargo)
values('Atendente');
insert into cargo(nome_cargo)
values('Cozinheiro');
insert into cargo(nome_cargo)
values('Garçon');

--cadastra funcionario
insert into funcionario(nome, data_nascimento, id_cargo, salario, cpf, telefone, login, senha)
values('Pedro Ramos', '27/06/2000', 1, 3000, '07181686151', '996760910', 'pedro_h', 'P123');
insert into funcionario(nome, data_nascimento, id_cargo, salario, cpf, telefone, login, senha)
values('Luiz Pio', '28/08/2000', 5, 1500, '54986523541', '999652168', 'luiz_pio', 'L123');

--select para a tabela de funcionarios
SELECT f.nome, c.nome_cargo, TO_CHAR(f.data_nascimento :: DATE, 'dd Mon yyyy'), 
f.cpf, f.telefone 
FROM funcionario f INNER JOIN cargo c 
ON f.id_cargo = c.id_cargo;

--select para verificar se é gerente ou não
SELECT nome
FROM funcionario 
WHERE id_cargo = 1 AND id_funcionario = 2;

alter table endereco add constraint un_endereco unique(id_endereco);
alter table funcionario drop constraint un_senha;

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
	SELECT COUNT(id_funcionario) INTO I FROM funcionario WHERE (cpf LIKE _cpf OR login LIKE _login) GROUP BY id_funcionario;
	IF I = 0 THEN
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

drop function cadastra_funcionario(_nome text, _cpf text, _telefone text, 
					 _salario decimal, _id_cargo int, _data_nasc date,
					 _login text, _senha text, _logradouro text, 
					 _numero text, _bairro text, _cidade text,
					 _estado text, _cep text);
					 
delete from funcionario where senha = 'abner'
select * from funcionario

SELECT cadastra_funcionario('Abner Damião', '84657591543', '995496852', 752.55, 2, '06/05/1996', 'abner_d', 'abner',
							'Rua Benjamin Adese', '581', 'Vila Jussara', 'Campo Grande', 'MS', '79092020');
							


