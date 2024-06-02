import json
from tkinter import messagebox

class Dados:

    def __init__(self, filename):
        self.filename = filename
        self.carregar_dados()

    def carregar_dados(self):
        try:
            with open(self.filename, 'r') as file:
                self.dados = json.load(file)
        except FileNotFoundError:
            self.dados = {}

    def adicionar_dados(self, novo_url):
        with open(self.filename, 'r+') as file:
            dados = json.load(file)

            if len(dados) == 24:
                try:
                    dados.pop(24)
                except KeyError:
                    messagebox.showinfo(title='Aviso', message='Número máximo de botões alcançado!!')
            else:
                novo_link = 'link' + str(len(dados) + 1)
                dados[novo_link] = novo_url
                file.seek(0)
                json.dump(dados, file, indent=4)

    def remover_dados(self, chave):
        with open(self.filename, 'r') as file:
            dados = json.load(file)

        if chave in dados:
            dados.pop(chave)

            with open(self.filename, 'w') as file:
                json.dump(dados, file, indent=4)

    def renomear_dados(self, chave_antiga, chave_nova):
        with open(self.filename, 'r') as file:
            dados = json.load(file)

        if chave_antiga in dados:
            valor = dados[chave_antiga]
            dados[chave_nova] = valor
            del dados[chave_antiga]

            with open(self.filename, 'w') as file:
                json.dump(dados, file, indent=2)

