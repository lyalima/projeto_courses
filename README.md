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

As funcionalidades do projeto foram desenvovidades utilizando recursos do Django como: Class-Based-View, Forms com Crispy-Forms, Signals, entre outros.

Para instalar as dependências necessárias para usar o projeto, execute: pip install -r./requirements.txt.

Atente-se à configuração de algumas credenciais que estão como variáveis de ambiente.