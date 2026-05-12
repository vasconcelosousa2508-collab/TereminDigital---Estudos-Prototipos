
def verificar_credenciais(usuario, senha):
    usuario_correto = "clara"
    senha_correta = "ifce2026"
    
    if usuario == usuario_correto and senha == senha_correta:
        return True, "Login realizado com sucesso!"
    else:
        return False, "Usuário ou senha incorretos."