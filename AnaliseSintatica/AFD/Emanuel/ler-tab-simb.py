import pandas as pd
import utils

class AFD:
  estados = []
  simbolos = []
  estadoInicial = ''
  estadosFinais = []
  regrasTransicao = []
  #construtor do AFD
  def __init__(self,arqConfiguracao):
    linhas = arqConfiguracao.readlines()
    if len(linhas)<5:
      print ('Erro')
      return 0
    else:
        self.estados = linhas[0].rstrip().split(',')
        self.simbolos = linhas[1].rstrip().split(',')
        self.estadoInicial = linhas[2].rstrip()
        self.estadosFinais = linhas[3].rstrip().split(',')
        for i in linhas[4:]:
            #EFB
            self.regrasTransicao += i.rstrip().split(',')
        self._regra_virgula()
  
  def _regra_virgula(self):
        self.regrasTransicao.append("q0:,:q7")
        self.simbolos.append(',')

  def reconhece(self,palavra: str):
    if len(self.regrasTransicao)>0:
        # for caracter in palavra.rstrip():
        #     if caracter not in self.simbolos:
        #         print('Símbolo não reconhecido pelo AFD!')
        #         return 0
        estadoAtual = self.estadoInicial
        token = ""
        for caracter in palavra.rstrip():
            reconhecido=False
            for regra in self.regrasTransicao:
                if regra.startswith(estadoAtual+':'+caracter):
                    estadoAtual = regra.split(':')[2]
                    reconhecido = True
                    token +=palavra[0]
                    palavra = palavra.removeprefix(palavra[0])
                    break
            if caracter not in self.simbolos:
                print("não tem o caracter", palavra)
                palavra = palavra.removeprefix(palavra[0])
                break
            if not reconhecido:
                print("Não reconhecido", palavra)
                # palavra = palavra.removeprefix(palavra[0])
                break
        
        for ef in self.estadosFinais:
            if ef.startswith(estadoAtual):
                if not reconhecido:
                    resultado = [[token, ef.split(':')[1]]]
                    tokens_restantes = self.reconhece(palavra)
                    if tokens_restantes:
                        resultado.extend(tokens_restantes)
                    return resultado
                return [[token, ef.split(':')[1]]]
    else:
        print('não iniciado')
        return 0
    
  def reconhece_sequencia(self, tipos):
        """Reconhece uma sequência de tipos de tokens"""
        if len(self.regrasTransicao) == 0:
            print('AFD não inicializado')
            return False, "AFD não inicializado"
        
        estadoAtual = self.estadoInicial
        caminho = [estadoAtual]
        
        for tipo in tipos:
            reconhecido = False
            for regra in self.regrasTransicao:
                if regra.strip() and ':' in regra:
                    partes = regra.split(':')
                    if len(partes) == 3:
                        estado_origem, simbolo, estado_destino = partes
                        if estado_origem == estadoAtual and simbolo == tipo:
                            estadoAtual = estado_destino
                            caminho.append(estadoAtual)
                            reconhecido = True
                            break
            
            if not reconhecido:
                return False, f"Transição não encontrada: {estadoAtual} -> {tipo}"
        
        for ef in self.estadosFinais:
            if ':' in ef:
                estado, nome = ef.split(':')
                if estado == estadoAtual:
                    return True, nome
        
        return False, f"Estado final não aceito: {estadoAtual}"


arquivo = open('config-as.txt')
afd = AFD(arquivo)

df = pd.read_csv('tab-simbolos.csv')

linhas_agrupadas = df.groupby('l').agg({
    'token': list,
    'tipo': list,
    'ID': list
}).reset_index()

for index, row in linhas_agrupadas.iterrows():
    linha = " ".join(row['tipo'])
    print(afd.reconhece_sequencia(row['tipo']))