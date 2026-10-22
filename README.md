
# Exercício: Jogo de RPG em Python com Banco de Dados
**Programação em Python — Ensino Médio IFSC**

## Objetivo
Completar o sistema de cadastro de um jogo de RPG escrito em Python. Ele guarda jogadores, personagens, classes, itens e o inventário de cada personagem em um banco de dados. Você vai aprender a criar uma conexão com o banco, incluir registros, buscar por id e por nome e listar tudo usando comandos SQL.

*   **Duração:** cerca de 90 min (Partes 1 a 4) + 15 a 20 min de desafio (Parte 5).
*   **Entrega:** Disponibilize o link do seu repositório do github (`(https://github.com)`), com os arquivos `.py` completos, e as respostas às perguntas Q1-Q13. (opcional) 

## O que você precisa
Python 3 e um editor. Recomendamos o **VS Code (Visual Studio Code)**. O banco de dados é o **SQLite**, que já faz parte do Python: não é preciso instalar nada. O professor vai fornecer o arquivo `rpg_aluno.zip` com estes arquivos:

| Arquivo | O que faz | Situação |
| :--- | :--- | :--- |
| `main.py` | Programa principal: abre a conexão com o banco e mostra o menu | pronto |
| `banco.py` | Cria o arquivo do banco e as 5 tabelas; tem dados de exemplo | pronto |
| `classes.py` | Funções da tabela classes (Guerreiro, Mago...) - é o arquivo-modelo | pronto |
| `jogadores.py`<br>`itens.py`<br>`personagens.py` | Funções das tabelas jogadores e itens<br>Funções da tabela personagens (usa JOIN) | você completa (Parte 3)<br>você completa (Parte 4) |
| `inventario.py` | Funções da tabela inventario | desafio (Parte 5) |

Em todos os arquivos de tabela existem as mesmas 4 funções. Toda função recebe a conexão `conn` como primeiro parâmetro (quem cria a conexão é o `main.py`):

| Função | Comando SQL | Devolve |
| :--- | :--- | :--- |
| `incluir(conn, ...)` | `INSERT INTO ... VALUES (?, ?)` | o id gerado (`cursor.lastrowid`) |
| `buscar_por_id(conn, id)` | `SELECT... WHERE id = ?` | uma linha, ou `None` (`fetchone`) |
| `buscar_por_nome(conn, nome)` | `SELECT ... WHERE nome LIKE ?` | uma lista de linhas (`fetchall`) |
| `listar(conn)` | `SELECT ... ORDER BY id` | uma lista de linhas (`fetchall`) |

---

## Parte 1: Conhecer e rodar o projeto (15 min)

1. Descompacte o `rpg_aluno.zip`. Todos os arquivos `.py` precisam ficar na mesma pasta.
2. Abra a pasta do projeto no **VS Code**. Abra o arquivo `main.py` e execute o arquivo (clicando no botão de *Play* no canto superior direito ou usando o atalho configurado no seu terminal). O menu aparecerá no terminal integrado: digite o número da opção e tecle Enter.
3. Escolha `6 - Carregar dados de exemplo`. Depois entre em `1 - Classes` e escolha `4 - Listar todos`.
4. Entre em `2 - Jogadores` e tente listar. Vai aparecer o aviso de que a função ainda não foi implementada: é você quem vai escrevê-la.
5. Saia do programa (opção `0`) e abra o arquivo `banco.py`. Leia a função `criar_tabelas`.

### Modelagem do Banco de Dados (As 5 tabelas e suas ligações)

Use o código com cuidado.
[jogadores]                   [personagens]                 [inventario]
┌───────────┐                 ┌──────────────┐              ┌────────────────┐
│ id     PK │◄──────┐         │ id        PK │◄──────────── │ id          PK │
│ nome      │       └─────────┤ jogador_id FK│              │ personagem_id FK│
│ apelido   │                 │ classe_id  FK├────────┐     │ item_id     FK │
└───────────┘                 │ nome         │        │     │ quantidade     │
│ nivel        │        │     └────────────────┘
[classes]                     └──────────────┘        │
┌───────────┐                                         │     [itens]
│ id     PK │◄────────────────────────────────────────┘     ┌────────────────┐
│ nome      │                                               │ id          PK │
└───────────┘                                               │ nome           │
│ tipo           │
│ poder          │
└────────────────┘
* **PK** = Chave Primária | **FK** = Chave Estrangeira (a seta aponta para a tabela de onde vem o id).

*   **Chave primária (PK):** a coluna `id`, um número que identifica cada linha. Dois personagens nunca têm o mesmo id.
*   **Chave estrangeira (FK):** uma coluna que guarda o id de uma linha de outra tabela. Por exemplo, `personagens.classe_id = 2` quer dizer que o personagem é da classe de id 2 (Mago).
*   Cada jogador (a pessoa) pode ter vários personagens, e cada linha do inventário diz que um personagem carrega um item.

### Questões da Parte 1
*   **Q1.** Depois de rodar o programa, apareceu um arquivo novo na pasta. Qual é o nome dele e o que ele guarda? O que acontece com os dados quando você fecha e abre o programa de novo?
*   **Q2.** Quais são as 5 tabelas do banco? Quais colunas tem a tabela personagens?
*   **Q3.** No `banco.py`, o id de cada tabela é `INTEGER PRIMARY KEY AUTOINCREMENT`. O que isso significa? Por que o programa não pede o id quando incluímos um registro?

---

## Parte 2: Estudar o arquivo-modelo `classes.py` (15 min)

Este é o arquivo que você vai usar como exemplo para escrever os outros. Leia com atenção:

