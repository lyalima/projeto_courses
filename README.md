# Projeto Courses
Projeto baseado em atividade extensionista da universidade Uninter, feito com Python, Django, HTML, CSS e JavaScript, para gerenciamento e centralização de cursos online gratuitos e vagas relacionadas aos cursos.

O objetivo do projeto é centralizar cursos online gratuitos em um só sistema, permitindo que o usuário possa encontrar um curso específico, adiconá-lo à sua lista de cursos caso deseje iniciá-lo, ir para o site oficial do curso, ver vagas de emprego relacionadas à categoria do curso e, quando finalizar o curso excluí-lo da sua lista.  

O projeto conta com funcionalidades como: 
  - Cadastro, login e logout de usuários;
  - Verificação de email;
  - Redefinição de senha;
  - Perfil de usuário;
  - Gerenciamento dos cursos gerais do sistema;
  - Gerenciamento de vagas de emprego relacionadas aos cursos;
  - Gerenciamento dos cursos específicos do usuário;
  - Filtragem e busca de cursos e vagas;
  - Uso do banco de dados PostgreSQL.

As funcionalidades do projeto foram desenvovidades utilizando recursos do Django como: Class-Based-View, Forms com Crispy-Forms, entre outros.

Além dessas funcionalidades, foi implementado o envio de email assíncrono com Celery e RabbitMQ integrados com Django.

Para instalar as dependências necessárias para usar o projeto, execute:

```bash
pip install -r./requirements.txt
```

Para executar o projeto use: 
(Atente-se às configurações do banco de dados e de algumas credenciais que estão como variáveis de ambiente)

```bash
python manage.py migrate

python manage.py runserver
```

Para executar o RabbitMQ use: 
(Certifique-se de ter o Docker instalado)

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

Para executar o Celery use: 

```bash
celery -A app worker -l INFO
```

## Uso com Docker

### Requisitos 

- Docker 
- Docker Compose

### Construir e iniciar os containers

```bash
docker-compose up --build
```

A aplicação estará disponível em http://127.0.0.1:8000/.

### Executando comandos no container

```bash
docker-compose exec courses <comando>
```

### Exemplo de comando: aplicar as migrações no container

```bash
docker-compose exec courses python manage.py migrate
```

### Acessar o shell do container

```bash
docker exec -it courses /bin/bash
```
