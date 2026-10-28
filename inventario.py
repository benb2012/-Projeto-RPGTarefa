
"""
inventario.py - Funções da tabela INVENTARIO.

Colunas: id, personagem_id, item_id, quantidade
"""

CONSULTA = """
    SELECT inventario.id, personagens.nome, itens.nome,
           itens.tipo, inventario.quantidade
    FROM inventario
    JOIN personagens ON personagens.id = inventario.personagem_id
    JOIN itens ON itens.id = inventario.item_id
"""


def incluir(conn, personagem_id, item_id, quantidade):
    """Coloca um item no inventário de um personagem e devolve o id gerado."""
    cursor = conn.execute(
        "INSERT INTO inventario (personagem_id, item_id, quantidade) VALUES (?, ?, ?)",
        (personagem_id, item_id, quantidade)
    )
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    """Devolve UMA linha, ou None."""
    cursor = conn.execute(
        CONSULTA + " WHERE inventario.id = ?", (id,)
    )
    return cursor.fetchone()


def buscar_por_nome(conn, nome_personagem):
    """Devolve uma LISTA com os itens dos personagens cujo nome contém o texto."""
    cursor = conn.execute(
        CONSULTA + " WHERE personagens.nome LIKE ? ORDER BY inventario.id",
        ("%" + nome_personagem + "%",)
    )
    return cursor.fetchall()


def listar(conn):
    """Devolve uma LISTA com todo o inventário."""
    cursor = conn.execute(CONSULTA + " ORDER BY inventario.id")
    return cursor.fetchall()
