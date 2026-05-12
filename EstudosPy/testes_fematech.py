import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sintetizador Ultrassônico")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark") # O modo escuro fica top para áudio

        # Exemplo de um Slider para o Volume Máximo
        self.slider_vol = ctk.CTkSlider(self, from_=0, to=1, command=self.mudar_volume)
        self.slider_vol.pack(pady=20)

    def mudar_volume(self, valor):
        print(f"Volume ajustado para: {valor}")

app = App()
app.mainloop()