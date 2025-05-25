-- Criando o cadastro de clientes
Create database if not exists Aura_Spa;
use Aura_Spa;

-- Criando a tabela de empresa
Create Table if not exists empresa (
id_empresa int primary key,
nome_empresa varchar(50),
tel_empresa varchar(20),
email_empresa varchar(50),
cep_empresa varchar(9)
# id_unidade
);

-- Criando a tabela de unidades
Create Table if not exists unidades(
id_unidade int primary key, # 1 2 
nome_unidade varchar(20) # Shopping Raposo Tavares, Shopping Taboão da Serra
);

-- Criando a tabela de clientes
Create Table if not exists clientes (
id_cliente BIGINT primary key,
nome_cliente varchar(50),
tel_cliente varchar(20),
email_cliente varchar(50),
data_cadastro date,
senha_cliente varchar(40),
id_empresa int,
atividade boolean default 1,
Foreign Key (id_empresa) references empresa (id_empresa)
);


-- Criando a tabela de funcionarios
Create table if not exists funcionarios(
id_adm int primary key,
id_empresa int,
id_unidade int,
senha_adm int,
nome_adm varchar(50),
tel_adm varchar(20),
email_adm varchar(50),
Foreign Key (id_empresa) references empresa (id_empresa),
Foreign Key (id_unidade) references unidades (id_unidade)
);

-- Criando a tabela de agendamentos 
Create Table agendamentos (
id_agendamento int primary key auto_increment,
id_cliente bigint,
procedimento varchar (20),
dia_agendamento date,
horario_agendamento time,
id_unidade int,
Foreign key (id_unidade) references unidades (id_unidade),
Foreign key (id_cliente) references clientes (id_cliente)
);


-- Inserindo valores nas Tabelas

Insert Into empresa values 
(8888, "Aura Spa", "(55)11 91275-1906", "auraspa@gmail.com", "12345-678");

 Insert into clientes values
(1616, "Josilda", "(55)11-82374-2819", "josilda@gmail.com", '2017-06-20', 123, 8888, 1), # Teste 1
(1818, "Roberto", "(55)11-82374-2718", "roberto@gmail.com", '2019-03-27', 321, 8888, 1); # Teste 2


Insert into unidades values 
(1, 'Shopping Taboão'),
(2, 'Shopping Raposo');

Insert into funcionarios values 
(2626, 8888, 1, 2006, 'Vinicius Alves de Souza', '(55)11-82374-2718', 'vinias@gmail.com');

Insert Into agendamentos  (id_cliente, procedimento, dia_agendamento, horario_agendamento, id_unidade)
values
(1818, 'Lavagem', '2025-06-25', '16:30:00', 2);

-- Selecionado Tabelas
select * from empresa;
select * from unidades;
select * from clientes;
select * from funcionarios;
select * from agendamentos;


-- Deixando os atributos como not null
# Formato ALTER TABLE (nome_tabela) MODIFY COLUMN (nome_atributo) (tipo_atributo) NOT NULL;
alter table clientes modify column nome_cliente varchar(50) not null;
alter table clientes modify column tel_cliente varchar(20) not null;
alter table clientes modify column email_cliente varchar (50) not null;

-- Não permitindo strings vazias
# Formato: ALTER TABLE (nome_tabela) ADD CONSTRAINT (nome_atributo) CHECK (condição)
alter table clientes add constraint nome_cliente check (nome_cliente <> '');
alter table clientes add constraint tel_cliente check (tel_cliente <> '');
alter table clientes add constraint email_cliente check (email_cliente <> '');
