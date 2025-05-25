# Objetivo: Perguntar dados do cliente, como se fosse um cadastro básico + integrar ao bd

# Importações relevantes para conexão e aplicação das informações ao bd.
import pandas as pd
from sqlalchemy import create_engine, text

# Importações necessárias para cadastro
from datetime import datetime, date, time

# Importações necessárias para configurações
from config import *

# Conectando ao bd para o uso de algumas funções:
db_engine = create_engine(db_connectionStr)

# Função responsável por: Criar um menu, permitindo
def menu():
    while True:
        linha()
        print("Menu Principal".center(18))
        linha()
        print('''1 - Cadastro
2 - Login
3 - Fechar Programa''')
        linha()

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cadastroCliente()
        elif escolha == '2':
            linha()
            print("Login".center(18))
            linha()
            login = input('''1- Logar como Cliente
2- Logar como Funcionário
3- Voltar\n''')
            while (login not in "123" or login == "123") and login != '':
                login = input('''Opção inválida. Tente novamente:
1- Logar como Cliente
2- Logar como Funcionário
3- Voltar\n''')
            if login == "1":
                loginCliente() # !!!
            elif login == "2":
                loginFuncionario() # !!!
            elif login == "3":
                menu()
        elif escolha == "3":
            print("Saindo do programa. Até logo!")
            exit()
        else:
            print("Opção inválida. Tente novamente.")
# Função responsável por: Sistema de Login
def loginCliente():
    linha()
    print ("Insira seus dados:")
    linha()
    email = input("Digite seu Email: ").lower().strip()
    senha_cli = input("Digite sua senha: ").strip()
    
    with db_engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM clientes WHERE email_cliente = :email AND BINARY senha_cliente = :senha"), parameters= {"email": email, "senha": senha_cli})
    
    cliente = result.fetchone()
    
    if cliente == None:
        print(f"{"=x="*6}\n{"Usuário inválido".center(18)}")

    # Caso existir, Acessa o Menu de Cliente
    else:
        linha()
        status = "Ativo" if cliente[7] == 1 else "Desativado"
        print(f'''Nome: {cliente[1]}
CPF: {cliente[0]}
Telefone: {cliente[2]}
Email: {cliente[3]}
Cadastrado em: {cliente[4]}
Estado da conta: {status}

Qual ação gostaria de realizar em sua conta?
1- Agendamentos
2- Editar informações da conta
3- Sair da conta'''
)
        acao_conta = input()

        if acao_conta == "1":
            agendamentos(cliente)
            print()
        elif acao_conta == "2":
            info = input('''Que tipo de informação deve ser editada?
        1- Nome
        2- Telefone
        3- Email\n''').strip()
            while info not in "123":
                info = input(f'''{"=x="*10}\nQue tipo de informação deve ser editada?
    1- Nome
    2- Telefone
    3- Email\n''').strip()
            if info == "1":
                info = "nome"
            elif info == "2":
                info = "telefone"
            else:
                info = "email"
            editarInfo(cliente[0], info)
        elif acao_conta == "3":
            linha()
            print ("Saindo da conta...")
            menu()
        else:
            print ("Ação Inválida")
# Sistema de login para Funcionários, que leva a "menu_funcionário"
def loginFuncionario():
    linha()
    print ("Insira seus dados:")
    linha()
    
    id_adm = input("Digite seu ID: ").strip()
    senha_adm = input("Digite sua Senha: ").strip()
    
    try:
        id_adm_int = int(id_adm)
    except ValueError:
        print("ID inválido")
        return

    #df = pd.read_sql('SELECT * FROM funcionarios', con = db_engine, dtype = str)
    with db_engine.connect() as conn:
        query = text("SELECT * FROM funcionarios WHERE id_adm = :id AND senha_adm = :senha")
        parametros = {"id": id_adm_int, "senha": senha_adm}
        funcionario = pd.read_sql(query, conn, params=parametros)
    # Tentando trocar o código abaixo pelo de cima.
    #funcionario = df[(df['id_adm']== id_adm)&(df['senha_adm'] == senha_adm)]
    
    if funcionario.empty:
        print(f"{"=x="*6}\n{"Usuário inválido".center(18)}")
    else:
        menuFuncionario(funcionario)
