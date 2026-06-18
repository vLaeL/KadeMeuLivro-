KademeuLivro

Projeto da faculdade UNA Aímores sendo desenvolvido por Victor Lael e Brian Rodrigues do curso de Engenharia de Software, utilizando Python para o desenvolvimento de uma aplicação desktop voltada para pesquisa e gerenciamento de livros.

O sistema permite que usuários realizem cadastro e login, pesquisem livros utilizando a Google Books API, visualizem informações detalhadas sobre as obras e gerenciem uma lista de livros favoritos armazenada em banco de dados PostgreSQL.

Funcionalidades:
- Cadastro de usuários
- Login de usuários
- Recuperação de senha
- Pesquisa de livros utilizando a Google Books API
- Direcionamento para o site de compra do livro
- Visualização de detalhes dos livros
- Adição e remoção de livros favoritos
- Consulta da lista de favoritos
- Persistência de dados utilizando PostgreSQL
- Interface gráfica desenvolvida com CustomTkinter
- Operações CRUD implementadas para usuários e favoritos

Tecnologias: 
- Python
- Tkinter
- Requests
- SQLAlchemy
- Pillow
- Python-dotenv
- Custom Tkinter
- PostregSQL

Arquitetura:
O projeto foi organizado seguindo uma estrutura em camadas, separando responsabilidades entre:

- Screens (interfaces gráficas)
- Services (integração com APIs)
- Repository (operações com banco de dados)
- Database (modelos e conexão)
- Assets (imagens e recursos visuais)


Autores: 
- Victor Lael Sousa Guimarães
- Brian Rodrigues da Silva

Como executar:

```bash
pip install -r requirements.txt
python main.py 

