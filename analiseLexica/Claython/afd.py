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
            return 0
        else:
            self.estados = linhas[0].rstrip().split(',')
            self.simbolos = linhas[1].rstrip().split(',')
            self.estadoInicial = linhas[2].rstrip()
            self.estadosFinais = linhas[3].rstrip().split(',')
            for i in linhas[4:]:
                self.regrasTransicao += i.rstrip().split(',')
            self._regra_virgula()

    def _regra_virgula(self):
        self.regrasTransicao.append("q0:,:q7")
        self.simbolos.append(',')

    def reconhece(self, palavra):
        if len(self.regrasTransicao) > 0:
            pilha_estados = [self.estadoInicial]
            for caracter in palavra.rstrip():
                if caracter not in self.simbolos:
                    print('Símbolo não reconhecido pelo AFD!')
                    return 0
                
                estado_atual = pilha_estados[-1]
                reconhecido = False
                for regra in self.regrasTransicao:
                    if regra.startswith(estado_atual + ':' + caracter):
                        novo_estado = regra.split(':')[2]
                        pilha_estados.append(novo_estado)
                        reconhecido = True
                        break
                
                if not reconhecido:
                    print("Não reconhecido")
                    return

            estado_final_atual = pilha_estados[-1]
            for ef in self.estadosFinais:
                if ef.startswith(estado_final_atual):
                    return [palavra, ef.split(':')[1]]
        else:
            print('não iniciado')
            return 0

arquivo = open('config.txt')
afd = AFD(arquivo)
code = open("code.c").readlines()
tabela = pd.DataFrame(columns=["ID", "token", "tipo", "l", "c"])
i = 0
token_id = 1
for linha in code:
    i += 1
    lexema = ""
    coluna = 0
    
    linha_processada = linha.rstrip() + " "
    
    for caracter in linha_processada:
        coluna += 1
        
        if caracter.isspace() or caracter in ['=', ';']:
            if lexema:
                result = afd.reconhece(lexema)
                if result:
                    tb = pd.DataFrame({
                        "ID": [token_id],
                        "token": [result[0]],
                        "tipo": [result[1]],
                        "l": [i],
                        "c": [coluna - len(lexema)]
                    })
                    tabela = pd.concat([tabela, tb], ignore_index=True)
                    token_id += 1
                lexema = ""
            
            if caracter in ['=', ';']:
                result = afd.reconhece(caracter)
                if result:
                    tb = pd.DataFrame({
                        "ID": [token_id],
                        "token": [result[0]],
                        "tipo": [result[1]],
                        "l": [i],
                        "c": [coluna]
                    })
                    tabela = pd.concat([tabela, tb], ignore_index=True)
                    token_id += 1
        else:
            lexema += caracter
            
tabela.to_csv("tab-simbolos.csv")