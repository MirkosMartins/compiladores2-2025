import re


def carregar_afd(arquivo):
    estados = set()
    alfabeto = set()
    estado_inicial = None
    finais = {}
    transicoes = {}

    with open(arquivo, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]

    estados = set(linhas[0].split(","))
    alfabeto = set(linhas[1].split(","))
    estado_inicial = linhas[2]

    for linha in linhas[3:]:
        if not linha:
            continue
        if linha.count(":") == 1:
            estado, token = linha.split(":")
            finais[estado] = token
        else:
            matches = re.findall(r'([^:,]+):(.):([^:,]+)', linha)
            for origem, simbolo, destino in matches:
                transicoes[(origem, simbolo)] = [destino]

    for letra in ["c", "f", "i"]:
        transicoes[("q0", letra)] = ["q1"]

    return estados, alfabeto, estado_inicial, finais, transicoes


def analisador_lexico(texto, afd):
    estados, alfabeto, inicial, finais, transicoes = afd
    tokens = []
    i = 0
    while i < len(texto):
        if texto[i].isspace():
            i += 1
            continue

        if texto[i] == "-" and i + 1 < len(texto) and texto[i+1].isdigit():
            j = i + 1
            while j < len(texto) and (texto[j].isdigit() or texto[j] == "."):
                j += 1
            lexema = texto[i:j]
            if "." in lexema:
                tokens.append(("FRACIONARIO", lexema))
            else:
                tokens.append(("INTEIRO", lexema))
            i = j
            continue

        estado = inicial
        ultimo_token = None
        ultimo_pos = i
        j = i
        while j < len(texto):
            c = texto[j]
            if (estado, c) in transicoes:
                estado = transicoes[(estado, c)][0]
                j += 1
                if estado in finais:
                    ultimo_token = finais[estado]
                    ultimo_pos = j
            else:
                break

        if ultimo_token:
            lexema = texto[i:ultimo_pos]
            if ultimo_token == "VARIAVEL":
                if lexema == "int":
                    ultimo_token = "PR_INT"
                elif lexema == "float":
                    ultimo_token = "PR_FLOAT"
                elif lexema == "char":
                    ultimo_token = "PR_CHAR"
            tokens.append((ultimo_token, lexema))
            i = ultimo_pos
        else:
            raise ValueError(f"Erro léxico na posição {i}: '{texto[i]}'")
    return tokens


def parser(tokens):
    pos = 0

    def consumir(tipo):
        nonlocal pos
        if pos < len(tokens) and tokens[pos][0] == tipo:
            pos += 1
            return True
        return False

    def tipo():
        return consumir("PR_INT") or consumir("PR_FLOAT") or consumir("PR_CHAR")

    def valor():
        if consumir("INTEIRO") or consumir("FRACIONARIO"):
            return True
        return False

    def var():
        if consumir("VARIAVEL"):
            if consumir("SA"):
                if not valor():
                    raise ValueError("Valor esperado após '='")
            return True
        return False

    def lista_vars():
        if not var():
            return False
        while consumir("VIRGULA"):
            if not var():
                raise ValueError("Variável esperada após ','")
        return True

    def decl():
        if not tipo():
            raise ValueError("Tipo esperado no início da declaração")
        if not lista_vars():
            raise ValueError("Esperada lista de variáveis")
        if not consumir("PV"):
            raise ValueError("Ponto e vírgula esperado no final")
        return True

    ok = decl()
    if ok and pos == len(tokens):
        return True
    else:
        raise ValueError("Tokens extras após declaração")


if __name__ == "__main__":
    afd = carregar_afd("AFD.txt")

    while True:
        entrada = input(
            "Digite uma declaração de variável (ou 'sair' para encerrar): ").strip()
        if entrada.lower() == "sair":
            break
        try:
            tokens = analisador_lexico(entrada, afd)
            print("Tokens reconhecidos:", tokens)
            if parser(tokens):
                print("✓ Sintaxe válida!\n")
        except Exception as e:
            print("✗ Erro:", e, "\n")
