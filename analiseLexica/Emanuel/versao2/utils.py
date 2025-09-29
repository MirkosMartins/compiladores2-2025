# def desempacotar_tokens(dados):
#     resultado = []
#     while isinstance(dados, list) and len(dados) == 2 and isinstance(dados[1], list):
#         resultado.append(dados[0])
#         dados = dados[1]
#     if isinstance(dados, list):
#         resultado.append(dados[0])
#     return resultado

def is_pr(tipo, token):
    if token.lower() in [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
            'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
            'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            '_Alignas', '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic',
            '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
        ]:
        return f"PR-{token}"
    return tipo

def controler_close(tipo, df):
    for index, row in df[::-1].iterrows():
        if row['token'] == tipo:
            return row["ID"]