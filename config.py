from sqlalchemy import URL

# Informações relevantes para a conexão
user = 'root'
senha = 'senha' # !IMPORTANTE! Alterar para a senha do usuário no Banco de Dados do MySQL
host = 'localhost'
port = 3306 # deve ser um número INT
database = 'cadastro_clientes' # nome do database

db_connectionStr = URL.create(
        drivername='mysql+pymysql',
        username=user,
        password=senha,
        host=host,
        port=port,
        database=database
)