import customtkinter as ctk

# Configura o tema e cor padrão
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Cria a janela principal
app = ctk.CTk()
app.geometry("400x240")
app.title("Exemplo CustomTkinter")

# Adiciona um botão estilizado
btn = ctk.CTkButton(app, text="Clique Aqui", command=lambda: print("Botão clicado!"))
btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

# Executa o loop do aplicativo
app.mainloop()