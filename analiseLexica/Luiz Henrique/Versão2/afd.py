# -*- coding: utf-8 -*-
import pandas as pd

class AFD:
    palavras_reservadas = {'int', 'return', 'if', 'else', 'while', 'for', 'break', 'continue',
                           'void', 'char', 'float', 'double', 'struct', 'typedef', 'const',
                           'static', 'switch', 'case', 'default', 'do', 'sizeof', 'true', 'false'}
    estados = []
    simbolos = []
    estadoInicial = ''
    estadosFinais = []
    regrasTransicao = []

    def __init__(self, arqConfiguracao):
        self.pilha_parenteses = []
        self.pilha_colchetes = []
        self.pilha_chaves = []
        self.contador_tokens = 0
        linhas = arqConfiguracao.readlines()
        if len(linhas) < 5:
            print('Erro: arquivo de configuração incompleto')
            return 0
        else:
            self.estados = [s.strip() for s in linhas[0].rstrip().split(',')]
            self.simbolos = [s for s in linhas[1].rstrip().split(',')]
            self.estadoInicial = linhas[2].rstrip().strip()
            self.estadosFinais = [s.strip() for s in linhas[3].rstrip().split(',')]
            for i in linhas[4:]:
                partes = [p.strip() for p in i.rstrip().split(',') if p.strip() != ""]
                self.regrasTransicao += partes
                # se quiser mesmo adicionar vírgula como símbolo/transição, mantenha virgula()
                # mas cuidado para não duplicar muitas vezes; aqui comento para evitar repetição
                # self.virgula()

    def virgula(self):
        # se usar, chame apenas uma vez (a sua versão chamava a cada linha)
        if ',' not in self.simbolos:
            self.regrasTransicao.append("q0:,:q7")
            self.simbolos.append(',')

    def analisar_codigo(self, codigo):
        tokens = []
        pos = 0
        atual = ""
        linha_atual = 1
        self.contador_tokens = 0
        usado_parenteses = set()
        usado_colchetes = set()
        usado_chaves = set()

        while pos < len(codigo):
            char = codigo[pos]

            # nova linha
            if char == '\n':
                if atual:
                    self.contador_tokens += 1
                    self.processar_token(atual, tokens, linha_atual)
                    atual = ""
                linha_atual += 1
                pos += 1
                continue

            # espaço / tab / outros espaços em branco (exceto '\n' que já tratamos)
            if char.isspace():
                if atual:
                    self.contador_tokens += 1
                    self.processar_token(atual, tokens, linha_atual)
                    atual = ""
                pos += 1
                continue

            # caracteres especiais tratados individualmente
            if char in ['+', '-', '=', ';', ',', '(', ')', '{', '}', '[', ']']:
                if atual:
                    self.contador_tokens += 1
                    self.processar_token(atual, tokens, linha_atual)
                    atual = ""

                self.contador_tokens += 1

                if char == '(':
                    tokens.append(('abrePar', char, linha_atual, None))
                elif char == ')':
                    ref_id = None
                    for idx in range(len(tokens)-1, -1, -1):
                        if tokens[idx][0] == 'abrePar' and idx + 1 not in usado_parenteses:
                            ref_id = idx + 1
                            usado_parenteses.add(ref_id)
                            break
                    tokens.append(('fechaPar', char, linha_atual, ref_id))

                elif char == '[':
                    tokens.append(('abreCol', char, linha_atual, None))
                elif char == ']':
                    ref_id = None
                    for idx in range(len(tokens)-1, -1, -1):
                        if tokens[idx][0] == 'abreCol' and idx + 1 not in usado_colchetes:
                            ref_id = idx + 1
                            usado_colchetes.add(ref_id)
                            break
                    tokens.append(('fechaCol', char, linha_atual, ref_id))

                elif char == '{':
                    tokens.append(('abreCha', char, linha_atual, None))
                elif char == '}':
                    ref_id = None
                    for idx in range(len(tokens)-1, -1, -1):
                        if tokens[idx][0] == 'abreCha' and idx + 1 not in usado_chaves:
                            ref_id = idx + 1
                            usado_chaves.add(ref_id)
                            break
                    tokens.append(('fechaCha', char, linha_atual, ref_id))
                elif char == ',':
                    tokens.append(('virgula', char, linha_atual, None))                
                    
                else:
                    # para símbolos simples (ex: '+' '-' '=' ';' ',') vamos tentar processar via AFD
                    # se preferir, pode mapear esses símbolos diretamente para um tipo (ex: ('op', '+', ...))
                    self.processar_token(char, tokens, linha_atual)

                pos += 1
                continue

            # acumula caractere em token atual
            atual += char
            pos += 1

        # token remanescente no final do arquivo
        if atual:
            self.contador_tokens += 1
            self.processar_token(atual, tokens, linha_atual)

        return tokens

    def eh_palavra_reservada(self, token):
        return token in self.palavras_reservadas or token.lower() in self.palavras_reservadas

    def processar_token(self, token, tokens, linha_atual):
        token = token.strip()
        if token == "":
            return

        # 1) Verifica palavra reservada (prioridade)
        if self.eh_palavra_reservada(token):
            tokens.append(('palavraReservada', token, linha_atual, None))
            return

        # 2) Tenta reconhecer com o AFD (caractere a caractere)
        estado_atual = self.estadoInicial
        for char in token:
            encontrou = False
            for regra in self.regrasTransicao:
                partes = [p.strip() for p in regra.split(':')]
                if len(partes) == 3 and partes[0] == estado_atual and partes[1] == char:
                    estado_atual = partes[2]
                    encontrou = True
                    break
            if not encontrou:
                tokens.append(('erro', token, linha_atual, None))
                return

        # 3) Se chegou aqui, testa se estado_atual é final (testa com split para evitar problemas de formatação)
        for ef in self.estadosFinais:
            partes = [p.strip() for p in ef.split(':')]
            if len(partes) >= 2 and partes[0] == estado_atual:
                tipo = partes[1]
                tokens.append((tipo, token, linha_atual, None))
                return

        # 4) se não for final, é erro
        tokens.append(('erro', token, linha_atual, None))

    def reconhece(self, palavra):
        if len(self.regrasTransicao) == 0:
            print('não iniciado')
            return 0

        p = palavra.rstrip()
        for caracter in p:
            if caracter not in self.simbolos:
                print('Símbolo não reconhecido pelo AFD!', repr(caracter))
                return 0
        estadoAtual = self.estadoInicial
        for caracter in p:
            for regra in self.regrasTransicao:
                if regra.startswith(estadoAtual + ':' + caracter + ':'):
                    estadoAtual = regra.split(':')[2]
                    break
        for ef in self.estadosFinais:
            partes = [x.strip() for x in ef.split(':')]
            if partes and partes[0] == estadoAtual:
                print('Símbolo', palavra, 'reconhecido como', partes[1])
                return 1
        print('não reconhecido')
        return 0


# ----- como usar (exemplo) -----
# arquivo = open('config.txt')
# afd = AFD(arquivo)
# with open("code.c", "r") as f:
#     codigo = f.read()
# tokens = afd.analisar_codigo(codigo)
# tabela = []
# for i, (tipo, token, linha, ref_id) in enumerate(tokens, 1):
#     tabela.append([i, token, tipo, linha, ref_id])
# df = pd.DataFrame(tabela, columns=["ID", "Token", "Símbolo", "Linha", "Ref_ID"])
# print(df)
# df.to_csv("tabela_tokens.csv", index=False)

arquivo = open('config.txt')
afd = AFD(arquivo)
tabela = []

with open("code.c", "r") as arquivoC:
    codigo = arquivoC.read()
    tokens = afd.analisar_codigo(codigo)
    
tabela = []
for i, (tipo, token, linha, ref_id) in enumerate(tokens, 1):
    tabela.append([i, token, tipo, linha, ref_id]) 

import pandas as pd
df = pd.DataFrame(tabela, columns=["ID", "Token", "Símbolo", "Linha", "Ref_ID"])
print(df)
df.to_csv("tabela_tokens.csv", index=False)

