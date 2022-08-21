<h1 align="center">M2P2-DevinHouse 👨‍💻</h1>

# Software de gestão de inventário de empresas - DEVinventory

O projeto Back-end desenvolvido durante o Módulo 2, consiste no desenvolvimento de uma API em Python, usando Flask com SQLAlchemy

# Requisitos:

<ul>
  <li><i>Utilizar Python</i> </li>
  <li><i>Utilizar Flask com SQLAlchemy.</i> </li>
  <li><i>Utilizar banco de dados PostgreSQL para armazenar os dados.</i> </li>
  <li><i>Utilizar conceito de Migrations.</i> </li>
  <li><i>Utilizar GitHub para armazenamento do código</i> </li>
  <li><i>Utilizar Trello para organização do projeto</i> </li>
  <li><i>Utilizar conceitos de squads, Kanban e Scrum.</i> </li>
  <li><i>Utilizar conhecimentos em SQL</i></li>
</ul>

# Pré requisitos ambiente:

Instalar Python na maquina através do link abaixo:
<a href="https://python.org.br/instalacao-windows/" target="_blank">Python 3</a>

Intalar o Poetry através do comando abaixo no cmd do Windows:
<<i>curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python</i>>


# Configuração ambiente:

<ul>
<li>Executar o comando: <i>poetry config --local virtualenvs.in-project true</i></li>
<li>Executar o comando: <i>poetry install</i> para instalar as dependencias</li>
<li>Criar um arquivo .env baseado no arquivo .env_example e colocar os campos necessários.</li>
</ul>

# Executar aplicação:

Executar o comando: <i>poetry run flask run</i>

# Criar tabelas no banco:

<i>poetry run flask db init</i>
<i>poetry run flask db migrate</i>
<i>poetry run flask db upgrade</i>

# Popular as tabelas do database:

<i>poetry run flask populate_db</i>


# Endpoints:

<>INVENTORY</b>


<b style="font-size:30px">POST/inventory/create</b>

<b>Parametros de entrada:</b>
<ul>
 <li>product_category_id (obrigatório)</li>
 <li>user_id  (opcional)</li>
 <li>product_code (obrigatório)</li> 
 <li>title  (obrigatório)</li>
 <li>value  (obrigatório)</li>
 <li>brand  (obrigatório)</li>
 <li>template  (obrigatório)</li>
 <li>description  (obrigatório)</li>
 </ul>
 
 <b>Saída:</b>
 
 <ul>
 <li>Sucesso, 201 (created)</li>
 <li>Error, 400</li>
 <li>Error premission, 403 (forbidden)</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Permissão WRITE</li>
 <li>Todos os campos obrigatórios preenchidos</li>
 <li>O código do produto deve ser unico</li> 
 <li>Value maior que zero</li>
 <li>Retornar status 201 quando o item for criado</li>
 </ul>


<b style="font-size:30px">GET/inventory</b>
<b>Parametros de entrada:</b>
<ul>
 <li>title (Opcional)</li>
 </ul>
 
 <b>Saída:</b>
 
 <ul>
 <li>Sucesso, 200 (OK)</li>
 <li>Error, 204 (No content)</li>
 <li>Error premission, 403 (forbidden)</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Permissão READ</li>
 <li>Retornar todos que tenham o mesmo titulo (usar like)</li>
 <li>O código do produto deve ser unico</li> 
 <li>Se não tiver parametros retornar todos os itens</li>
 <li>Utilizar paginação, retornando 20 itens</li>
 <li>Se user_id = null retornar id: None e name: "Na empresa"</li>
 <li>Se nenhum resultado status 204 (No content)</li>
 <li>Se encontrado o resultado retornar em JSON contendo: id, product_code, title, product_category, user e Status 200 (OK)</li>
 </ul>
 

<b style="font-size:30px">GET/inventory</b> 

<b>Sem parametros de entrada</b>