# Acessar o menu de funcionários (para edições de Administradores)
def menuFuncionario(funcionario):
    nome_funcionario = funcionario['nome_adm'][0]
    acao_adm = input(f'''---------------------------------------------------
Bem vindo, {nome_funcionario}

Qual ação gostaria de realizar?
1- Visualização da sua conta
2- Acessar dados de clientes
3- Sair da conta\n''')
    while acao_adm not in "123":
        acao_adm = input(f'''---------------------------------------------------
Bem vindo, {nome_funcionario}

===x===x===x===x===x===x===
Opção Escolhida Inválida.
    Tente novamente:
===x===x===x===x===x===x===

Qual ação gostaria de realizar?
1- Visualização da sua conta
2- Acessar dados de clientes
3- Sair''')
    
    # Verificação das opções
    while acao_adm not in ["1", "2", "3"]:
        acao_adm = input(f"{"=x="*6}\nOpção inválida. Tente novamente: ")
    if acao_adm == "1":
        # Visualizar no banco para procurar o nome da unidade para colocar junto do 'id_unidade'
        #df = pd.read_sql('SELECT * FROM Unidades', con = conexao, dtype = str)
        print ()
        print (f'''\nInformações da Conta:

Nome: {funcionario['nome_adm'].values[0]}
CPF: {funcionario['id_adm'].values[0]}
Telefone: {funcionario['tel_adm'].values[0]}
Email: {funcionario['email_adm'].values[0]}
CNPJ da Empresa: 
Unidade de Trabalho: 
---------------------------------------------------'''
# {funcionario['id_empresa'].values[0]} Ver com Vinicius sobre
# funcionario['id_unidade'].values[0]}             ↑
)
        voltar_1 = input('''1- Voltar para seu Menu
2- Voltar para Menu Principal\n''')
        if voltar_1 == "1":
            return(menuFuncionario(funcionario))
        elif voltar_1 == "2":
            return()
        else:
            acao_adm = input(f"{"=x="*6}\nOpção inválida. Tente novamente: ")
    # ↓ Opção Acessar dados clientes
    elif acao_adm == "2":
        sistemaBusca(funcionario)
    # ↓ Opção Sair:
    elif acao_adm == "3":
        menu()
