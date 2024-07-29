import json
from tkinter import messagebox


class Data:

    def __init__(self, filename):
        self.data = None
        self.filename = filename
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print('Arquivo não encontrado')

    def add_data(self, new_url):
        with open(self.filename, 'r+') as file:
            data = json.load(file)

            if len(data) == 24:
                try:
                    data.pop(24)
                except KeyError:
                    messagebox.showinfo(title='Aviso', message='Número máximo de botões alcançado!!')
            else:
                new_link = 'link' + str(len(data) + 1)
                data[new_link] = new_url
                file.seek(0)
                json.dump(data, file, indent=4)

    def remove_data(self, key):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        if key in data:
            data.pop(key)

            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)

    def rename_data(self, old_key, new_key):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        if old_key in data:
            valor = data[old_key]
            data[new_key] = valor
            del data[old_key]

            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=2)
