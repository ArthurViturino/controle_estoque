#v1.4 - Sistema de Controle de Estoque em Python

# Bibliotecas.
import unicodedata

def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", texto)

    texto_sem_acentos = ""

    for caractere in texto:
        if unicodedata.category(caractere) != "Mn":
            texto_sem_acentos += caractere

    return texto_sem_acentos.lower().strip()

estoque_produtos = [
    {
        "nome": "Notebook",
        "quantidade": 10,
        "preco": 3500.00,
        "categoria": "Informática"
    },
    {
        "nome": "Mouse",
        "quantidade": 25,
        "preco": 89.90,
        "categoria": "Periféricos"
    },
    {
        "nome": "Teclado",
        "quantidade": 15,
        "preco": 150.50,
        "categoria": "Periféricos"
    },
    {
        "nome": "Monitor",
        "quantidade": 8,
        "preco": 1200.00,
        "categoria": "Informática"
    },
    {
        "nome": "Impressora",
        "quantidade": 5,
        "preco": 800.00,
        "categoria": "Impressoras"
    }
]

# Menu principal do sistema.
def exibir_menu():

    print("\n=== Sistema de Controle de Estoque ===")
    print("0 - Encerrar o sistema")
    print("1 - Visualizar Estoque Atual")
    print("2 - Registrar Entrada de Produto")
    print("3 - Registrar Saída de Produto")
    print("4 - Gerenciar Produtos")

    opcao_usuario = input("Escolha uma opção: ")

    return opcao_usuario

# Submenu de visualização do estoque.
def menu_visualizacao(estoque_produtos):
    while True:
        print("\n=== Visualizar Estoque ===")
        print("0 - Encerrar o sistema")
        print("1 - Visualizar todos os produtos")
        print("2 - Filtrar por categoria")
        print("3 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Encerrando o sistema...")
            return True

        elif opcao == "1":
            visualizar_estoque(estoque_produtos)

        elif opcao == "2":
            if menu_categorias(estoque_produtos):
                return True

        elif opcao == "3":
            return False

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Submenu de gerenciamento de produtos.
def gerenciamento_produtos(estoque_produtos):
    while True:
        print("\n=== Gerenciamento de Produtos ===")
        print("0 - Voltar ao menu principal")
        print("1 - Cadastrar novo produto")
        print("2 - Excluir produto")
        print("3 - Pesquisar produto")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Voltando ao menu principal...")
            return False

        elif opcao == "1":
            cadastrar_produto(estoque_produtos)

        elif opcao == "2":
            excluir_produto(estoque_produtos)

        elif opcao == "3":
            pesquisar_produto(estoque_produtos)

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Menu principal, opção 1 - Visualizar estoque.
def visualizar_estoque(estoque_produtos):
    print("\n" + "=== Estoque Atual ===".center(69))
    print("\n")

    if not estoque_produtos:
        print("Não há produtos cadastrados no estoque.".center(69))
        return

    valor_total_estoque = 0

    print(f"{'Produto':<15}{'Quantidade':^12}{'Preço':>12}{'Categoria':>15}{'Valor Total':>15}")
    print("-" * 70)

    for produto in estoque_produtos:
        print(f"{produto['nome']:<15}{produto['quantidade']:^12}{produto['preco']:>12.2f}{produto['categoria']:>16}{produto['quantidade'] * produto['preco']:>13.2f}")
        valor_total_estoque += produto['quantidade'] * produto['preco']

    print("-" * 70)
    print(f"Valor total do estoque: R${valor_total_estoque:.2f}")

# Menu principal, opção 2 - Registrar entrada de produto.
def registrar_entrada(estoque_produtos):
    print("\n=== Registrar Entrada de Produto ===")

    while True:
        nome_produto = input("Digite o nome do produto (ou 0 para voltar): ").strip()

        if nome_produto == "0":
            print("Operação cancelada. Voltando ao menu principal...")
            return

        produto_encontrado = None
        for produto in estoque_produtos:
            if normalizar_texto(produto["nome"]) == normalizar_texto(nome_produto):
                produto_encontrado = produto
                break

        if produto_encontrado is None:
            print("Produto não encontrado.")
            continue

        while True:
            try:
                quantidade_entrada = int(input("Digite a quantidade de entrada (ou 0 para voltar): "))
            except ValueError:
                print("Digite um número inteiro válido.")
                continue

            if quantidade_entrada == 0:
                print("Operação cancelada. Voltando ao menu principal...")
                return

            if quantidade_entrada <= 0:
                print("A quantidade deve ser maior que zero.")
                continue

            break

        produto_encontrado["quantidade"] += quantidade_entrada
        print("Quantidade atualizada com sucesso.")
        break

