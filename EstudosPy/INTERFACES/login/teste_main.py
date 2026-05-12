# main.py
import customtkinter as ctk
from teste_engenie import verificar_credenciais # Aqui está a mágica!

class AppLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Acesso")
        self.geometry("300x400")

        # Widgets
        self.label = ctk.CTkLabel(self, text="Faça seu Login", font=("Arial", 20))
        self.label.pack(pady=20)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_pass.pack(pady=10)

        self.btn = ctk.CTkButton(self, text="Entrar", command=self.executar_login)
        self.btn.pack(pady=20)

    def executar_login(self):
        u = self.entry_user.get()
        s = self.entry_pass.get()
        
        # Chamamos a função que está no outro arquivo
        sucesso, mensagem = verificar_credenciais(u, s)
        
        if sucesso:
            self.label.configure(text=mensagem, text_color="green")
        else:
            self.label.configure(text=mensagem, text_color="red")

if __name__ == "__main__":
    app = AppLogin()
    app.mainloop()