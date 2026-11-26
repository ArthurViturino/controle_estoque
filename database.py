# Bibliotecas.
import sqlite3
import json
import hashlib
from datetime import datetime
SINCRONIZACAO_REALIZADA = "sincronizacao_realizada"
CONTINUAR_DADOS_ANTIGOS = "continuar_dados_antigos"
ENCERRAR_SISTEMA = "encerrar_sistema"

conexao = sqlite3.connect("estoque.db")
conexao.execute("PRAGMA foreign_keys = ON")

def carregar_dados_json():
    with open("estoque.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados

# Criação das tabelas.
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        proximo_numero INTEGER NOT NULL DEFAULT 1
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
        preco REAL NOT NULL CHECK (preco > 0),
        categoria_id INTEGER NOT NULL,
        codigo_produto TEXT UNIQUE,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL CHECK (quantidade > 0),
        tipo_movimentacao TEXT NOT NULL CHECK (
            tipo_movimentacao IN ('entrada', 'saida')
        ),
        data_movimentacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sincronizacao(
        id_sincronizacao INTEGER PRIMARY KEY AUTOINCREMENT,
        hash_anterior TEXT,
        data_ultima_atualizacao TEXT
    )
""")

def atualizar_estrutura_banco():
    cursor.execute("PRAGMA table_info(categorias)")
    colunas_categorias = [coluna[1] for coluna in cursor.fetchall()]

    if "proximo_numero" not in colunas_categorias:
        cursor.execute("""
            ALTER TABLE categorias
            ADD COLUMN proximo_numero INTEGER NOT NULL DEFAULT 1
        """)

    cursor.execute("PRAGMA table_info(produtos)")
    colunas_produtos = [coluna[1] for coluna in cursor.fetchall()]

    if "codigo_produto" not in colunas_produtos:
        cursor.execute("""
            ALTER TABLE produtos
            ADD COLUMN codigo_produto TEXT
        """)

    cursor.execute("PRAGMA table_info(sincronizacao)")
    colunas_sincronizacao = [
        coluna[1] for coluna in cursor.fetchall()
    ]

    if "id_sincronizacao" not in colunas_sincronizacao:
        cursor.execute("""
            ALTER TABLE sincronizacao
            ADD COLUMN id_sincronizacao INTEGER
        """)

        cursor.execute("""
            UPDATE sincronizacao
            SET id_sincronizacao = 1
            WHERE id_sincronizacao IS NULL
        """)
    conexao.commit()

atualizar_estrutura_banco()

# Carregamento e inserção dos produtos do arquivo JSON.
def processar_produtos():
    try:
        produtos = carregar_dados_json()
        for produto in produtos:
            nome = produto["nome"]
            categoria = produto["categoria"]

            cursor.execute(
                "SELECT id FROM categorias WHERE nome = ?",
                (categoria,)
            )
            categoria_encontrada = cursor.fetchone()

            if categoria_encontrada:
                produto["categoria_id"] = categoria_encontrada[0]
            else:
                cursor.execute(
                    "INSERT INTO categorias (nome) VALUES (?)",
                    (categoria,)
                )
                produto["categoria_id"] = cursor.lastrowid

            cursor.execute(
                "SELECT id FROM produtos WHERE nome = ?",
                (nome,)
            )
            produto_encontrado = cursor.fetchone()

            if produto_encontrado:
                cursor.execute(
                    """
                    UPDATE produtos
                    SET quantidade = ?, preco = ?
                    WHERE id = ?
                    """,
                    (
                        produto["quantidade"],
                        produto["preco"],
                        produto_encontrado[0]
                    )
                )
                print(f"Produto '{nome}' atualizado com sucesso.")
            else:
                cursor.execute(
                    "SELECT proximo_numero FROM categorias WHERE id = ?",
                    (produto["categoria_id"],)
                )
                proximo_numero = cursor.fetchone()[0]
                produto["codigo_produto"] = f"{produto['categoria_id']}.{proximo_numero}"
                cursor.execute(
                    "UPDATE categorias SET proximo_numero = ? WHERE id = ?",
                    (proximo_numero + 1, produto["categoria_id"])
                )
                cursor.execute(
                    """
                    INSERT INTO produtos (nome, quantidade, preco, categoria_id, codigo_produto)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        produto["nome"],
                        produto["quantidade"],
                        produto["preco"],
                        produto["categoria_id"],
                        produto["codigo_produto"],
                    )
                )

    except Exception as e:
        print(f"Erro ao processar produtos: {e}")
        conexao.rollback()
        raise

