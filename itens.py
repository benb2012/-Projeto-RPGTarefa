"""
itens.py - Funções da tabela ITENS (armas, poções, armaduras...).

Colunas: id, nome, tipo, poder

TAREFA: complete as 4 funções. Use o arquivo classes.py como modelo.
Apague a linha "raise NotImplementedError" quando escrever o código.
"""


def incluir(conn, nome, tipo, poder):
    """Insere um item e devolve o id gerado."""
    cursor = conn.execute("INSERT INTO itens (nome, tipo, poder) VALUES (?, ?, ?)", (nome, tipo, poder, ))
    conn.commit()                 # grava de verdade no arquivo
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Devolve UMA linha (id, nome, tipo, poder), ou None."""
    cursor = conn.execute("SELECT id, nome, tipo, poder FROM itens WHERE id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    """Devolve uma LISTA com os itens cujo nome contém o texto."""
    cursor = conn.execute(
            "SELECT id, nome, tipo, poder FROM itens WHERE nome LIKE ? ORDER BY nome",
            ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    """Devolve uma LISTA com todos os itens (id, nome, tipo, poder)."""
    cursor = conn.execute("SELECT id, nome, tipo, poder FROM itens ORDER BY id")
    return cursor.fetchall()
