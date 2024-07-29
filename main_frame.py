import customtkinter as ctk
from settings import *
from data import Data
from PIL import Image
from tkinter import messagebox
import webbrowser


class MainFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(master=parent,
                         width=WINDOW_WIDTH,
                         height=WINDOW_HEIGHT - 75,
                         fg_color=MAIN_FRAME_COLOR)

        self.place(relx=0, rely=0)
        self.create_buttons()

    def create_buttons(self):
        data = Data('dados.json')
        i = 0

        for link, url in data.data.items():
            button_text = ctk.StringVar()
            button_text.set(link)

            # ----// Botões Planilha \\----
            button = ctk.CTkButton(self, text=f'{button_text.get()}', textvariable=button_text,
                                   command=lambda u=url: webbrowser.open(u),
                                   font=ctk.CTkFont(family='<Helvetica>', size=14),
                                   width=BUTTON_WIDTH,
                                   height=BUTTON_HEIGHT,
                                   fg_color=MAIN_BUTTON_COLOR,
                                   corner_radius=25
                                   )

            button.grid(row=i // 6, column=i % 6, padx=20, pady=10)

            button.bind('<Enter>', lambda event, btn=button: btn.configure(fg_color=HOLD_BUTTON_COLOR))
            button.bind('<Leave>', lambda event, btn=button: btn.configure(fg_color=MAIN_BUTTON_COLOR))

            # ----// Botões Remover \\----
            remove_button = ctk.CTkButton(self, text='X', width=12, height=12, bg_color=MAIN_BUTTON_COLOR,
                                          fg_color=REMOVE_BUTTON_COLOR,
                                          corner_radius=25,
                                          command=lambda b=button_text: self.remove_button_func(b, data))

            remove_button.bind('<Enter>', lambda event, btn=remove_button: btn.configure(fg_color=REMOVE_HOLD_COLOR))
            remove_button.bind('<Leave>', lambda event, btn=remove_button: btn.configure(fg_color=REMOVE_BUTTON_COLOR))

            remove_button.grid(row=i // 6, column=i % 6, sticky='ne', pady=BUTTON_WIDTH / 6,
                               padx=BUTTON_HEIGHT / 4)

            # ----// Botões Renomear \\----
            rename_buttons = ctk.CTkButton(self, text='R', width=12, height=12, bg_color=MAIN_BUTTON_COLOR,
                                           fg_color=HOLD_BUTTON_COLOR,
                                           command=lambda b=button_text: self.rename_button_func(b, data))

            rename_buttons.bind('<Enter>', lambda event, btn=rename_buttons: btn.configure(
                fg_color=HOLD_BUTTON_COLOR2))
            rename_buttons.bind('<Leave>',
                                lambda event, btn=rename_buttons: btn.configure(fg_color=HOLD_BUTTON_COLOR))

            rename_buttons.grid(row=i // 6, column=i % 6, padx=BUTTON_HEIGHT / 4, sticky='nw',
                                pady=BUTTON_WIDTH / 6)
            i += 1

    def remove_button_func(self, button_text, data):
        key = button_text.get()
        data.remove_data(key)

        self.update_buttons()

    def update_buttons(self):
        for widget in self.grid_slaves():
            widget.destroy()

        self.create_buttons()

    def rename_button_func(self, button_text, data):

        entry_stringvar = ctk.StringVar()
        entry = ctk.CTkEntry(self, width=90, textvariable=entry_stringvar, bg_color=MAIN_BUTTON_COLOR)

        for idx, (link, url) in enumerate(data.data.items(), start=1):

            if button_text.get() == link:
                row = idx // 7
                col = idx % 6

                if col == 0:
                    entry.grid(row=row, column=col + 5)
                else:
                    entry.grid(row=row, column=col - 1)

                # ----// Idx's especificos \\----
                if idx == 13:
                    entry.grid(row=2, column=col - 1)
                elif idx == 20:
                    entry.grid(row=3, column=col - 1)
                elif idx == 19:
                    entry.grid(row=3, column=col - 1)
                break

        def set_name(event):
            new_name = entry.get()
            idx_space = new_name.rfind(' ', 0)
            if len(new_name) >= 14 and idx_space < 0:
                messagebox.showinfo(title='Aviso', message='Nome muito grande')

            elif len(new_name) >= 14 and idx_space > 0:
                new_name = new_name.replace(' ', '\n')

            data.rename_data(old_key=link, new_key=new_name)
            self.update_buttons()

        entry.bind('<Return>', set_name)
