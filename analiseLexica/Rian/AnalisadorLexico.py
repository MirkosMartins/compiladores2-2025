# -*- coding: utf-8 -*-
config_content = """q0|q1|q2|q3|q4|q5|q6|q7|q8
a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|0|1|2|3|4|5|6|7|8|9|+|-|.|_|=|,|;
q0
q1:VARIAVEL|q2:NUMERO|q5:NUMERO|q6:PONTOVIRGULA|q7:VIRGULA|q8:ATRIBUICAO
q0:a:q1|q0:b:q1|q0:c:q1|q0:d:q1|q0:e:q1|q0:f:q1|q0:g:q1|q0:h:q1|q0:i:q1|q0:j:q1|q0:k:q1|q0:l:q1|q0:m:q1|q0:n:q1|q0:o:q1|q0:p:q1|q0:q:q1|q0:r:q1|q0:s:q1|q0:t:q1|q0:u:q1|q0:v:q1|q0:w:q1|q0:x:q1|q0:y:q1|q0:z:q1|q0:A:q1|q0:B:q1|q0:C:q1|q0:D:q1|q0:E:q1|q0:F:q1|q0:G:q1|q0:H:q1|q0:I:q1|q0:J:q1|q0:K:q1|q0:L:q1|q0:M:q1|q0:N:q1|q0:O:q1|q0:P:q1|q0:Q:q1|q0:R:q1|q0:S:q1|q0:T:q1|q0:U:q1|q0:V:q1|q0:W:q1|q0:X:q1|q0:Y:q1|q0:Z:q1|q0:_:q1|q1:a:q1|q1:b:q1|q1:c:q1|q1:d:q1|q1:e:q1|q1:f:q1|q1:g:q1|q1:h:q1|q1:i:q1|q1:j:q1|q1:k:q1|q1:l:q1|q1:m:q1|q1:n:q1|q1:o:q1|q1:p:q1|q1:q:q1|q1:r:q1|q1:s:q1|q1:t:q1|q1:u:q1|q1:v:q1|q1:w:q1|q1:x:q1|q1:y:q1|q1:z:q1|q1:A:q1|q1:B:q1|q1:C:q1|q1:D:q1|q1:E:q1|q1:F:q1|q1:G:q1|q1:H:q1|q1:I:q1|q1:J:q1|q1:K:q1|q1:L:q1|q1:M:q1|q1:N:q1|q1:O:q1|q1:P:q1|q1:Q:q1|q1:R:q1|q1:S:q1|q1:T:q1|q1:U:q1|q1:V:q1|q1:W:q1|q1:X:q1|q1:Y:q1|q1:Z:q1|q1:_:q1|q1:0:q1|q1:1:q1|q1:2:q1|q1:3:q1|q1:4:q1|q1:5:q1|q1:6:q1|q1:7:q1|q1:8:q1|q1:9:q1|q0:0:q2|q0:1:q2|q0:2:q2|q0:3:q2|q0:4:q2|q0:5:q2|q0:6:q2|q0:7:q2|q0:8:q2|q0:9:q2|q0:+:q3|q0:-:q3|q3:0:q2|q3:1:q2|q3:2:q2|q3:3:q2|q3:4:q2|q3:5:q2|q3:6:q2|q3:7:q2|q3:8:q2|q3:9:q2|q2:0:q2|q2:1:q2|q2:2:q2|q2:3:q2|q2:4:q2|q2:5:q2|q2:6:q2|q2:7:q2|q2:8:q2|q2:9:q2|q2:.:q4|q2:,:q4|q4:0:q5|q4:1:q5|q4:2:q5|q4:3:q5|q4:4:q5|q4:5:q5|q4:6:q5|q4:7:q5|q4:8:q5|q4:9:q5|q5:0:q5|q5:1:q5|q5:2:q5|q5:3:q5|q5:4:q5|q5:5:q5|q5:6:q5|q5:7:q5|q5:8:q5|q5:9:q5|q0:=:q8|q0:;:q6|q0:,:q7
"""

with open('config.txt', 'w') as f:
    f.write(config_content)

class AFD:
  estados = []
  simbolos = []
  estadoInicial = ''
  estadosFinais = []
  regrasTransicao = []
  
  def __init__(self, arqConfiguracao):
    linhas = arqConfiguracao.readlines()
    if len(linhas) < 5:
      print('Erro: Arquivo de configuração incompleto')
      return 0
    else:
      self.estados = linhas[0].rstrip().split('|')
      self.simbolos = linhas[1].rstrip().split('|')
      self.estadoInicial = linhas[2].rstrip()
      self.estadosFinais = linhas[3].rstrip().split('|')
      
      transicoes_brutas = []
      for linha in linhas[4:]:
          transicoes_brutas.extend([t for t in linha.rstrip().split('|') if t])
      self.regrasTransicao = transicoes_brutas
      
      self.mapaTransicoes = {}
      for regra in self.regrasTransicao:
        if regra.count(':') == 2:
          origem, simbolo, destino = regra.split(':')
          if origem not in self.mapaTransicoes:
              self.mapaTransicoes[origem] = {}
          self.mapaTransicoes[origem][simbolo] = destino

  def reconhece(self, palavra):
    if not self.mapaTransicoes:
      print('AFD não iniciado ou com regras inválidas.')
      return 0
      
    estadoAtual = self.estadoInicial
    
    for caracter in palavra.rstrip():
      if caracter not in self.simbolos:
        print(f"Símbolo '{caracter}' não reconhecido pelo AFD!")
        print(f"O termo '{palavra}' não é reconhecido por este autômato.")
        return
      
      if estadoAtual in self.mapaTransicoes and caracter in self.mapaTransicoes[estadoAtual]:
        estadoAtual = self.mapaTransicoes[estadoAtual][caracter]
      else:
        print(f"O termo '{palavra}' não é reconhecido por este autômato.")
        return
        
    for ef in self.estadosFinais:
      nome_estado, tipo = ef.split(':')
      if nome_estado == estadoAtual:
        print(f"O termo '{palavra}' foi reconhecido como '{tipo}'. ✅")
        return
    
    print(f"O termo '{palavra}' não é reconhecido por este autômato.")

try:
    with open('config.txt', 'r') as arquivo:
        afd = AFD(arquivo)

    if afd.estados:
        while True:
            termo = input('Digite algo para reconhecer no AFD (ou digite "sair" para terminar): ')
            if termo.lower() == 'sair':
                print("Encerrando o programa.")
                break
            afd.reconhece(termo)
except FileNotFoundError:
    print("Erro: O arquivo 'config.txt' não foi encontrado. Verifique se ele foi criado corretamente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
