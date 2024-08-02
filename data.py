import json
from tkinter import messagebox
import os


class Data:

    def __init__(self, filename):
        self.filename = filename
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print('Arquivo não encontrado')
            self.data = {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_data(self, new_url):

        with open(self.filename, 'r+') as file:
            data = json.load(file)

            if len(data) == 24:
                oldest_key = next(iter(data))
                messagebox.showinfo(title='Aviso', message='Número máximo de botões alcançado!')
                data.pop(oldest_key)

            else:
                path = new_url
                new_link = os.path.splitext(os.path.basename(path))[0]
                if new_link:
                    data[new_link] = new_url

                    if self.verify_data(new_link):
                        messagebox.showerror(title='Erro', message='Esse nome já existe. Por favor, coloque um diferente!')
                        return
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

            # ----// Verify \\----
            if self.verify_data(new_key):
                messagebox.showerror(title='Erro', message='Esse nome já existe. Por favor, coloque um diferente!')
                return

            data[new_key] = valor
            del data[old_key]
            self.verify_data(new_key)

            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=2)

    def verify_data(self, new_key_or_value):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        if new_key_or_value in data:
            return True

        if new_key_or_value in data.values():
            return True

        return False
