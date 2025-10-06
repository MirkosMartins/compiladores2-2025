tabela_de_simbolos = {}
while True:
    comando_str = input("> ")
    partes = comando_str.strip().split()

    if not partes:
        continue
    if partes[0] == 'sair':
        print("Finalizando.")
        break

    if len(partes) == 2 and partes[0] in ['int', 'float', 'char', 'double','string']:
        tipo_var = partes[0]
        nome_var = partes[1]
        
        if nome_var in tabela_de_simbolos:
            print(f"  ERRO SEMÂNTICO: Variável '{nome_var}' já foi declarada.\n")
        else:
            tabela_de_simbolos[nome_var] = {'tipo': tipo_var}
            print(f"  '{nome_var}' declarada com o tipo '{tipo_var}'.\n")
        continue

    if len(partes) == 3 and partes[1] == '=':
        var_destino = partes[0]
        var_origem = partes[2]

        if var_destino not in tabela_de_simbolos:
            print(f"  ERRO SEMÂNTICO: Variável de destino '{var_destino}' não foi declarada.\n")
            continue

        if var_origem not in tabela_de_simbolos:
            print(f"  ERRO SEMÂNTICO: Variável de origem '{var_origem}' não foi declarada.\n")
            continue
            
        tipo_destino = tabela_de_simbolos[var_destino]['tipo']
        tipo_origem = tabela_de_simbolos[var_origem]['tipo']

        if tipo_destino == tipo_origem:
            print(f"  Atribuição válida. Tipos compatíveis ('{tipo_destino}').\n")
        else:
            print(f"  ERRO SEMÂNTICO: Incompatibilidade de tipos")
            print(f"                 A variável '{var_origem}' não é do mesmo tipo que '{var_destino}'.\n")
        continue

    print("  Comando inválido. Tente novamente.\n")