<b>Saída:</b>
 
 <ul>
 <li>Sucesso, 200 (OK)</li>
 <li>Error premission, 403 (forbidden)</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Permissão READ</li>
 <li>Calcular numero de usuários</li>
 <li>Calcular o número de itens</li> 
 <li>Calcular o valor da soma de todos os itens.</li>
 <li>Calcular quantos itens estão emprestados para usuários</li>
 <li>Retornar statísticas e status 200 (OK)</li>
 </ul>
 
<b style="font-size:30px">PATH/inventory</b>

<b>Parametros de entrada:</b>
<ul>
<li>id (obrigatório)</li>
<li>Quaisquer camplos (opcional)</li>
</ul>
 
<b>Saída:</b>
 
<ul>
<li>Sucesso, 204 (No Content)</li>
<li>Error, 400</li>
<li>Error premission, 403 (forbidden)</li>
</ul>
 
 <b>Regras de negócio:</b>
<ul>
<li>Permissão UPDATE</li>
<li>É possível alterar todos os campos exceto: product_category_id e product_code, senão status 400</li>
<li>Respeitas as regras de negócio do endpoint POST</li>
<li>Ao atualizar item, retornar status 204 (No Content)</li>
</ul>
 

<b>USERS</b>

<b style="font-size:30px">POST/user</b>

<b>Parametros de entrada:</b>
<ul>
 <li>city_id (obrigatório)</li>
 <li>gender_id  (obrigatório)</li>
 <li>role_id (obrigatório)</li> 
 <li>name   (obrigatório)</li>
 <li>age  (obrigatório)</li>
 <li>email  (obrigatório)</li>
 <li>phone  (obrigatório)</li>
 <li>password  (obrigatório)</li>
 <li>cep  (obrigatório)</li>
 <li>street  (obrigatório)</li>
 <li>number_street  (obrigatório)</li>
 <li>district  (obrigatório)</li>
 <li>complement  (opcional)</li>
 <li>landmark  (opcional)</li>
 </ul>
 
 <b>Saída:</b>
 
 <ul>
 <li>Sucesso, 201 (created)</li>
 <li>Error, 400</li>
 <li>Error premission, 403 (forbidden)</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Permissão READ, WRITE, UPDATE e DELETE (role = Administrador do sistema)</li>
 <li>Todos os campos obrigatórios preenchidos</li>
 <li>O email deve ser unico no banco</li> 
 <li>Password criptrografado no banco de dados (regra na models) e conter 8 digitos, sendo pelo menos um caracter especial</li>
 <li>Telefone deve conter 11 digitos sem letras ou caracter especial</li>
 <li>Retornar status 201 quando o item for criado</li>
 </ul>

<b style="font-size:30px">POST/user/auth/google</b>

<b>Parametros de entrada:</b>
<ul>
 <li>Login google</li>
 </ul>
 
 <b>Saída:</b>
 
 <ul>
 <li>Sucesso, 200</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Usuário deve estar desconectado</li>
 <li>Utilizar configuração OAuth2</li>
 <li>Se todas as informações estiverem corretas, retornar url do redirecionamento da aplicação e status 200</li>
 </ul>
 
<b style="font-size:30px">POST/user/logout</b>

<b>Saída:</b>
 
 <ul>
 <li>Delogado, 202</li>
 </ul>
 
<b>Regras de negócio:</b>
<ul>
 <li>Limpa os dados da sessão: token e validações de login</li>
 </ul>

<b style="font-size:30px">GET/user/callback</b>

<b>Sem parametros de entrada</b>

<b>Saída:</b>
 
 <ul>
 <li>Redirecionamento</li>
 <li>Cadastro do usuário, caso não seja cadastrado</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Verificar se o email recebido está cadastrado no banco de dados, senão cadastrar</li>
 <li>Redirecionar após validação dos valores enviados da url e do client do backend</li> 

 </ul>
 

<b style="font-size:30px">POST/user/login</b>

