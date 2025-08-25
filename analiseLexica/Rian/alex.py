# -*- coding: utf-8 -*-
import re
import csv


class AFD:
    def __init__(self, arqConfiguracao):
        linhas = arqConfiguracao.readlines()
        if len(linhas) < 5:
            print('Erro: Arquivo de configuração incompleto')
            return
        else:
            self.estados = re.split(r'[,|]', linhas[0].rstrip())
            self.simbolos = re.split(r'[,|]', linhas[1].rstrip())
            self.estadoInicial = linhas[2].rstrip()
            self.estadosFinais = re.split(r'[,|]', linhas[3].rstrip())

            transicoes_brutas = []
            for linha in linhas[4:]:
                transicoes_brutas.extend(re.split(r'[,|]', linha.rstrip()))
            self.regrasTransicao = [t for t in transicoes_brutas if t]

            self.mapaTransicoes = {}
            for regra in self.regrasTransicao:
                if regra.count(':') == 2:
                    origem, simbolo, destino = regra.split(':')
                    if origem not in self.mapaTransicoes:
                        self.mapaTransicoes[origem] = {}
                    self.mapaTransicoes[origem][simbolo] = destino

    def reconhece(self, palavra):
        if not self.mapaTransicoes:
            return None

        estadoAtual = self.estadoInicial
        for caracter in palavra:
            if estadoAtual in self.mapaTransicoes and caracter in self.mapaTransicoes[estadoAtual]:
                estadoAtual = self.mapaTransicoes[estadoAtual][caracter]
            else:
                return None

        for ef in self.estadosFinais:
            if ":" in ef:
                nome_estado, tipo = ef.split(':')
                if nome_estado == estadoAtual:
                    if tipo == "NUMERO" and "." in palavra:
                        return "NUMERO FRACIONARIO"
                    return tipo
        return None


if __name__ == "__main__":
    try:
        palavras_reservadas = [
            "auto", "break", "case", "const", "continue", "default", "do", "double", 
            "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", 
            "register", "return", "short", "signed", "sizeof", "static", "struct", 
            "string", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
        ]

        simbolos_especiais = {
            '=': 'ATRIBUICAO',
            ',': 'VIRGULA',
            ';': 'PONTOVIRGULA',
            '-': 'OPERADOR_ARITMETICO',
            '(': 'A.PAR',
            ')': 'F.PAR',
            '{': 'A.CHA',
            '}': 'F.CHA',
            '[': 'A.COL',
            ']': 'F.COL',
        }
        
        # Mapeamento para a lógica de referenciamento
        simbolos_correspondentes = {
            ')': '(',
            '}': '{',
            ']': '['
        }

        with open('conf.txt', 'r') as arquivo:
            afd = AFD(arquivo)

        with open("code.c", "r") as f:
            linhas = f.readlines()

        resultados_totais = []
        id_global_contador = 1
        # Pilha para armazenar IDs de símbolos de abertura
        pilha_referenciamento = []

        for i, linha in enumerate(linhas):
            if linha.strip():
                token_matches = re.finditer(
                    r"[A-Za-z_][A-Za-z0-9_]*|\d+\.\d+|\d+|[=,;(){}[\]]|-", linha)
                
                for match in token_matches:
                    token = match.group(0)
                    coluna = match.start() + 1
                    
                    tipo = None
                    referenciamento = ''

                    if token in simbolos_especiais:
                        tipo = simbolos_especiais[token]
                        # Se for um símbolo de abertura, adiciona o ID à pilha
                        if token in ['(', '{', '[']:
                            pilha_referenciamento.append(id_global_contador)
                        # Se for um símbolo de fechamento, remove o ID da pilha e preenche o referenciamento
                        elif token in [')', '}', ']']:
                            if pilha_referenciamento:
                                id_abertura = pilha_referenciamento.pop()
                                referenciamento = id_abertura
                            else:
                                referenciamento = 'ERRO' # Sinaliza um erro se a pilha estiver vazia
                    elif token in palavras_reservadas:
                        tipo = f"PR:{token.upper()}"
                    else:
                        tipo = afd.reconhece(token)
                        if tipo == "VARIAVEL":
                            tipo = "PALAVRA RESERVADA"
                    
                    if tipo:
                        resultados_totais.append({
                            'ID': id_global_contador,
                            'token': token,
                            'tipo token': tipo,
                            'Linha': i + 1,
                            'Coluna': coluna,
                            'Referenciamento': referenciamento
                        })
                        id_global_contador += 1
                    else:
                        resultados_totais.append({
                            'ID': id_global_contador,
                            'token': token,
                            'tipo token': "NÃO RECONHECIDO",
                            'Linha': i + 1,
                            'Coluna': coluna,
                            'Referenciamento': ''
                        })
                        id_global_contador += 1

        with open("tokens.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["ID", "token", "tipo token", "Linha", "Coluna", "Referenciamento"])
            
            ultima_linha = -1
            for resultado in resultados_totais:
                if resultado['Linha'] != ultima_linha and ultima_linha != -1:
                    writer.writerow([])  # Adiciona linha em branco entre as tabelas
                
                writer.writerow([
                    resultado['ID'],
                    resultado['token'],
                    resultado['tipo token'],
                    resultado['Linha'],
                    resultado['Coluna'],
                    resultado['Referenciamento']
                ])
                ultima_linha = resultado['Linha']

    except FileNotFoundError:
        print("Erro: Arquivo 'conf.txt' ou 'code.c' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")