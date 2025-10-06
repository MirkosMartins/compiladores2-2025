import re
import csv


funcoes = {
    "f": {"parametros": ["int"], "retorno": "float"},
    "g": {"parametros": ["float", "int"], "retorno": "bool"}
}


tabela_simbolos = {
    "x": "int",
    "y": "float",
    "banana": "string",
    "z": "int"
}


token_specification = [
    ("TIPO", r"\b(int|float|string|bool)\b"),
    ("IDENT", r"[a-zA-Z_]\w*"),
    ("NUM", r"\b\d+(\.\d+)?\b"),
    ("ATRIB", r"="),
    ("PV", r";"),
    ("VIRG", r","),
    ("ABRE_PAR", r"\("),
    ("FECHA_PAR", r"\)"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n")
]

token_regex = "|".join(
    f"(?P<{name}>{pattern})" for name, pattern in token_specification)


def lexer(code):
    tokens = []
    line_num = 1
    for m in re.finditer(token_regex, code):
        kind = m.lastgroup
        value = m.group()
        if kind == "NEWLINE":
            line_num += 1
        elif kind == "SKIP":
            continue
        else:
            tokens.append((kind, value, line_num))
    return tokens


def analisar_semantica(tokens, linhas_codigo):
    erros = []
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "IDENT" and i + 2 < len(tokens):
            var_dest = tokens[i][1]
            linha = tokens[i][2]

            if tokens[i + 1][0] == "ATRIB":
                tipo_dest = tabela_simbolos.get(var_dest)
                valor = tokens[i + 2][1]

                if tokens[i + 2][0] == "IDENT" and (i + 3 >= len(tokens) or tokens[i + 3][0] != "ABRE_PAR"):
                    tipo_valor = tabela_simbolos.get(valor)
                    if tipo_dest and tipo_valor and tipo_dest != tipo_valor:
                        erros.append((linhas_codigo[linha - 1].strip(),
                                      f"A variável {var_dest} não é do mesmo tipo que {valor}",
                                      linha))

                elif tokens[i + 2][0] == "NUM":
                    tipo_valor = "float" if "." in valor else "int"
                    if tipo_dest and tipo_dest != tipo_valor:
                        erros.append((linhas_codigo[linha - 1].strip(),
                                      f"A variável {var_dest} não é do tipo {tipo_valor}",
                                      linha))

                elif tokens[i + 2][0] == "IDENT" and i + 3 < len(tokens) and tokens[i + 3][0] == "ABRE_PAR":
                    nome_func = valor
                    if nome_func in funcoes:
                        tipo_retorno = funcoes[nome_func]["retorno"]
                        tipos_param_esperados = funcoes[nome_func]["parametros"]

                        parametros_passados = []
                        j = i + 4
                        while j < len(tokens) and tokens[j][0] != "FECHA_PAR":
                            if tokens[j][0] == "IDENT":
                                parametros_passados.append(tokens[j][1])
                            j += 1

                        if len(parametros_passados) != len(tipos_param_esperados):
                            erros.append((linhas_codigo[linha - 1].strip(),
                                          f"A função '{nome_func}' espera {len(tipos_param_esperados)} parâmetro(s), mas foram passados {len(parametros_passados)}.",
                                          linha))
                        else:

                            for k, param in enumerate(parametros_passados):
                                tipo_param_passado = tabela_simbolos.get(param)
                                tipo_param_esperado = tipos_param_esperados[k]
                                if tipo_param_passado and tipo_param_passado != tipo_param_esperado:
                                    erros.append((linhas_codigo[linha - 1].strip(),
                                                  f"A função '{nome_func}' espera o parâmetro {k+1} do tipo {tipo_param_esperado}, mas foi passado '{param}' do tipo {tipo_param_passado}",
                                                  linha))

                        if tipo_dest and tipo_retorno != tipo_dest:
                            erros.append((linhas_codigo[linha - 1].strip(),
                                          f"O retorno da função '{nome_func}' não é do mesmo tipo de '{var_dest}'",
                                          linha))
        i += 1
    return erros


def salvar_erros_csv(erros):
    with open("erros.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Código", "Descrição do erro", "Linha"])
        for codigo, desc, linha in erros:
            writer.writerow([codigo, desc, linha])


def main():
    with open("comando.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()
        codigo = "".join(linhas)

    tokens = lexer(codigo)
    erros = analisar_semantica(tokens, linhas)
    salvar_erros_csv(erros)

    if erros:
        print("\nErros semânticos encontrados:")
        for e in erros:
            print(f"Linha {e[2]}: {e[1]}")
            print(f"  >> {e[0]}")
    else:
        print("\nNenhum erro semântico encontrado.")


if __name__ == "__main__":
    main()
