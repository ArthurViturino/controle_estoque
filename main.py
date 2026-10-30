#v1 - Sistema de Controle de Estoque em Python

estoque_produtos = [
    {
        "nome": "Notebook",
        "quantidade": 10,
        "preco": 3500.00
    },
    {
        "nome": "Mouse",
        "quantidade": 25,
        "preco": 89.90
    },
    {
        "nome": "Teclado",
        "quantidade": 15,
        "preco": 150.50
    }
]

# Loop principal do sistema.
def exibir_menu():
    print("\n=== Sistema de Controle de Estoque ===")
    print("1 - Visualizar Estoque Atual")
    print("2 - Registrar Entrada de Produto")
    print("3 - Registrar Saída de Produto")
    print("4 - Sair do Sistema")

    opcao_usuario = input("Escolha uma opção: ")

    return opcao_usuario

while True:
    opcao_usuario = exibir_menu()

    if opcao_usuario == "4":
        print("Encerrando o sistema...")
        break


# Opção 1 - Visualizar estoque.
    if opcao_usuario == "1":
        print("\n=== Estoque Atual ===")

        for produto in estoque_produtos:
            print(f"Produto: {produto['nome']}")
            print(f"Quantidade: {produto['quantidade']}")
            print(f"Preço: R${produto['preco']:.2f}\n")

# Opção 2 - Registrar entrada de produto.
    elif opcao_usuario == "2":
        nome_produto = input("Digite o nome do produto: ")

        quantidade_entrada = int(input("Digite a quantidade de entrada: "))

        produto_encontrado = False

        for produto in estoque_produtos:
            if produto["nome"] == nome_produto:
                produto["quantidade"] += quantidade_entrada
                produto_encontrado = True

                print("Quantidade atualizada com sucesso.")
                break

        if not produto_encontrado:
            print("Produto não encontrado.")

# Opção 3 - Registrar saída de produto.
    elif opcao_usuario == "3":
        nome_produto = input("Digite o nome do produto: ")

        quantidade_saida = int(input("Digite a quantidade de saída: "))

        produto_encontrado = False

        for produto in estoque_produtos:
            if produto["nome"] == nome_produto:
                produto_encontrado = True

                if produto["quantidade"] >= quantidade_saida:
                    produto["quantidade"] -= quantidade_saida

                    print("Saída registrada com sucesso.")
                else:
                    print("Estoque insuficiente.")

                break

        if not produto_encontrado:
            print("Produto não encontrado.")

# Opção 4 - Encerrar o sistema.
    