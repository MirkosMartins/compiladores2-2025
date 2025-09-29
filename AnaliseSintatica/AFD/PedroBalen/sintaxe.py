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
            print(f"Erro: Arquivo de configuração '{arqConfiguracao.name}' inválido.")
            return
        self.estados = linhas[0].strip().split(',')
        self.simbolos = linhas[1].strip().split(',')
        self.estadoInicial = linhas[2].strip()
        self.estadosFinais = linhas[3].strip().split(',')
        self.regrasTransicao = []
        for i in linhas[4:]:
            regras_limpas = [regra for regra in i.strip().split(',') if regra]
            self.regrasTransicao.extend(regras_limpas)

    def validar_sequencia(self, sequencia_de_tipos):
        estado_atual = self.estadoInicial
        for tipo in sequencia_de_tipos:
            transicao_encontrada = False
            for regra in self.regrasTransicao:
                partes = regra.split(':')
                if len(partes) == 3:
                    origem, simbolo, destino = partes
                    if origem == estado_atual and simbolo == tipo:
                        estado_atual = destino
                        transicao_encontrada = True
                        break
            if not transicao_encontrada:
                return False
        for ef in self.estadosFinais:
            if ef.startswith(estado_atual):
                return True
        return False
try:
    with open('config-sintatico.txt', 'r') as f:
        parser_afd = AFD(f)
except FileNotFoundError:
    print("Erro: Arquivo de gramática 'config-sintatico.txt' não encontrado.")
    exit()

try:
    df = pd.read_csv('tab-simbolos.csv')
except FileNotFoundError:
    print("Erro: Tabela de símbolos 'tab-simbolos.csv' não encontrada.")
    exit()

if 'linha' not in df.columns:
    print("Erro: A tabela de símbolos não contém a coluna 'linha'.")
    exit()
    
linhas_agrupadas = df.groupby('linha')

for numero_linha, grupo in linhas_agrupadas:
    sequencia_tipos_original = grupo['tipo'].tolist()
    tokens_da_linha = grupo['token'].tolist()
    
    tipos_para_validar = []
    palavras_reservadas_de_tipo = {'int', 'float', 'char', 'double'}

    for i, tipo_original in enumerate(sequencia_tipos_original):
        token_atual = tokens_da_linha[i]
        
        if tipo_original == 'id' or tipo_original == 'nome_variavel':
            if token_atual in palavras_reservadas_de_tipo:
                tipos_para_validar.append('tipo')
            else:
                tipos_para_validar.append('id')
        else:
            tipos_para_validar.append(tipo_original)
    
    valido = parser_afd.validar_sequencia(tipos_para_validar)
    
    sentenca = " ".join(map(str, tokens_da_linha))

    if valido:
        componentes_padrao = []
        for i, tipo_validado in enumerate(tipos_para_validar):
            if tipo_validado == 'id':
                componentes_padrao.append("NOME_VARIAVEL")
            else:
                componentes_padrao.append(tipo_validado.upper())
        
        padrao_sintatico = " ".join(componentes_padrao)
        
        print(f"Linha {numero_linha}: '{sentenca}' -> {padrao_sintatico}")

    else:
        print(f"Linha {numero_linha}: '{sentenca}' -> INVÁLIDA")