<b>Parametros de entrada:</b>
<ul>
 <li>email (obrigatório)</li>
 <li>password  (obrigatório)</li>
 </ul>
 
 <b>Saída:</b>
 
 <ul>
 <li>Sucesso, 200 (token)</li>
 <li>Error, 400</li>
 <li>Error, 401</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Usuário deve estar desconectado</li>
 <li>Todos os campos obrigatórios preenchidos</li>
 <li>O email deve existir no banco</li> 
 <li>Se Password estiver errado, retornar erro ao efetuar login</li>
 <li>Se todas as informações estiverem corretas, retornar token e status 200</li>
 </ul>

<b style="font-size:30px">GET/user</b>

<b>Parametros de entrada:</b>
<ul>
 <li>Name (Opcional)</li>
 </ul>
 
 <b>Saída:</b>
 
 <ul>
 <li>Sucesso, 200 (OK)</li>
 <li>Error, 204 (No content)</li>
 <li>Error premission, 403 (forbidden)</li>
 </ul>
 
 <b>Regras de negócio:</b>
<ul>
 <li>Permissão READ</li>
 <li>Retornar todos os usuários tenham o mesmo nome (usar like)</li>
 <li>Se não tiver parametros retornar todos os usuários de acordo com páginação</li>
 <li>Utilizar paginação, retornando 20 usuários por página</li>
 <li>Se nenhum resultado status 204 (No content)</li>
 <li>Se encontrado o resultado retornar em JSON contendo: id, nome, email, phone, role.name e Status 200 (OK)</li>
 </ul>
 

Utilizamos oSwagger para a documentação dos endpoints para acessar <a href="http://localhost:5000/apidocs/" target="_blank">http://localhost:5000/apidocs/</a>

# Tecnologias utilizadas:

<p align="center">
<img width="70px" height="70px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original-wordmark.svg" />
<img width="65px" height="65px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original-wordmark.svg" />
<img width="70px" height="70px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" />
<img width="65px" height="65px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original-wordmark.svg" />
<img width="65px" height="65px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/trello/trello-plain-wordmark.svg" />
<img width="65px" height="65px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original-wordmark.svg" />
</p>

# Desenvolvedores - DEVinSanes:

Somos os DEVinSanes, time de desenvolvedores full-stak, desenvolvemos o projeto DEVinventory.

# Redes Sociais:

<ul>
<li><a href="https://www.linkedin.com/in/adriano-matos-meier/" target="_blank"><i>Adriano Matos Meier</i></a></li>
<li><a href="https://www.linkedin.com/in/bruno-v-bedretchuk-b0ab3122a/" target="_blank"><i>Bruno Vinicius Bedretchuk</i></a></li>
<li><a href="https://www.linkedin.com/in/edumrib/" target="_blank"><i>Eduardo Martins Ribeiro</i></a></li>
<li><a href="https://www.linkedin.com/in/julia-m-9abba9110/" target="_blank"><i>Julia Moura</i></a></li>
<li><a href="https://www.linkedin.com/in/kau%C3%A3-kirchner-de-souza-4b8327219/" target="_blank"><i>Kauã Kirchner de Souza</i></a></li>
<li><a href="https://www.linkedin.com/in/mayconrcampos/" target="_blank"><i>Maycon Campos</i></a></li>
<li><a href="https://www.linkedin.com/in/wellyngton-caetano-dos-santos/" target="_blank"><i>Wellyngton Santos</i></a></li>
</ul>

# Referências:

<ul>
<li><a href="https://flask.palletsprojects.com/en/2.2.x/" target="_blank">Flask</a></li>
<li><a href="https://python-poetry.org/docs/" target="_blank">Poetry</a></li>
<li><a href="https://github.com/flasgger/flasgger#installation" target="_blank">Swagger</a></li>
<li><a href="https://flask-marshmallow.readthedocs.io/en/latest/" target="_blank">Flask-marshmallow</a></li>
<li><a href="https://developers.google.com/identity/protocols/oauth2" target="_blank">Google-Auth</a></li>
<li><a href="https://jwt.io/" target="_blank">JWT</a></li>
  </ul>
