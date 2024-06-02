import webbrowser
import tkinter as tk
import customtkinter
import customtkinter as ctk
import os
import json
from settings import *
from dados import Dados

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Planilha Inventário")
        self.geometry(f'{str(WINDOW_WIDTH)}x{str(WINDOW_HEIGHT)}')
        self.configure(fg_color=MAIN_FRAME_COLOR)
        self.resizable(width=False, height=False)

        frame_buttons = FrameButtons(self)
        frame_buttons.place(relx=0, rely=0)

        FrameEntry(self, frame_buttons)

class FrameButtons(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(master=parent,
                         width=WINDOW_WIDTH,
                         height=WINDOW_HEIGHT - 75,
                         fg_color=MAIN_FRAME_COLOR)

        self.place(relx=0, rely=0)
        self.create_buttons()

    def create_buttons(self):

        for widget in self.grid_slaves():
            widget.destroy()

        self.dados = Dados('dados.json')
        self.i = 0

        for link, url in self.dados.dados.items():
            self.botao_text = ctk.StringVar()
            self.botao_text.set(link)

            # ----// Botões Planilha \\----
            self.botao = ctk.CTkButton(self, text=f'{self.botao_text.get()}', textvariable=self.botao_text,
                                       command=lambda u=url: webbrowser.open(u),
                                       font=customtkinter.CTkFont(family='<Helvetica>', size=14),
                                       width=100,
                                       height=100,
                                       fg_color=MAIN_BUTTON_COLOR,
                                       corner_radius=25
                                       )

            self.botao.grid(row=self.i // 6, column=self.i % 6, padx=10, pady=10)

            self.botao.bind('<Enter>', lambda event, btn=self.botao: btn.configure(fg_color=HOLD_BUTTON_COLOR))
            self.botao.bind('<Leave>', lambda event, btn=self.botao: btn.configure(fg_color=MAIN_BUTTON_COLOR))


            # ----// Botões Remover \\----
            self.botao_remover = ctk.CTkButton(self, text='X', width=12, height=12, bg_color=MAIN_BUTTON_COLOR, fg_color=REMOVE_BUTTON_COLOR,
                                               corner_radius=25,
                                               command=lambda b=self.botao_text: self.remover_botao(b))

            self.botao_remover.bind('<Enter>', lambda event, btn=self.botao_remover: btn.configure(fg_color=REMOVE_HOLD_COLOR))
            self.botao_remover.bind('<Leave>', lambda event, btn=self.botao_remover: btn.configure(fg_color=REMOVE_BUTTON_COLOR))

            self.botao_remover.grid(row=self.i // 6, column=self.i % 6, sticky='ne', pady=13, padx=25)

            # ----// Botões Renomear \\----
            self.botoes_renomear = ctk.CTkButton(self, text='R', width=12, height=12, bg_color=MAIN_BUTTON_COLOR, fg_color=HOLD_BUTTON_COLOR,
                                                 command=lambda b=self.botao_text: self.renomear_botao(b))

            self.botoes_renomear.bind('<Enter>', lambda event, btn=self.botoes_renomear: btn.configure(fg_color=HOLD_BUTTON_COLOR2))
            self.botoes_renomear.bind('<Leave>', lambda event, btn=self.botoes_renomear: btn.configure(fg_color=HOLD_BUTTON_COLOR))


            self.botoes_renomear.grid(row=self.i // 6, column=self.i % 6, padx=20, sticky='nw', pady=15)
            self.i += 1

    def remover_botao(self, botao_text):
        chave = botao_text.get()
        self.dados.remover_dados(chave)

        self.update_buttons()

    def update_buttons(self):
        self.create_buttons()

    def renomear_botao(self, botao_text):

        def set_name(event):
            novo_nome = entry.get()
            if len(entry.get()) > 7:
                meio = len(entry.get()) // 2
                indice_espaco = entry.get().rfind(' ', 0, meio)
                if indice_espaco == -1:
                    indice_espaco = novo_nome.find(' ', meio)
                if indice_espaco == -1:
                    novo_nome = novo_nome[:meio] + '\n' + novo_nome[meio:]
                else:
                    novo_nome = novo_nome[:indice_espaco] + '\n' + novo_nome[indice_espaco + 1:]


            self.dados.renomear_dados(chave_antiga=link, chave_nova=novo_nome)
            entry.destroy()
            self.update_buttons()

        entry_stringvar = ctk.StringVar()
        entry = ctk.CTkEntry(self, width=90, textvariable=entry_stringvar, bg_color=MAIN_BUTTON_COLOR)

        for idx, (link, url) in enumerate(self.dados.dados.items(), start=1):

            if botao_text.get() == link:
                row = idx // 7
                col = idx % 6

                if col == 0:
                    entry.grid(row=row, column=col + 5)
                else:
                    entry.grid(row=row, column=col - 1)

                if idx == 13:
                    entry.grid(row=2, column=col - 1)
                elif idx == 20:
                    entry.grid(row=3, column=col - 1)
                elif idx == 19:
                    entry.grid(row=3, column=col - 1)
                break

        entry.bind('<Return>', set_name)


class FrameEntry(ctk.CTkFrame):

    def __init__(self, parent, frame_buttons):
        super().__init__(master=parent,
                         height=WINDOW_HEIGHT - 525,
                         width=WINDOW_WIDTH)

        self.dados = Dados('dados.json')
        self.place(relx=0, rely=0.874)
        self.configure(fg_color=FOOTER_FRAME_COLOR)

        self.frame_buttons = frame_buttons

        self.create_widgets()

    def create_widgets(self):

        # entry
        self.adicionar_planilha_entry = ctk.CTkEntry(self)
        self.adicionar_planilha_entry.place(relx=0.12, rely=0.4)

        # label
        self.adicionar_planilha_label = ctk.CTkLabel(self, text='Adicionar Planilha', height=15, text_color=TEXT_COLOR,
                                                     font=ctk.CTkFont('<Helvetica>', size=14))
        self.adicionar_planilha_label.place(relx=0.14, rely=0.15)

        # button
        self.adicionar_planilha_botao = ctk.CTkButton(self, height=25, width=25, text='+', fg_color=MAIN_BUTTON_COLOR,
                                                      font=ctk.CTkFont('<Helvetica>', size=14),
                                                      command=self.adicionar_planilha_json)

        self.adicionar_planilha_botao.bind('<Enter>', lambda event, btn=self.adicionar_planilha_botao: btn.configure(fg_color=HOLD_BUTTON_COLOR))
        self.adicionar_planilha_botao.bind('<Leave>', lambda event, btn=self.adicionar_planilha_botao: btn.configure(fg_color=MAIN_BUTTON_COLOR))

        self.adicionar_planilha_botao.place(relx=0.31, rely=0.45)

    def adicionar_planilha_json(self):
        nova_url = self.adicionar_planilha_entry.get()

        self.dados.adicionar_dados(nova_url)
        self.frame_buttons.update_buttons()
        self.adicionar_planilha_entry.delete(0, tk.END)


if __name__ == "__main__":
    try:
        print('Sucesso')
        app = App()
        app.mainloop()
    except:
        print('Erro')
