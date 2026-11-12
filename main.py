#v1.2 - Sistema de Controle de Estoque em Python

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
    }
]

# Menu principal do sistema.
def exibir_menu():

    print("\n=== Sistema de Controle de Estoque ===")
    print("1 - Visualizar Estoque Atual")
    print("2 - Registrar Entrada de Produto")
    print("3 - Registrar Saída de Produto")
    print("4 - Sair do Sistema")

    opcao_usuario = input("Escolha uma opção: ")

    return opcao_usuario

# Menu de visualização do estoque.
def menu_visualizacao(estoque_produtos):
    while True:
        print("\n=== Visualizar Estoque ===")
        print("1 - Visualizar todos os produtos")
        print("2 - Filtrar por categoria")
        print("3 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizar_estoque(estoque_produtos)

        elif opcao == "2":
            menu_categorias(estoque_produtos)

        elif opcao == "3":
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Opção 1 - Visualizar estoque.
def visualizar_estoque(estoque_produtos):
    print("\n=== Estoque Atual ===")

    for produto in estoque_produtos:
        print(f"Produto: {produto['nome']}")
        print(f"Quantidade: {produto['quantidade']}")
        print(f"Preço: R${produto['preco']:.2f}")
        print(f"Categoria: {produto['categoria']}\n")

# Opção 2 - Registrar entrada de produto.
def registrar_entrada(estoque_produtos):
    print("\n=== Registrar Entrada de Produto ===")

    while True:
        nome_produto = input("Digite o nome do produto: ").strip()

        produto_encontrado = None
        for produto in estoque_produtos:
            if produto["nome"].lower() == nome_produto.lower():
                produto_encontrado = produto
                break

        if produto_encontrado is None:
            print("Produto não encontrado.")
            continue

        while True:
            try:
                quantidade_entrada = int(input("Digite a quantidade de entrada: "))
            except ValueError:
                print("Digite um número inteiro válido.")
                continue

            if quantidade_entrada <= 0:
                print("A quantidade deve ser maior que zero.")
                continue

            break

        produto_encontrado["quantidade"] += quantidade_entrada
        print("Quantidade atualizada com sucesso.")
        break

# Opção 3 - Registrar saída de produto.
def registrar_saida(estoque_produtos):
    print("\n=== Registrar Saída de Produto ===")

    while True:
        nome_produto = input("Digite o nome do produto: ").strip()

        produto_encontrado = None
        for produto in estoque_produtos:
            if produto["nome"].lower() == nome_produto.lower():
                produto_encontrado = produto
                break

        if produto_encontrado is None:
            print("Produto não encontrado.")
            continue

        while True:
            try:
                quantidade_saida = int(input("Digite a quantidade de saída: "))
            except ValueError:
                print("Digite um número inteiro válido.")
                continue

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

# Opção 2 - Filtrar por categoria.
def menu_categorias(estoque_produtos):
    categorias = {
        "1": "Informática",
        "2": "Periféricos"
    }

    while True:
        print("\n=== Categorias ===")
        print("1 - Informática")
        print("2 - Periféricos")
        print("3 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao in categorias:
            categoria = categorias[opcao]
            produtos_filtrados = [
                produto
                for produto in estoque_produtos
                if produto["categoria"] == categoria
            ]
            visualizar_estoque(produtos_filtrados)
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Loop de suporte para o sistema principal.
while True:
    opcao_usuario = exibir_menu()

    if opcao_usuario == "1":
        menu_visualizacao(estoque_produtos)

    elif opcao_usuario == "2":
        registrar_entrada(estoque_produtos)

    elif opcao_usuario == "3":
        registrar_saida(estoque_produtos)

    elif opcao_usuario == "4":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")