```python
# classes.py (sem os comentários de documentação)

def incluir(conn, nome):
    cursor = conn.execute("INSERT INTO classes (nome) VALUES (?)", (nome,))
    conn.commit() # grava de verdade no arquivo
    return cursor.lastrowid

def buscar_por_id(conn, id):
    cursor = conn.execute("SELECT id, nome FROM classes WHERE id = ?", (id,))
    return cursor.fetchone() # uma linha, ou None se não existir

def buscar_por_nome(conn, nome):
    cursor = conn.execute(
        "SELECT id, nome FROM classes WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",)
    )
    return cursor.fetchall() # lista de linhas

def listar(conn):
    cursor = conn.execute("SELECT id, nome FROM classes ORDER BY id")
    return cursor.fetchall() # lista de linhas
```

1. Rode o programa. Em Classes, inclua a classe Ladino (opção 1).
2. Busque por id (opção 2) o número que o programa mostrou. Depois busque um id que não existe, como 99.
3. Busque por nome (opção 3) o texto `ro`.

> ⚠️ **Atenção à vírgula:** `(nome,)` é uma tupla com um elemento. Sem a vírgula, `(nome)` é só o texto entre parênteses, e o Python apresentará o erro `Incorrect number of bindings supplied` porque o SQLite trata cada letra do texto como um valor separado.

### Questões da Parte 2
*   **Q4.** Que id a classe Ladino recebeu? Em qual linha do incluir esse número é obtido?
*   **Q5.** Qual a diferença entre `fetchone()` e `fetchall()`? Por que `buscar_por_id` usa um e `buscar_por_nome` usa o outro?
*   **Q6.** Quais classes apareceram na busca por "ro"? Para que servem os sinais `%` no `LIKE`?
*   **Q7.** Nos comandos SQL usamos `?` e passamos os valores separados, numa tupla. Por que não montamos o comando juntando textos, como `"VALUES ('" + nome + "')"`?
*   **Q8.** O que aconteceria se apagássemos a linha `conn.commit()` da função incluir?

---

## Parte 3: Escrever `jogadores.py` e `itens.py` (25 min)

1. Abra o `jogadores.py`. As 4 funções já têm nome, parâmetros e uma explicação do que devem devolver, mas o corpo é só `raise NotImplementedError`.
2. Escreva o código de cada função seguindo o modelo do `classes.py`. A tabela jogadores tem as colunas `id`, `nome`, `apelido`. Apague a linha `raise NotImplementedError` de cada função que completar.
3. Rode o programa e teste as 4 opções do menu Jogadores. Cadastre você mesmo como jogador, com o seu apelido de jogo, e anote o id que recebeu: você vai usá-lo na Parte 4.
4. Faça o mesmo com o `itens.py` (colunas `id`, `nome`, `tipo`, `poder`). Inclua um item inventado por você, por exemplo `Machado de Gelo`, tipo `Arma`, poder `40`, e anote o id.

### Questões da Parte 3
*   **Q9.** Busque os itens com o texto `poção` e depois com `POÇÃO`. Os resultados foram iguais? Por que você acha que isso aconteceu?

---

## Parte 4: `personagens.py`: chave estrangeira e JOIN (20 min)

A tabela personagens não guarda o apelido do jogador, só o `jogador_id`. Mas na tela queremos mostrar o apelido. Para isso usamos o `JOIN`, que junta as linhas de duas tabelas quando os ids combinam:

*Exemplo: nome de cada personagem com o apelido do jogador dono dele*
```sql
SELECT personagens.nome, jogadores.apelido
FROM personagens
JOIN jogadores ON jogadores.id = personagens.jogador_id
```
> *Lê-se:* "para cada personagem, encontre o jogador cujo id é igual ao `jogador_id` do personagem". Quando há colunas com o mesmo nome em duas tabelas (como nome e id, que existem em personagens, jogadores e classes), escrevemos `tabela.coluna`.

1. No `personagens.py`, a variável `CONSULTA` já tem o `JOIN` com jogadores. Acrescente o `JOIN` com classes (a dica está no comentário).
2. Complete as 4 funções. As três consultas usam `CONSULTA` + o final do comando, por exemplo: `conn.execute(CONSULTA + " WHERE personagens.id = ?", (id,))`. A busca por nome procura em `personagens.nome`.
3. Teste: liste os personagens. Depois crie o seu personagem: escolha um nome, nível 1, o seu id de jogador (Parte 3) e uma classe (por exemplo, Ladino, id 5).
4. Agora tente criar um personagem com id do jogador = 99.

### Questões da Parte 4
*   **Q10.** O que aconteceu ao tentar criar um personagem para o jogador de id 99? Quem impediu a inclusão: o seu código Python ou o banco de dados?
*   **Q11.** Por que a tabela personagens guarda o id do jogador, e não o apelido dele escrito por extenso?

---

## Parte 5: Desafio: `inventario.py` (15 a 20 min)

1. Escreva a `CONSULTA` do `inventario.py`. Ela precisa de dois `JOINS` (com personagens e com itens) e deve devolver as colunas nesta ordem: id da linha do inventário, nome do personagem, nome do item, tipo do item, quantidade.
2. Complete as 4 funções. Aqui a busca por nome procura pelo nome do personagem, para ver tudo o que ele carrega.
3. Teste: liste o inventário, busque por "gork" e coloque o item que você criou na Parte 3 no inventário do seu personagem.

### Questões da Parte 5
*   **Q12.** Quais itens o personagem Gork carrega, e em que quantidade?
*   **Q13.** Que outra função deixaria o jogo mais completo? Escreva o comando SQL que ela usaria.