# Verificação de versão.
def verificar_sincronizacao():
    try:
        dados_atuais = carregar_dados_json()
        dados_serializados = json.dumps(
            dados_atuais,
            ensure_ascii=False,
            sort_keys=True
        )
        dados_bytes = dados_serializados.encode("utf-8")
        hash_atual = hashlib.sha256(dados_bytes).hexdigest()

        cursor.execute("SELECT hash_anterior, data_ultima_atualizacao FROM sincronizacao")
        ultima_sincronizacao = cursor.fetchone()
        respostas_positivas = ["s", "sim", "ss"]
        respostas_negativas = ["n", "não", "nao", "nn"]
        if ultima_sincronizacao is None:
            resposta_sincronizacao = input("É a primeira sincronização do sistema, Deseja sincronizar os dados? (s/n): ")

            while resposta_sincronizacao.strip().lower() not in respostas_positivas and resposta_sincronizacao.strip().lower() not in respostas_negativas:
                print("Digite uma opção válida.")
                resposta_sincronizacao = input("É a primeira sincronização do sistema, Deseja sincronizar os dados? (s/n): ")

            if resposta_sincronizacao.strip().lower() in respostas_positivas:
                processar_produtos()
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    """
                    INSERT INTO sincronizacao (hash_anterior, data_ultima_atualizacao)
                    VALUES (?, ?)
                    """,
                    (hash_atual, data_atual)
                )
                conexao.commit()
                return SINCRONIZACAO_REALIZADA
            elif resposta_sincronizacao.strip().lower() in respostas_negativas:
                print("Sincronização cancelada.")
                return ENCERRAR_SISTEMA
        else:
            if hash_atual != ultima_sincronizacao[0]:
                resposta_sincronizacao = input("Você deseja atualizar o banco de dados? (s/n):")
                while resposta_sincronizacao.strip().lower() not in respostas_positivas and resposta_sincronizacao.strip().lower() not in respostas_negativas:
                    print("Digite uma opção válida.")
                    resposta_sincronizacao = input("Você deseja atualizar o banco de dados? (s/n):")

                if resposta_sincronizacao.strip().lower() in respostas_positivas:
                    processar_produtos()
                    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        """
                        UPDATE sincronizacao
                        SET hash_anterior = ?, data_ultima_atualizacao = ?
                        WHERE id_sincronizacao = ?
                        """,
                        (hash_atual, data_atual, 1)
                    )
                    conexao.commit()
                    return SINCRONIZACAO_REALIZADA
                elif resposta_sincronizacao.strip().lower() in respostas_negativas:
                    print("Sincronização cancelada.")
                    continuar_sistema = input("Deseja continuar usando os dados antigos do SQL? (s/n):")

                    while continuar_sistema.strip().lower() not in respostas_positivas and continuar_sistema.strip().lower() not in respostas_negativas:
                        print("Digite uma opção válida.")
                        continuar_sistema = input("Deseja continuar usando os dados antigos do SQL? (s/n):")

                    if continuar_sistema.strip().lower() in respostas_positivas:
                        print(f"O sistema continuará utilizando dados do SQL, a data da última atualização é {ultima_sincronizacao[1]}.")
                        return CONTINUAR_DADOS_ANTIGOS
                    elif continuar_sistema.strip().lower() in respostas_negativas:
                        print("Você optou por não continuar utilizando os dados antigos, o sistema vai ser encerrado.")
                        return ENCERRAR_SISTEMA
            else:
                print("Hashes iguais: Nenhuma alteração será feita.")
                return SINCRONIZACAO_REALIZADA

    except Exception as e:
        print(f"Erro ao verificar sincronização: {e}")
        conexao.rollback()
        raise

def consulta_produtos():
    cursor.execute("""
        SELECT
            produtos.id,
            produtos.nome,
            produtos.quantidade,
            produtos.preco,
            produtos.codigo_produto,
            categorias.nome AS categoria
        FROM produtos
        INNER JOIN categorias
            ON produtos.categoria_id = categorias.id
    """)

    resultados = cursor.fetchall()
    produtos = []

    for registro in resultados:
        produto = {
            "id": registro[0],
            "nome": registro[1],
            "quantidade": registro[2],
            "preco": registro[3],
            "codigo_produto": registro[4],
            "categoria": registro[5]
        }

        produtos.append(produto)
    return produtos