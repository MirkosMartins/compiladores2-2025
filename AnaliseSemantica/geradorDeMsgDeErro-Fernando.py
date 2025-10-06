def verificar_codigo(codigo):
    if "++" in codigo:
        print(f"A variável '{codigo[:-2].strip()}' não é do tipo inteiro.")
    elif "=" in codigo:
        split = codigo.split("=")
        if split[1].strip().isdigit():
            print(f"A variável '{split[0].strip()}' não é do tipo inteiro.")
        elif "função" in split[1]:
            print(f"A função 'função' não é do mesmo tipo da variável '{split[0].strip()}'.")
        else:
            print(f"A variável '{split[0].strip()}' não é do mesmo tipo de '{split[1].strip()}'.")
    else:
        print("Erro: Código inválido.")

# Solicitar ao usuário para digitar o código
codigo = input("Digite o código: ")

# Chama a função para verificar o código
verificar_codigo(codigo)