# Função responsável por: Cadastrar e Aplicar no BD
def cadastroCliente():
    while True:
        # Informações por beleza
        linha()
        print(f'''{"Cadastro".center(18)}
{"de".center(18)}
{"Clientes".center(18)}''')
        linha()

        # Pedindo informações (nome, cpf, telefone, email)
        nome = input("Nome: ").title().strip()
        while nome == "":
            nome = input(f"{"=x="*6}\nErro, digite um nome válido.\n{"=x="*6}\nNome: ").title().strip()
        cpf = input("CPF: ")
        cpf = cpf.replace(".", "").replace("-", "")
        
        # Validador de cpf
        '''Preciso fazer o cálculo de cada número individual, com exceção do
            último (sendo esse o validador). Multiplicando-o em forma decrescente
            de 10 até o número 2. Ex: 1° num = 1 → 1 * 10, 2° num = 2 → 2 * 9, etc'''
        while True:
            # Checa se o cpf não excede o valor de caracteres (sem considerar pontuação)
            if len(cpf) != 11:
                cpf = input("CPF Informado muito curto/longo. Tente novamente: ")
                cpf = cpf.replace(".", "").replace("-", "")
            # Checa se o Cpf possui valores não-numéricos:
            elif not cpf.isnumeric():
                cpf = input("CPF não pode conter letras, somente números. Tente novamente: ")
                cpf = cpf.replace(".", "").replace("-", "")
            # Checa se o Cpf não tem caracteres repetidos (111.111.111-11, etc)
            elif cpf == cpf[::-1] or all(d == cpf[0] for d in cpf):
                cpf = input("CPF inválido. Tente novamente. Digite seu cpf: ")
                cpf = cpf.replace(".", "").replace("-", "")
            # Valida o Cpf com base nos dígitos validadores.
            elif not validarCpf(cpf):
                cpf = input("CPF informado não é Válido.\nTente novamente: ")
                cpf = cpf.replace(".", "").replace("-", "") 
            # Se tudo der certo, sai do bloco While e continua o programa.
            else:
                break
        
        # Faz a conexão e roda o comando de selecionar o id pelo Cpf
        with db_engine.connect() as connection:
            result = connection.execute(text('SELECT * FROM clientes WHERE id_cliente = :cpf'), parameters= {"cpf": cpf})
        # Checa se o Cpf já existe na tabela
        if result.fetchone():
            linha()
            print("CPF já existente na base de dados.")
            linha()
            resp = input('''O que deseja fazer?
    1- Tentar novamente
    2- Voltar ao menu principal\n''')
            while resp not in "12":
                resp = input('''Erro. O que deseja fazer?
    1- Tentar novamente
    2- Voltar ao menu principal\n''')
            if resp == "1":
                cadastroCliente()
            else:
                menu()
        senha = input("Digite uma senha. Deve ter pelo menos 8 dígitos e ter números e letras: ").strip()
        while len(senha) < 8 or not(senha.isalnum() and (not senha.isalpha() and not senha.isdigit())):
            senha = input(f'''{"=x="*6}
Erro, tente novamente.
{"=x="*6}
Digite uma senha. Deve ter pelo menos 8 dígitos e ter números e letras: ''').strip()
        telefone = input("Telefone: ")
        while telefone == "":
            telefone = input(f"{"=x="*6}\nErro, digite um telefone válido.\n{"=x="*6}\nTelefone: ").title().strip()
        email = input("E-mail: ").lower().strip()
        print(email.find("@"))
        while email == "" or email.find("@") == -1:
            email = input(f"{"=x="*6}\nErro, digite um email válido.\n{"=x="*6}\nEmail: ").lower().strip()
        dataCad = date.today()
        atividade = bool(1)
        cnpj = 8888
        
        df = pd.DataFrame(columns= ['id_cliente', 'nome_cliente', 'tel_cliente', 'email_cliente', 'data_cadastro', 'senha_cliente', 'id_empresa', 'atividade'])
        # Adiciona localmente as informações
        df.loc[len(df)] = cpf, nome, telefone, email, dataCad, senha, cnpj, atividade   
   
        # Jogando dados pra data-base:
        df.to_sql('clientes', con= db_engine, if_exists='append', index= False)
        break
# Função responsável por: Validador de cpf
def validarCpf(cpf):
    '''Preciso fazer o cálculo de cada número individual, com exceção do
    último (sendo esse o validador). Multiplicando-o em forma decrescente
    de 10 até o número 2. Ex: 1° num = 1 → 1 * 10, 2° num = 2 → 2 * 9, etc'''
    
    # Transformando cpf em String pra facilitar e evitar bugs
    cpf = str(cpf)
    cpf = cpf.replace(".", "").replace("-", "")
    
    # Cálculo em sí:
    soma = 0
    for dig, mult in zip(cpf[:-2], range(10, 1, -1)):
        soma += int(dig) * mult

    '''Após isso, eu divido o valor da soma por 11, salvando apenas o resto da conta, e faço as verificações'''

    resto = soma % 11

    # Cálculo do PRIMEIRO DÍGITO verificador
    digVerific = [11 - resto]

    if digVerific[0] > 9:
        digVerific[0] = 0

    # Cálculo do SEGUNDO DÍGITO verificador
    soma = 0
    for dig, mult in zip(cpf[:-1], range(11, 1, -1)):
        soma += int(dig) * mult

    resto = soma % 11

    digVerific.append((11 - resto))

    if digVerific[1] > 9:
        digVerific[1] = 0

    # Validação:
    # Transformando os números validadores em str, para permitir a validação
    digVerific = list(map(str, digVerific))
    # Retornando se é ou não um cpf válido
    if digVerific[0] == cpf[-2] and digVerific[1] == cpf[-1]:
        return True
    else:
        return False
