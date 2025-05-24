📚 API de Reserva de Salas
Este repositório contém a API de Reserva de Salas, desenvolvida com Flask e SQLAlchemy, projetada para ser executada em contêineres Docker como parte de uma arquitetura de microsserviços.

🧩 Arquitetura
A API de Reserva de Salas é um microsserviço dedicado exclusivamente ao gerenciamento das reservas de salas por turma. Ela opera dentro de um sistema maior de Getão escolar o Gest-o-escolar-API.

⚠️ Importante: Esta API depende da API de Gerenciamento Escolar (responsável por turmas, alunos, etc.). A API de Gerenciamento Escolar também deve estar em execução, atraves deste link https://gest-o-escolar-api-docker.onrender.com , para que a validação das turmas ocorra corretamente via requisições HTTP REST.

🚀 Tecnologias Utilizadas
Python 3.10+
Flask
SQLAlchemy
SQLite (utilizado como banco de dados local para desenvolvimento e persistência de reservas)
Requests (para comunicação com a API de Gerenciamento Escolar)
Docker (para containerização da aplicação)
▶️ Como Executar a API (com Docker)
A maneira mais recomendada de executar esta API é usando Docker. Certifique-se de ter o Docker Desktop (ou Docker Engine) instalado e rodando em sua máquina.

Clone o repositório:

Bash

git clone https://github.com/guilhermee78/Reserva
cd Reserva
obs* na branch Developing
Construa a imagem Docker da API de Reserva:

Bash

docker build -t minha-api-reservas .
Este comando lê o Dockerfile no diretório atual e constrói uma imagem Docker chamada minha-api-reservas.
Execute o contêiner da API de Reserva:

Bash

docker run -d -p 5002:5002 --name api-reservas minha-api-reservas
-d: Executa o contêiner em modo detached (em segundo plano).
-p 5002:5002: Mapeia a porta 5002 do seu computador (host) para a porta 5002 dentro do contêiner. É através desta porta que você acessará a API.
--name api-reservas: Atribui um nome fácil de usar ao seu contêiner.
A aplicação estará disponível em: 📍 http://localhost:5002



📝 Observação: O banco de dados SQLite (instance/site.db) é criado automaticamente dentro do contêiner na primeira execução. Para persistência de dados entre reinícios do contêiner, você pode considerar usar um volume Docker (-v /caminho/do/seu/host/data:/app/instance).



📡 Endpoints Principais
A API de Reserva de Salas expõe os seguintes endpoints:

GET /reservas – Lista todas as reservas cadastradas.
POST /reservas – Cria uma nova reserva de sala.

Exemplo de corpo JSON para criação:
JSON

{
  "turma_id": 1,
  "sala": "Laboratório 3",
  "data": "25/05/2025",
  "hora_inicio": "14:00",
  "hora_fim": "16:00"
}

Exemplo de corpo JSON output:

{
    "mensagem": "Reserva criada com sucesso",
    "reserva": {
        "data": "30/05/2025",
        "hora_fim": "16:00",
        "hora_inicio": "14:00",
        "id": 2,
        "sala": "Laboratório 3",
        "turma": {
            "alunos": [],
            "id": 1,
            "nome": "9º Ano B",
            "professor": {
                "disciplina": "Física",
                "id": 2,
                "nome": "Ana Paula"
            },
            "professor_id": 2,
            "turno": "Tarde"
        }
    }
}


GET /reservas/<id> – Retorna os detalhes de uma reserva específica pelo seu id.
PUT /reservas/<id> – Atualiza uma reserva existente pelo seu id.

Para que a API de Reserva de Salas funcione corretamente, a API de Gerenciamento Escolar (serviço de turmas) precisa estar acessível.

Certifique-se de que a API de Gerenciamento Escolar esteja rodando e acessível em:
https://gest-o-escolar-api-docker.onrender.com

Esta API de Reserva utiliza o endpoint https://gest-o-escolar-api-docker.onrender.com para validar a existência da turma através de um cache interno.



📦 Estrutura do Projeto
RESERVA/
│
├── app.py                  # Ponto de entrada da aplicação Flask
├── config.py               # Configurações de porta e api   
├── Dockerfile              # Define a imagem Docker para a aplicação
├── reserva_model.py        # Modelo de dados da Reserva (SQLAlchemy)
├── sql.py                  # Configuração do banco de dados (db Flask-SQLAlchemy)
├── reserva_controler.py    # Definição das rotas e lógica dos endpoints da API
├── requirements.txt        # Dependências Python do projeto
└── README.md               # Este arquivo de documentação


🛠️ Futuras Melhorias
Validação de Conflito de Horário e Sala: Implementar lógica para evitar reservas duplicadas ou sobrepostas para a mesma sala e horário.
Integração com Fila de Mensagens: Utilizar uma fila (e.g., RabbitMQ, Kafka) para comunicação assíncrona com outros microsserviços.
Autenticação e Autorização: Adicionar mecanismos de segurança para controlar o acesso aos endpoints da API.
Banco de Dados Externo: Migrar de SQLite para um banco de dados mais robusto (e.g., PostgreSQL, MySQL) para produção.


🧑‍💻 Autor
Jonathan Nascimento 2401750 
Caio Matheus Caetano Silva  2401362
Juan Bernardini Grenzi Cavadinha  2401187
Guilherme Freire Azevedo  2401421

