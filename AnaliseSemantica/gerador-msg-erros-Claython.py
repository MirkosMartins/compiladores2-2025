

codigo = input("Digite o codigo: ")

if codigo.find("++") != -1:
    print(f"A variavel {codigo[:-2]} não é do tipo inteiro")
else:
    split = codigo.split("=")
    try:
        numero = int(codigo[:-1])
        print(f"A variavel do tipo {split[0]} não é do tipo inteiro")
    except:
        if split[1].find("(") != -1 and split[1].find(")") != -1:
            nome_funcao = split[1].split("(")[0]
            print(f"A função {nome_funcao} espera um parametro do tipo '__' e foi passado do tipo '___'.")
            print(f"O retorno da função {nome_funcao} não é do mesmo tipo de {split[0]}")
        else:
            print(f"A variavel {split[0]} não é do mesmo tipo de {split[1]}")