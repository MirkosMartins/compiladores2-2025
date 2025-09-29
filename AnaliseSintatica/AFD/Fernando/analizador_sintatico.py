import json
import pandas as pd

class AnalisadorSintatico:
    """
    Uma classe que representa um Analisador Sintático baseado em um
    Autômato Finito Determinístico (AFD).

    Esta classe é carregada a partir de um arquivo de configuração JSON
    e pode validar sequências de tipos de token.
    """

    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        """
        Construtor do analisador. É recomendado usar o método `from_json_file`.
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states  # Dicionário de estado final -> nome do resultado

    @classmethod
    def from_json_file(cls, filepath):
        """
        Cria uma instância do AnalisadorSintatico a partir de um arquivo JSON.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validação básica do arquivo de configuração
            required_keys = ['states', 'alphabet', 'transitions', 'initial_state', 'final_states']
            if not all(key in config for key in required_keys):
                raise ValueError("O arquivo de configuração JSON não contém todas as chaves necessárias.")

            return cls(
                states=config['states'],
                alphabet=config['alphabet'],
                transitions=config['transitions'],
                initial_state=config['initial_state'],
                final_states=config['final_states']
            )
        except FileNotFoundError:
            print(f"Erro: Arquivo de configuração '{filepath}' não encontrado.")
            return None
        except json.JSONDecodeError:
            print(f"Erro: O arquivo '{filepath}' não é um JSON válido.")
            return None
        except ValueError as e:
            print(f"Erro de configuração: {e}")
            return None

    def validar_sequencia(self, token_types: list):
        """
        Valida uma sequência de tipos de token usando o AFD.

        Retorna uma tupla (bool, str) indicando sucesso/falha e uma mensagem.
        """
        estado_atual = self.initial_state
        
        for i, tipo in enumerate(token_types):
            if tipo not in self.alphabet:
                return False, f"Erro: Símbolo '{tipo}' não pertence ao alfabeto definido."
            
            try:
                # A busca aqui é O(1) graças à estrutura de dicionário aninhado
                estado_atual = self.transitions[estado_atual][tipo]
            except KeyError:
                token_anterior = token_types[i-1] if i > 0 else "início da linha"
                return False, f"Erro de sintaxe: Transição inválida após '{token_anterior}' com o token '{tipo}'."

        # Ao final da sequência, verifica se o estado atual é um estado final
        if estado_atual in self.final_states:
            nome_resultado = self.final_states[estado_atual]
            return True, nome_resultado
        else:
            return False, f"Erro: A linha terminou de forma inesperada. Estado final era '{estado_atual}'."


def processar_codigo_fonte(analisador, arquivo_simbolos):
    """
    Lê uma tabela de símbolos, agrupa por linha e valida cada linha
    usando o analisador sintático.
    """
    try:
        df = pd.read_csv(arquivo_simbolos)
    except FileNotFoundError:
        print(f"Erro: Arquivo de tabela de símbolos '{arquivo_simbolos}' não encontrado.")
        return

    # Agrupa os tipos de token por número de linha ('l')
    linhas_agrupadas = df.groupby('l')['tipo'].apply(list).reset_index()

    print("--- Iniciando Análise Sintática ---")
    for _, row in linhas_agrupadas.iterrows():
        num_linha = row['l']
        sequencia_tipos = row['tipo']
        
        valido, mensagem = analisador.validar_sequencia(sequencia_tipos)
        
        if valido:
            print(f"Linha {num_linha}: SINTAXE VÁLIDA ({mensagem})")
        else:
            print(f"Linha {num_linha}: SINTAXE INVÁLIDA - {mensagem}")
    print("--- Análise Sintática Concluída ---")


# --- Execução Principal ---
if __name__ == "__main__":
    # Define os caminhos dos arquivos
    ARQUIVO_CONFIG = 'config.json'
    ARQUIVO_SIMBOLOS = 'tab-simbolos.csv'
    
    # 1. Cria o analisador a partir do arquivo JSON
    analisador = AnalisadorSintatico.from_json_file(ARQUIVO_CONFIG)
    
    # 2. Se o analisador foi criado com sucesso, processa o código-fonte
    if analisador:
        processar_codigo_fonte(analisador, ARQUIVO_SIMBOLOS)