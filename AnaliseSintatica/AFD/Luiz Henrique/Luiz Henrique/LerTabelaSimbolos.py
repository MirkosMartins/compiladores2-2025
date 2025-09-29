import csv

class AFD:
    def __init__(self, arqConfiguracao):
        linhas = arqConfiguracao.readlines()
        self.estados = linhas[0].rstrip().split(',')
        self.simbolos = linhas[1].rstrip().split(',')
        self.estadoInicial = linhas[2].rstrip()
        self.estadosFinais = [ef for ef in linhas[3].rstrip().split(',')]
        self.regrasTransicao = []
        for i in linhas[4:]:
            partes = i.rstrip().split(':')
            if len(partes) == 3:
                self.regrasTransicao.append(i.rstrip())

    def reconhece_tokens(self, tokens):
        estadoAtual = self.estadoInicial
        for token in tokens:
            transicao_encontrada = False
            for regra in self.regrasTransicao:
                origem, simbolo, destino = regra.split(':')
                if origem == estadoAtual and simbolo == token:
                    estadoAtual = destino
                    transicao_encontrada = True
                    break
            if not transicao_encontrada:
                return None
        for ef in self.estadosFinais:
            estado, tipo = ef.split(':')
            if estado == estadoAtual:
                return tipo
        return None


with open("config.txt", "r") as arquivo:
    afd = AFD(arquivo)

with open("tabela.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    declaracao = []  # acumula tokens de uma linha
    for row in reader:
        token_tipo = row['TIPO']
        declaracao.append(token_tipo)
        if token_tipo == 'ponto_virgula':  # fim de uma declaração
            resultado = afd.reconhece_tokens(declaracao)
            if resultado:
                print(f"Declaração reconhecida como: {resultado} -> Tokens: {declaracao}")
            else:
                print(f"Declaração inválida -> Tokens: {declaracao}")
            declaracao = []  # reseta para próxima declaração