# Deleção e desativação de contas
def deletarConta(id, df_fun):
    cpf = id[0]
    with db_engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM clientes WHERE id_cliente = :id"), parameters={"id":cpf})

    df = result.fetchone()
    
    # Checagem de Atividade:
    status = "Ativo" if df[7] == 1 else "Desativado"
    
    print (f'''Informações da conta:
Nome: {df[1]}
CPF: {df[0]}
Telefone: {df[2]}
Email: {df[3]}
CNPJ da Empresa: {df[4]}
Data de Cadastro: {df[5]}
Status de Cadastro: {status}''')

    resp = input('''Deseja:
1- ALTERAR ESTADO DE ATIVIDADE
2- DELETAR CONTA
3- VOLTAR\n''')
    while resp not in "123":
        resp = input(f'''{linha()}\nErro, tente novamente.{linha()}\nDeseja:
1- ALTERAR ESTADO DE ATIVIDADE
2- DELETAR CONTA
3- VOLTAR\n''')
    if resp == "1":
        confirm = input('''Tem certeza que quer Alterar o estado da conta?
    Digite: [S ou N] para continuar: ''').upper()
        if confirm.upper() == "S":
            try:
                if df[7] == 1:
                    with db_engine.begin() as connection:
                        connection.execute(text('UPDATE clientes SET atividade = 0 WHERE id_cliente = :cpf'), parameters= {"cpf": cpf})
                        connection.commit()
                    print ('''Conta desativada com sucesso!
        1- Voltar ao seu menu
        2- Voltar ao menu principal''')
                    voltar = input()

                    if (voltar == "1"):
                        menuFuncionario(df_fun)
                                
                    elif (voltar == "2"):
                        menu()
                elif df[7] == 0:
                    with db_engine.begin() as connection:
                        connection.execute(text('UPDATE clientes SET atividade = 1 WHERE id_cliente = :cpf'), parameters= {"cpf": cpf})
                        connection.commit()
                    print ('''Conta Ativada com sucesso!
        1- Voltar ao seu menu
        2- Voltar ao menu principal''')
                    voltar = input()

                    if (voltar == "1"):
                        menuFuncionario(df_fun)
                                
                    elif (voltar == "2"):
                        menu()
            except Exception as e:
                print (f"Erro ao alterar conta.\n {e}")
    elif resp == "2":
        confirm = input('''Ao deletar sua conta, todas as informações cadastradas dentro dela serão deletadas
    Você realmente deseja deletar esta conta?
    Digite: [S ou N] para continuar: ''').upper()
        if confirm == "S":
            try:
                with db_engine.begin() as connection:
                    connection.execute(text('DELETE FROM clientes WHERE id_cliente = :cpf'), parameters= {"cpf": cpf})
                    connection.commit()
                print ('''Conta deletada com sucesso!
    1- Voltar ao menu principal
    2- Sair do programa''')
                voltar = input()

                if (voltar == "1"):
                    menuFuncionario(df_fun)
                            
                elif (voltar == "2"):
                    menu()
                    
            except Exception as e:
                print (f"Erro ao deletar conta.\n {e}")
    elif resp == "3":
        menuFuncionario(df_fun)
# Menu que permite edição dos cadastros como funcionário
def menuEdit(df, funcionario):
    resp = input(f'''{"=x="*10}\nO que deseja fazer?
1- Editar Cadastro
2- Deletar Cadastro
3- Sair\n''')
    while resp not in "123":
        resp = input(f'''{"=x="*10}\nInválido. Digite novamente:
1- Editar Cadastro
2- Deletar Cadastro
3- Sair\n''')
    # Separadamente, roda o comando de edição.
    if resp == "1":
        info = input(f'''{"=x="*10}\nO que deseja editar?
1- Nome
2- Telefone
3- Email
4- CPF\n''')
        while not(info.isnumeric()) and info not in "123":
            info = input(f'''{"=x="*10}\nInválido.\nO que deseja editar?
    1- Nome
    2- Telefone
    3- Email
    4- CPF\n''')
        if info == "1":
            info = "nome"
        elif info == "2":
            info = "telefone"
        elif info == "3":
            info = "email"
        elif info == "4":
            info = "cpf"
        editarInfo(df[0], info, funcionario, adm=True)
    elif resp == "2":
        deletarConta(df, funcionario)
    elif resp == "3":
        if funcionario.empty():
            menuFuncionario(funcionario)
        else:
            loginCliente()
        print("Chegou ao fim")
