import re

variavel = input("digite uma atribuição\n")

if "++" in variavel:
    antes = variavel.split("++")[0]
    print("A variável", antes, "não é do tipo int/float")

else:
    partes = re.split(r"[=;]", variavel)
    antes = partes[0].strip()
    depois = partes[1].strip()

    if "(" in depois and ")" in depois:
        print("Possíveis erros:")
        print("O parâmetro pode não ser do tipo esperado")
        print("A função pode retornar um tipo diferente do esperado")
    else:
        print("A variável", antes, "não é do tipo de", depois)