# Menu principal, opção 3 - Registrar saída de produto.
def registrar_saida(estoque_produtos):
    print("\n=== Registrar Saída de Produto ===")

    while True:
        nome_produto = input("Digite o nome do produto (ou 0 para voltar): ").strip()

        if nome_produto == "0":
            print("Operação cancelada. Voltando ao menu principal...")
            return

        produto_encontrado = None
        for produto in estoque_produtos:
            if normalizar_texto(produto["nome"]) == normalizar_texto(nome_produto):
                produto_encontrado = produto
                break

        if produto_encontrado is None:
            print("Produto não encontrado.")
            continue

        while True:
            try:
                quantidade_saida = int(input("Digite a quantidade de saída (ou 0 para voltar): "))
            except ValueError:
                print("Digite um número inteiro válido.")
                continue

            if quantidade_saida == 0:
                print("Operação cancelada. Voltando ao menu principal...")
                return

            if quantidade_saida <= 0:
                print("A quantidade deve ser maior que zero.")
                continue

            if quantidade_saida > produto_encontrado["quantidade"]:
                print("Quantidade insuficiente em estoque.")
                continue

            break

        produto_encontrado["quantidade"] -= quantidade_saida
        print("Quantidade atualizada com sucesso.")
        break

# Filtrar por categoria.
def menu_categorias(estoque_produtos):
    if not estoque_produtos:
        print("\n" + "=== Categorias ===".center(69))
        print("Não existem categorias cadastradas.".center(69))
        return False

    categorias_produtos = []

    for produto in estoque_produtos:
        categoria = produto["categoria"]

        if categoria not in categorias_produtos:
            categorias_produtos.append(categoria)

    while True:
        print("\n" + "=== Categorias ===".center(69))
        print("0 - Encerrar o sistema")

        for indice, categoria in enumerate(categorias_produtos, start=1):
            print(f"{indice} - {categoria}")

        print(f"{len(categorias_produtos) + 1} - Voltar")

        try:
            opcao_categoria = int(input("Escolha uma categoria: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao_categoria == 0:
            print("Encerrando o sistema...")
            return True

        if opcao_categoria == len(categorias_produtos) + 1:
            return False

        if opcao_categoria < 1 or opcao_categoria > len(categorias_produtos):
            print("Escolha uma categoria válida.")
            continue

        categoria_escolhida = categorias_produtos[opcao_categoria - 1]
        break

    produtos_filtrados = []

    for produto in estoque_produtos:
        if produto["categoria"] == categoria_escolhida:
            produtos_filtrados.append(produto)

    visualizar_estoque(produtos_filtrados)
    return False

# Submenu de cadastro de produto.
def cadastrar_produto(estoque_produtos):
    print("\n" + "=== Cadastrar Novo Produto ===".center(69))

    while True:
        nome_cadastro = input("Digite o nome do produto (ou 0 para voltar): ").strip()

        if nome_cadastro == "0":
            print("Cadastro cancelado. Voltando ao menu de gerenciamento...")
            return

        elif not nome_cadastro:
            print("Preencha o nome do produto.")
            continue

        produto_existente = False
        for produto in estoque_produtos:
            if normalizar_texto(produto["nome"]) == normalizar_texto(nome_cadastro):
                produto_existente = True
                break
            
        if produto_existente is True:
            print("Produto já cadastrado.")
            continue
        break

    while True:
        try:
            quantidade_cadastro = int(input("Digite a quantidade do produto: "))
        except ValueError:
            print("Digite um número inteiro válido.")
            continue
        if quantidade_cadastro < 0:
            print("A quantidade não pode ser negativa.")
            continue
        break

    while True:
        try:
            preco_cadastro = float(input("Digite o preço do produto: "))
        except ValueError:
            print("Digite um número válido.")
            continue
        if preco_cadastro <= 0:
            print("O preço não pode ser zero ou negativo.")
            continue
        break

    while True:
        categoria_cadastro = input("Digite a categoria do produto: ").strip()
        if not categoria_cadastro:
            print("Preencha a categoria do produto.")
            continue

        for produto in estoque_produtos:
            if normalizar_texto(produto["categoria"]) == normalizar_texto(categoria_cadastro):
                categoria_cadastro = produto["categoria"]
                print(f"Categoria já cadastrada. Utilizando categoria existente: {categoria_cadastro}")
                break

        break

    novo_produto = {
        "nome": nome_cadastro,
        "quantidade": quantidade_cadastro,
        "preco": preco_cadastro,
        "categoria": categoria_cadastro
    }

    print("\n" + "=== Confirmação de Cadastro ===".center(69))
    print(f"Nome: {novo_produto['nome']}")
    print(f"Quantidade: {novo_produto['quantidade']}")
    print(f"Preço: R$ {novo_produto['preco']:.2f}")
    print(f"Categoria: {novo_produto['categoria']}")
    print("\n")
    print("0 - Confirmar cadastro")
    print("1 - Cancelar e voltar")

    while True:
        try:
            opcao_confirmacao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue
        if opcao_confirmacao not in [0, 1]:
            print("Escolha uma opção válida.")
            continue

        if opcao_confirmacao == 0:
            estoque_produtos.append(novo_produto)
            print("Produto cadastrado com sucesso.")
        elif opcao_confirmacao == 1:
            print("Cadastro cancelado.")
        break

# Loop de suporte para o sistema principal.
while True:
    opcao_usuario = exibir_menu()

    if opcao_usuario == "1":
        if menu_visualizacao(estoque_produtos):
            break

    elif opcao_usuario == "2":
        registrar_entrada(estoque_produtos)

    elif opcao_usuario == "3":
        registrar_saida(estoque_produtos)

    elif opcao_usuario == "4":
        if gerenciamento_produtos(estoque_produtos):
            break

    elif opcao_usuario == "0":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")