# Sistema de menus para busca de cadastro, que chama a função "buscaInfo" para fazer a devida busca
def sistemaBusca(funcionario=''):
    respMenu = input(f'''{'=x='*10}
Pesquisa de Cliente
{'=x='*10}
Busca por:
    1- Nome
    2- CPF
    3- Telefone
    4- Email
    5- Voltar
{"Digite o Número com base na lista acima:\n".center(30)}''')
    while True:
    # Pesquisa por NOME
        if respMenu == '1':
            print(f"{'=x='*10}\nBusca por Nome\n{"=x="*10}")
            nome = input("Digite o nome a ser buscado: ").title().strip()
            df = buscaInfo(nome, "nome")
            if len(df) == 0:
                menuFuncionario(funcionario)
            menuEdit(df, funcionario)
    # Pesquisa por CPF
        elif respMenu == '2':
            print('=x='*10)
            print(f"Busca por CPF\n{"=x="*10}")
            cpf = input("Digite o CPF: ").strip()
            # Ajustando cpf pra funcionar sem os pontos e traços e com.
            cpf = cpf.replace(".", "").replace("-", "")
            while not validarCpf(cpf):
                cpf = input("CPF informado inválido.\nTente novamente: ")
                cpf = cpf.replace(".", "").replace("-", "")
            df = buscaInfo(cpf, "cpf")
            if df.size == 0 or df is None:
                menuFuncionario(funcionario)
            elif df is not None and not df.empty:
                menuEdit(df, funcionario)
            
    # Pesquisa por TELEFONE
        elif respMenu == '3':
            print('=x='*10)
            print(f"Busca por Telefone\n{"=x="*10}")
            telefone = input("Digite o número de Telefone: ")
            df = buscaInfo(telefone, "telefone")
            if df.size == 0:
                menuFuncionario(funcionario)
            menuEdit(df, funcionario)
    # Pesquisa por EMAIL
        elif respMenu == '4':
            print('=x='*10)
            print(f"Busca por E-mail\n{"=x="*10}")
            email = input("Digite o número de email: ")
            df = buscaInfo(email, "email")
            if df.size == 0:
                menuFuncionario(funcionario)
            menuEdit(df, funcionario)
        elif respMenu == '5':
            break
    # CASO NENHUMA DAS ANTERIORES
        else:
            respMenu = input(f'''{'=x='*10}
Pesquisa de Cliente
{'=x='*10}
Busca por:
    1- Nome
    2- CPF
    3- Telefone
    4- Email
    5- Voltar
{"Número inválido. Tente novamente:\n".center(30)}''')
# Funções de Edição de cadastro
def editarInfo(id, info, funcionario='', adm=False): # Deixarei a opção adm=False, para caso for necessário a separação
    try:
        if info == "nome":
            tipo = "Nome"
            info = "nome_cliente"
        elif info == "cpf":
            tipo = "CPF"
            info = "id_cliente"
        elif info == "telefone":
            tipo = "Telefone"
            info = "tel_cliente"
        elif info == "email":
            tipo = "Email"
            info = "email_cliente"
        elif info == "CNPJ" or info == "empresa":
            tipo = "Id de Relação Empresa"
            info = "id_empresa"
        elif info == "senha":
            tipo = "Senha"
            info = "senha_cliente"
        else:
            print("Tipo de formatação inválido.")
            return
    except Exception as e:
        print(f"Erro.\n{e}")
    # Coletando a informação:
    if info == "email_cliente":
        nova_info = input(f"Insira o novo {tipo} do usuário: \n").strip().lower()
        while nova_info == "" or nova_info.find("@") == 1:
            nova_info = input(f"{"=x="*6}\nErro, digite um email válido.\n{"=x="*6}\nEmail: ").strip().lower()
    else: nova_info = input(f"Insira o novo {tipo} do usuário: \n").strip()
    
    #Checagens para rodar o código corretamente.        
    with db_engine.connect() as conn:
        conn.execute(text(f"UPDATE clientes SET {info} = :nova_info WHERE id_cliente = :id"), parameters= {"nova_info": nova_info, "id": id})
        conn.commit()
        
        if info == "cpf":
            result = conn.execute(text("SELECT * FROM clientes WHERE id_cliente = :cpf"),parameters={"cpf": nova_info})
        else:
            result = conn.execute(text("SELECT * FROM clientes WHERE id_cliente = :id"), parameters={"id":id})
    cliente = pd.DataFrame(result.fetchall())
    
    status = "Ativo" if cliente["atividade"][0] == 1 else "Desativado"
    resp = input(f'''\n{tipo} alterado!
Suas informações atualizadas:

Nome: {cliente["nome_cliente"][0]}
CPF: {cliente["id_cliente"][0]}
Telefone: {cliente["tel_cliente"][0]}
Email: {cliente["email_cliente"][0]}
CNPJ da Empresa: {cliente["id_empresa"][0]}
Data de Cadastro: {cliente["data_cadastro"][0]}
Status de Cadastro: {status}
---------------------------------------------------
1- Voltar ao menu principal
0- Sair do programa\nOpção escolhida: ''')

    while resp not in "10":
        resp = input(f'''\n{tipo} alterado!
Suas informações atualizadas:

{"=x="*10}
{"Opção Não disponível, tente novamente.".center(30)}
{"=x="*10}

Nome: {cliente["nome_cliente"][0]}
CPF: {cliente["id_cliente"][0]}
Telefone: {cliente["tel_cliente"][0]}
Email: {cliente["email_cliente"][0]}
CNPJ da Empresa: {cliente["id_empresa"][0]}
Data de Cadastro: {cliente["data_cadastro"][0]}
Status de Cadastro: {cliente["atividade"][0]}
---------------------------------------------------
1- Voltar ao menu principal
0- Sair do programa\nOpção escolhida: ''')
    if resp == "1":
        if adm == True:
            menuFuncionario(funcionario)
        else:
            menu()
    elif resp == "0":
        exit()
