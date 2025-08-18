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
            self.estados = re.split(r'[,\|]', linhas[0].rstrip())
            self.simbolos = re.split(r'[,\|]', linhas[1].rstrip())
            self.estadoInicial = linhas[2].rstrip()
            self.estadosFinais = re.split(r'[,\|]', linhas[3].rstrip())

            transicoes_brutas = []
            for linha in linhas[4:]:
                transicoes_brutas.extend(re.split(r'[,\|]', linha.rstrip()))
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

        for caracter in palavra.rstrip():
            if caracter not in self.simbolos:
                return None

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

        with open('conf.txt', 'r') as arquivo:
            afd = AFD(arquivo)

        with open("code.c", "r") as f:
            conteudo = f.read()

        tokens = re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*|\d+\.\d+|\d+|[=,;]", conteudo)

        resultados = []
        for token in tokens:
            tipo = afd.reconhece(token)
            if tipo:
                resultados.append((token, tipo))
            else:
                resultados.append((token, "NÃO RECONHECIDO"))

        with open("tokens.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["token", "tipo"])
            writer.writerows(resultados)

        print("✅ Arquivo 'tokens.csv' gerado com sucesso!")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
