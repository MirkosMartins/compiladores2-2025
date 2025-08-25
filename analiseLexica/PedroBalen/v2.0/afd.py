# -*- coding: utf-8 -*-
import pandas as pd

class AFD:
    estados = []
    simbolos = []
    estadoInicial = ''
    estadosFinais = []
    regrasTransicao = []

    def __init__(self, arqConfiguracao):
        linhas = arqConfiguracao.readlines()
        if len(linhas) < 5:
            print('Erro')
            return
        else:
            self.estados = linhas[0].rstrip().split(',')
            self.simbolos = linhas[1].rstrip().split(',')
            self.estadoInicial = linhas[2].rstrip()
            self.estadosFinais = linhas[3].rstrip().split(',')
            for i in linhas[4:]:
                self.regrasTransicao += i.rstrip().split(',')

    def get_proximo_estado(self, estado_atual, caracter):
        if caracter not in self.simbolos:
            return None
        for regra in self.regrasTransicao:
            if regra.startswith(estado_atual + ':' + caracter):
                return regra.split(':')[2]
        return None

    def is_estado_final(self, estado):
        for ef in self.estadosFinais:
            if ef.startswith(estado):
                return ef.split(':')[1]
        return None

def processar_delimitadores(lista_de_tokens):
    pilha = [] 
    mapa_delimitadores = {
        '(': ')',
        '[': ']',
        '{': '}'
    }
    tipos_abertura = ['parenteses_abre', 'colchetes_abre', 'chaves_abre']
    tipos_fechamento = ['parenteses_fecha', 'colchetes_fecha', 'chaves_fecha']

    for token in lista_de_tokens:
        token['referencia'] = ''
        if token['tipo'] in tipos_abertura:
            pilha.append(token)
        elif token['tipo'] in tipos_fechamento:
            if not pilha:
                token['referencia'] = 'ERRO: Sem abertura correspondente'
            else:
                token_abre = pilha.pop()
                if mapa_delimitadores.get(token_abre['token']) == token['token']:
                    token['referencia'] = token_abre['id']
                else:
                    token['referencia'] = f"ERRO: Esperava fechar '{mapa_delimitadores.get(token_abre['token'])}' (id: {token_abre['id']})"
                    pilha.append(token_abre)
    for token_abre in pilha:
        token_abre['referencia'] = 'ERRO: Não foi fechado'
        
    return lista_de_tokens


try:
    arquivo_config = open('config.txt')
    afd = AFD(arquivo_config)
    arquivo_config.close()
except FileNotFoundError:
    print("Erro: Arquivo 'config.txt' não encontrado.")
    exit()

lista_de_tokens = []
token_id_counter = 1

try:
    with open('code.c', 'r') as arquivo_codigo:
        numero_linha = 1
        for linha in arquivo_codigo:
            posicao = 0
            while posicao < len(linha):
                if linha[posicao].isspace():
                    posicao += 1
                    continue
                
                coluna_inicio = posicao + 1
                lexema_encontrado = None
                tipo_do_lexema = None
                posicao_final_lexema = posicao
                
                estado_atual = afd.estadoInicial
                for i in range(posicao, len(linha)):
                    caracter = linha[i]
                    proximo_estado = afd.get_proximo_estado(estado_atual, caracter)
                    if proximo_estado:
                        estado_atual = proximo_estado
                        tipo_token_parcial = afd.is_estado_final(estado_atual)
                        if tipo_token_parcial:
                            lexema_encontrado = linha[posicao:i+1]
                            tipo_do_lexema = tipo_token_parcial
                            posicao_final_lexema = i + 1
                    else:
                        break
                
                if lexema_encontrado:
                    lista_de_tokens.append({
                        'id': token_id_counter,
                        'token': lexema_encontrado,
                        'tipo': tipo_do_lexema,
                        'linha': numero_linha,
                        'coluna': coluna_inicio
                    })
                    token_id_counter += 1
                    posicao = posicao_final_lexema
                else:
                    caracter_invalido = linha[posicao]
                    lista_de_tokens.append({
                        'id': token_id_counter,
                        'token': caracter_invalido,
                        'tipo': 'ERRO: Caractere invalido',
                        'linha': numero_linha,
                        'coluna': coluna_inicio
                    })
                    token_id_counter += 1
                    posicao += 1
            
            numero_linha += 1
    lista_de_tokens_processada = processar_delimitadores(lista_de_tokens)
            
    if lista_de_tokens_processada:
        tabela = pd.DataFrame(lista_de_tokens_processada)
        nome_arquivo_csv = 'tab-simbolos.csv'
        colunas_ordenadas = ['id', 'token', 'tipo', 'linha', 'coluna', 'referencia']
        tabela = tabela[colunas_ordenadas]
        tabela.to_csv(nome_arquivo_csv, index=False, encoding='utf-8')
        print("Tabela gerada")

    else:
        print("\n nenhum token valido")

except FileNotFoundError:
    print("arquivo c nao encontrado")
    exit()