# Busca de cadastro através do "tipo" e "info" 
def buscaInfo(val_busca, info):
    try:
        if info.lower() == "cpf":
            tipo = "id_cliente"
            info = "CPF"
        elif info.lower() == "nome":
            tipo = "nome_cliente"
            info = "Nome"
        elif info.lower() == "telefone":
            tipo = "tel_cliente"
            info = "Telefone"
        elif info.lower() == "email":
            tipo = "email_cliente"
            info = "Email"
        elif info.lower() == "CNPJ" or info.lower() in "Empresa":
            tipo = "id_empresa"
            info = "CNPJ da Empresa"
        else:
            print("'Info' Inválida. Revise o código com mais atenção!")
    except TypeError as e:
        print(f"Tipo de informação inválida. Reveja o Código.\nErro:\n{e}")
    with db_engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM clientes WHERE {tipo} LIKE :busca"), parameters= {"busca": f"{val_busca}%"})
        df = pd.DataFrame(result.fetchall())
        
        if df.size == 0:
            print(f"{"=x="*10}\nNão foi possível encontrar o cadastro especificado.\n{"=x="*10}")
            return df
        else:
            print(df)
            print("=x="*10)
            df_solo = pd.DataFrame.to_numpy(df)
            selecResp = input(f'''Digite o valor do Index para continuar.
Digite "S" para Voltar\n''').upper()
            if selecResp == "S":
                return()
            elif selecResp != "S":
                respVal = False
                while respVal == False:
                    if selecResp.isnumeric():
                        selecResp = int(selecResp)
                        if selecResp >= 0 and selecResp <= len(df)-1:
                            respVal = True
                        else:
                            selecResp = input("\nInválido.\nDigite o valor de index do Cliente para continuar: ")
                    else:
                        selecResp = input("\nInválido.\nDigite o valor de index do Cliente para continuar: ")
                # CASO PASSAR PELO FILTRO ATIVA: Função de Edição Mestre do Omnitrix
                df = df_solo[selecResp]
            return df
