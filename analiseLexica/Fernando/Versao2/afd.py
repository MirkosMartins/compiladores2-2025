import pandas

class AFD:
    estados = []
    simbolos = []
    estadoInicial = ''
    estadosFinais = []
    regrasTransicao = []

    reservadas = [
        "auto","break","case","char","const","continue","default","do",
        "double","else","enum","extern","float","for","goto","if",
        "inline","int","long","register","restrict","return","short",
        "signed","sizeof","static","struct","switch","typedef",
        "union","unsigned","void","volatile","while","_Alignas",
        "_Alignof","_Atomic","_Bool","_Complex","_Generic","_Imaginary",
        "_Noreturn","_Static_assert","_Thread_local"
    ]

    # Construtor do AFD
    def __init__(self, arqConfiguracao):
        linhas = arqConfiguracao.readlines()
        if len(linhas) < 5:
            print('Erro')
            return 0
        else:
            self.estados = linhas[0].rstrip().split(',')
            self.simbolos = linhas[1].rstrip().split(',')
            self.estadoInicial = linhas[2].rstrip()
            self.estadosFinais = linhas[3].rstrip().split(',')
            for i in linhas[4:]:
                self.regrasTransicao += i.rstrip().split(',')
                self.virgula()

    def virgula(self):
        self.regrasTransicao.append("q0:,:q7")
        self.simbolos.append(',')

    def analisar_codigo(self, codigo):
        tokens = []
        pilha = []  # Guarda (char_abertura, token_id_abertura)
        i = 0
        atual = ""
        token_id = 1  # ID sequencial de tokens
        
        while i < len(codigo):
            char = codigo[i]
            
            if char.isspace():
                if atual:
                    self.processar_token(atual, tokens, token_id)
                    token_id += 1
                    atual = ""
                i += 1
                continue

            if char in ['+', '-', '=', ';', ',', '.']:
                if atual:
                    self.processar_token(atual, tokens, token_id)
                    token_id += 1
                    atual = ""
                self.processar_token(char, tokens, token_id)
                token_id += 1
                i += 1
                continue

            # Aberturas
            if char in ['(', '{', '[']:
                if atual:
                    self.processar_token(atual, tokens, token_id)
                    token_id += 1
                    atual = ""
                tokens.append((token_id, char, f"abre{ {'(': 'Par', '{': 'Chave', '[': 'Col'}[char] }", None))
                pilha.append((char, token_id))
                token_id += 1
                i += 1
                continue

            # Fechamentos
            if char in [')', '}', ']']:
                if atual:
                    self.processar_token(atual, tokens, token_id)
                    token_id += 1
                    atual = ""
                if pilha:
                    abertura, id_abertura = pilha.pop()
                    if (abertura == '(' and char != ')') or \
                       (abertura == '{' and char != '}') or \
                       (abertura == '[' and char != ']'):
                        tokens.append((token_id, char, "fechamento_erro", None))
                    else:
                        tokens.append((token_id, char, f"fecha{ {'(': 'Par', '{': 'Chave', '[': 'Col'}[abertura] }", id_abertura))
                else:
                    tokens.append((token_id, char, "fechamento_erro", None))
                token_id += 1
                i += 1
                continue

            # Acumula identificadores/números
            atual += char
            i += 1

        if atual:
            self.processar_token(atual, tokens, token_id)
            token_id += 1

        # Fecha automaticamente aberturas restantes na pilha
        while pilha:
            abertura, id_abertura = pilha.pop()
            tokens.append((token_id, "", f"fechaFaltando{ {'(': 'Par', '{': 'Chave', '[': 'Col'}[abertura] }", id_abertura))
            token_id += 1

        return tokens

    def processar_token(self, token, tokens, token_id, ref_id=None):
        estadoAtual = self.estadoInicial
        tipo = None

        if token in self.reservadas:
            tokens.append((token_id, token, "reservada", ref_id))
            return

        for char in token:
            if char not in self.simbolos:
                tipo = "Símbolo não reconhecido"
                break
            for regra in self.regrasTransicao:
                if regra.startswith(estadoAtual + ':' + char):
                    estadoAtual = regra.split(':')[2]
                    break

        if not tipo:
            for ef in self.estadosFinais:
                if ef.startswith(estadoAtual):
                    tipo = ef.split(':')[1]
                    break

        tokens.append((token_id, token, tipo, ref_id))

    def reconhece(self, palavra):
        if len(self.regrasTransicao) > 0:
            for caracter in palavra.rstrip():
                if caracter not in self.simbolos:
                    print('Símbolo não reconhecido pelo AFD!')
                    return 0
            estadoAtual = self.estadoInicial
            for caracter in palavra.rstrip():
                for regra in self.regrasTransicao:
                    if regra.startswith(estadoAtual + ':' + caracter):
                        estadoAtual = regra.split(':')[2]
                        break
            for ef in self.estadosFinais:
                if ef.startswith(estadoAtual):
                    print('Símbolo', palavra, 'reconhecido como', ef.split(':')[1])
        else:
            print('não iniciado')
            return 0


# ----- Uso -----
arquivo = open('config.txt')
afd = AFD(arquivo)

with open("code.c", "r") as arquivoC:
    codigo = arquivoC.read()
    tokens = afd.analisar_codigo(codigo)

# Monta a tabela com a coluna "Referencia"
tabela = []
for token_id, token, tipo, ref_id in tokens:
    tabela.append([token_id, token, tipo, ref_id if ref_id is not None else 1])

df = pandas.DataFrame(tabela, columns=["ID", "Token", "Símbolo", "Referencia"])
print(df)
df.to_csv("tabela_tokens.csv", index=False)
