import pandas as pd

class AFD:
    def __init__(self, arqConfiguracao):
        linhas = arqConfiguracao.readlines()
        if len(linhas) < 5:
            raise ValueError('AFD incompleto.')
        self.estados = linhas[0].strip().split(',')
        self.simbolos = linhas[1].strip().split(',')
        self.estadoInicial = linhas[2].strip()
        self.estadosFinais = linhas[3].strip().split(',')
        self.regrasTransicao = []

        for linha in linhas[4:]:
            if linha.strip():
                regras = linha.strip().split(',')
                for r in regras:
                    if r:  #evitar string vazia
                        self.regrasTransicao.append(r.strip())

    def reconhece_sequencia(self, tipos):
        """Verifica se a sequência de tipos é reconhecida pelo AFD."""
        if not self.regrasTransicao:
            return False, "AFD não inicializado"

        estadoAtual = self.estadoInicial

        for tipo in tipos:
            if tipo not in self.simbolos:
                return False, f"Erro: Tipo '{tipo}' não encontrado nos símbolos definidos."

            transicao_encontrada = False
            for regra in self.regrasTransicao:
                partes = regra.split(':')
                if len(partes) == 3:
                    origem, simbolo, destino = partes
                    if origem == estadoAtual and simbolo == tipo:
                        estadoAtual = destino
                        transicao_encontrada = True
                        break

            if not transicao_encontrada:
                return False, f"Erro: Transição não encontrada de '{estadoAtual}' com símbolo '{tipo}'"

        #verificação de estado final
        for estado_final in self.estadosFinais:
            if ':' in estado_final:
                estado, nome = estado_final.split(':')
                if estado == estadoAtual:
                    return True, nome
            elif estado_final == estadoAtual:
                return True, "Aceito"

        return False, f"Erro: Estado final '{estadoAtual}' não é um estado de aceitação"

with open('config.txt', 'r') as arquivo:
    afd = AFD(arquivo)

df = pd.read_csv('tab-simbolos.csv')

linhas_agrupadas = df.groupby('l').agg({
    'token': list,
    'tipo': list
}).reset_index()

print("resultado:")
for _, row in linhas_agrupadas.iterrows():
    tipos = row['tipo']
    tokens = row['token']
    linha = row['l']

    resultado, mensagem = afd.reconhece_sequencia(tipos)
    sequencia_tokens = " ".join(tokens)
    sequencia_tipos = " -> ".join(tipos)
    print(f"Linha {linha}:")
    print(f"  Tokens: {sequencia_tokens}")
    print(f"  Tipos:  {sequencia_tipos}")
    print(f"  Resultado: {mensagem}\n")