# Menu de Agendamentos
def agendamentos(cliente):
    acao_agenda = input(f'''{"=x="*6}
{"Agendamentos".center(18)}
{"=x="*6}
1- Seus agendamentos
2- Agendar sessão\n''')
    
    while acao_agenda not in "12" or acao_agenda == "12":
        acao_agenda = input(f'''{"=x="*6}
Opção inválida.
{"=x="*6}
{"Agendamentos".center(18)}
{"=x="*6}
1- Seus agendamentos
2- Agendar sessão\n''')
    
    if acao_agenda == "1":
        visualizarAgendamentos(cliente)
    elif acao_agenda == "2":
        agendarSessao(cliente)
# visualizador de agendamentos   
def visualizarAgendamentos(cliente):
    id_clai = cliente[0]
    #visu_agend = pd.read_sql("SELECT * FROM agendamentos WHERE id_cliente = :id_clai", params = {"id_clai": id_clai})
    visu_agend = pd.read_sql("SELECT * FROM agendamentos WHERE id_cliente = %s", db_engine, params = (id_clai,))
    
    # Caso não tenha nada em visu_agend, ele printa essa mensagem
    if visu_agend.empty:
        linha()
        print ("Você não possui agendamentos no momento")
        return(agendamentos(cliente))
    else:
        #connection.execute (text (visu_agend), params)
        print ("Seus Agendamentos")
        print(visu_agend)
    voltar_2 = input(''''-----------------------------------------------------------------------------------------------
O que deseja fazer agora?
1 - Voltar para agendamentos
2 - Sair da conta
\n''')
    
    if voltar_2 == "1":
        return(agendamentos(cliente))
    elif voltar_2 == "2":
        return(menu())
    else:
        while voltar_2 not in "12":
            print ("Escolha uma opção válida")
            voltar_2 = input()      
# função pra agendar sessões. (fazer agendamentos)  
def agendarSessao(cliente):
    # id_clai referencia a coluna id_cliente na tabela clientes (usando a filtragem 'cliente')
    id_clai = cliente[0]
    # unidades faz a leitura da tabela unidades
    unidades = pd.read_sql("SELECT * FROM unidades", db_engine)
    
    print('''
Preencha as informações:
-------------------------
Nossos serviços:
-----------------   
Limpeza de pele
Massagem
Drenagem
Head Spa  
''')
    # Servicos define o que é aceitavel o cliente escrever para passar
    servicos = ["limpeza de pele","massagem","drenagem","head spa"]
    # proced pega a string do cliente e transforma em minúsculo para poder se encaixar com 'servicos'
    proced = input("Digite o serviço que deseja realizar: ").strip().lower()
    
    # Caso o cliente digitar uma string que não esteja em 'servicos', vai pedir o 'proced' novamente
    while (proced not in servicos):
        # Quando for uma string que estiver em 'servicos', ele vai passar do while
        print ('''
Insira um serviço valido para continuar''')
        proced = input("Digite o serviço que deseja realizar: ").lower()
    
    while True:
        try:
            # Recebe a data em string e depois converte ela para formato data
            dia_agend = input("Escolha um dia de sua preferencia (ex:20/06/2025): ").strip()
            dia_agend = dia_agend.replace("-", "/")
            
            # Convertendo
            #print(dia_agend.find("/")) teste 1
            #if dia_agend not in "/": teste 2
            #    print("true")
            if dia_agend.find("/") == -1:
                dia = dia_agend[0:2]
                mes = dia_agend[2:4]
                ano = dia_agend[4:]
                #print(dia, mes, ano) teste 3
                dia_agend = "{}/{}/{}".format(dia, mes, ano)
            dia_agend = datetime.strptime(dia_agend, '%d/%m/%Y')
            # Caso a data inserida seja antes do dia atual, ela não deixará continuar
            dia_hoje = datetime.today()
            if dia_agend.date() < dia_hoje.date():
                print ("Data muito antiga, digite uma data válida para continuar")
                continue
            else:
                break
        except ValueError:
            print ("Digite uma data válida para continuar")
    
    while True:
        try:
            print (f"{"=x="*6}\nHorários disponiveis: 08:00 às 20:00")
            # Recebe horário em string e transorma em formato de horas e minutos
            horario_agend = input("Escolha o horário de sua preferencia (ex: 15:30): ").strip()
            
            if horario_agend.find(":") == -1:
                hora = horario_agend[0:2]
                if len(horario_agend) > 2:
                       minuto = horario_agend[2:]
                elif len(horario_agend) > 0 and len(horario_agend) < 2:
                    if hora[0] != "0":
                        horario_agend = "0{}:00".format(hora)
                elif len(horario_agend) > 0 and len(horario_agend) == 2:
                    horario_agend = "{}:00".format(hora)
                else:
                    horario_agend = "{}:{}".format(hora, minuto)

            horario_agend = datetime.strptime(horario_agend, '%H:%M')
            dia_hoje = datetime.today()
            if horario_agend.time() < dia_hoje.time() and dia_agend.date() == dia_hoje.date():
                print ("Horário muito antigo, digite uma data válida para continuar")
            # Caso o horário seja anterior ás 08:00, vai retornar uma mensagem e o while
            elif (horario_agend.time() < time(8, 0)):
                print ("Muito cedo, escolha um horário de atendimento válido")
            
            # Caso o horário seja posterior ás 20:00, vai retonar uma mensagem e o while
            elif (horario_agend.time() > time(20, 0)):
                print ("Muito tarde, escolha um horário de atendimento válido")
            
            # Caso não houver nenhum erro (tanto dos 'if' e 'elif' quanto do except), vai passar
            else:
                break
        
        # Caso gere algum erro que não esteja relacionado com o 'if' e 'elif', vai retornar essa mensagem e o while novamente
        except:
            print ("Insira um horário válido para continuar")   
    
    # Printa unidades para que o cliente possa escolher
    print('--------------------------------')
    print(unidades.to_string(index= False))
    print('--------------------------------')
    while True:
        try:
            # id_unidades vai incluir as 'id_unidade' que já estão criadas na tabela 'agendamentos'
            id_unidades = unidades['id_unidade']
            # O cliente seleciona uma unidade e transforma em inteiro para encaixar no id_unidade (SQL)
            id_uni = (input("Escolha a unidade que deseja realizar a sessão: ")).strip()
            id_uni = int(id_uni)
            
            # Caso a unidade selecionada não existir, vai pedir para selecionar uma unidade válida e voltar o while
            while id_uni not in id_unidades.tolist():
                id_uni = (input(f'''Selecione uma unidade disponivel para continuar.
{"=x==x==x="*6}
Escolha a unidade que deseja realizar a sessão: ''')).strip()
                id_uni = int(id_uni)
            break
        
        # Caso gerar algum erro que não esteja no 'if', vai gerar uma mensagem e retornar o while novamente
        except ValueError:
            print ("Unidade inválida, escolha uma unidade disponivel para continuar")
            
    dados_agend = ("""
                   INSERT INTO agendamentos
                   (id_cliente, procedimento, dia_agendamento, horario_agendamento, id_unidade)
                   VALUES (:id_clai, :procedimento, :dia_agendamento, :horario_agendamento, :id_unidade)"""
                   )
    params = {'id_clai': id_clai, 'procedimento': proced, 'dia_agendamento': dia_agend, 'horario_agendamento': horario_agend, 'id_unidade': id_uni}
    
    with db_engine.begin() as connection:
        connection.execute(text(dados_agend), params)
    
    print (f'''{"=x==x==x="*6}
Sessão agendada com sucesso!

Retornando ao Menu Principal...''')

    # voltando para o menu principal.
    menu()

# Cria uma linha, usada em algumas partes do código.
def linha():
    print("=x="*6)

db_engine.dispose()